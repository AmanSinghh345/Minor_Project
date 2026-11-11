# DESIGN_DECISIONS.md - Architectural & Methodological Decisions

This document details every major design decision made in this project. For each choice, we state the selected approach, the alternative candidates considered, the supporting evidence or literature, and candid rationale regarding compute or hardware limits.

---

## 1. Number of Qubits ($N = 4$)
- **Choice Made**: 4 qubits.
- **Alternatives Considered**:
  - *2 qubits*: Faster simulation, but overly restricted feature representation that collapses image variance.
  - *8–16 qubits*: Higher capacity, but density matrix simulation on `default.mixed` scales as $\mathcal{O}(4^N)$ in memory and runtime. Evaluating hundreds of sweep configurations on 8+ mixed-state qubits would take tens of hours.
- **Evidence / Justification**:
  - Lamichhane & Rawat (2025) and Satpathy et al. (2024) identify 4 to 8 qubits as the sweet spot for NISQ hybrid classification benchmarks.
  - A 4-qubit mixed-state density matrix is $16 \times 16$, which enables fast, exact numerical simulation of noise channels while maintaining non-trivial multi-qubit entanglement.

---

## 2. Dimensionality Reduction: PCA to 4 Features
- **Choice Made**: Principal Component Analysis (PCA) fit strictly on the training set to reduce 784 flattened pixels down to 4 continuous components.
- **Alternatives Considered**:
  - *Autoencoder (Neural)*: Non-linear compression, but introduces an auxiliary neural network training stage, hyperparameter tuning complexity, and potential data leakage risk.
  - *Convolutional Quanvolutional filter*: High computational overhead on quantum simulator and adds multi-stage complexity.
  - *Random projection or cropping*: Loses structural variance and diagnostic patterns of chest X-rays.
- **Evidence / Justification**:
  - The top 4 PCA components capture **60.04%** of the total variance across PneumoniaMNIST images.
  - Fitting strictly on training data prevents test data leakage.
  - Linear orthogonal projection ensures predictable, stable scaling into quantum rotation angles.

---

## 3. Quantum State Encoding: $R_y$ Angle Encoding
- **Choice Made**: Angle encoding using single-qubit $R_y(\theta)$ rotation gates where $\theta \in [0, \pi]$.
- **Alternatives Considered**:
  - *Amplitude encoding*: Encodes $2^N$ features into $N$ qubits, but requires deep state-preparation circuits ($\mathcal{O}(2^N)$ CNOT gates) which degrade completely under NISQ noise before classification even begins.
  - *Basis encoding*: Requires binarizing features into bitstrings, destroying continuous medical grayscale gradation.
  - *$R_x$ or $R_z$ rotations*: Mathematically equivalent to $R_y$ up to global/local phase rotations, but $R_y$ operates strictly in real amplitudes when acting on $|0\rangle$, maintaining clear geometric intuition on the Bloch sphere ($|0\rangle \xrightarrow{R_y(\pi)} |1\rangle$).
- **Evidence / Justification**:
  - Easom-McCaldin et al. (2021) and Rahman (2024) emphasize angle encoding for shallow NISQ pipelines due to its depth-1 constant overhead.
  - Features are mapped via `MinMaxScaler` to $[0, \pi]$ so that minimum feature values map to $|0\rangle$ and maximum values map to $|1\rangle$ without periodic wrapping ambiguity.

---

## 4. Variational Ansatz Architecture
- **Choice Made**: Layered ansatz consisting of parameterized $R_y(\theta)$ rotations on all 4 qubits followed by an entangling block of two-qubit CNOT gates.
- **Alternatives Considered**:
  - *Strongly Entangling Layers (Rot(x,y,z) + entangler)*: 3 parameters per qubit per layer. High parameter count increases susceptibility to barren plateaus (McClean et al., 2018) and slows convergence.
  - *Hardware-efficient ansatz with CZ gates*: Functionally equivalent to CNOT up to Hadamard rotations, but CNOT is the canonical entangler in standard quantum literature.
- **Evidence / Justification**:
  - The $R_y + \text{CNOT}$ ansatz keeps parameters compact ($4 \times L$ parameters) while providing sufficient expressibility to bifurcate the Hilbert space.
  - Single-qubit rotations provide local decision boundaries, and CNOTs generate non-local quantum correlations (entanglement).

---

## 5. Circuit Depth / Layer Counts ($L \in \{1, 2, 3\}$)
- **Choice Made**: Evaluate depths of 1, 2, and 3 layers.
- **Alternatives Considered**:
  - *Deep circuits ($L \ge 5$)*:
- **Evidence / Justification**:
  - Satpathy et al. (2024) and Sajadimanesh et al. (2025) demonstrated that deep circuits collapse under NISQ noise (e.g. from 98% down to 26%).
  - Keeping $L \in \{1, 2, 3\}$ allows us to observe the critical inflection point where adding another layer increases theoretical expressibility under ideal conditions, but increases noise vulnerability under realistic hardware conditions.

---

## 6. CNOT Entanglement Topologies: Linear vs. Circular
- **Choice Made**: Systematically compare two topologies:
  - *Linear*: CNOT(0,1), CNOT(1,2), CNOT(2,3) $\rightarrow 3$ two-qubit gates per layer.
  - *Circular*: CNOT(0,1), CNOT(1,2), CNOT(2,3), CNOT(3,0) $\rightarrow 4$ two-qubit gates per layer.
- **Alternatives Considered**:
  - *All-to-all entanglement*: Requires 6 CNOTs per layer, which is physically unrealistic on standard planar superconducting coupling grids without substantial SWAP gate overhead.
- **Evidence / Justification**:
  - Comparing linear vs. circular provides an exact ablation study: circular adds one extra CNOT (closing the loop between qubit 3 and 0).
  - Because two-qubit gates have an order of magnitude higher error rate than single-qubit gates on physical hardware (IBM calibration data), testing whether the circular loop justifies its extra noise cost is a core scientific question.

---

## 7. Noise Rates Sweep: $[0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]$
- **Choice Made**: Granular micro-noise sweep from $0\%$ up to $5\%$, specifically targeting $[0.1\%, 0.2\%, 0.5\%, 1.0\%, 2.0\%, 5.0\%]$.
- **Alternatives Considered**:
  - *Coarse macro-sweep ($0\%, 25\%, 50\%, 100\%$)*: Fails to capture the practical operating regime of NISQ hardware and misses the crossover point.
- **Evidence / Justification**:
  - Real IBM superconducting processors (Eagle, Heron) report single-qubit errors around $0.02\% - 0.05\%$ and two-qubit CNOT errors around $0.5\% - 1.2\%$.
  - Our micro-sweep straddles this exact physical threshold, making our crossover analysis directly relevant to practical deployment decisions.

---

## 8. Noise Channel Physics: Depolarizing vs. Amplitude Damping
- **Choice Made**: Benchmark both Depolarizing Channel and Amplitude Damping Channel.
- **Physical Rationale**:
  - *Depolarizing Channel*: Models symmetric environmental interaction (white noise), pulling the density matrix toward the maximally mixed state $\frac{I}{2}$. It isotropically shrinks the Bloch sphere.
  - *Amplitude Damping Channel*: Models non-symmetric energy relaxation ($T_1$ decay) caused by physical energy loss into the thermal bath, driving qubits toward $|0\rangle$.
  - Comparing both reveals whether asymmetric energy relaxation impacts VQCs differently from isotropic decoherence.

---

## 9. Dataset Selection: PneumoniaMNIST (MedMNIST)
- **Choice Made**: PneumoniaMNIST binary classification (300 train / 100 test balanced samples).
- **Alternatives Considered**:
  - *Synthetic Two-Moons or Circles*: Too simplistic; does not demonstrate clinical or real-world applicability.
  - *Standard MNIST digits (e.g. 0 vs 1)*: Widely overused and often linearly separable after trivial pooling.
  - *Full size PneumoniaMNIST (4,708 samples)*: Simulation of 4,708 samples under noisy density matrix backends for dozens of configurations would require dozens of compute hours.
- **Evidence / Justification**:
  - PneumoniaMNIST represents real chest X-ray diagnosis (Normal vs Pneumonia).
  - Balanced subset (150/150 train, 50/50 test) ensures that 50% accuracy is strictly random chance, and performance metrics (precision, recall, F1) are unskewed.

---

## 10. Classical Baselines: Logistic Regression + Small MLP
- **Choice Made**: Benchmark against BOTH a linear baseline (PyTorch Logistic Regression) and a compact non-linear baseline (PyTorch Small MLP: 4-8-1).
- **Alternatives Considered**:
  - *Deep ResNet or DenseNet*: Unfair comparison because a deep network has millions of parameters and requires massive compute, whereas a 4-qubit VQC has only 4 to 12 parameters.
- **Evidence / Justification**:
  - Logistic Regression provides a clean, convex linear decision boundary with 5 parameters ($4 \times 1 + 1$).
  - Small MLP provides a non-linear classical model with 49 parameters, closely mirroring the small parameter scale of near-term VQCs.
  - Both operate on the exact same 4 PCA features with zero noise by definition.
