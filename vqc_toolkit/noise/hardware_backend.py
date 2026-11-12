"""
Hardware-realistic IBM Quantum backend simulator.
Models physical gate times, asymmetric single/two-qubit gate infidelities,
T1 thermal relaxation, T2 pure dephasing, coupling graph routing overhead (SWAPs),
and asymmetric readout error with optional matrix-inversion mitigation (REM).
"""

from typing import Tuple, Optional, Dict
import numpy as np
import pennylane as qml
from vqc_toolkit.noise.calibration import PRESET_PROFILES, HardwareNoiseProfile


def get_hardware_noise_channels(profile: HardwareNoiseProfile):
    """
    Computes exact physical Kraus parameters from device calibration:
    - Single-qubit depolarizing error & decay
    - Two-qubit CNOT depolarizing error & decay
    """
    t_1q_us = profile.gate_time_single_ns / 1000.0
    t_2q_us = profile.gate_time_cnot_ns / 1000.0

    # 1-qubit channels
    p_1q = profile.single_qubit_gate_error
    gamma_1q = float(1.0 - np.exp(-t_1q_us / profile.t1_us))
    inv_tphi_1q = max(0.0, (1.0 / profile.t2_us) - (1.0 / (2.0 * profile.t1_us)))
    lambda_1q = float(1.0 - np.exp(-t_1q_us * inv_tphi_1q))

    # 2-qubit CNOT channels
    p_2q = profile.two_qubit_cnot_error
    gamma_2q = float(1.0 - np.exp(-t_2q_us / profile.t1_us))
    inv_tphi_2q = max(0.0, (1.0 / profile.t2_us) - (1.0 / (2.0 * profile.t1_us)))
    lambda_2q = float(1.0 - np.exp(-t_2q_us * inv_tphi_2q))

    return {
        "p_1q": p_1q, "gamma_1q": gamma_1q, "lambda_1q": lambda_1q,
        "p_2q": p_2q, "gamma_2q": gamma_2q, "lambda_2q": lambda_2q
    }


def make_hardware_vqc_qnode(
    profile_name: str = "ibm_manila",
    n_qubits: int = 4,
    n_layers: int = 2,
    topology: str = "linear",
    model_type: str = "standard_vqc",
    transpile_routing: bool = True
):
    """
    Constructs a PennyLane QNode operating on default.mixed that executes
    a circuit under exact physical IBM hardware calibration parameters.
    
    If transpile_routing is True and topology is 'circular', models the
    mandatory SWAP routing overhead on physical linear/T-coupling architectures.
    """
    if profile_name not in PRESET_PROFILES:
        raise ValueError(f"Unknown profile: {profile_name}. Available: {list(PRESET_PROFILES.keys())}")

    profile = PRESET_PROFILES[profile_name]
    ch = get_hardware_noise_channels(profile)
    dev = qml.device("default.mixed", wires=n_qubits)

    def apply_1q_noise(wire: int):
        if ch["p_1q"] > 1e-7:
            qml.DepolarizingChannel(ch["p_1q"], wires=wire)
        if ch["gamma_1q"] > 1e-7:
            qml.AmplitudeDamping(ch["gamma_1q"], wires=wire)
        if ch["lambda_1q"] > 1e-7:
            qml.PhaseDamping(ch["lambda_1q"], wires=wire)

    def apply_2q_noise(ctrl: int, tgt: int):
        if ch["p_2q"] > 1e-7:
            # Two-qubit depolarizing channel applied to both wires
            qml.DepolarizingChannel(ch["p_2q"], wires=ctrl)
            qml.DepolarizingChannel(ch["p_2q"], wires=tgt)
        if ch["gamma_2q"] > 1e-7:
            qml.AmplitudeDamping(ch["gamma_2q"], wires=ctrl)
            qml.AmplitudeDamping(ch["gamma_2q"], wires=tgt)
        if ch["lambda_2q"] > 1e-7:
            qml.PhaseDamping(ch["lambda_2q"], wires=ctrl)
            qml.PhaseDamping(ch["lambda_2q"], wires=tgt)

    def execute_physical_cnot(ctrl: int, tgt: int):
        qml.CNOT(wires=[ctrl, tgt])
        apply_2q_noise(ctrl, tgt)

    def execute_physical_swap(w1: int, w2: int):
        # Physical SWAP decomposed into 3 CNOTs
        execute_physical_cnot(w1, w2)
        execute_physical_cnot(w2, w1)
        execute_physical_cnot(w1, w2)

    @qml.qnode(dev)
    def circuit(inputs, weights):
        # 1. Feature Encoding Layer
        for i in range(n_qubits):
            qml.RY(inputs[i], wires=i)
            apply_1q_noise(i)

        # 2. Variational Entangling Layers
        for l in range(n_layers):
            # Parameterized Rotations
            for i in range(n_qubits):
                w = weights[l, i]
                if getattr(w, "ndim", 0) > 0 and len(w) == 3:
                    qml.Rot(w[0], w[1], w[2], wires=i)
                else:
                    qml.RY(w, wires=i)
                apply_1q_noise(i)

            # Entangling Gates & Coupling Graph Routing
            if topology == "linear":
                # Natively maps to IBM linear coupling: 0-1-2-3 (0 SWAPs required)
                for i in range(n_qubits - 1):
                    execute_physical_cnot(i, i + 1)

            elif topology == "circular":
                # First 3 CNOTs are native nearest-neighbor
                for i in range(n_qubits - 1):
                    execute_physical_cnot(i, i + 1)

                # The wrap-around CNOT between Q3 and Q0 is non-local on linear chips
                if transpile_routing:
                    # Routed via SWAP(0, 1), SWAP(1, 2) -> CNOT(2, 3) -> inverse SWAPs
                    execute_physical_swap(0, 1)
                    execute_physical_swap(1, 2)
                    execute_physical_cnot(2, 3)
                    execute_physical_swap(1, 2)
                    execute_physical_swap(0, 1)
                else:
                    # Idealized all-to-all coupling assumption
                    execute_physical_cnot(n_qubits - 1, 0)

        # Readout: Pauli Z expectation value on Qubit 0
        return qml.expval(qml.PauliZ(0))

    return circuit, profile


def apply_hardware_readout_noise_and_mitigation(
    clean_prob: float,
    profile: HardwareNoiseProfile,
    mitigate: bool = False
) -> float:
    """
    Applies real physical asymmetric readout error:
      P_noisy(1) = p_01 * P(0) + (1 - p_10) * P(1)
    And optionally inverts with Readout Error Mitigation (REM):
      P_mit = M^-1 * P_noisy
    """
    p01 = profile.readout_error_p01
    p10 = profile.readout_error_p10

    p_clean_0 = 1.0 - clean_prob
    p_clean_1 = clean_prob

    # Forward noisy measurement
    p_noisy_1 = p01 * p_clean_0 + (1.0 - p10) * p_clean_1
    p_noisy_0 = 1.0 - p_noisy_1

    if not mitigate or (p01 == 0.0 and p10 == 0.0):
        return float(np.clip(p_noisy_1, 0.0, 1.0))

    # Readout confusion matrix M:
    # [ [1 - p01,  p10    ],
    #   [p01,      1 - p10] ]
    det = (1.0 - p01 - p10)
    if abs(det) < 1e-5:
        return float(p_noisy_1)

    # Invert M:
    # M^-1 = (1/det) * [ [1 - p10, -p10], [-p01, 1 - p01] ]
    p_mit_1 = ( -p01 * p_noisy_0 + (1.0 - p01) * p_noisy_1 ) / det
    return float(np.clip(p_mit_1, 0.0, 1.0))
