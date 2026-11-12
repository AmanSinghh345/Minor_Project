"""
Quantum Kernel Estimator (QSVC) based on Havlíček et al., Nature 2019.
Maps classical data x into quantum Hilbert space states |psi(x)> and computes
the transition fidelity kernel matrix K(x_1, x_2) = |<psi(x_1)|psi(x_2)>|^2.
Under hardware noise, fidelity degrades into Tr(rho(x_1) rho(x_2)).
"""

from typing import List
import pennylane as qml
import numpy as np
from sklearn.svm import SVC


def build_quantum_kernel_circuit(n_qubits: int = 4, noise_type: str = None, noise_rate: float = 0.0):
    wires = list(range(n_qubits))
    
    if noise_type is not None and noise_rate > 0.0:
        dev = qml.device("default.mixed", wires=wires)
        def noise_fn(wire):
            if noise_type == "depolarizing":
                qml.DepolarizingChannel(noise_rate, wires=wire)
            elif noise_type == "amplitude_damping":
                qml.AmplitudeDamping(noise_rate, wires=wire)
    else:
        dev = qml.device("default.qubit", wires=wires)
        noise_fn = None

    @qml.qnode(dev)
    def kernel_eval(x1, x2):
        # Apply encoding for x1
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
            qml.RZ(x1[i], wires=i)
            if noise_fn: noise_fn(i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])
            if noise_fn:
                noise_fn(i)
                noise_fn(i + 1)
                
        # Apply adjoint encoding for x2
        for i in reversed(range(n_qubits - 1)):
            if noise_fn:
                noise_fn(i)
                noise_fn(i + 1)
            qml.CNOT(wires=[i, i + 1])
        for i in range(n_qubits):
            if noise_fn: noise_fn(i)
            qml.RZ(-x2[i], wires=i)
            qml.Hadamard(wires=i)
            
        # Return probability of returning to |00...0>
        return qml.probs(wires=wires)

    def compute_similarity(x1, x2):
        probs = kernel_eval(x1, x2)
        # Probability of state |0000> is the first element
        return float(np.clip(probs[0], 0.0, 1.0))

    return compute_similarity


def compute_kernel_matrix(X1, X2, kernel_fn):
    """
    Computes Gram matrix between datasets X1 and X2.
    """
    n1 = len(X1)
    n2 = len(X2)
    K = np.zeros((n1, n2), dtype=float)
    for i in range(n1):
        for j in range(n2):
            if X1 is X2 and i == j:
                K[i, j] = 1.0
            elif X1 is X2 and j < i:
                K[i, j] = K[j, i]  # Symmetry optimization
            else:
                K[i, j] = kernel_fn(X1[i], X2[j])
    return K
