"""
run_experiments.py - Multi-Seed Experiment Sweep for Noisy VQC vs Classical Baselines.

This module automates the complete experimental matrix:
- 5 Seeds: [42, 43, 44, 45, 46]
- 2 Classical Baselines: Logistic Regression, Small MLP (4-8-1)
- 2 Quantum Topologies: 'linear' (3 CNOTs/layer), 'circular' (4 CNOTs/layer)
- 3 Circuit Depths: L in {1, 2, 3}
- 2 Quantum Noise Channels: Depolarizing, Amplitude Damping
- 7 Noise Rates: [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]
Total: 30 trained VQC models, 420 quantum noisy evaluation runs, 10 classical baseline runs.

Features:
- Checkpoint persistence for all trained models (.pt files).
- Incremental CSV writing with resume capability (skips already computed runs).
- Real-time progress logging with elapsed time and ETA.
"""

import os
import time
import argparse
import numpy as np
import pandas as pd
import pennylane as qml
import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from data import load_and_preprocess_data
from baseline import train_and_evaluate_baseline
from model import VariationalQuantumClassifier, train_vqc


# ==============================================================================
# FAST CACHED NOISY EVALUATOR
# ==============================================================================

class CachedNoisyVQCManager:
    """
    Caches PennyLane QNodes on 'default.mixed' per (noise_type, topology, n_layers)
    so devices and computational graphs are instantiated once, rather than re-compiled
    hundreds of times.
    """
    def __init__(self, n_qubits: int = 4):
        self.n_qubits = n_qubits
        self.qnodes = {}

    def get_qnode(self, noise_type: str, topology: str, n_layers: int):
        key = (noise_type, topology, n_layers)
        if key in self.qnodes:
            return self.qnodes[key]

        dev = qml.device("default.mixed", wires=self.n_qubits)

        @qml.qnode(dev, interface="torch")
        def circuit(weights: torch.Tensor, features: torch.Tensor, noise_rate: float):
            def apply_channel(wire):
                if noise_rate > 0.0:
                    if noise_type == "depolarizing":
                        qml.DepolarizingChannel(noise_rate, wires=wire)
                    elif noise_type == "amplitude_damping":
                        qml.AmplitudeDamping(noise_rate, wires=wire)

            # Step 1: Angle Encoding Layer + noise
            for i in range(self.n_qubits):
                qml.RY(features[:, i], wires=i)
                apply_channel(i)

            # Step 2: Variational Layers + noise after each gate
            for l in range(n_layers):
                for i in range(self.n_qubits):
                    qml.RY(weights[l, i], wires=i)
                    apply_channel(i)

                for i in range(self.n_qubits - 1):
                    qml.CNOT(wires=[i, i + 1])
                    apply_channel(i)
                    apply_channel(i + 1)

                if topology == "circular":
                    qml.CNOT(wires=[self.n_qubits - 1, 0])
                    apply_channel(self.n_qubits - 1)
                    apply_channel(0)

            # Step 3: Measurement on readout qubit 0
            return qml.expval(qml.PauliZ(0))

        self.qnodes[key] = circuit
        return circuit

    def evaluate(self, weights: torch.Tensor, X_test: torch.Tensor, y_test: np.ndarray,
                 noise_type: str, noise_rate: float, topology: str, n_layers: int) -> dict:
        qnode = self.get_qnode(noise_type, topology, n_layers)
        with torch.no_grad():
            expvals = qnode(weights, X_test, noise_rate).float()
            preds = (expvals <= 0.0).int().cpu().numpy()

        return {
            "accuracy": float(accuracy_score(y_test, preds)),
            "precision": float(precision_score(y_test, preds, zero_division=0)),
            "recall": float(recall_score(y_test, preds, zero_division=0)),
            "f1": float(f1_score(y_test, preds, zero_division=0)),
        }


# ==============================================================================
# CLASSICAL BASELINES SWEEP
# ==============================================================================

def run_classical_baselines(seeds: list[int], output_csv: str, lr: float = 0.05,
                            epochs: int = 250, verbose: bool = True) -> pd.DataFrame:
    """
    Trains and evaluates Logistic Regression and Small MLP across all seeds.
    Saves and returns the classical baseline benchmark dataframe.
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    records = []
    if os.path.exists(output_csv):
        existing_df = pd.read_csv(output_csv)
        records = existing_df.to_dict("records")
        completed_keys = set((r["seed"], r["model"]) for r in records)
    else:
        completed_keys = set()

    print(f"\n=======================================================")
    print(f"--- RUNNING CLASSICAL BASELINES SWEEP ({len(seeds)} Seeds) ---")
    print(f"=======================================================", flush=True)

    for seed in seeds:
        for model_name in ["Logistic Regression", "Small MLP (4-8-1)"]:
            if (seed, model_name) in completed_keys:
                if verbose:
                    print(f"Skipping completed classical baseline: Seed={seed}, Model={model_name}", flush=True)
                continue

        t0 = time.time()
        results = train_and_evaluate_baseline(seed=seed, lr=lr, epochs=epochs, verbose=False)
        dt = time.time() - t0

        logreg_m = results["logreg"]
        mlp_m = results["mlp"]

        rec_logreg = {
            "seed": seed,
            "model": "Logistic Regression",
            "accuracy": logreg_m["accuracy"],
            "precision": logreg_m["precision"],
            "recall": logreg_m["recall"],
            "f1": logreg_m["f1"],
            "runtime_sec": round(dt / 2.0, 3)
        }
        rec_mlp = {
            "seed": seed,
            "model": "Small MLP (4-8-1)",
            "accuracy": mlp_m["accuracy"],
            "precision": mlp_m["precision"],
            "recall": mlp_m["recall"],
            "f1": mlp_m["f1"],
            "runtime_sec": round(dt / 2.0, 3)
        }

        records.extend([rec_logreg, rec_mlp])
        completed_keys.add((seed, "Logistic Regression"))
        completed_keys.add((seed, "Small MLP (4-8-1)"))

        # Save to CSV incrementally
        pd.DataFrame(records).to_csv(output_csv, index=False)

        if verbose:
            print(f"Seed {seed:2d} | LogReg Acc: {rec_logreg['accuracy']:.4f} (F1: {rec_logreg['f1']:.4f}) | "
                  f"MLP Acc: {rec_mlp['accuracy']:.4f} (F1: {rec_mlp['f1']:.4f}) | {dt:.1f}s", flush=True)

    df = pd.DataFrame(records)
    print(f"\nClassical Baselines Summary Across Seeds:")
    for m_name in ["Logistic Regression", "Small MLP (4-8-1)"]:
        sub = df[df["model"] == m_name]
        print(f"  {m_name:22s} -> Acc: {sub['accuracy'].mean():.4f} +/- {sub['accuracy'].std():.4f} | "
              f"F1: {sub['f1'].mean():.4f} +/- {sub['f1'].std():.4f}", flush=True)

    return df


# ==============================================================================
# QUANTUM VQC EXPERIMENTAL SWEEP
# ==============================================================================

def run_vqc_noise_sweep(seeds: list[int],
                        topologies: list[str],
                        layers: list[int],
                        noise_types: list[str],
                        noise_rates: list[float],
                        output_csv: str = "results/vqc_noise_sweep_results.csv",
                        checkpoints_dir: str = "checkpoints",
                        epochs: int = 120,
                        lr: float = 0.05,
                        resume: bool = True) -> pd.DataFrame:
    """
    Executes the full quantum experimental sweep.
    Trains VQCs noise-free on default.qubit, saves weights, then evaluates under
    noise on default.mixed across all combinations.
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(checkpoints_dir, exist_ok=True)

    # Load existing results if resuming
    records = []
    completed_runs = set()
    if resume and os.path.exists(output_csv):
        existing_df = pd.read_csv(output_csv)
        records = existing_df.to_dict("records")
        for r in records:
            key = (int(r["seed"]), str(r["topology"]), int(r["layers"]), str(r["noise_type"]), round(float(r["noise_rate"]), 5))
            completed_runs.add(key)
        print(f"Resuming experiment sweep: found {len(completed_runs)} already completed runs.", flush=True)

    total_runs = len(seeds) * len(topologies) * len(layers) * len(noise_types) * len(noise_rates)
    remaining_runs = total_runs - len(completed_runs)
    print(f"\n=======================================================")
    print(f"--- QUANTUM VQC NOISE EXPERIMENT SWEEP ---")
    print(f"Total Sweep Matrix Configurations: {total_runs}")
    print(f"Completed Configurations:         {len(completed_runs)}")
    print(f"Remaining Runs to Execute:        {remaining_runs}")
    print(f"=======================================================", flush=True)

    manager = CachedNoisyVQCManager(n_qubits=4)
    run_counter = len(completed_runs)
    sweep_start_time = time.time()

    # Pre-load datasets per seed to avoid repeated data loading
    data_cache = {}

    for seed in seeds:
        if seed not in data_cache:
            data = load_and_preprocess_data(seed=seed)
            data_cache[seed] = {
                "X_train": torch.tensor(data["X_train"], dtype=torch.float32),
                "y_train": torch.tensor(data["y_train"], dtype=torch.float32),
                "X_test": torch.tensor(data["X_test"], dtype=torch.float32),
                "y_test": data["y_test"],
            }

        X_train = data_cache[seed]["X_train"]
        y_train = data_cache[seed]["y_train"]
        X_test = data_cache[seed]["X_test"]
        y_test = data_cache[seed]["y_test"]

        for topology in topologies:
            for n_layers in layers:
                # 1. Model Checkpoint & Training
                ckpt_path = os.path.join(checkpoints_dir, f"vqc_seed{seed}_{topology}_L{n_layers}.pt")
                model = VariationalQuantumClassifier(n_qubits=4, n_layers=n_layers, topology=topology, seed=seed)

                if os.path.exists(ckpt_path):
                    model.load(ckpt_path)
                else:
                    t_train0 = time.time()
                    train_vqc(model, X_train, y_train, lr=lr, epochs=epochs, verbose=False)
                    t_train = time.time() - t_train0
                    model.save(ckpt_path)
                    print(f"[Train] Seed {seed} | {topology:8s} | L={n_layers} | Trained {epochs} epochs in {t_train:.1f}s -> Saved {ckpt_path}", flush=True)

                weights = model.weights.detach()

                # 2. Noisy Evaluations Sweep
                for noise_type in noise_types:
                    for noise_rate in noise_rates:
                        run_key = (seed, topology, n_layers, noise_type, round(float(noise_rate), 5))
                        if run_key in completed_runs:
                            continue

                        t_eval0 = time.time()
                        metrics = manager.evaluate(
                            weights=weights,
                            X_test=X_test,
                            y_test=y_test,
                            noise_type=noise_type,
                            noise_rate=noise_rate,
                            topology=topology,
                            n_layers=n_layers
                        )
                        eval_time = time.time() - t_eval0

                        record = {
                            "seed": seed,
                            "topology": topology,
                            "layers": n_layers,
                            "noise_type": noise_type,
                            "noise_rate": noise_rate,
                            "accuracy": metrics["accuracy"],
                            "precision": metrics["precision"],
                            "recall": metrics["recall"],
                            "f1": metrics["f1"],
                            "runtime_sec": round(eval_time, 3)
                        }
                        records.append(record)
                        completed_runs.add(run_key)
                        run_counter += 1

                        # Incremental persistence
                        pd.DataFrame(records).to_csv(output_csv, index=False)

                        # Progress & ETA reporting
                        elapsed = time.time() - sweep_start_time
                        avg_time_per_run = elapsed / max(1, (run_counter - (total_runs - remaining_runs)))
                        eta_sec = (total_runs - run_counter) * avg_time_per_run

                        if run_counter % 5 == 0 or run_counter == total_runs:
                            print(f"[{run_counter:3d}/{total_runs}] Seed={seed} {topology:8s} L={n_layers} "
                                  f"{noise_type:18s} p={noise_rate:.3f} -> Acc: {metrics['accuracy']:.4f} (F1: {metrics['f1']:.4f}) "
                                  f"| Elapsed: {elapsed:.0f}s | ETA: {eta_sec / 60:.1f}m", flush=True)

    print(f"\nExperiment sweep completed successfully! Results saved to {output_csv}", flush=True)
    return pd.DataFrame(records)


# ==============================================================================
# MAIN CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Stage 4: Automated Experiment Sweep")
    parser.add_argument("--seeds", nargs="+", type=int, default=[42, 43, 44, 45, 46], help="List of random seeds")
    parser.add_argument("--topologies", nargs="+", type=str, default=["linear", "circular"], help="Topologies to benchmark")
    parser.add_argument("--layers", nargs="+", type=int, default=[1, 2, 3], help="Ansatz depths")
    parser.add_argument("--noise-types", nargs="+", type=str, default=["depolarizing", "amplitude_damping"], help="Noise channels")
    parser.add_argument("--noise-rates", nargs="+", type=float, default=[0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05], help="Noise rates")
    parser.add_argument("--epochs", type=int, default=120, help="Training epochs per VQC")
    parser.add_argument("--lr", type=float, default=0.05, help="Learning rate")
    parser.add_argument("--output-dir", type=str, default="results", help="Directory for output CSVs")
    parser.add_argument("--checkpoints-dir", type=str, default="checkpoints", help="Directory for VQC weight checkpoints")
    parser.add_argument("--quick", action="store_true", help="Run quick sanity sweep (seed 42 only, 3 rates)")
    args = parser.parse_args()

    if args.quick:
        args.seeds = [42]
        args.noise_rates = [0.0, 0.01, 0.05]
        print(">>> RUNNING IN QUICK SANITY MODE <<<")

    output_baseline_csv = os.path.join(args.output_dir, "classical_baseline_results.csv")
    output_vqc_csv = os.path.join(args.output_dir, "vqc_noise_sweep_results.csv")

    # Step 1: Classical Baselines
    run_classical_baselines(
        seeds=args.seeds,
        output_csv=output_baseline_csv,
        lr=args.lr,
        epochs=250,
        verbose=True
    )

    # Step 2: Quantum VQC Noise Sweep
    run_vqc_noise_sweep(
        seeds=args.seeds,
        topologies=args.topologies,
        layers=args.layers,
        noise_types=args.noise_types,
        noise_rates=args.noise_rates,
        output_csv=output_vqc_csv,
        checkpoints_dir=args.checkpoints_dir,
        epochs=args.epochs,
        lr=args.lr,
        resume=True
    )


if __name__ == "__main__":
    main()
