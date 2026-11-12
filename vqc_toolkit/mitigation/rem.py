"""
Readout Error Mitigation wrapper.
"""

from ..noise.readout import ReadoutErrorModel

def mitigate_readout_probabilities(p_noisy, p01=0.02, p10=0.03):
    model = ReadoutErrorModel(p01=p01, p10=p10)
    # p_noisy can be scalar expectation value or probability vector
    if isinstance(p_noisy, (int, float)):
        return model.mitigate_expval(float(p_noisy))
    return model.M_inv @ p_noisy
