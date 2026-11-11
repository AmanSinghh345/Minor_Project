"""
model.py - 4-Qubit Variational Quantum Classifier (VQC) in PennyLane & PyTorch.

This module implements a Parameterized Quantum Circuit (PQC) for binary classification:
1. Qubits:
   - 4 qubits (wires 0 to 3), each dedicated to one of the 4 PCA-reduced features.
2. Quantum Encoding Layer:
   - Ry(theta) angle encoding where theta in [0, pi].
   - Rotates the ground state |0> around the Y-axis:
     Ry(0)|0> = |0> (class 0 direction), Ry(pi)|0> = |1> (class 1 direction).
3. Parameterized Variational Ansatz:
   - Configurable number of layers (L in {1, 2, 3}).
   - In each layer:
     a) Trainable single-qubit Ry rotations on all 4 qubits.
     b) Two-qubit CNOT entanglement with configurable topology:
        - 'linear':   CNOT(0,1), CNOT(1,2), CNOT(2,3) -> 3 entangling gates / layer
        - 'circular': CNOT(0,1), CNOT(1,2), CNOT(2,3), CNOT(3,0) -> 4 entangling gates / layer
4. Observable & Readout:
   - PauliZ expectation value measured on qubit 0: <Z_0> in [-1, +1].
   - Continuous probability mapping: p(y=1) = (1 - <Z_0>) / 2 in [0, 1].
   - Binary decision boundary: predict class 1 if <Z_0> <= 0 (p >= 0.5), else class 0.
5. Optimization:
   - Noise-free training on PennyLane's 'default.qubit' device.
   - Optimized using PyTorch's Adam optimizer with Mean Squared Error (MSE) loss
     against parity labels (+1 for class 0, -1 for class 1).
"""

import argparse
import numpy as np
import pennylane as qml
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from data import load_and_preprocess_data


class VariationalQuantumClassifier(nn.Module):
    """
    Hybrid PyTorch Module encapsulating a 4-qubit PennyLane VQC.

    Args:
        n_qubits: Number of quantum wires (fixed at 4 for our 4 PCA components).
        n_layers: Depth of the variational ansatz (1, 2, or 3 layers).
        topology: Entanglement scheme, either 'linear' or 'circular'.
        seed: Random seed for weight initialization.
    """
    def __init__(self, n_qubits: int = 4, n_layers: int = 2, topology: str = "linear", seed: int = 42):
        super().__init__()
        assert topology in ["linear", "circular"], f"Topology must be 'linear' or 'circular', got {topology}"
        assert n_layers in [1, 2, 3], f"n_layers should be 1, 2, or 3, got {n_layers}"

        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.topology = topology

        # Create PennyLane noise-free statevector simulation device
        self.dev = qml.device("default.qubit", wires=n_qubits)

        # Build parameterized QNode with PyTorch autograd integration
        self.qnode = qml.QNode(self._circuit, self.dev, interface="torch", diff_method="backprop")

        # Initialize variational rotation weights with small random angles
        torch.manual_seed(seed)
        initial_weights = 0.01 * torch.randn(n_layers, n_qubits, dtype=torch.float32)
        self.weights = nn.Parameter(initial_weights)

    def save(self, filepath: str):
        """Saves model weights and architectural configuration to disk."""
        torch.save({
            "weights": self.weights.data,
            "n_qubits": self.n_qubits,
            "n_layers": self.n_layers,
            "topology": self.topology,
        }, filepath)

    def load(self, filepath: str):
        """Loads model weights and architecture from disk."""
        checkpoint = torch.load(filepath, map_location="cpu")
        self.n_qubits = checkpoint["n_qubits"]
        self.n_layers = checkpoint["n_layers"]
        self.topology = checkpoint["topology"]
        self.weights = nn.Parameter(checkpoint["weights"])

    def _circuit(self, weights: torch.Tensor, features: torch.Tensor):
        """
        Quantum Circuit Definition:
        features: shape (batch_size, n_qubits) in [0, pi]
        weights:  shape (n_layers, n_qubits)
        """
        # Step 1: Angle Encoding Layer (Depth 1)
        # Each feature rotates the corresponding qubit around the Y-axis.
        for i in range(self.n_qubits):
            qml.RY(features[:, i], wires=i)

        # Step 2: Variational Layers (Depth L)
        for layer in range(weights.shape[0]):
            # Parameterized single-qubit rotations
            for i in range(self.n_qubits):
                qml.RY(weights[layer, i], wires=i)

            # Two-qubit CNOT entanglement
            # Linear topology: chain of 3 CNOT gates
            for i in range(self.n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])

            # Circular topology: closes the loop with an extra CNOT from qubit 3 to 0
            if self.topology == "circular":
                qml.CNOT(wires=[self.n_qubits - 1, 0])

        # Step 3: Measurement on readout qubit 0
        return qml.expval(qml.PauliZ(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass: returns PauliZ expectation values in [-1, +1].
        """
        # PennyLane default.qubit returns float64 tensor; cast to float32 for PyTorch consistency
        return self.qnode(self.weights, x).float()

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        """
        Maps expectation value <Z_0> in [-1, 1] to class 1 probability in [0, 1]:
        p(y=1) = (1 - <Z_0>) / 2
        When <Z_0> = +1 (ground state |0>), p = 0.0 (Class 0).
        When <Z_0> = -1 (excited state |1>), p = 1.0 (Class 1).
        """
        expvals = self.forward(x)
        return (1.0 - expvals) / 2.0

    def predict(self, x: torch.Tensor) -> np.ndarray:
        """
        Returns binary class predictions (0 or 1).
        Decision threshold: <Z_0> <= 0 implies p(y=1) >= 0.5.
        """
        with torch.no_grad():
            expvals = self.forward(x)
            preds = (expvals <= 0.0).int().cpu().numpy()
        return preds


def train_vqc(model: VariationalQuantumClassifier, X_train: torch.Tensor, y_train: torch.Tensor,
              lr: float = 0.05, epochs: int = 150, verbose: bool = True):
    """
    Trains the VQC noise-free using the Adam optimizer and Mean Squared Error
    against target parity eigenvalues: y'=+1 for class 0, y'=-1 for class 1.
    """
    # Parity targets: class 0 -> +1.0, class 1 -> -1.0
    target_eigenvalues = (1.0 - 2.0 * y_train).float()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        expvals = model(X_train)
        loss = torch.mean((expvals - target_eigenvalues) ** 2)
        loss.backward()
        optimizer.step()

        if verbose and (epoch % 30 == 0 or epoch == epochs):
            with torch.no_grad():
                train_preds = (expvals <= 0.0).int().cpu().numpy()
                train_acc = accuracy_score(y_train.cpu().numpy(), train_preds)
            print(f"[VQC {model.topology} L={model.n_layers}] Epoch [{epoch:3d}/{epochs}] - Loss: {loss.item():.4f} - Train Acc: {train_acc:.4f}")

    return model


def evaluate_vqc(model: VariationalQuantumClassifier, X_test: torch.Tensor, y_test: np.ndarray,
                 verbose: bool = True):
    """
    Evaluates the trained VQC on the held-out test set and reports
    Accuracy, Precision, Recall, and F1 score.
    """
    preds = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds, zero_division=0)),
        "recall": float(recall_score(y_test, preds, zero_division=0)),
        "f1": float(f1_score(y_test, preds, zero_division=0)),
    }

    if verbose:
        print(f"\n=== VQC Test Results ({model.topology} topology, {model.n_layers} layers) ===")
        print(f"Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy'] * 100:.2f}%)")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1']:.4f}")
        print("=====================================================================")

    return metrics


def run_stage2_demo(seed: int = 42, n_layers: int = 2, topology: str = "circular",
                    lr: float = 0.05, epochs: int = 150):
    """
    Demonstration runner for Stage 2: loads data, initializes VQC, trains noise-free,
    and reports the 4 evaluation metrics.
    """
    print(f"Loading PneumoniaMNIST dataset (Seed: {seed})...")
    data = load_and_preprocess_data(seed=seed)
    X_train = torch.tensor(data["X_train"], dtype=torch.float32)
    y_train = torch.tensor(data["y_train"], dtype=torch.float32)
    X_test = torch.tensor(data["X_test"], dtype=torch.float32)
    y_test = data["y_test"]

    print(f"\nInitializing 4-Qubit VQC (Layers: {n_layers}, Topology: '{topology}')...")
    model = VariationalQuantumClassifier(n_qubits=4, n_layers=n_layers, topology=topology, seed=seed)

    print(f"Training VQC noise-free on default.qubit for {epochs} epochs (Adam, lr={lr})...")
    train_vqc(model, X_train, y_train, lr=lr, epochs=epochs, verbose=True)

    metrics = evaluate_vqc(model, X_test, y_test, verbose=True)
    return model, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 2: Noise-Free VQC")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--layers", type=int, default=2, choices=[1, 2, 3], help="Ansatz layers (1, 2, or 3)")
    parser.add_argument("--topology", type=str, default="circular", choices=["linear", "circular"], help="CNOT topology")
    parser.add_argument("--lr", type=float, default=0.05, help="Learning rate")
    parser.add_argument("--epochs", type=int, default=150, help="Training epochs")
    args = parser.parse_args()

    run_stage2_demo(seed=args.seed, n_layers=args.layers, topology=args.topology, lr=args.lr, epochs=args.epochs)
