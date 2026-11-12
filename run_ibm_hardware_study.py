"""
run_ibm_hardware_study.py - Physical IBM Quantum Hardware Calibration Benchmark.

Executes 4-qubit VQC models under realistic calibration profiles:
- IBM Eagle (127-qubit r3)
- IBM Perth (7-qubit r5)
- IBM Manila (5-qubit r5)
- IBM Bogota (5-qubit r4)
- Ideal Statevector Baseline

Analyzes:
1. Physical device degradation (T1/T2 decoherence + gate infidelities)
2. Hardware coupling topology penalty (Native Linear vs Transpiled SWAP Circular)
3. Readout Error Mitigation (REM via M^-1 inversion) recovery
"""

import os
import sys
import json
import time
import numpy as np
import torch
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

sys.path.insert(0, os.path.abspath("."))
from data import load_and_preprocess_data
from vqc_toolkit.noise.calibration import PRESET_PROFILES
from vqc_toolkit.noise.hardware_backend import (
    make_hardware_vqc_qnode,
    apply_hardware_readout_noise_and_mitigation
)


def run_hardware_study():
    print("=" * 75)
    print("STARTING IBM QUANTUM HARDWARE CALIBRATION BENCHMARK STUDY")
    print("=" * 75)

    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    # 1. Load Test Data
    print("\n[1/4] Loading PneumoniaMNIST Test Dataset (100 samples)...")
    data_dict = load_and_preprocess_data(seed=42)
    X_test = data_dict["X_test"]
    y_test = data_dict["y_test"]

    # 2. Load Pretrained VQC Checkpoints (Seed 42, L=2)
    print("\n[2/4] Loading Pre-trained VQC Weights (L=2)...")
    ckpt_lin = torch.load("checkpoints/vqc_seed42_linear_L2.pt", map_location="cpu", weights_only=True)
    ckpt_circ = torch.load("checkpoints/vqc_seed42_circular_L2.pt", map_location="cpu", weights_only=True)
    w_lin = ckpt_lin["weights"]
    w_circ = ckpt_circ["weights"]

    # First, compute Ideal Clean Predictions as reference
    print("\n[3/4] Computing Clean Ideal Statevector Reference...")
    clean_qnode, _ = make_hardware_vqc_qnode(profile_name="ideal_baseline", topology="linear", n_layers=2)
    clean_probs = []
    for x in X_test:
        exp_z = float(clean_qnode(x, w_lin))
        clean_probs.append(float(np.clip((1.0 - exp_z) / 2.0, 0.0, 1.0)))
    clean_probs = np.array(clean_probs)
    clean_preds = (clean_probs >= 0.5).astype(int)
    ideal_acc = accuracy_score(y_test, clean_preds)
    print(f"  Ideal Statevector Accuracy: {ideal_acc * 100:.2f}%")

    # 3. Benchmark Devices & Configurations
    profiles_to_test = ["ibm_eagle", "ibm_perth", "ibm_manila", "ibm_bogota"]
    
    study_results = {
        "metadata": {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dataset": "PneumoniaMNIST (4 PCA)",
            "n_test_samples": len(y_test),
            "layers": 2,
            "trained_checkpoint_seed": 42,
            "ideal_accuracy": float(ideal_acc)
        },
        "devices": {}
    }

    print("\n[4/4] Simulating Physical Hardware Backends...")
    print(f"{'Device Profile':<22} | {'Topology':<10} | {'Routing':<8} | {'REM':<5} | {'Acc (%)':<8} | {'F1':<6} | {'CNOTs':<6} | {'P-Drift':<7}")
    print("-" * 88)

    for dev_name in ["ideal_baseline"] + profiles_to_test:
        prof = PRESET_PROFILES[dev_name]
        study_results["devices"][dev_name] = {
            "device_name": prof.name,
            "t1_us": prof.t1_us,
            "t2_us": prof.t2_us,
            "cnot_error": prof.two_qubit_cnot_error,
            "readout_p01": prof.readout_error_p01,
            "readout_p10": prof.readout_error_p10,
            "evaluations": []
        }

        # Configurations to test for this device:
        # A: Linear Native (0 SWAPs, 6 CNOTs) - Raw & REM
        # B: Circular Unrouted (Ideal 8 CNOTs) - Raw & REM
        # C: Circular SWAP-Routed (Physical 32 CNOTs) - Raw & REM
        configs = [
            ("linear", False, False, "Linear Native (Raw)", 6),
            ("linear", False, True, "Linear Native (REM Mitigated)", 6),
            ("circular", False, False, "Circular (Unrouted)", 8),
            ("circular", True, False, "Circular (SWAP Routed Raw)", 32),
            ("circular", True, True, "Circular (SWAP Routed REM)", 32)
        ]

        if dev_name == "ideal_baseline":
            configs = [("linear", False, False, "Ideal Reference", 6)]

        for topo, transpile, use_rem, label, cnot_count in configs:
            weights = w_lin if topo == "linear" else w_circ
            qnode, profile = make_hardware_vqc_qnode(
                profile_name=dev_name,
                n_qubits=4,
                n_layers=2,
                topology=topo,
                transpile_routing=transpile
            )

            noisy_probs = []
            for x in X_test:
                exp_z = float(qnode(x, weights))
                raw_prob = (1.0 - exp_z) / 2.0
                # Apply physical asymmetric readout noise & optional REM
                final_prob = apply_hardware_readout_noise_and_mitigation(raw_prob, profile, mitigate=use_rem)
                noisy_probs.append(final_prob)

            noisy_probs = np.array(noisy_probs)
            preds = (noisy_probs >= 0.5).astype(int)

            acc = float(accuracy_score(y_test, preds))
            prec = float(precision_score(y_test, preds, zero_division=0))
            rec = float(recall_score(y_test, preds, zero_division=0))
            f1 = float(f1_score(y_test, preds, zero_division=0))
            prob_drift = float(np.mean(np.abs(noisy_probs - clean_probs)))

            rem_str = "YES" if use_rem else "NO"
            rout_str = "SWAP" if transpile else "None"
            print(f"{prof.name[:21]:<22} | {topo:<10} | {rout_str:<8} | {rem_str:<5} | {acc*100:>6.2f}% | {f1:>6.4f} | {cnot_count:<6} | {prob_drift:<7.4f}")

            eval_entry = {
                "label": label,
                "topology": topo,
                "transpile_routing": transpile,
                "readout_mitigation": use_rem,
                "total_effective_cnots": cnot_count,
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "mean_prob_drift": prob_drift
            }
            study_results["devices"][dev_name]["evaluations"].append(eval_entry)

    # 4. Save JSON Results
    with open("results/ibm_hardware_benchmark_results.json", "w") as f:
        json.dump(study_results, f, indent=2)
    print("\nSaved results to results/ibm_hardware_benchmark_results.json")

    # 5. Generate Publication Figure
    print("Generating publication figure: figures/ibm_hardware_benchmark.png ...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)

    # Plot 1: Device-by-Device Degradation (Linear Native vs Clean)
    dev_labels = ["Ideal Simulator", "IBM Eagle (127Q)", "IBM Perth (7Q)", "IBM Manila (5Q)", "IBM Bogota (5Q)"]
    dev_keys = ["ideal_baseline", "ibm_eagle", "ibm_perth", "ibm_manila", "ibm_bogota"]
    
    linear_accs = []
    linear_rems = []
    for k in dev_keys:
        evals = study_results["devices"][k]["evaluations"]
        raw_eval = evals[0]["accuracy"] * 100
        rem_eval = evals[1]["accuracy"] * 100 if len(evals) > 1 else raw_eval
        linear_accs.append(raw_eval)
        linear_rems.append(rem_eval)

    x = np.arange(len(dev_labels))
    width = 0.35

    ax = axes[0]
    bars1 = ax.bar(x - width/2, linear_accs, width, label="Raw Hardware", color="#3b82f6", edgecolor="#1d4ed8")
    bars2 = ax.bar(x + width/2, linear_rems, width, label="With REM (M⁻¹)", color="#10b981", edgecolor="#047857")
    ax.set_ylabel("Test Accuracy (%)", fontsize=11, fontweight="bold")
    ax.set_title("A. Physical IBM Hardware Degradation & Mitigation", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(["Ideal", "Eagle\n(r3)", "Perth\n(r5)", "Manila\n(r5)", "Bogota\n(r4)"], fontsize=10)
    ax.set_ylim(60, 95)
    ax.axhline(82.0, color="#dc2626", linestyle="--", linewidth=1.5, label="Logistic Regression (82%)")
    ax.legend(frameon=True, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Plot 2: Coupling Graph Routing Penalty (Native Linear vs SWAP Circular)
    ax = axes[1]
    swap_labels = ["Eagle", "Perth", "Manila", "Bogota"]
    swap_keys = ["ibm_eagle", "ibm_perth", "ibm_manila", "ibm_bogota"]
    
    lin_native = [study_results["devices"][k]["evaluations"][0]["accuracy"] * 100 for k in swap_keys]
    circ_routed = [study_results["devices"][k]["evaluations"][3]["accuracy"] * 100 for k in swap_keys]

    x2 = np.arange(len(swap_labels))
    b1 = ax.bar(x2 - width/2, lin_native, width, label="Linear (Native, 6 CNOTs)", color="#2563eb")
    b2 = ax.bar(x2 + width/2, circ_routed, width, label="Circular (SWAP Routed, 32 CNOTs)", color="#f59e0b")
    ax.set_ylabel("Test Accuracy (%)", fontsize=11, fontweight="bold")
    ax.set_title("B. Hardware Coupling Graph SWAP Penalty", fontsize=12, fontweight="bold")
    ax.set_xticks(x2)
    ax.set_xticklabels(swap_labels, fontsize=10)
    ax.set_ylim(60, 95)
    ax.legend(frameon=True, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Plot 3: Probability Drift vs Ideal Statevector
    ax = axes[2]
    drift_keys = ["ibm_eagle", "ibm_perth", "ibm_manila", "ibm_bogota"]
    drift_vals = [study_results["devices"][k]["evaluations"][0]["mean_prob_drift"] for k in drift_keys]
    cnot_errors = [study_results["devices"][k]["cnot_error"] * 100 for k in drift_keys]

    ax.scatter(cnot_errors, drift_vals, s=150, c="#8b5cf6", edgecolor="#4c1d95", zorder=3)
    for i, txt in enumerate(["Eagle", "Perth", "Manila", "Bogota"]):
        ax.annotate(f" {txt}", (cnot_errors[i], drift_vals[i]), fontsize=10, fontweight="bold")

    ax.set_xlabel("Physical CNOT Error Rate (%)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Mean |P_noisy - P_ideal| Drift", fontsize=11, fontweight="bold")
    ax.set_title("C. Gate Infidelity vs Probability Contraction", fontsize=12, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig("figures/ibm_hardware_benchmark.png", dpi=300)
    plt.close()
    print("Saved figure to figures/ibm_hardware_benchmark.png")
    print("\n" + "=" * 75)
    print("IBM HARDWARE BENCHMARK STUDY COMPLETE!")
    print("=" * 75)


if __name__ == "__main__":
    run_hardware_study()
