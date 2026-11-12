"""
baseline.py - Classical Machine Learning Baselines in PyTorch.

This script implements two classical baselines to benchmark against the VQC:
1. Logistic Regression:
   - PyTorch nn.Linear(4, 1) mapping 4 PCA features to 1 output logit.
   - Represents a convex, linear decision boundary baseline.
2. Multi-Layer Perceptron (Small MLP):
   - Architecture: Linear(4, 8) -> ReLU() -> Linear(8, 1).
   - Represents a non-linear classical baseline with a parameter count (~49 parameters)
     comparable to near-term quantum circuits.

Both models:
- Train on the exact same 4 PCA-reduced, [0, pi]-scaled features as the VQC.
- Use Binary Cross-Entropy with Logits loss (nn.BCEWithLogitsLoss).
- Optimize using Adam with seed control for reproducible initialization.
- Evaluate on test Accuracy, Precision, Recall, and F1 score.
"""

import argparse
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from data import load_and_preprocess_data


class LogisticRegressionPyTorch(nn.Module):
    """
    Standard linear logistic regression model:
    z = X * w + b
    p(y=1|X) = sigmoid(z)
    """
    def __init__(self, in_features: int = 4):
        super().__init__()
        self.linear = nn.Linear(in_features, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)


class SmallMLPPyTorch(nn.Module):
    """
    Small non-linear Multi-Layer Perceptron:
    Input (4) -> Linear(4, 8) -> ReLU -> Linear(8, 1) -> Output Logit.
    Compact capacity chosen to match the parameter scale of NISQ VQCs.
    Uses Kaiming/Xavier initialization to ensure stable convergence across all seeds.
    """
    def __init__(self, in_features: int = 4, hidden_dim: int = 8):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        # Kaiming normal init for ReLU layer, Xavier normal for linear output layer
        nn.init.kaiming_normal_(self.net[0].weight, nonlinearity="relu")
        nn.init.zeros_(self.net[0].bias)
        nn.init.xavier_normal_(self.net[2].weight)
        nn.init.zeros_(self.net[2].bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def set_seed(seed: int):
    """Set random seeds across Python, NumPy, and PyTorch for exact reproducibility."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_single_model(model: nn.Module, X_train: torch.Tensor, y_train: torch.Tensor,
                       X_test: torch.Tensor, y_test: np.ndarray,
                       lr: float = 0.05, epochs: int = 250, model_name: str = "Model",
                       verbose: bool = True):
    """Train a given PyTorch binary classification model and evaluate on test data."""
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        logits = model(X_train)
        loss = criterion(logits, y_train)
        loss.backward()
        optimizer.step()

        if verbose and (epoch % 50 == 0 or epoch == epochs):
            with torch.no_grad():
                train_preds = (torch.sigmoid(logits) >= 0.5).int().cpu().numpy()
                train_acc = accuracy_score(y_train.cpu().numpy(), train_preds)
            print(f"[{model_name}] Epoch [{epoch:3d}/{epochs}] - Loss: {loss.item():.4f} - Train Acc: {train_acc:.4f}")

    model.eval()
    with torch.no_grad():
        test_logits = model(X_test)
        test_probs = torch.sigmoid(test_logits).squeeze(1).cpu().numpy()
        test_preds = (test_probs >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_test, test_preds)),
        "precision": float(precision_score(y_test, test_preds, zero_division=0)),
        "recall": float(recall_score(y_test, test_preds, zero_division=0)),
        "f1": float(f1_score(y_test, test_preds, zero_division=0)),
        "model": model,
    }

    if verbose:
        print(f"\n--- {model_name} Test Results ---")
        print(f"Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy'] * 100:.2f}%)")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1']:.4f}")

    return metrics


def train_and_evaluate_baseline(seed: int = 42, lr: float = 0.05, epochs: int = 250,
                                lr_mlp: float = 0.01, epochs_mlp: int = 300, verbose: bool = True):
    """
    Trains both Classical Baselines (Logistic Regression and Small MLP)
    using the exact seed and preprocessed data.
    Logistic Regression uses lr=0.05, epochs=250.
    Small MLP uses calibrated lr_mlp=0.01, epochs_mlp=300 with Kaiming init.

    Returns:
        dict containing 'logreg' and 'mlp' metric dicts.
    """
    set_seed(seed)

    dataset = load_and_preprocess_data(seed=seed)
    X_train = torch.tensor(dataset["X_train"], dtype=torch.float32)
    y_train = torch.tensor(dataset["y_train"], dtype=torch.float32).unsqueeze(1)
    X_test = torch.tensor(dataset["X_test"], dtype=torch.float32)
    y_test = dataset["y_test"]

    # 1. Logistic Regression
    set_seed(seed)
    logreg_model = LogisticRegressionPyTorch(in_features=4)
    logreg_metrics = train_single_model(
        logreg_model, X_train, y_train, X_test, y_test,
        lr=lr, epochs=epochs, model_name="Logistic Regression", verbose=verbose
    )

    # 2. Small MLP (Calibrated lr=0.01, epochs=300, Kaiming init)
    set_seed(seed)
    mlp_model = SmallMLPPyTorch(in_features=4, hidden_dim=8)
    mlp_metrics = train_single_model(
        mlp_model, X_train, y_train, X_test, y_test,
        lr=lr_mlp, epochs=epochs_mlp, model_name="Small MLP (4-8-1)", verbose=verbose
    )

    return {
        "logreg": logreg_metrics,
        "mlp": mlp_metrics,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classical Machine Learning Baselines")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--lr", type=float, default=0.05, help="Learning rate")
    parser.add_argument("--epochs", type=int, default=250, help="Number of epochs")
    args = parser.parse_args()

    results = train_and_evaluate_baseline(seed=args.seed, lr=args.lr, epochs=args.epochs, verbose=True)
