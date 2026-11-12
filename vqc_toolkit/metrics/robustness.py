"""
Noise-Robustness Score (NRS) and Crossover Metrics.
"""

from typing import List, Tuple
import numpy as np


def compute_noise_robustness_score(noise_rates: List[float], accuracies: List[float]) -> float:
    """
    Computes the normalized Noise-Robustness Score (NRS).
    Defined as the normalized area under the relative accuracy curve:
    NRS = (1 / (p_max - p_min)) * integral( Acc(p) / Acc(0) dp )
    
    Returns a score in [0.0, 1.0], where 1.0 represents perfect noise invariance.
    """
    rates = np.array(noise_rates, dtype=float)
    accs = np.array(accuracies, dtype=float)
    
    # Sort by noise rate
    sort_idx = np.argsort(rates)
    rates = rates[sort_idx]
    accs = accs[sort_idx]
    
    clean_acc = accs[0]
    if clean_acc <= 0:
        return 0.0
        
    rel_accs = accs / clean_acc
    p_span = rates[-1] - rates[0]
    if p_span <= 0:
        return 1.0
        
    # Trapezoidal numerical integration (supports NumPy 1.x and 2.x)
    trapz_fn = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
    auc = trapz_fn(rel_accs, rates)
    nrs = float(auc / p_span)
    return float(np.clip(nrs, 0.0, 1.0))


def compute_crossover_noise_rate(
    noise_rates: List[float],
    accuracies: List[float],
    threshold_accuracy: float
) -> float:
    """
    Returns the highest noise rate where mean accuracy remains >= threshold_accuracy.
    """
    rates = np.array(noise_rates, dtype=float)
    accs = np.array(accuracies, dtype=float)
    
    valid_rates = rates[accs >= threshold_accuracy]
    if len(valid_rates) == 0:
        return 0.0
    return float(np.max(valid_rates))
