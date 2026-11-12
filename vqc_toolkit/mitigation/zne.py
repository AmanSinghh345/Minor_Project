"""
Quantum Error Mitigation (QEM) algorithms.
Implements Zero-Noise Extrapolation (ZNE) and Readout Error Mitigation (REM).
"""

from typing import List, Tuple, Callable
import numpy as np


class ZeroNoiseExtrapolator:
    """
    Zero-Noise Extrapolation (ZNE) via noise-scale amplification.
    Given circuit evaluation at noise scale factors c in {1.0, 2.0, 3.0},
    fits polynomial/linear model to extrapolate to c -> 0.
    """
    def __init__(self, scale_factors: List[float] = None, order: int = 1):
        if scale_factors is None:
            self.scale_factors = [1.0, 2.0, 3.0]
        else:
            self.scale_factors = [float(s) for s in scale_factors]
        self.order = min(order, len(self.scale_factors) - 1)

    def extrapolate(self, measured_expvals: List[float]) -> float:
        """
        Extrapolates measured expectation values back to zero noise scale.
        """
        if len(measured_expvals) != len(self.scale_factors):
            raise ValueError("Length of measured_expvals must match scale_factors.")
        
        scales = np.array(self.scale_factors, dtype=float)
        values = np.array(measured_expvals, dtype=float)

        if self.order == 1 or len(scales) == 2:
            # Linear extrapolation: E(c) = a*c + b -> b is E(0)
            poly = np.polyfit(scales, values, deg=1)
            extrapolated = float(poly[1])  # intercept at c=0
        else:
            # Quadratic polynomial extrapolation
            poly = np.polyfit(scales, values, deg=self.order)
            extrapolated = float(np.polyval(poly, 0.0))

        # Clamp to physical expectation bounds [-1.0, 1.0]
        return float(np.clip(extrapolated, -1.0, 1.0))


def apply_zne_to_sample(
    eval_fn: Callable[[float], float],
    base_noise_rate: float,
    scale_factors: List[float] = None
) -> Tuple[float, float]:
    """
    Helper function to evaluate a sample across amplified noise rates and extrapolate.
    Returns: (unmitigated_expval, mitigated_expval)
    """
    if scale_factors is None:
        scale_factors = [1.0, 2.0, 3.0]
        
    measured = []
    for s in scale_factors:
        eff_noise = min(1.0, base_noise_rate * s)
        val = eval_fn(eff_noise)
        measured.append(val)
        
    zne = ZeroNoiseExtrapolator(scale_factors=scale_factors, order=1)
    mitigated = zne.extrapolate(measured)
    return measured[0], mitigated
