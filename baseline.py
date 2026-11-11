"""
baseline.py - Classical Logistic Regression baseline in PyTorch.

This script implements the classical baseline for our study:
- Binary Logistic Regression using PyTorch (nn.Linear(in_features=4, out_features=1)).
- Operates on the exact same 4-dimensional PCA-reduced, [0, pi]-scaled features
  used by the Variational Quantum Classifier (VQC).
- Trained using Binary Cross-Entropy with Logits loss (BCEWithLogitsLoss) and
  the Adam optimizer.
- Evaluated on accuracy, precision, recall, and F1 score on the held-out test set.
- All random elements (data split sampling, torch parameter initialization)
  are strictly controlled via a seed argument.
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
        # 4 input features corresponding to the 4 PCA dimensions
        # 1 output logit for binary classification
        self.linear = nn.Linear(in_features, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Returns unnormalized log-odds (logits)
        return self.linear(x)


def set_seed(seed: int):
    """Set random seeds across Python, NumPy, and PyTorch for exact reproducibility."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_and_evaluate_baseline(seed: int = 42, lr: float = 0.05, epochs: int = 250, verbose: bool = True):
    """
    Trains the PyTorch logistic regression baseline and evaluates on test set.

    Args:
        seed: Random seed for data sampling and weight initialization.
        lr: Learning rate for Adam optimizer.
        epochs: Number of optimization epochs.
        verbose: Whether to print training progress and final test metrics.

    Returns:
        dict: Test metrics {'accuracy', 'precision', 'recall', 'f1'} and trained model.
    """
    # 1. Ensure exact reproducibility
    set_seed(seed)

    # 2. Load the 4-dimensional preprocessed dataset
    dataset = load_and_preprocess_data(seed=seed)
    X_train = torch.tensor(dataset["X_train"], dtype=torch.float32)
    y_train = torch.tensor(dataset["y_train"], dtype=torch.float32).unsqueeze(1)
    X_test = torch.tensor(dataset["X_test"], dtype=torch.float32)
    y_test = dataset["y_test"]

    # 3. Instantiate model, loss criterion, and optimizer
    model = LogisticRegressionPyTorch(in_features=4)
    # BCEWithLogitsLoss combines Sigmoid and BCE into one numerically stable layer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # 4. Training loop (full-batch gradient descent with Adam)
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
                train_acc = accuracy_score(dataset["y_train"], train_preds)
            print(f"Epoch [{epoch:3d}/{epochs}] - Loss: {loss.item():.4f} - Train Acc: {train_acc:.4f}")

    # 5. Evaluation on held-out test set
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
        print("\n=== Classical Logistic Regression Test Results ===")
        print(f"Seed:      {seed}")
        print(f"Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy'] * 100:.2f}%)")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1']:.4f}")
        print("==================================================")

    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classical Logistic Regression Baseline")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--lr", type=float, default=0.05, help="Learning rate")
    parser.add_argument("--epochs", type=int, default=250, help="Number of epochs")
    args = parser.parse_args()

    train_and_evaluate_baseline(seed=args.seed, lr=args.lr, epochs=args.epochs, verbose=True)
