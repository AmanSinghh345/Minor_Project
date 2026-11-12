# VQC Benchmarking & Quantum Error Mitigation Toolkit

### A Modular Framework for Benchmarking Variational Quantum Classifiers (VQCs) Under Physical Hardware Noise Channels with Quantum Error Mitigation (QEM) and Circuit Selection Rules

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![PennyLane](https://img.shields.io/badge/PennyLane-0.45+-brightgreen.svg)](https://pennylane.ai/)
[![React 19](https://img.shields.io/badge/React-19.0-61dafb.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Executive Summary & Key Research Contributions

While Variational Quantum Classifiers (VQCs) are frequently proposed for quantum machine learning on NISQ devices, prior studies often rely on noise-free statevector simulations or unrealistically high noise levels ($20\%-50\%$), without benchmark parity against classical models or active noise mitigation.

This project reframes VQC evaluation into a **modular, reusable benchmarking and quantum error mitigation toolkit (`vqc_toolkit`)** paired with empirical guidelines for NISQ deployment:

1. **Modular Benchmarking Architecture (`vqc_toolkit/`)**:
   - `encoders/`: Monotonic $R_y(\theta)$ angle encoding bounded strictly to $[0, \pi]$ to prevent aliasing, and dense $R_x R_z$ multi-feature encoding.
   - `ansatz/`: Linear, Circular, Strongly Entangling, and Hardware-Efficient topologies with parameterized depth $L \in \{1, 2, 3\}$ and arbitrary wire readout position.
   - `noise/`: First-principles hand-written Kraus operators for **Depolarizing**, **Amplitude Damping** ($T_1$ energy relaxation), **Phase Damping** ($T_2$ pure dephasing), **Bit-Flip**, and asymmetric **Readout Error** calibrated against public IBM Quantum hardware specifications (e.g. `ibmq_manila`, `ibmq_bogota`).
   - `mitigation/`: **Zero-Noise Extrapolation (ZNE)** (linear & polynomial noise-scaling extrapolation) and **Readout Error Mitigation (REM)** (confusion matrix inversion).
   - `training/`: **Three Training Regimes**: (1) Clean-train / Noisy-test, (2) Noisy-train / Noisy-test, and (3) Noise-aware fine-tuning.
   - `metrics/`: **Noise-Robustness Score (NRS)** and an algorithmic **Circuit-Selection Rule Engine**.
   - `benchmarks/`: Multi-dataset support across **PneumoniaMNIST**, **Iris**, and **Breast Cancer**.

2. **Quantum Error Mitigation (QEM) Recovery**:
   - **Readout Error Mitigation (REM)**: Inverts detector measurement bit-flip confusion matrix ($p_{01}=2.5\%, p_{10}=3.5\%$), recovering true classification boundary without gate overhead.
   - **Zero-Noise Extrapolation (ZNE)**: Scales noise by $c \in [1.0, 2.0, 3.0]$ and extrapolates to $c \to 0$, recovering $+2.0\%$ accuracy under $2\%$ amplitude damping.

3. **Three Comparative Training Regimes**:
   - **Regime 1 (Clean-Train / Noisy-Test)**: Standard baseline ($83.0\%$ at $2\%$ noise).
   - **Regime 2 (Noisy-Train / Noisy-Test)**: Trains under stochastic Kraus maps ($69.0\%$; exhibits gradient variance under backpropagation).
   - **Regime 3 (Noise-Aware Fine-Tuning)**: Pre-trains clean for rapid convergence, then fine-tunes under physical noise with reduced learning rate ($79.0\%$; recalibrates expectation boundary).

4. **Noise-Robustness Score (NRS) Formulation**:
   Normalized trapezoidal area under the relative accuracy-vs-noise curve:
   $$\text{NRS} = \frac{1}{p_{\max} - p_{\min}} \int_{p_{\min}}^{p_{\max}} \frac{\text{Acc}(p)}{\text{Acc}(0)} \, dp$$
   - **Circular $L=3$ (Depolarizing)**: $\text{NRS} = \mathbf{0.9943}$ (decision sign preserved since $(1 - 4p/3) > 0$).
   - **Linear $L=3$ (Amplitude Damping)**: $\text{NRS} = \mathbf{0.9870}$ (superior under $T_1$ relaxation).
   - **Circular $L=3$ (Amplitude Damping)**: $\text{NRS} = \mathbf{0.9268}$ (worst degradation due to wrap-around CNOT decay).

5. **Algorithmic Circuit-Selection Rule**:
   - *If Amplitude Damping dominant ($p \ge 2\%$)*: Use **Linear topology with Depth $L \le 2$ and readout on terminal qubit (wire 3)**. Linear holds a $+12.4\%$ empirical edge over Circular at $5\%$ noise by avoiding the 4th wrap-around CNOT.
   - *If Depolarizing dominant ($p \le 5\%$)*: Use **Circular topology with Depth $L=3$ and readout on Qubit 0**. Circular's full entangling connectivity is fully preserved because depolarizing noise uniformly shrinks expectation margins without flipping the sign.
   - *If Readout Bit-Flip error dominant ($p_{\text{read}} \ge 1.5\%$)*: Apply **Readout Error Mitigation (REM)** via confusion matrix inversion.

6. **Interactive React Presentation Dashboard**:
   - Live presentation suite in `frontend/` featuring Slide Deck, Crossover Curves, Real-Time Quantum Simulator, Topology & Readout Wire Ablations, QEM Recovery & Regimes Hub, and 15 Viva Defense Q&As.

---

## 📊 Summary of Benchmark Results

| Model / Architecture | Clean Acc | Acc at 2% Depol | Acc at 5% Depol | Acc at 2% Amp | Acc at 5% Amp | NRS Score | Crossover Noise Rate ($B - 1s = 82.31\%$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Primary)** | **84.80% ± 2.49%** | — | — | — | — | — | Baseline Threshold |
| **Small MLP (Secondary)** | **84.40% ± 2.07%** | — | — | — | — | — | Baseline Secondary |
| **Circular VQC ($L=3$)** | 84.60% ± 3.58% | 84.20% | 83.60% | 82.80% | 66.40% | **0.9943** (Depol) / **0.9268** (Amp) | **5.0%** (Depol) / **2.0%** (Amp) |
| **Linear VQC ($L=3$)** | 82.20% ± 3.42% | 82.40% | 82.20% | 81.60% | **78.80%** | **1.0000** (Depol) / **0.9870** (Amp) | **2.0%** (Depol) / **1.0%** (Amp) |
| **Circular VQC ($L=2$)** | 81.80% ± 4.15% | 82.00% | 81.80% | 81.40% | 78.00% | **1.0000** (Depol) / **0.9867** (Amp) | 0.0% (Depol) / **1.0%** (Amp) |
| **Linear VQC ($L=2$)** | 81.80% ± 4.15% | 81.80% | 82.00% | 81.20% | 78.60% | **1.0000** (Depol) / **0.9849** (Amp) | 0.0% (Depol) / 0.0% (Amp) |
| **Linear VQC ($L=1$, Wire 3)** | **77.80% ± 4.49%** | — | — | — | — | — | *Recovers 17.6% gap vs Qubit 0* |

---

## 🔬 Scientific Disclosures & Methodological Notes

> [!IMPORTANT]
> 1. **Sample Standard Deviation ($s$, $\text{ddof}=1$)**: All error bounds are reported as sample standard deviations across the 5 independent seeds.
> 2. **MLP Hyperparameter Tuning**: Small MLP hyperparameters (Kaiming normal init, $\text{lr}=0.01$, 300 epochs) were tuned after observing training collapse on Seed 46. Disclosed as an empirical upper bound on classical non-linear performance.
> 3. **Gate-Level Uniform Noise**: Uniform Kraus insertion after each gate provides a reproducible, hardware-agnostic benchmark. Calibrated IBM backend profiles are provided in `vqc_toolkit.noise.calibration`.

---

## 🚀 Getting Started

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/AmanSinghh345/Minor_Project.git
cd Minor_Project

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Modular Toolkit Tests
```bash
python tests/test_toolkit.py
```

### 3. Run the Advanced QEM & Regimes Study
```bash
python run_advanced_study.py
```

### 4. Launch the Interactive React Presentation App
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173/ in your browser
```

---

## 📁 Repository Structure

```text
vqc-noise/
├── vqc_toolkit/                    # Modular Quantum Benchmarking & Mitigation Framework
│   ├── encoders/                   # Angle Ry in [0, pi] & dense Rx/Rz encoders
│   ├── ansatz/                     # Linear, Circular, Strongly Entangling, Hardware-Efficient
│   ├── noise/                      # Depol, Amp Damping, Phase Damping, Bit-Flip, IBM presets
│   ├── mitigation/                 # Zero-Noise Extrapolation (ZNE) & Readout Error Mitigation (REM)
│   ├── training/                   # Clean-train, Noisy-train, and Noise-Aware Fine-Tuning
│   ├── metrics/                    # Noise-Robustness Score (NRS) & Circuit Selection Rules
│   └── benchmarks/                 # PneumoniaMNIST, Iris, Breast Cancer loaders & classical models
├── checkpoints/                    # Saved PyTorch model checkpoints (.pt) across 5 seeds
├── data.py                         # Data loading & PCA pipeline
├── model.py                        # PennyLane VQC model definition
├── noise.py                        # Hand-written Kraus maps & verification
├── run_experiments.py              # Automated 420-run evaluation sweep
├── run_advanced_study.py           # Multi-regime, QEM recovery, and NRS runner
├── plot.py                         # Publication figure generation
├── demo.ipynb                      # Pre-rendered Jupyter demonstration notebook
├── results/                        # Sweep CSVs and advanced study JSONs
├── figures/                        # Generated high-resolution publication figures
│   ├── noise_degradation_curves.png
│   ├── crossover_analysis.png
│   ├── topology_ablation.png
│   ├── depth_ablation.png
│   ├── mitigation_recovery.png
│   └── training_regimes.png
└── frontend/                       # Interactive React Presentation Dashboard (Vite + React 19)
```

---

## 📄 License & Attribution

This project is licensed under the MIT License. Developed as a Semester 7 Capstone Project on Benchmarking Variational Quantum Classifiers under Physical NISQ Noise Channels.
