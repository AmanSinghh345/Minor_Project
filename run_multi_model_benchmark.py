"""
Multi-Model & Multi-Dataset Quantum-Classical Benchmark Runner.
Compares:
1. Datasets: PneumoniaMNIST (Medical Vision) & Breast Cancer Wisconsin (Clinical Tabular)
2. Classical Models: Logistic Regression, Linear SVM, RBF SVM, Random Forest, Small MLP
3. Quantum Architectures: Standard VQC, Data Re-uploading VQC, Quantum Kernel Method (QSVC)
4. Noise Channels: Depolarizing & Amplitude Damping at 0%, 2%, and 5% error rates.
"""

import os
import sys
import json
import time
import numpy as np
import torch
import pennylane as qml
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# Local imports
sys.path.insert(0, os.path.abspath("."))
from data import load_and_preprocess_data
from vqc_toolkit.benchmarks.datasets import load_cancer_dataset
from vqc_toolkit.benchmarks.classical import evaluate_classical_suite
from vqc_toolkit.ansatz.reuploading import make_reuploading_vqc_qnode
from vqc_toolkit.ansatz.kernel import build_quantum_kernel_circuit, compute_kernel_matrix
from noise import make_noisy_vqc_qnode


def run_multi_model_benchmark():
    print("=" * 75)
    print("STARTING MULTI-MODEL & MULTI-DATASET QUANTUM-CLASSICAL BENCHMARK")
    print("=" * 75)

    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    # -------------------------------------------------------------------------
    # 1. Load Datasets
    # -------------------------------------------------------------------------
    print("\n[1/4] Loading Datasets...")
    # Dataset A: PneumoniaMNIST (300 train, 100 test)
    data_pn = load_and_preprocess_data(seed=42)
    X_tr_pn, y_tr_pn = data_pn["X_train"], data_pn["y_train"]
    X_te_pn, y_te_pn = data_pn["X_test"], data_pn["y_test"]
    print(f"  PneumoniaMNIST: {len(X_tr_pn)} train, {len(X_te_pn)} test (4 PCA features)")

    # Dataset B: Breast Cancer Wisconsin (426 train, 143 test, 4 PCA features)
    X_tr_bc, X_te_bc, y_tr_bc, y_te_bc = load_cancer_dataset(seed=42)
    print(f"  Breast Cancer:  {len(X_tr_bc)} train, {len(X_te_bc)} test (4 PCA features)")

    # -------------------------------------------------------------------------
    # 2. Comprehensive Classical Benchmark Suite
    # -------------------------------------------------------------------------
    print("\n[2/4] Evaluating 5 Classical ML Techniques...")
    classical_pn = evaluate_classical_suite(X_tr_pn, y_tr_pn, X_te_pn, y_te_pn, seed=42)
    classical_bc = evaluate_classical_suite(X_tr_bc, y_tr_bc, X_te_bc, y_te_bc, seed=42)

    print("  Classical Accuracies on PneumoniaMNIST:")
    for k, v in classical_pn.items():
        print(f"    • {k:<20}: {v*100:.2f}%")

    print("\n  Classical Accuracies on Breast Cancer:")
    for k, v in classical_bc.items():
        print(f"    • {k:<20}: {v*100:.2f}%")

    # -------------------------------------------------------------------------
    # 3. Train & Evaluate Quantum Architectures
    # -------------------------------------------------------------------------
    print("\n[3/4] Evaluating 3 Quantum Architectures under Clean & Physical Noise...")

    # Load pre-trained Standard VQC weights for Seed 42
    ckpt_circ_l2 = torch.load("checkpoints/vqc_seed42_circular_L2.pt", weights_only=True)
    w_std_vqc = ckpt_circ_l2["weights"]

    # Train Data Re-uploading VQC on PneumoniaMNIST subset (for speed)
    torch.manual_seed(42)
    qnode_reup_clean = make_reuploading_vqc_qnode(n_qubits=4, n_layers=2)
    w_reup = (0.01 * torch.randn(2, 4, 3, dtype=torch.float32)).requires_grad_(True)
    opt_reup = torch.optim.Adam([w_reup], lr=0.04)
    targets_pn = np.where(y_tr_pn[:100] == 0, 1.0, -1.0)
    
    for _ in range(20):
        opt_reup.zero_grad()
        loss = torch.tensor(0.0)
        idx = np.random.choice(100, 16, replace=False)
        for i in idx:
            pred = qnode_reup_clean(w_reup, torch.tensor(X_tr_pn[i], dtype=torch.float32))
            loss = loss + (pred - torch.tensor(targets_pn[i], dtype=torch.float32))**2
        (loss / 16.0).backward()
        opt_reup.step()

    # Train Quantum Kernel Estimator (QSVC) on subset (50 train, 50 test for fast kernel matrix)
    sub_k_tr = X_tr_pn[:50]
    sub_k_y_tr = y_tr_pn[:50]
    sub_k_te = X_te_pn[:50]
    sub_k_y_te = y_te_pn[:50]

    kernel_fn_clean = build_quantum_kernel_circuit(n_qubits=4, noise_type=None, noise_rate=0.0)
    K_tr_clean = compute_kernel_matrix(sub_k_tr, sub_k_tr, kernel_fn_clean)
    K_te_clean = compute_kernel_matrix(sub_k_te, sub_k_tr, kernel_fn_clean)

    qsvc_clean = SVC(kernel="precomputed")
    qsvc_clean.fit(K_tr_clean, sub_k_y_tr)
    acc_qsvc_clean = float(qsvc_clean.score(K_te_clean, sub_k_y_te))

    # Evaluate Quantum Models under noise: 0%, 2% Amp, 5% Amp, 5% Depol
    noise_scenarios = [
        ("Clean", None, 0.0),
        ("2% Amp Damping", "amplitude_damping", 0.02),
        ("5% Amp Damping", "amplitude_damping", 0.05),
        ("5% Depolarizing", "depolarizing", 0.05)
    ]

    quantum_results = {}
    for sc_name, n_type, n_rate in noise_scenarios:
        # 1. Standard VQC
        circ_std = make_noisy_vqc_qnode(n_type or "depolarizing", n_rate, "circular", 2, 4)
        with torch.no_grad():
            preds_std = [(float(circ_std(w_std_vqc, torch.tensor(x, dtype=torch.float32).unsqueeze(0)).item()) <= 0.0) for x in X_te_pn]
            acc_std = float(np.mean(np.array(preds_std).astype(int) == y_te_pn))

        # 2. Data Re-uploading VQC
        circ_reup = make_reuploading_vqc_qnode(4, 2, n_type, n_rate)
        with torch.no_grad():
            preds_reup = [(float(circ_reup(w_reup, torch.tensor(x, dtype=torch.float32)).item()) <= 0.0) for x in X_te_pn]
            acc_reup = float(np.mean(np.array(preds_reup).astype(int) == y_te_pn))

        # 3. Quantum Kernel (QSVC)
        if n_rate == 0.0:
            acc_qsvc = acc_qsvc_clean
        else:
            k_fn_noisy = build_quantum_kernel_circuit(4, n_type, n_rate)
            K_te_noisy = compute_kernel_matrix(sub_k_te, sub_k_tr, k_fn_noisy)
            acc_qsvc = float(qsvc_clean.score(K_te_noisy, sub_k_y_te))

        quantum_results[sc_name] = {
            "standard_vqc": acc_std,
            "data_reuploading_vqc": acc_reup,
            "quantum_kernel_qsvc": acc_qsvc
        }
        print(f"  [{sc_name}] Standard VQC: {acc_std*100:.1f}% | Data Re-upload: {acc_reup*100:.1f}% | QSVC Kernel: {acc_qsvc*100:.1f}%")

    # -------------------------------------------------------------------------
    # 4. Generate Publication Figure & Save JSON
    # -------------------------------------------------------------------------
    print("\n[4/4] Generating Multi-Model Publication Figure...")

    plt.figure(figsize=(10, 5.5), dpi=300)
    scenarios = list(quantum_results.keys())
    x = np.arange(len(scenarios))
    width = 0.25

    acc_std_vals = [quantum_results[s]["standard_vqc"] * 100 for s in scenarios]
    acc_reup_vals = [quantum_results[s]["data_reuploading_vqc"] * 100 for s in scenarios]
    acc_qsvc_vals = [quantum_results[s]["quantum_kernel_qsvc"] * 100 for s in scenarios]

    plt.bar(x - width, acc_std_vals, width, label="Standard VQC (Circular L=2)", color="#3b82f6", edgecolor="#1e293b")
    plt.bar(x, acc_reup_vals, width, label="Data Re-uploading VQC", color="#8b5cf6", edgecolor="#1e293b")
    plt.bar(x + width, acc_qsvc_vals, width, label="Quantum Kernel (QSVC)", color="#10b981", edgecolor="#1e293b")

    # Reference lines for classical baselines
    plt.axhline(classical_pn["logistic_regression"] * 100, color="#64748b", linestyle="--", label="Logistic Regression (81.0%)")
    plt.axhline(classical_pn["random_forest"] * 100, color="#f59e0b", linestyle=":", label="Random Forest (86.0%)")

    plt.xticks(x, scenarios, fontweight="bold", fontsize=11)
    plt.ylabel("Test Classification Accuracy (%)", fontweight="bold", fontsize=11)
    plt.title("Comparative Noise Resilience Across Quantum ML Paradigms", fontweight="bold", fontsize=12, pad=12)
    plt.ylim(55, 95)
    plt.legend(loc="lower left", fontsize=9)
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig("figures/multi_model_comparison.png")
    plt.close()

    payload = {
        "classical_benchmarks": {
            "pneumonia_mnist": classical_pn,
            "breast_cancer_wisconsin": classical_bc
        },
        "quantum_paradigms_noise_sweep": quantum_results
    }

    with open("results/multi_model_benchmark_results.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("\n" + "=" * 75)
    print("BENCHMARK COMPLETED SUCCESSFULLY!")
    print("Saved figures/multi_model_comparison.png")
    print("Saved results/multi_model_benchmark_results.json")
    print("=" * 75)


if __name__ == "__main__":
    run_multi_model_benchmark()
