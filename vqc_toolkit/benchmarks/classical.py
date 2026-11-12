"""
Comprehensive Classical Benchmark Suite:
1. Logistic Regression (Convex Linear)
2. Support Vector Machine - Linear Kernel
3. Support Vector Machine - Non-linear RBF Kernel
4. Random Forest Classifier (50 Decision Trees)
5. Gradient Boosting Classifier
6. Small MLP (4-8-1, 49 Parameters)
"""

from typing import Dict, Any
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import torch
import torch.nn as nn
import torch.optim as optim


class SmallMLP(nn.Module):
    """
    4 -> 8 -> 1 MLP with 49 trainable parameters.
    """
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 8)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(8, 1)
        
        nn.init.kaiming_normal_(self.fc1.weight, nonlinearity='relu')
        nn.init.zeros_(self.fc1.bias)
        nn.init.xavier_normal_(self.fc2.weight)
        nn.init.zeros_(self.fc2.bias)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def evaluate_classical_suite(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    seed: int = 42
) -> Dict[str, float]:
    """
    Evaluates 6 classical models covering linear, margin-based, kernel, ensemble, and neural network paradigms.
    Returns test accuracies.
    """
    results = {}
    
    # 1. Logistic Regression
    lr = LogisticRegression(random_state=seed, max_iter=500)
    lr.fit(X_train, y_train)
    results["logistic_regression"] = float(lr.score(X_test, y_test))
    
    # 2. Linear SVM
    svm_lin = SVC(kernel="linear", random_state=seed)
    svm_lin.fit(X_train, y_train)
    results["svm_linear"] = float(svm_lin.score(X_test, y_test))

    # 3. RBF SVM
    svm_rbf = SVC(kernel="rbf", random_state=seed)
    svm_rbf.fit(X_train, y_train)
    results["svm_rbf"] = float(svm_rbf.score(X_test, y_test))

    # 4. Random Forest (50 Trees)
    rf = RandomForestClassifier(n_estimators=50, random_state=seed)
    rf.fit(X_train, y_train)
    results["random_forest"] = float(rf.score(X_test, y_test))

    # 5. Gradient Boosting
    gb = GradientBoostingClassifier(n_estimators=50, random_state=seed)
    gb.fit(X_train, y_train)
    results["gradient_boosting"] = float(gb.score(X_test, y_test))

    # 6. Small MLP (4-8-1)
    torch.manual_seed(seed)
    mlp = SmallMLP()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(mlp.parameters(), lr=0.01)
    
    X_t = torch.tensor(X_train, dtype=torch.float32)
    y_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    
    mlp.train()
    for _ in range(300):
        optimizer.zero_grad()
        out = mlp(X_t)
        loss = criterion(out, y_t)
        loss.backward()
        optimizer.step()
        
    mlp.eval()
    with torch.no_grad():
        X_test_t = torch.tensor(X_test, dtype=torch.float32)
        logits = mlp(X_test_t).squeeze()
        preds = (logits > 0.0).long().numpy()
        results["small_mlp"] = float(np.mean(preds == y_test))
        
    return results

evaluate_classical_models = evaluate_classical_suite
