# DESIGN_DECISIONS.md - Architectural & Methodological Decisions

This document details every major design decision made in this project. For each choice, we state the selected approach, the alternative candidates considered, the supporting evidence or verified literature, and candid rationale regarding compute or hardware limits.

---

## 1. Number of Qubits ($N = 4$)
- **Choice Made**: 4 qubits.
- **Alternatives Considered**:
  - *2 qubits*: Faster simulation, but overly restricted feature representation that collapses image variance.
  - *8–16 qubits*: Higher capacity, but density matrix simulation on `default.mixed` scales as $\mathcal{O}(4^N)$ in memory and runtime. Evaluating hundreds of sweep configurations on 8+ mixed-state qubits would take tens of hours.
- **Evidence / Justification**:
  - A 4-qubit mixed-state density matrix is $16 \times 16$, which enables fast, exact numerical simulation of noise channels while maintaining non-trivial multi-qubit entanglement.
  - 4 qubits align cleanly with 4 principal components extracted from PneumoniaMNIST.

---

## 2. Dimensionality Reduction: PCA to 4 Features
- **Choice Made**: Principal Component Analysis (PCA) fit strictly on the training set to reduce 784 flattened pixels down to 4 continuous components.
- **Alternatives Considered**:
  - *Autoencoder (Neural)*: Non-linear compression, but introduces an auxiliary neural network training stage, hyperparameter tuning complexity, and potential data leakage risk.
  - *Random projection or cropping*: Loses structural variance and diagnostic patterns of chest X-rays.
- **Evidence / Justification**:
  - The top 4 PCA components capture **60.04%** of the total variance across PneumoniaMNIST images.
  - Fitting strictly on training data prevents test data leakage.
  - Rahman et al. (COMPSAC 2024, p. 1064) demonstrated that reducing input feature dimensionality drastically reduces quantum optimization time (e.g. from 1441 s to 356 s).

---

## 3. Quantum State Encoding: $R_y$ Angle Encoding
- **Choice Made**: Angle encoding using single-qubit $R_y(\theta)$ rotation gates where $\theta \in [0, \pi]$.
- **Alternatives Considered**:
  - *Amplitude encoding*: Encodes $2^N$ features into $N$ qubits, but requires complex multi-qubit state preparation circuits which introduce significant gate overhead and error before classification begins.
  - *Basis encoding*: Requires binarizing features into bitstrings, destroying continuous medical grayscale gradation.
- **Evidence / Justification**:
  - Maheshwari et al. (IEEE Access 2022, pp. 3707–3714) established that the choice of encoding strategy critically dictates VQC performance and overhead.
  - Prerana M N et al. (IEEE INDICON 2025, p. 6) demonstrated that the encoding layer is the most vulnerable stage in QNNs (suffering up to 42.9% Layerwise Sensitivity Drop under amplitude damping). Angle encoding has constant depth 1, minimizing the number of gates exposed to noise during state initialization.
  - Scaling features via `MinMaxScaler` to $[0, \pi]$ ensures that minimum feature values map to $|0\rangle$ and maximum values map to $|1\rangle$ without periodic wrapping ambiguity:
    $$R_y(0)|0\rangle = |0\rangle, \quad R_y(\pi)|0\rangle = |1\rangle$$

---

## 4. Variational Ansatz Architecture
- **Choice Made**: Layered ansatz consisting of parameterized $R_y(\theta)$ rotations on all 4 qubits followed by an entangling block of two-qubit CNOT gates.
- **Alternatives Considered**:
  - *Strongly Entangling Layers (Rot(x,y,z) + entangler)*: 3 parameters per qubit per layer. High parameter count increases susceptibility to barren plateaus and slows convergence.
  - *Hardware-efficient ansatz with CZ gates*: Functionally equivalent to CNOT up to Hadamard rotations.
- **Evidence / Justification**:
  - The $R_y + \text{CNOT}$ ansatz keeps parameters compact ($4 \times L$ parameters) while providing sufficient expressibility to separate classes in Hilbert space.

---

## 5. Circuit Depth / Layer Counts ($L \in \{1, 2, 3\}$)
- **Choice Made**: Evaluate depths of 1, 2, and 3 layers.
- **Alternatives Considered**:
  - *Deep circuits ($L \ge 5$)*: Substantially increases two-qubit gate counts and circuit depth, accelerating noise accumulation on NISQ simulators.
- **Evidence / Justification**:
  - Easom-McCaldin et al. (IEEE Access 2021, pp. 65135–65137) demonstrated that the sharpest robustness improvements against noise occur between 1 and 3 layers, after which robustness benefits saturate.
  - Keeping $L \in \{1, 2, 3\}$ enables clear tracking of the depth-vs-noise trade-off.

---

## 6. CNOT Entanglement Topologies: Linear vs. Circular (Author's Hypothesis)
- **Choice Made**: Systematically compare two topologies:
  - *Linear*: CNOT(0,1), CNOT(1,2), CNOT(2,3) $\rightarrow 3$ two-qubit gates per layer.
  - *Circular*: CNOT(0,1), CNOT(1,2), CNOT(2,3), CNOT(3,0) $\rightarrow 4$ two-qubit gates per layer.
- **Author's Hypothesis & Rationale**:
  - This is the **author's own independent design hypothesis**, not a finding from a prior paper.
  - Verified IBM Quantum calibration data shows that two-qubit entangling gates have an error rate an order of magnitude higher ($0.2\% - 1.5\%$) than single-qubit gates ($0.02\% - 0.05\%$).
  - Circular topology adds an extra CNOT (closing the loop from qubit 3 back to qubit 0). We hypothesize that circular topology will suffer greater cumulative accuracy degradation under noise than linear topology, particularly under depolarizing noise.

---

## 7. Noise Rates Sweep: $[0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]$
- **Choice Made**: Granular micro-noise sweep from $0\%$ up to $5\%$, specifically targeting $[0.1\%, 0.2\%, 0.5\%, 1.0\%, 2.0\%, 5.0\%]$.
- **Alternatives Considered**:
  - *Coarse macro-sweep ($0\%, 25\%, 50\%, 100\%$)*: Fails to capture the practical operating regime of NISQ hardware.
- **Evidence / Justification**:
  - Verified against IBM Quantum processor calibration data (IBM Heron, Eagle, Falcon):
    - Median single-qubit error: $0.02\% - 0.05\%$.
    - Median two-qubit error (CNOT / CZ / ECR): $0.2\% - 1.5\%$.
  - Our micro-sweep directly straddles this physical operating regime, enabling identification of realistic crossover points.

---

## 8. Noise Channel Physics: Depolarizing vs. Amplitude Damping
- **Choice Made**: Benchmark both Depolarizing Channel and Amplitude Damping Channel.
- **Physical Rationale**:
  - *Depolarizing Channel*: Models symmetric environmental interaction (white noise), pulling the density matrix toward the maximally mixed state $\frac{I}{2}$. It isotropically shrinks the Bloch sphere.
  - *Amplitude Damping Channel*: Models non-symmetric energy relaxation ($T_1$ decay) caused by physical energy loss into the environment, driving qubits toward the ground state $|0\rangle$.
  - Satpathy et al. (IEEE IoT J. 2024, p. 3849) observed monotonic accuracy degradation under both channels.

---

## 9. Dataset Selection: PneumoniaMNIST (MedMNIST)
- **Choice Made**: PneumoniaMNIST binary classification (300 train / 100 test balanced samples).
- **Alternatives Considered**:
  - *Synthetic Two-Moons or Circles*: Too simplistic; does not demonstrate clinical or real-world applicability.
  - *Standard MNIST digits (e.g. 0 vs 1)*: Widely overused and often linearly separable after trivial pooling.
  - *Full size PneumoniaMNIST (4,708 samples)*: Simulating 4,708 samples under noisy density matrix backends for dozens of configurations would require dozens of compute hours.
- **Evidence / Justification**:
  - PneumoniaMNIST represents real chest X-ray diagnosis (Normal vs Pneumonia).
  - Balanced subset (150/150 train, 50/50 test) ensures that 50% accuracy is strictly random chance, and performance metrics (precision, recall, F1) are unskewed.

---

## 10. Optimizer Choice: PyTorch Adam (Author's Design Choice)
- **Choice Made**: `torch.optim.Adam` via PennyLane's PyTorch autograd interface.
- **Alternatives Considered**:
  - *Derivative-free optimizers (COBYLA, Nelder-Mead)*: Used in Qiskit-based literature (e.g., Rahman et al., COMPSAC 2024), but often slow or prone to premature stopping.
  - *Standard SGD*: Slower convergence without adaptive learning rate moments.
- **Author's Rationale**:
  - PennyLane natively supports the parameter-shift rule with PyTorch (`interface="torch"`).
  - Adam accelerates convergence on the noise-free loss landscape via first and second gradient moments, providing stable, reproducible parameter convergence.

---

## 11. Classical Baselines: Logistic Regression + Small MLP (Author's Methodology)
- **Choice Made**: Benchmark against BOTH a linear baseline (PyTorch Logistic Regression) and a compact non-linear baseline (PyTorch Small MLP: 4-8-1).
- **Author's Rationale**:
  - Logistic Regression provides a clean, convex linear decision boundary with 5 parameters ($4 \times 1 + 1$).
  - Small MLP provides a non-linear classical model with 49 parameters, closely mirroring the small parameter scale of near-term VQCs (which have 4 to 12 parameters).
  - Both operate on the exact same 4 PCA features with zero noise by definition.
