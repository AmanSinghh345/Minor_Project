"""
Three training regimes for Variational Quantum Classifiers:
1. Clean-train / Noisy-test
2. Noisy-train / Noisy-test
3. Noise-aware fine-tuning (pre-trained clean, fine-tuned under noise)
"""

from typing import Tuple, Dict, Any
import numpy as np
import torch
import pennylane as qml

from ..noise.channels import (
    get_depolarizing_kraus,
    get_amplitude_damping_kraus,
    get_phase_damping_kraus,
    get_bit_flip_kraus
)
from ..encoders.angle import apply_angle_encoding
from ..ansatz.circuits import apply_variational_layer


def build_vqc_qnode(
    n_qubits: int = 4,
    n_layers: int = 2,
    topology: str = "circular",
    readout_qubit: int = 0,
    noise_channel: str = None,
    noise_rate: float = 0.0
):
    """
    Constructs a PennyLane QNode with PyTorch interface.
    Uses default.mixed if noise is active, or default.qubit if noise-free.
    """
    wires = list(range(n_qubits))
    
    if noise_channel is not None and noise_rate > 0.0:
        dev = qml.device("default.mixed", wires=wires)
        
        def noise_fn(p, wire):
            if noise_channel == "depolarizing":
                qml.QubitChannel(get_depolarizing_kraus(p), wires=wire)
            elif noise_channel == "amplitude_damping":
                qml.QubitChannel(get_amplitude_damping_kraus(p), wires=wire)
            elif noise_channel == "phase_damping":
                qml.QubitChannel(get_phase_damping_kraus(p), wires=wire)
            elif noise_channel == "bit_flip":
                qml.QubitChannel(get_bit_flip_kraus(p), wires=wire)
    else:
        dev = qml.device("default.qubit", wires=wires)
        noise_fn = None

    @qml.qnode(dev, interface="torch", diff_method="best")
    def circuit(weights, features):
        apply_angle_encoding(features, wires)
        for l in range(n_layers):
            apply_variational_layer(
                weights[l], wires, topology=topology,
                noise_fn=noise_fn, noise_rate=noise_rate
            )
        return qml.expval(qml.PauliZ(wires=readout_qubit))

    return circuit


def train_vqc_model(
    qnode,
    init_weights: torch.Tensor,
    X_train: np.ndarray,
    y_train: np.ndarray,
    epochs: int = 25,
    lr: float = 0.05,
    batch_size: int = 16
) -> torch.Tensor:
    """
    Trains VQC weights using MSE loss against {-1, +1} targets.
    """
    weights = init_weights.clone().detach().requires_grad_(True)
    optimizer = torch.optim.Adam([weights], lr=lr)
    
    # Map binary {0, 1} to Pauli-Z targets {+1, -1}
    targets = np.where(y_train == 0, 1.0, -1.0)
    
    N = len(X_train)
    for epoch in range(epochs):
        indices = np.random.permutation(N)
        for i in range(0, N, batch_size):
            batch_idx = indices[i:i + batch_size]
            batch_x = X_train[batch_idx]
            batch_y = targets[batch_idx]
            
            optimizer.zero_grad()
            batch_loss = torch.tensor(0.0, requires_grad=True)
            for x_sample, y_target in zip(batch_x, batch_y):
                pred = qnode(weights, torch.tensor(x_sample, dtype=torch.float32))
                diff = pred - torch.tensor(y_target, dtype=torch.float32)
                batch_loss = batch_loss + (diff ** 2)
                
            loss = batch_loss / len(batch_idx)
            loss.backward()
            optimizer.step()
            
    return weights.detach()


def evaluate_vqc_accuracy(qnode, weights: torch.Tensor, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Evaluates classification accuracy on test dataset:
    <Z> > 0.0 -> class 0, <Z> <= 0.0 -> class 1.
    """
    correct = 0
    with torch.no_grad():
        for x, y_true in zip(X_test, y_test):
            expval = float(qnode(weights, torch.tensor(x, dtype=torch.float32)))
            pred = 1 if expval <= 0.0 else 0
            if pred == y_true:
                correct += 1
    return float(correct / len(y_test))
