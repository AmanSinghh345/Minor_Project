"""
export_dashboard_data.py - Data exporter for the presentation dashboard.

Generates:
1. dashboard/public/data/metrics.json:
   - Grouped metrics (mean ± std, ddof=1) for VQC configurations across
     noise type, noise rate, depth, and topology.
   - Classical baselines (Logistic Regression & Small MLP) mean ± std.
2. dashboard/public/data/predictions.json:
   - 12 test images (6 normal, 6 pneumonia).
   - Real model predictions from saved VQC checkpoints across all noise rates/types.
   - Real predictions from trained Logistic Regression and Small MLP.
3. dashboard/public/data/images/:
   - 12 test chest X-ray images saved as PNGs (img_0.png .. img_11.png).
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from sklearn.linear_model import LogisticRegression
from medmnist import PneumoniaMNIST

# Local project imports
from data import load_and_preprocess_data
from noise import make_noisy_vqc_qnode
from baseline import SmallMLPPyTorch


def export_dashboard_data():
    print("=" * 70)
    print("STEP 1: EXPORTING DASHBOARD METRICS & PREDICTIONS")
    print("=" * 70)

    # Create target directories
    os.makedirs("dashboard/public/data/images", exist_ok=True)

    # -------------------------------------------------------------------------
    # 1. Export Metrics JSON
    # -------------------------------------------------------------------------
    print("\n[1/3] Processing sweep results and classical baselines...")
    vqc_sweep_path = "results/vqc_noise_sweep_results.csv"
    classical_path = "results/classical_baseline_results.csv"

    if not os.path.exists(vqc_sweep_path) or not os.path.exists(classical_path):
        raise FileNotFoundError("Results CSV files missing in results/ directory!")

    df_vqc = pd.read_csv(vqc_sweep_path)
    df_classical = pd.read_csv(classical_path)

    # Compute classical baselines summary (mean ± sample std, ddof=1)
    classical_summary = {}
    for model_name, sub in df_classical.groupby("model"):
        clean_key = "logistic_regression" if "Logistic" in model_name else "small_mlp"
        classical_summary[clean_key] = {
            "name": model_name,
            "accuracy_mean": float(sub["accuracy"].mean()),
            "accuracy_std": float(sub["accuracy"].std(ddof=1)),
            "precision_mean": float(sub["precision"].mean()),
            "precision_std": float(sub["precision"].std(ddof=1)),
            "recall_mean": float(sub["recall"].mean()),
            "recall_std": float(sub["recall"].std(ddof=1)),
            "f1_mean": float(sub["f1"].mean()),
            "f1_std": float(sub["f1"].std(ddof=1)),
            "per_seed_accuracy": sub.set_index("seed")["accuracy"].to_dict()
        }

    # Compute quantum sweep summary grouped by topology, layers, noise_type, noise_rate
    vqc_grouped = []
    group_cols = ["topology", "layers", "noise_type", "noise_rate"]
    for (topo, depth, n_type, n_rate), group in df_vqc.groupby(group_cols):
        vqc_grouped.append({
            "topology": topo,
            "layers": int(depth),
            "noise_type": n_type,
            "noise_rate": float(n_rate),
            "accuracy_mean": float(group["accuracy"].mean()),
            "accuracy_std": float(group["accuracy"].std(ddof=1)),
            "precision_mean": float(group["precision"].mean()),
            "precision_std": float(group["precision"].std(ddof=1)),
            "recall_mean": float(group["recall"].mean()),
            "recall_std": float(group["recall"].std(ddof=1)),
            "f1_mean": float(group["f1"].mean()),
            "f1_std": float(group["f1"].std(ddof=1)),
            "n_runs": len(group)
        })

    # Prepare structured line-chart curve series for front-end convenience
    chart_series = {}
    for topo in ["circular", "linear"]:
        for depth in [1, 2, 3]:
            for n_type in ["depolarizing", "amplitude_damping"]:
                key = f"{topo}_L{depth}_{n_type}"
                matching = [
                    g for g in vqc_grouped
                    if g["topology"] == topo and g["layers"] == depth and g["noise_type"] == n_type
                ]
                matching = sorted(matching, key=lambda x: x["noise_rate"])
                chart_series[key] = [
                    {
                        "rate": m["noise_rate"],
                        "accuracy": round(m["accuracy_mean"] * 100, 2),
                        "std": round(m["accuracy_std"] * 100, 2),
                        "upper": round((m["accuracy_mean"] + m["accuracy_std"]) * 100, 2),
                        "lower": round((m["accuracy_mean"] - m["accuracy_std"]) * 100, 2),
                    }
                    for m in matching
                ]

    metrics_payload = {
        "classical_baselines": classical_summary,
        "vqc_grouped_metrics": vqc_grouped,
        "chart_series": chart_series,
        "available_rates": sorted(df_vqc["noise_rate"].unique().tolist()),
        "available_noise_types": ["depolarizing", "amplitude_damping"],
        "available_topologies": ["circular", "linear"],
        "available_layers": [1, 2, 3]
    }

    with open("dashboard/public/data/metrics.json", "w") as f:
        json.dump(metrics_payload, f, indent=2)
    print("  Saved dashboard/public/data/metrics.json")

    # -------------------------------------------------------------------------
    # 2. Select 12 Test Images & Save PNGs
    # -------------------------------------------------------------------------
    print("\n[2/3] Extracting 12 test chest X-rays (6 normal, 6 pneumonia)...")
    data_dict = load_and_preprocess_data(seed=42)
    X_train_scaled = data_dict["X_train"]
    y_train = data_dict["y_train"]
    X_test_scaled = data_dict["X_test"]
    y_test = data_dict["y_test"]

    # Load raw PneumoniaMNIST test images to extract corresponding raw 28x28 arrays
    raw_test = PneumoniaMNIST(split="test", download=True)
    rng = np.random.default_rng(42)
    test_labels = raw_test.labels.flatten()
    test_idx_0 = np.where(test_labels == 0)[0]
    test_idx_1 = np.where(test_labels == 1)[0]
    chosen_test_0 = rng.choice(test_idx_0, size=50, replace=False)
    chosen_test_1 = rng.choice(test_idx_1, size=50, replace=False)
    test_indices = np.concatenate([chosen_test_0, chosen_test_1])
    rng.shuffle(test_indices)
    raw_test_imgs = raw_test.imgs[test_indices]  # (100, 28, 28)

    # Pick 6 normal (y=0) and 6 pneumonia (y=1)
    norm_indices = np.where(y_test == 0)[0][:6]
    pneu_indices = np.where(y_test == 1)[0][:6]
    selected_indices = np.concatenate([norm_indices, pneu_indices])

    selected_samples = []
    for sample_id, idx in enumerate(selected_indices):
        img_filename = f"img_{sample_id}.png"
        img_path = os.path.join("dashboard/public/data/images", img_filename)
        
        # Save raw 28x28 image
        raw_arr = raw_test_imgs[idx]
        img = Image.fromarray(raw_arr)
        img.save(img_path)

        selected_samples.append({
            "id": sample_id,
            "test_idx": int(idx),
            "image_filename": img_filename,
            "true_label": int(y_test[idx]),
            "true_class_name": "Normal" if y_test[idx] == 0 else "Pneumonia",
            "pca_features": [round(float(val), 4) for val in X_test_scaled[idx]]
        })
    print(f"  Saved 12 images to dashboard/public/data/images/")

    # -------------------------------------------------------------------------
    # 3. Compute Real Classical & VQC Predictions
    # -------------------------------------------------------------------------
    print("\n[3/3] Evaluating real VQC checkpoints and classical baselines on the 12 samples...")
    # Train classical models on Seed 42
    lr_model = LogisticRegression(random_state=42, max_iter=500)
    lr_model.fit(X_train_scaled, y_train)

    torch.manual_seed(42)
    mlp_model = SmallMLPPyTorch()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(mlp_model.parameters(), lr=0.01)
    X_train_t = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    for _ in range(300):
        optimizer.zero_grad()
        loss = criterion(mlp_model(X_train_t), y_train_t)
        loss.backward()
        optimizer.step()
    mlp_model.eval()

    # Pre-load VQC model checkpoints for Seed 42 (primary seed)
    vqc_checkpoints = {}
    for topo in ["circular", "linear"]:
        for depth in [1, 2, 3]:
            ckpt_file = f"checkpoints/vqc_seed42_{topo}_L{depth}.pt"
            ckpt = torch.load(ckpt_file, map_location="cpu", weights_only=True)
            vqc_checkpoints[(topo, depth)] = ckpt["weights"]

    # Calculate real predictions for each of the 12 samples
    sample_features = np.array([X_test_scaled[s["test_idx"]] for s in selected_samples])

    # Classical predictions
    lr_probs = lr_model.predict_proba(sample_features)[:, 1]
    lr_preds = (lr_probs >= 0.5).astype(int)

    with torch.no_grad():
        mlp_logits = mlp_model(torch.tensor(sample_features, dtype=torch.float32)).squeeze().numpy()
        mlp_probs = 1.0 / (1.0 + np.exp(-mlp_logits))
        mlp_preds = (mlp_probs >= 0.5).astype(int)

    for i, s in enumerate(selected_samples):
        s["classical_predictions"] = {
            "logistic_regression": {
                "probability_pneumonia": round(float(lr_probs[i]), 4),
                "predicted_label": int(lr_preds[i]),
                "predicted_class_name": "Pneumonia" if lr_preds[i] == 1 else "Normal",
                "is_correct": bool(lr_preds[i] == s["true_label"])
            },
            "small_mlp": {
                "probability_pneumonia": round(float(mlp_probs[i]), 4),
                "predicted_label": int(mlp_preds[i]),
                "predicted_class_name": "Pneumonia" if mlp_preds[i] == 1 else "Normal",
                "is_correct": bool(mlp_preds[i] == s["true_label"])
            }
        }
        s["vqc_predictions"] = {}

    # Run real VQC circuits
    noise_rates = [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]
    total_configs = 2 * 3 * 2 * len(noise_rates)
    count = 0

    for topo in ["circular", "linear"]:
        for depth in [1, 2, 3]:
            weights = vqc_checkpoints[(topo, depth)]
            for n_type in ["depolarizing", "amplitude_damping"]:
                for n_rate in noise_rates:
                    count += 1
                    qnode = make_noisy_vqc_qnode(
                        noise_type=n_type,
                        noise_rate=n_rate,
                        topology=topo,
                        n_layers=depth,
                        n_qubits=4
                    )
                    
                    config_key = f"{topo}_L{depth}_{n_type}_{n_rate}"
                    with torch.no_grad():
                        for i, s in enumerate(selected_samples):
                            x_sample = sample_features[i]
                            feat_t = torch.tensor(x_sample, dtype=torch.float32).unsqueeze(0)
                            expval = float(qnode(weights, feat_t).item())
                            
                            # Decision logic: expval in [-1, +1]
                            # p(pneumonia = 1) = (1 - <Z>) / 2
                            prob_pneu = (1.0 - expval) / 2.0
                            pred_label = 1 if expval <= 0.0 else 0
                            
                            s["vqc_predictions"][config_key] = {
                                "expectation_value": round(expval, 4),
                                "probability_pneumonia": round(prob_pneu, 4),
                                "predicted_label": int(pred_label),
                                "predicted_class_name": "Pneumonia" if pred_label == 1 else "Normal",
                                "is_correct": bool(pred_label == s["true_label"])
                            }

    predictions_payload = {
        "metadata": {
            "n_samples": len(selected_samples),
            "evaluated_checkpoint_seed": 42,
            "description": "Real model inference on 12 test samples across all configurations."
        },
        "samples": selected_samples
    }

    with open("dashboard/public/data/predictions.json", "w") as f:
        json.dump(predictions_payload, f, indent=2)
    print("  Saved dashboard/public/data/predictions.json")

    # Copy multi-model benchmark results if available
    multi_model_res_path = "results/multi_model_benchmark_results.json"
    if os.path.exists(multi_model_res_path):
        with open(multi_model_res_path, "r") as src, open("dashboard/public/data/multi_model.json", "w") as dst:
            dst.write(src.read())
        print("  Copied multi-model benchmark results to dashboard/public/data/multi_model.json")

    print("\n" + "=" * 70)
    print("STEP 1 COMPLETE: DASHBOARD EXPORT SUCCESSFUL!")
    print("=" * 70)


if __name__ == "__main__":
    export_dashboard_data()
