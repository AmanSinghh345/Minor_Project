# Variational Quantum Classifier (VQC) Under Physical Noise Channels

### Benchmarking Quantum Classification Against Classical Baselines on PneumoniaMNIST Under Depolarizing and Amplitude Damping Noise

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![PennyLane](https://img.shields.io/badge/PennyLane-0.40+-brightgreen.svg)](https://pennylane.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Abstract & Research Overview

Variational Quantum Classifiers (VQCs) are leading candidates for demonstrating quantum utility in the Noisy Intermediate-Scale Quantum (NISQ) era. However, near-term quantum processors are heavily impaired by environmental decoherence, gate infidelities, and energy relaxation. 

This project conducts a rigorous experimental investigation into the performance degradation of a **4-qubit Parameterized Quantum Circuit (PQC)** applied to medical image binary classification (**PneumoniaMNIST** from MedMNIST). We benchmark the VQC against both linear (**Logistic Regression**, 5 parameters) and non-linear (**Small MLP**, 49 parameters) classical baselines across physical noise models.

### Key Contributions & Highlights
1. **First-Principles Kraus Operators**: Hand-written implementations of single-qubit Kraus maps for both **Depolarizing Noise** (isotropic white noise) and **Amplitude Damping** (asymmetric $T_1$ energy relaxation) in NumPy, mathematically verified for completeness ($\sum_k K_k^\dagger K_k = I$) and trace preservation ($\text{Tr}(\mathcal{E}(\rho))=1$), with exact numerical parity ($\Delta < 10^{-14}$) confirmed against PennyLane's built-in operations on `default.mixed`.
2. **Gate-Level Noise Injection**: Noise channels inserted after *every single gate* (encoding, variational rotation, and two-qubit CNOTs across both control and target wires).
3. **Realistic Micro-Noise Sweep**: Evaluation over physical error rates $[0.0\%, 0.1\%, 0.2\%, 0.5\%, 1.0\%, 2.0\%, 5.0\%]$, directly straddling median gate error calibration regimes of physical superconducting QPUs (such as IBM Quantum Eagle/Heron processors).
4. **Automated Multi-Seed Sweep**: Orchestrates $5 \text{ seeds} \times 2 \text{ topologies} \times 3 \text{ depths} \times 2 \text{ noise types} \times 7 \text{ noise rates} = 420$ evaluation runs with model checkpointing and resumption.
5. **Exact Crossover Rate Interpolation**: Scientific algorithm identifying the critical physical noise rate threshold ($p^*, \gamma^*$) where quantum classification performance drops below classical baselines.
6. **Author's Independent Hypothesis on Entanglement Topology**: Systematic ablation comparing **Linear** (3 CNOTs/layer) vs. **Circular** (4 CNOTs/layer) CNOT connectivity, verifying that additional two-qubit entangling gates accelerate noise accumulation.

---

## Methodological Notes & Scientific Disclosures

> [!IMPORTANT]
> In the spirit of rigorous academic transparency, two key experimental design disclosures are noted:
> 1. **MLP Hyperparameter Tuning on Test Set**: The Small MLP (4-8-1) baseline hyperparameters ($\text{lr}=0.01$, Kaiming normal initialization, 300 epochs) were adjusted after observing that an initial learning rate of $\text{lr}=0.05$ caused training collapse on Seed 46 (stagnating at $\ln(2)$ loss and predicting the majority class with $52\%$ accuracy). Because the benchmark dataset uses a direct train/test split (300 train, 100 test) without a separate validation set, these hyperparameters were tuned based on test set stability. This represents an empirical ceiling on the classical non-linear baseline.
> 2. **Uniform Gate Noise Model**: In our circuit simulation on `default.mixed`, noise channels (Depolarizing and Amplitude Damping) are applied uniformly after *every single gate* across all active qubits with the identical parameter rate ($p$ or $\gamma$). In physical superconducting quantum hardware (such as IBM Quantum chips), two-qubit entangling gates typically exhibit error rates an order of magnitude higher ($0.2\% - 1.5\%$) than single-qubit rotation gates ($0.02\% - 0.05\%$). Our uniform noise injection provides a clean, controlled theoretical benchmark rather than a device-specific calibration map.

---

## Repository Structure

```text
vqc-noise/
├── baseline.py                 # Classical PyTorch baselines (Logistic Regression & Small MLP)
├── data.py                     # PneumoniaMNIST loader, balanced sampler, PCA, [0, pi] scaler
├── model.py                    # 4-qubit VQC in PennyLane & PyTorch (Ry encoding, Linear/Circular CNOT)
├── noise.py                    # Hand-written Kraus maps, verification, and noisy QNodes
├── run_experiments.py          # Automated 420-run multi-seed experiment sweep harness
├── plot.py                     # Scientific crossover interpolation & publication-quality figures
├── demo.ipynb                  # Interactive end-to-end Jupyter demonstration notebook
├── requirements.txt            # Python package dependencies
├── DESIGN_DECISIONS.md         # Comprehensive architectural choices and literature rationales
├── IMPLEMENTATION_NOTES.md     # Breakdown of original vs library-provided components
├── LITERATURE.md               # Verified citations, DOIs, and findings from research papers
├── checkpoints/                # Saved PyTorch model checkpoints (.pt)
├── results/                    # CSV sweep data and crossover summary reports
└── figures/                    # High-resolution generated publication figures
    ├── noise_degradation_curves.png
    ├── depth_ablation.png
    ├── topology_ablation.png
    └── crossover_analysis.png
```

---

## Mathematical Formulations

### 1. Quantum State Encoding
Features $\mathbf{x} \in [0, \pi]^4$ obtained from PCA on flattened $28 \times 28$ chest X-rays are mapped into quantum states using single-qubit $R_y(\theta)$ rotation gates on 4 qubits initialized in $|0\rangle^{\otimes 4}$:
$$R_y(\theta) = \exp\left(-i \frac{\theta}{2} Y\right) = \begin{bmatrix} \cos(\theta / 2) & -\sin(\theta / 2) \\ \sin(\theta / 2) & \cos(\theta / 2) \end{bmatrix}$$
Scaling features strictly to $[0, \pi]$ maps the minimum feature value to $|0\rangle$ and maximum to $|1\rangle$:
$$R_y(0)|0\rangle = |0\rangle, \quad R_y(\pi)|0\rangle = |1\rangle$$

### 2. Depolarizing Channel (Isotropic Environmental White Noise)
With probability $1 - p$, the qubit is uncorrupted; with probability $p$, an error occurs uniformly across the three Pauli matrices:
$$\mathcal{E}_{\text{depol}}(\rho) = (1 - p)\rho + \frac{p}{3}\left(X\rho X + Y\rho Y + Z\rho Z\right)$$
Kraus representation:
$$K_0 = \sqrt{1 - p} \, I, \quad K_1 = \sqrt{\frac{p}{3}} \, X, \quad K_2 = \sqrt{\frac{p}{3}} \, Y, \quad K_3 = \sqrt{\frac{p}{3}} \, Z$$

### 3. Amplitude Damping Channel ($T_1$ Energy Relaxation)
Models physical energy loss into the thermal bath / cold environment, driving excited states $|1\rangle \to |0\rangle$:
$$K_0 = \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1 - \gamma} \end{bmatrix}, \quad K_1 = \begin{bmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{bmatrix}$$

### 4. Continuous Readout & Parity Mapping
Measurement is performed via the Pauli-Z expectation value on readout qubit 0:
$$\langle Z_0 \rangle = \text{Tr}\left(\rho_{\text{final}} (Z \otimes I^{\otimes 3})\right) \in [-1, +1]$$
Probability of class 1 (Pneumonia):
$$p(y = 1) = \frac{1 - \langle Z_0 \rangle}{2} \in [0, 1]$$
Classification rule: predict Pneumonia if $\langle Z_0 \rangle \le 0$ ($p \ge 0.5$), else Normal.

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/vqc-noise.git
   cd vqc-noise
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Execution Guide

### Step 1: Classical Baselines
Train PyTorch Logistic Regression and Small MLP (4-8-1) on 4 PCA features:
```bash
python baseline.py --seed 42 --lr 0.05 --epochs 250
```

### Step 2: Noise-Free VQC Training
Train the 4-qubit VQC using Adam on `default.qubit`:
```bash
python model.py --seed 42 --layers 2 --topology circular --epochs 150
```

### Step 3: Kraus Operator Verification & Noise Evaluation
Verify hand-written Kraus operators against PennyLane built-in channels and evaluate noisy VQC on `default.mixed`:
```bash
python noise.py --seed 42
```

### Step 4: Full Multi-Seed Experiment Sweep (420 Configurations)
Execute the complete matrix across 5 seeds, 2 topologies, 3 depths, 2 noise types, and 7 noise rates:
```bash
python run_experiments.py
```
*(For a quick sanity check across 1 seed and 3 rates, run `python run_experiments.py --quick`)*

### Step 5: Crossover Analysis & Publication Figures
Compute exact crossover thresholds and render all publication-grade plots:
```bash
python plot.py
```

### Step 6: Interactive Demo Notebook
Launch Jupyter to explore the interactive inference demonstration:
```bash
jupyter notebook demo.ipynb
```

---

## Key Experimental Findings

| Dimension | Observation & Physical Interpretation |
| :--- | :--- |
| **Noise Channel Asymmetry** | **Amplitude Damping** causes substantially sharper accuracy and F1 degradation than Depolarizing noise. Because amplitude damping forces excited states $|1\rangle \to |0\rangle$, it systematically shifts the readout expectation $\langle Z_0 \rangle \to +1$, causing massive False Negative rates on Pneumonia cases. |
| **Linear vs. Circular Topology** | **Linear topology** (3 CNOTs/layer) exhibits greater resilience than **Circular topology** (4 CNOTs/layer). Two-qubit entangling gates suffer an order of magnitude higher error rates on physical QPUs; eliminating redundant CNOTs improves noise robustness. |
| **Depth vs. Noise Trade-off** | While $L=3$ achieves slightly higher clean accuracy on some seeds, deeper circuits accumulate more gate noise, resulting in steeper degradation slopes and earlier crossover against classical baselines. |
| **Physical Crossover Rate** | Across configurations, the VQC matches or outperforms classical baselines under low noise ($p < 0.5\%$), but drops below classical Logistic Regression and MLP once error rates exceed $\sim 1.0\% - 2.0\%$. |

---

## Comprehensive Viva Defense Guide (15 Rigorous Q&As)

### Q1: Why did you limit the quantum circuit to 4 qubits and 4 PCA features instead of 8 or 16?
> **Answer**: Simulating noisy open quantum systems requires density matrix simulation ($\rho \in \mathbb{C}^{2^N \times 2^N}$). Memory and matrix multiplication costs scale as $\mathcal{O}(4^N)$. For $N=4$, $\rho$ is $16 \times 16$, enabling exact, fast simulation of 420 sweep runs in minutes. Scaling to $N=8$ would require $256 \times 256$ density matrices at every gate application, increasing runtime by orders of magnitude without altering the fundamental physics of noise degradation. Furthermore, 4 PCA components capture **60.04%** of the total variance across PneumoniaMNIST.

### Q2: How did you ensure there was no data leakage in your preprocessing pipeline?
> **Answer**: Both the `PCA` projection matrix and the `MinMaxScaler` feature transformation were **fit strictly on the training split** (300 samples). The test split (100 samples) was transformed using only the pre-fitted parameters, with test values strictly clipped to $[0, \pi]$ to guarantee valid rotation angles. Fitting PCA on the full dataset before splitting is a common flaw that artificially inflates test metrics through data leakage.

### Q3: Why use $R_y$ angle encoding into $[0, \pi]$ rather than amplitude encoding or full $[0, 2\pi]$?
> **Answer**: Angle encoding requires constant circuit depth 1 ($N$ parallel single-qubit gates), minimizing gate exposure to noise before the variational ansatz begins. Amplitude encoding requires complex multi-qubit state preparation circuits involving $\mathcal{O}(2^N)$ CNOT gates, introducing massive gate errors on NISQ devices before classification even starts. We bound angles strictly to $[0, \pi]$ because $R_y(0)|0\rangle = |0\rangle$ and $R_y(\pi)|0\rangle = |1\rangle$, ensuring a bijective mapping between normalized feature magnitudes and orthogonal basis states without periodic wrapping ambiguity.

### Q4: What is the physical and mathematical distinction between Depolarizing and Amplitude Damping channels?
> **Answer**: 
> - **Depolarizing Noise** represents symmetric environmental interaction (white noise). It uniformly contracts the Bloch sphere toward the maximally mixed state $\frac{I}{2}$, attenuating polarization without favoring any specific eigenstate.
> - **Amplitude Damping** models asymmetric energy relaxation ($T_1$ dissipation) caused by spontaneous photon emission into a cold thermal environment. It irreversibly transitions excited state population $|1\rangle$ down to ground state $|0\rangle$, fundamentally skewing the quantum state toward $|0\rangle$.

### Q5: Why are Kraus operators necessary to simulate quantum noise instead of standard unitary statevectors?
> **Answer**: Unitary operators preserve state purity and norm ($\|\psi\|=1$), representing closed, isolated quantum systems ($U^\dagger U = I$). Real physical quantum processors interact continuously with an external environment, undergoing decoherence and energy exchange. This open quantum evolution is non-unitary and transforms pure states into mixed states. The Kraus representation theorem proves that any completely positive, trace-preserving (CPTP) quantum operation $\mathcal{E}(\rho)$ can be decomposed into an operator-sum $\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$ satisfying $\sum_k K_k^\dagger K_k = I$.

### Q6: How did you verify that your hand-written Kraus operators are physically valid?
> **Answer**: We verified them mathematically and numerically across two independent checks:
> 1. **Mathematical Completeness**: Asserted $\sum_k K_k^\dagger K_k = I_{2 \times 2}$ with numerical tolerance $< 10^{-15}$.
> 2. **Trace Preservation & Reference Parity**: Applied our hand-written maps $\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$ to pure ground $|0\rangle\langle0|$, pure excited $|1\rangle\langle1|$, superposition $|+\rangle\langle+|$, and mixed density matrices, asserting $\text{Tr}(\rho') = 1$ and confirming maximum absolute difference $< 10^{-14}$ against PennyLane's compiled `default.mixed` channel operations (`qml.DepolarizingChannel` and `qml.AmplitudeDamping`).

### Q7: Why does Amplitude Damping cause a catastrophic drop in Recall while Precision remains high?
> **Answer**: In our VQC readout scheme, $\langle Z_0 \rangle = +1$ corresponds to class 0 (Normal) and $\langle Z_0 \rangle = -1$ corresponds to class 1 (Pneumonia). Probability of class 1 is $p(y=1) = (1 - \langle Z_0 \rangle)/2$. Amplitude damping drives qubits toward the ground state $|0\rangle$ ($\langle Z_0 \rangle \to +1$), which forces predicted probabilities toward $0$. As a result, the model increasingly predicts Normal for almost all inputs, resulting in severe False Negatives (Pneumonia misdiagnosed as Normal), collapsing Recall ($TP / (TP + FN)$) down to $\sim 50\%$.

### Q8: Why evaluate micro-noise rates ($0.1\% - 5\%$) instead of coarse rates ($20\% - 50\%$)?
> **Answer**: Typical published calibration reports for physical superconducting quantum processors (such as IBM Quantum Eagle/Heron chips) exhibit median single-qubit gate errors of $0.02\% - 0.05\%$ and median two-qubit CNOT errors of $0.2\% - 1.5\%$. A coarse sweep from $0\%$ to $50\%$ tests regimes irrelevant to near-term hardware. Our fine-grained sweep ($0.1\%, 0.2\%, 0.5\%, 1.0\%, 2.0\%, 5.0\%$) directly straddles the physical operating boundaries of NISQ hardware, revealing the exact crossover threshold where quantum utility is lost.

### Q9: What is your independent hypothesis on CNOT entanglement topology, and did the data support it?
> **Answer**: **Hypothesis**: Circular topology (4 CNOTs/layer) introduces an additional entangling gate closing the loop from qubit 3 back to qubit 0. Because two-qubit entangling gates suffer roughly $10\times$ higher physical error rates than single-qubit gates, circular topology should experience steeper cumulative error accumulation and degrade faster under noise than Linear topology (3 CNOTs/layer).  
> **Empirical Result**: The experimental sweep confirmed that Linear topology matched or exceeded Circular topology accuracy across noise rates while reducing gate count and depth, validating the hypothesis that minimizing entangling gates preserves noise resilience.

### Q10: How is the crossover noise rate ($p^*, \gamma^*$) calculated?
> **Answer**: For each architecture and noise channel, we obtain the empirical mean accuracy curve $\bar{A}(p)$ over 5 random seeds across the 7 evaluated noise rates. We compute the mean test accuracy $B$ of the classical baseline (e.g. Logistic Regression). We locate the bracket $[p_i, p_{i+1}]$ where $\bar{A}(p_i) \ge B > \bar{A}(p_{i+1})$ and calculate the exact intersection via continuous linear interpolation:
> $$p^* = p_i + \frac{B - \bar{A}(p_i)}{\bar{A}(p_{i+1}) - \bar{A}(p_i)} (p_{i+1} - p_i)$$

### Q11: Why benchmark against both Logistic Regression and Small MLP?
> **Answer**: 
> 1. **Logistic Regression** (5 parameters: $4 \times 1 + 1$) provides a convex, linear baseline operating on the exact same 4 PCA features with zero noise.
> 2. **Small MLP** (49 parameters: $4 \to 8 \to 1$) provides a non-linear classical baseline whose parameter scale closely mirrors NISQ quantum circuits (which have 4 to 12 parameters).
> This provides two distinct reference standards: whether the noisy VQC can beat a simple linear model, and whether it can match a compact non-linear neural network.

### Q12: How are gradients calculated during VQC training?
> **Answer**: During noise-free training on `default.qubit`, gradients are computed via reverse-mode automatic differentiation (backpropagation through the statevector simulation) integrated with PyTorch autograd (`interface="torch", diff_method="backprop"`). For execution on physical quantum hardware, gradients would instead be computed using the **parameter-shift rule**:
> $$\frac{\partial \langle Z \rangle}{\partial \theta_j} = \frac{\langle Z \rangle_{\theta_j + \pi/2} - \langle Z \rangle_{\theta_j - \pi/2}}{2}$$

### Q13: What are barren plateaus, and how does your circuit avoid them?
> **Answer**: Barren plateaus occur when the variance of the cost function gradient vanishes exponentially with the number of qubits: $\text{Var}[\partial_\theta C] \in \mathcal{O}(2^{-N})$, rendering gradient descent ineffective. Our design avoids barren plateaus because:
> 1. We operate in the shallow, low-qubit regime ($N = 4, L \le 3$).
> 2. We use a local observable (measuring Pauli-Z on a single qubit, qubit 0) rather than a global multi-qubit projector. Cerezo et al. (Nature Commun. 2021) proved that shallow circuits with local cost functions exhibit polynomially bounded gradients $\mathcal{O}(1/\text{poly}(N))$, preventing barren plateaus.
> 3. We initialize variational weights with small random angles near zero rather than completely random Haar-distributed states.

### Q14: Why train the VQC noise-free and evaluate under noise, rather than training under noise?
> **Answer**: Training under noise on `default.mixed` requires density matrix propagation and noisy gradient shifts at every optimization step, which is computationally prohibitive and slows optimization. More fundamentally, our methodology mirrors the standard NISQ deployment workflow: models are designed, optimized, or pre-trained on noise-free simulators or cloud clusters, and then deployed directly onto physical, noisy QPUs. Evaluating pre-trained weights under noise directly quantifies the **inference robustness** and operational degradation of quantum models deployed on NISQ processors.

### Q15: What modifications would be necessary to run this VQC on physical IBM Quantum hardware?
> **Answer**: 
> 1. **Transpilation & Gate Decomposition**: Decompose $R_y(\theta)$ into the native gate set (e.g. $R_z$, $\sqrt{X}$, $X$) and map CNOTs to native physical couplings (e.g. ECR or CZ gates).
> 2. **Qubit Routing**: Map our 4 virtual qubits to a contiguous subgraph of 4 physical qubits with the lowest calibration error rates.
> 3. **Shot-Based Sampling**: Replace exact statevector expectation values with statistical sampling over finite measurement shots (e.g., 4096 shots), introducing finite shot noise: $\sigma_{\text{shot}} \approx 1/\sqrt{N_{\text{shots}}}$.
> 4. **Readout Error Mitigation**: Apply M3 (Matrix-free Measurement Mitigation) or complete readout inversion calibration to mitigate measurement bit-flip errors.

---

## Authors & Academic Integrity

- Author: Sem 7 Capstone Project
- All literature citations, page numbers, and findings have been directly verified against primary research PDFs (see `LITERATURE.md`).
- Original implementation components versus library utilities are documented in `IMPLEMENTATION_NOTES.md`.
