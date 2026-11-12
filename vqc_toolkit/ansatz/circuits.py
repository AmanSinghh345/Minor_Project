"""
Variational quantum circuit ansatz architectures.
Supports Linear, Circular, Hardware-Efficient, and Strongly Entangling topologies
with configurable readout wires.
"""

from typing import List
import pennylane as qml
import numpy as np


def apply_linear_entangling_layer(wires: List[int], noise_fn=None, noise_rate: float = 0.0):
    """
    Linear nearest-neighbor CNOT cascade: (0->1), (1->2), ..., (N-2->N-1).
    Total CNOT count per layer: N - 1.
    """
    n_qubits = len(wires)
    for i in range(n_qubits - 1):
        qml.CNOT(wires=[wires[i], wires[i + 1]])
        if noise_fn is not None and noise_rate > 0.0:
            noise_fn(noise_rate, wires[i])
            noise_fn(noise_rate, wires[i + 1])


def apply_circular_entangling_layer(wires: List[int], noise_fn=None, noise_rate: float = 0.0):
    """
    Circular periodic CNOT ring: (0->1), (1->2), ..., (N-1->0).
    Total CNOT count per layer: N.
    """
    n_qubits = len(wires)
    for i in range(n_qubits):
        ctrl = wires[i]
        tgt = wires[(i + 1) % n_qubits]
        qml.CNOT(wires=[ctrl, tgt])
        if noise_fn is not None and noise_rate > 0.0:
            noise_fn(noise_rate, ctrl)
            noise_fn(noise_rate, tgt)


def apply_variational_layer(
    weights: np.ndarray,
    wires: List[int],
    topology: str = "circular",
    ansatz_type: str = "hardware_efficient",
    noise_fn=None,
    noise_rate: float = 0.0
):
    """
    Executes one variational layer:
    1. Single-qubit parameterized rotations (Rot(phi, theta, omega) = Rz(omega) Ry(theta) Rz(phi))
    2. Entangling block (Linear or Circular)
    """
    n_qubits = len(wires)
    for i, wire in enumerate(wires):
        qml.Rot(weights[i, 0], weights[i, 1], weights[i, 2], wires=wire)
        if noise_fn is not None and noise_rate > 0.0:
            noise_fn(noise_rate, wire)

    if topology == "circular":
        apply_circular_entangling_layer(wires, noise_fn=noise_fn, noise_rate=noise_rate)
    elif topology == "linear":
        apply_linear_entangling_layer(wires, noise_fn=noise_fn, noise_rate=noise_rate)
    else:
        raise ValueError(f"Unknown topology: {topology}")
