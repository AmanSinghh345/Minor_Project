"""
Measurement Readout Error and Calibration Mitigation (REM).
Models asymmetric detector bit-flip errors on projective Z-measurement
and applies confusion matrix inversion to mitigate expectation values.
"""

from typing import Tuple
import numpy as np


class ReadoutErrorModel:
    """
    Asymmetric single-qubit measurement error model:
    p01: Probability state |0> is erroneously read as 1.
    p10: Probability state |1> is erroneously read as 0.
    """
    def __init__(self, p01: float = 0.02, p10: float = 0.03):
        self.p01 = float(p01)
        self.p10 = float(p10)
        # Confusion matrix M where M_ij = P(read i | true j)
        # Column 0: true |0> -> [1 - p01, p01]^T
        # Column 1: true |1> -> [p10, 1 - p10]^T
        self.M = np.array([
            [1.0 - self.p01, self.p10],
            [self.p01, 1.0 - self.p10]
        ], dtype=float)
        
        det = (1.0 - self.p01) * (1.0 - self.p10) - (self.p01 * self.p10)
        if abs(det) < 1e-6:
            raise ValueError("Readout confusion matrix is singular or non-invertible.")
        self.M_inv = np.linalg.inv(self.M)

    def apply_readout_noise_to_expval(self, clean_expval: float) -> float:
        """
        Converts ideal <Z> = P(0) - P(1) to noisy <Z> under readout bit-flip.
        P(0) = (1 + <Z>)/2, P(1) = (1 - <Z>)/2.
        P_noisy = M @ P_ideal.
        <Z>_noisy = P_noisy[0] - P_noisy[1].
        """
        clean_expval = np.clip(clean_expval, -1.0, 1.0)
        p0 = (1.0 + clean_expval) / 2.0
        p1 = (1.0 - clean_expval) / 2.0
        p_ideal = np.array([p0, p1])
        
        p_noisy = self.M @ p_ideal
        noisy_expval = float(p_noisy[0] - p_noisy[1])
        return float(np.clip(noisy_expval, -1.0, 1.0))

    def mitigate_expval(self, noisy_expval: float) -> float:
        """
        Applies Readout Error Mitigation (REM) via M_inv:
        P_mitigated = M_inv @ P_noisy.
        <Z>_mitigated = P_mitigated[0] - P_mitigated[1].
        """
        noisy_expval = np.clip(noisy_expval, -1.0, 1.0)
        p0_noisy = (1.0 + noisy_expval) / 2.0
        p1_noisy = (1.0 - noisy_expval) / 2.0
        p_noisy = np.array([p0_noisy, p1_noisy])
        
        p_mit = self.M_inv @ p_noisy
        # Clip probabilities to valid simplex [0, 1]
        p_mit = np.clip(p_mit, 0.0, 1.0)
        s = np.sum(p_mit)
        if s > 0:
            p_mit /= s
            
        mit_expval = float(p_mit[0] - p_mit[1])
        return float(np.clip(mit_expval, -1.0, 1.0))
