"""
Physical noise channels implemented from first principles via Kraus operator representations.
Includes Depolarizing, Amplitude Damping, Phase Damping, and Bit-Flip noise.
"""

from typing import List
import numpy as np


def get_depolarizing_kraus(p: float) -> List[np.ndarray]:
    """
    Single-qubit depolarizing channel:
    rho -> (1 - p)*rho + (p/3)*(X*rho*X + Y*rho*Y + Z*rho*Z)
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Depolarizing probability p must be in [0, 1], got {p}")
    
    k0 = np.sqrt(1.0 - p) * np.eye(2, dtype=complex)
    factor = np.sqrt(p / 3.0)
    k1 = factor * np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)        # X
    k2 = factor * np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)     # Y
    k3 = factor * np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)       # Z
    return [k0, k1, k2, k3]


def get_amplitude_damping_kraus(gamma: float) -> List[np.ndarray]:
    """
    Single-qubit amplitude damping (T1 energy dissipation) channel:
    Models spontaneous decay from |1> to |0>.
    """
    if not (0.0 <= gamma <= 1.0):
        raise ValueError(f"Damping parameter gamma must be in [0, 1], got {gamma}")
    
    k0 = np.array([
        [1.0, 0.0],
        [0.0, np.sqrt(1.0 - gamma)]
    ], dtype=complex)
    
    k1 = np.array([
        [0.0, np.sqrt(gamma)],
        [0.0, 0.0]
    ], dtype=complex)
    
    return [k0, k1]


def get_phase_damping_kraus(gamma: float) -> List[np.ndarray]:
    """
    Single-qubit phase damping (pure dephasing / T2 dephasing) channel:
    Models loss of quantum coherence without energy dissipation.
    """
    if not (0.0 <= gamma <= 1.0):
        raise ValueError(f"Dephasing parameter gamma must be in [0, 1], got {gamma}")
    
    k0 = np.array([
        [1.0, 0.0],
        [0.0, np.sqrt(1.0 - gamma)]
    ], dtype=complex)
    
    k1 = np.array([
        [0.0, 0.0],
        [0.0, np.sqrt(gamma)]
    ], dtype=complex)
    
    return [k0, k1]


def get_bit_flip_kraus(p: float) -> List[np.ndarray]:
    """
    Single-qubit bit-flip channel:
    rho -> (1 - p)*rho + p * X*rho*X
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Bit-flip probability p must be in [0, 1], got {p}")
    
    k0 = np.sqrt(1.0 - p) * np.eye(2, dtype=complex)
    k1 = np.sqrt(p) * np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    return [k0, k1]


def verify_kraus_completeness(kraus_ops: List[np.ndarray], atol: float = 1e-12) -> bool:
    """
    Verifies that sum(K_i^dagger @ K_i) == Identity within absolute tolerance.
    """
    dim = kraus_ops[0].shape[0]
    identity = np.eye(dim, dtype=complex)
    total = np.zeros((dim, dim), dtype=complex)
    for k in kraus_ops:
        total += np.conjugate(k.T) @ k
    return bool(np.allclose(total, identity, atol=atol))
