"""
Hardware-simulated backend noise calibration presets.
Calibrated against public IBM Quantum device specifications (e.g. ibmq_manila, ibmq_bogota).
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class HardwareNoiseProfile:
    name: str
    t1_us: float
    t2_us: float
    single_qubit_gate_error: float
    two_qubit_cnot_error: float
    readout_error_p01: float
    readout_error_p10: float
    gate_time_single_ns: float = 35.0
    gate_time_cnot_ns: float = 300.0

    @property
    def effective_amp_damping_gamma(self) -> float:
        """
        Approximate T1 energy decay per CNOT gate:
        gamma = 1 - exp(-t_gate / T1)
        """
        t_gate_us = self.gate_time_cnot_ns / 1000.0
        import numpy as np
        return float(1.0 - np.exp(-t_gate_us / self.t1_us))

    @property
    def effective_phase_damping_lambda(self) -> float:
        """
        Approximate pure dephasing parameter per CNOT gate:
        1/T_phi = 1/T2 - 1/(2*T1)
        """
        import numpy as np
        t_gate_us = self.gate_time_cnot_ns / 1000.0
        inv_tphi = (1.0 / self.t2_us) - (1.0 / (2.0 * self.t1_us))
        inv_tphi = max(0.0, inv_tphi)
        return float(1.0 - np.exp(-t_gate_us * inv_tphi))


PRESET_PROFILES: Dict[str, HardwareNoiseProfile] = {
    "ibm_manila": HardwareNoiseProfile(
        name="IBM Manila (5-qubit Falcon r5)",
        t1_us=154.2,
        t2_us=63.8,
        single_qubit_gate_error=0.00028,
        two_qubit_cnot_error=0.0084,
        readout_error_p01=0.018,
        readout_error_p10=0.026
    ),
    "ibm_bogota": HardwareNoiseProfile(
        name="IBM Bogota (5-qubit Falcon r4)",
        t1_us=102.5,
        t2_us=88.1,
        single_qubit_gate_error=0.00035,
        two_qubit_cnot_error=0.0121,
        readout_error_p01=0.022,
        readout_error_p10=0.034
    ),
    "ibm_perth": HardwareNoiseProfile(
        name="IBM Perth (7-qubit Falcon r5)",
        t1_us=180.5,
        t2_us=112.4,
        single_qubit_gate_error=0.00024,
        two_qubit_cnot_error=0.0075,
        readout_error_p01=0.015,
        readout_error_p10=0.021
    ),
    "ibm_eagle": HardwareNoiseProfile(
        name="IBM Eagle (127-qubit Eagle r3)",
        t1_us=285.0,
        t2_us=135.0,
        single_qubit_gate_error=0.00019,
        two_qubit_cnot_error=0.0058,
        readout_error_p01=0.011,
        readout_error_p10=0.016
    ),
    "ideal_baseline": HardwareNoiseProfile(
        name="Ideal Statevector Simulator",
        t1_us=1e9,
        t2_us=1e9,
        single_qubit_gate_error=0.0,
        two_qubit_cnot_error=0.0,
        readout_error_p01=0.0,
        readout_error_p10=0.0
    )
}
