"""
Unit tests for the modular VQC toolkit.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np

from vqc_toolkit.noise.channels import (
    get_depolarizing_kraus,
    get_amplitude_damping_kraus,
    get_phase_damping_kraus,
    get_bit_flip_kraus,
    verify_kraus_completeness
)
from vqc_toolkit.noise.readout import ReadoutErrorModel
from vqc_toolkit.mitigation.zne import ZeroNoiseExtrapolator
from vqc_toolkit.metrics.robustness import compute_noise_robustness_score, compute_crossover_noise_rate
from vqc_toolkit.metrics.selection_rules import recommend_vqc_architecture
from vqc_toolkit.benchmarks.datasets import load_iris_dataset


def test_kraus_completeness():
    for p in [0.0, 0.01, 0.05, 0.2]:
        assert verify_kraus_completeness(get_depolarizing_kraus(p))
        assert verify_kraus_completeness(get_amplitude_damping_kraus(p))
        assert verify_kraus_completeness(get_phase_damping_kraus(p))
        assert verify_kraus_completeness(get_bit_flip_kraus(p))


def test_readout_error_mitigation():
    rem = ReadoutErrorModel(p01=0.04, p10=0.04)
    true_expval = 0.8
    noisy_expval = rem.apply_readout_noise_to_expval(true_expval)
    mitigated_expval = rem.mitigate_expval(noisy_expval)
    # Mitigated expval should be very close to original true expval
    assert abs(mitigated_expval - true_expval) < 1e-3


def test_zero_noise_extrapolator():
    zne = ZeroNoiseExtrapolator(scale_factors=[1.0, 2.0, 3.0], order=1)
    # Suppose true E(0) = 0.8, slope = -0.1
    # E(1) = 0.7, E(2) = 0.6, E(3) = 0.5
    extrapolated = zne.extrapolate([0.7, 0.6, 0.5])
    assert abs(extrapolated - 0.8) < 1e-4


def test_noise_robustness_score():
    rates = [0.0, 0.01, 0.02, 0.05]
    # Perfect robustness
    perfect_accs = [0.85, 0.85, 0.85, 0.85]
    nrs_perfect = compute_noise_robustness_score(rates, perfect_accs)
    assert abs(nrs_perfect - 1.0) < 1e-4
    
    # Degraded robustness
    degraded_accs = [0.85, 0.75, 0.65, 0.50]
    nrs_degraded = compute_noise_robustness_score(rates, degraded_accs)
    assert 0.0 < nrs_degraded < 1.0


def test_circuit_selection_rules():
    # Heavy amplitude damping should recommend linear topology
    rec = recommend_vqc_architecture("amplitude_damping", 0.04, 0.02)
    assert rec["recommended_topology"] == "linear"
    assert "Readout Error Mitigation (REM)" in rec["recommended_mitigations"]
    assert "Zero-Noise Extrapolation (ZNE)" in rec["recommended_mitigations"]


def test_iris_benchmark_loader():
    X_tr, X_te, y_tr, y_te = load_iris_dataset(seed=42)
    assert X_tr.shape[1] == 4
    assert np.all(X_tr >= -1e-7) and np.all(X_tr <= np.pi + 1e-7)
    assert np.all(X_te >= -1e-7) and np.all(X_te <= np.pi + 1e-7)


if __name__ == "__main__":
    test_kraus_completeness()
    test_readout_error_mitigation()
    test_zero_noise_extrapolator()
    test_noise_robustness_score()
    test_circuit_selection_rules()
    test_iris_benchmark_loader()
    print("All unit tests passed successfully!")
