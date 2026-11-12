"""
Data Re-uploading Variational Quantum Classifier (Pérez-Salinas et al., 2020).
Interleaves feature encoding and parameterized variational rotations at every layer:
[U_enc(x) U_var(theta)]^L
This theoretically allows even low-qubit quantum circuits to achieve universal function approximation.
"""

from typing import List
import pennylane as qml
import torch
import numpy as np


def apply_data_reuploading_layer(features, weights, wires: List[int], noise_fn=None, noise_rate: float = 0.0):
    """
    Single layer of data re-uploading:
    1. Feature encoding Ry(x_i)
    2. Trainable rotations Rot(phi, theta, omega)
    3. Entanglement (circular or linear)
    """
    n_qubits = len(wires)
    
    # Re-upload features
    for i, wire in enumerate(wires):
        val = features[i]
        qml.RY(val, wires=wire)
        if noise_fn is not None and noise_rate > 0.0:
            noise_fn(noise_rate, wire)
            
    # Parameterized rotations
    for i, wire in enumerate(wires):
        qml.Rot(weights[i, 0], weights[i, 1], weights[i, 2], wires=wire)
        if noise_fn is not None and noise_rate > 0.0:
            noise_fn(noise_rate, wire)
            
    # Entanglement ring
    for i in range(n_qubits):
        ctrl = wires[i]
        tgt = wires[(i + 1) % n_qubits]
        qml.CNOT(wires=[ctrl, tgt])
        if noise_fn is not None and noise_rate > 0.0:
            noise_fn(noise_rate, ctrl)
            noise_fn(noise_rate, tgt)


def make_reuploading_vqc_qnode(n_qubits: int = 4, n_layers: int = 2, noise_type: str = None, noise_rate: float = 0.0):
    wires = list(range(n_qubits))
    
    if noise_type is not None and noise_rate > 0.0:
        dev = qml.device("default.mixed", wires=wires)
        def noise_fn(p, wire):
            if noise_type == "depolarizing":
                qml.DepolarizingChannel(p, wires=wire)
            elif noise_type == "amplitude_damping":
                qml.AmplitudeDamping(p, wires=wire)
    else:
        dev = qml.device("default.qubit", wires=wires)
        noise_fn = None
        
    @qml.qnode(dev, interface="torch")
    def circuit(weights, features):
        for l in range(n_layers):
            apply_data_reuploading_layer(features, weights[l], wires, noise_fn=noise_fn, noise_rate=noise_rate)
        return qml.expval(qml.PauliZ(0))
        
    return circuit
