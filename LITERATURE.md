# LITERATURE.md - Research Foundations & Verified Citations

This document catalogues all literature and technical references directly consulted, verified against PDF texts, and used to guide the experimental design of this project.

> [!IMPORTANT]
> Every citation, DOI, page number, and finding in this document has been directly verified against the original text in the respective PDF files. Unverified claims, third-party slide decks, and external proposal summaries have been strictly excluded.

---

## 1. Primary Research Papers (Verified in `papers/`)

### Paper 1: Satpathy et al. (IEEE IoT Journal 2024)
- **Full Citation**: Sritam Kumar Satpathy, Vallabh Vibhu, Bikash K. Behera, Saif Al-Kuwari, Shahid Mumtaz, and Ahmed Farouk. *"Analysis of Quantum Machine Learning Algorithms in Noisy Channels for Classification Tasks in the IoT Extreme Environment."* *IEEE Internet of Things Journal*, vol. 11, no. 3, pp. 3840–3852, 1 February 2024.
- **Verified DOI**: [10.1109/JIOT.2023.3300577](https://doi.org/10.1109/JIOT.2023.3300577)
- **Verified Findings from Text**:
  1. **Architecture & Application** (Section V, pp. 3844–3847): Evaluates multiple quantum classification approaches ($UU^\dagger$, variational $UU^\dagger$, and QNN) across two energy datasets (TWTDUS and SDWTT18) related to IoT extreme environments, demonstrating high classification accuracy under ideal conditions.
  2. **Noise Channel Sweep** (Section V-B.4, pp. 3849–3851): Investigates four quantum noise channels (bit-flip, phase-flip, depolarizing, and amplitude damping) by sweeping the noise probability parameter $\eta$ from 0 to 1 with step increments of 0.1 (Figs. 14 and 15).
  3. **Differential Noise Degradation** (Section V-B.4, p. 3849): Observes that the bit-flip noise model exhibits a sharp decline in classification accuracy as $\eta$ increases, whereas depolarizing and amplitude damping noise show a gradual, monotonic downward accuracy trend with increasing noise parameter probability.
- **Influence on This Project**:
  - Directly justifies benchmarking both depolarizing and amplitude damping channels to observe gradual performance degradation under simulated hardware noise.

---

### Paper 2: Easom-McCaldin et al. (IEEE Access 2021)
- **Full Citation**: Philip Easom-McCaldin, Ahmed Bouridane, Ammar Belatreche, and Richard Jiang. *"On Depth, Robustness and Performance Using the Data Re-Uploading Single-Qubit Classifier."* *IEEE Access*, vol. 9, pp. 65127–65139, April 2021.
- **Verified DOI**: [10.1109/ACCESS.2021.3075492](https://doi.org/10.1109/ACCESS.2021.3075492)
- **Verified Findings from Text**:
  1. **Noise Channel Implementation** (Section III-C, pp. 65133–65134, Equations 4–6): Models environmental noise during training using amplitude damping channels applied after each unitary gate via the PennyLane mixed-state simulator (`default.mixed`). Tested amplitude damping only.
  2. **Depth vs. Robustness Saturation** (Section IV-C, pp. 65135–65137, Figs. 11 & 12): Studies the effect of circuit depth ($L \in [1, 10]$) on noise robustness; finds that increasing depth from 1 to 3 layers provides the sharpest robustness improvements during training, but this robustness benefit saturates as additional layers are added.
  3. **MNIST Binary Classification Breakdown** (Section IV-D, pp. 65136–65137): On a binary MNIST classification task (digits 0 and 1) using a single-layer single-qubit architecture, good performance is maintained under low noise, but the model fails to converge once the amplitude damping parameter exceeds $\lambda = 0.3$.
- **Influence on This Project**:
  - Motivates evaluating shallow circuit depths ($L \in \{1, 2, 3\}$) to examine how layer depth affects noise sensitivity.
  - Provides mathematical Kraus formulations for the amplitude damping channel: $K_0 = \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix}$, $K_1 = \begin{bmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{bmatrix}$.

---

### Paper 3: Maheshwari et al. (IEEE Access 2022)
- **Full Citation**: Danyal Maheshwari, Daniel Sierra-Sosa, and Begonya Garcia-Zapirain. *"Variational Quantum Classifier for Binary Classification: Real vs Synthetic Dataset."* *IEEE Access*, vol. 10, pp. 3705–3715, December 2021 / January 2022.
- **Verified DOI**: [10.1109/ACCESS.2021.3139323](https://doi.org/10.1109/ACCESS.2021.3139323)
- **Verified Findings from Text**:
  1. **State Preparation Comparison** (Section III-A & III-B, pp. 3707–3709): Directly compares two data encoding strategies—Basis Encoding VQC vs. Amplitude Encoding VQC—across three binary classification benchmarks: a synthetic dataset, UCI Sonar, and Diabetes.
  2. **Encoding Performance Metrics** (Section IV, Table 2 & Table 3, pp. 3711–3713): Reports that Amplitude Encoding VQC achieves 98.40% testing accuracy on the synthetic dataset (at depth 5, 100 epochs), 67.30% on Sonar, and 74.50% on Diabetes.
  3. **Impact of Encoding Strategy** (Section IV-A & IV-C, pp. 3712–3714): Concludes that Amplitude Encoding substantially outperforms Basis Encoding on the synthetic and diabetes datasets, establishing that the choice of input encoding directly impacts classification accuracy and circuit resource overhead.
- **Influence on This Project**:
  - Highlights the paramount importance of data encoding in VQCs. This influenced our choice of angle encoding with PCA-reduced features as a compact, constant-depth alternative to multi-qubit basis or amplitude encoding circuits.

---

### Paper 4: Sajadimanesh et al. - NR-QNN (IEEE Access 2025)
- **Full Citation**: Sohrab Sajadimanesh, Hanieh Aghaee Rad, Jean Paul Latyr Faye, and Ehsan Atoofian. *"NR-QNN: Noise-Resilient Quantum Neural Network."* *IEEE Access*, vol. 13, pp. 38550–38562, March 2025.
- **Verified DOI**: [10.1109/ACCESS.2025.3546956](https://doi.org/10.1109/ACCESS.2025.3546956)
- **Verified Findings from Text**:
  1. **Two-Stage Noise Mitigation** (Abstract & Section III, pp. 38550–38552): Proposes NR-QNN, which mitigates hardware noise during inference using two complementary techniques: **quantum pruning** and **sensitivity-aware qubit mapping**.
  2. **Quantum Gate Pruning** (Section III-B, pp. 38555–38556): Identifies parameterized rotation gates whose rotation angle $|\theta|$ falls below a threshold and removes them, simplifying the circuit structure and reducing gate count and depth to minimize noise accumulation.
  3. **Sensitivity-Aware Qubit Mapping** (Section III-C, pp. 38556–38557): Analyzes the non-uniform error rates across physical NISQ qubits and maps higher-sensitivity logical qubits to more reliable physical qubits.
- **Influence on This Project**:
  - Demonstrates that circuit complexity (gate count and circuit depth) directly determines noise accumulation on NISQ devices.

---

### Paper 5: Prerana M N et al. - Layerwise Noise Sensitivity (IEEE INDICON 2025)
- **Full Citation**: Prerana M N, Poorav J Bolar, and Jayashree R. *"Layerwise Noise Sensitivity in Quantum Neural Networks for NISQ Devices."* *2025 IEEE 22nd India Council International Conference (INDICON)*, 2025.
- **Verified DOI**: [10.1109/INDICON68490.2025.11393039](https://doi.org/10.1109/INDICON68490.2025.11393039)
- **Verified Findings from Text**:
  1. **Layerwise Sensitivity Drop Metric** (Section III, p. 3, Eq. 9): Introduces the LSD metric:
     $$\text{LSD}_L = \frac{A_{\text{clean}} - A_{L,\text{noisy}}}{A_{\text{clean}}}$$
     to quantitatively isolate and measure performance degradation when noise is restricted to individual layers.
  2. **Sensitivity Hierarchy** (Abstract & Section V, pp. 1, 6): Identifies a consistent vulnerability ranking: the **encoding layer is the most vulnerable**, variational layers are moderately robust, and the measurement layer is the most resilient.
  3. **Vulnerability of Encoding Stage** (Section V & Table III, p. 6): Under amplitude damping noise, the encoding layer suffers a maximum LSD of **42.9%**, because noise occurring during state preparation corrupts input representations before variational processing begins.
- **Influence on This Project**:
  - Highlights why angle encoding on calibrated channels must be strictly modeled, and confirms that early gate errors propagate significantly throughout quantum circuits.

---

### Paper 6: Rahman et al. - Fine-Tuned VQC (IEEE COMPSAC 2024)
- **Full Citation**: Md Abdur Rahman, Mst. Shapna Akter, Emily Miller, Bogdan Timofti, Hossain Shahriar, Mohammad Masum, and Fan Wu. *"Fine-tuned Variational Quantum Classifiers for Cyber Attacks Detection based on Parameterized Quantum Circuits and Optimizers."* *2024 IEEE 48th Annual Computers, Software, and Applications Conference (COMPSAC)*, pp. 1060–1065, 2024.
- **Verified DOI**: [10.1109/COMPSAC61105.2024.00164](https://doi.org/10.1109/COMPSAC61105.2024.00164)
- **Verified Findings from Text**:
  1. **PQC & Optimizer Evaluation in Qiskit** (Section IV & V, pp. 1062–1064): Implements VQCs using IBM's Qiskit to evaluate parameterized quantum circuit architectures (`EfficientSU2` vs. `RealAmplitudes`) and classical derivative-free optimizers (`COBYLA` vs. `AQSD`) on network anomaly data.
  2. **Superiority of EfficientSU2 + COBYLA** (Section V, Table on p. 1064): Demonstrates that `EfficientSU2` with `COBYLA` on 3 attributes achieves 90% test accuracy (93% training accuracy), whereas `AQSD` underperforms significantly, yielding only 46% test accuracy.
  3. **Feature Reduction Speedup** (Section V, Table on p. 1064): Reducing the attribute set from 8 features to 3 features reduced training time under `EfficientSU2` and `COBYLA` from 1441 seconds down to 356 seconds.
- **Influence on This Project**:
  - Confirms that reducing input feature dimensionality drastically speeds up quantum optimization.
  - *Distinction*: Rahman et al. used derivative-free COBYLA in Qiskit. In our project, we deliberately choose gradient-based Adam in PyTorch via PennyLane parameter-shift gradients (see Author's Design Choices below).

---

## 2. Hardware Error Rates: IBM Quantum Calibration Data

- **Source**: IBM Quantum Platform compute resources & Qiskit Runtime processor documentation:
  - Link: [IBM Quantum Processor Types & Calibration Metrics](https://docs.quantum.ibm.com/guides/processor-types)
  - Link: [IBM Quantum Compute Resources](https://quantum.ibm.com/)
- **Verified Hardware Figures**:
  - **Single-Qubit Gate Error (Median $SX$ Error)**: Typically $2.0 \times 10^{-4}$ to $5.0 \times 10^{-4}$ ($0.02\% - 0.05\%$) on modern Heron and Eagle processors.
  - **Two-Qubit Gate Error (Median 2Q / CNOT / CZ / ECR Error)**: Typically $2.0 \times 10^{-3}$ to $8.0 \times 10^{-3}$ ($0.2\% - 0.8\%$) on modern architectures (e.g., Heron), and $1.0 \times 10^{-2}$ to $1.5 \times 10^{-2}$ ($1.0\% - 1.5\%$) on earlier Falcon/Eagle architectures.
  - **Readout Error**: Typically $1.0 \times 10^{-2}$ to $2.5 \times 10^{-2}$ ($1\% - 2.5\%$).
- **Direct Justification for Our Sweep Range**:
  - Our selected noise rate sweep: `[0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]` ($0\%$ to $5\%$) directly spans this real-world operational regime:
    - `0.001` ($0.1\%$) represents near-ideal two-qubit hardware performance.
    - `0.005`–`0.01` ($0.5\% - 1.0\%$) represents typical physical CNOT/ECR gate error rates.
    - `0.02`–`0.05` ($2.0\% - 5.0\%$) represents degraded or unmitigated multi-gate noise accumulation.

---

## 3. Author's Own Hypotheses and Design Choices (NOT Paper Findings)

The following choices are the author's own independent design hypotheses and engineering decisions, formulated for this project:

1. **Linear vs. Circular CNOT Topology Sensitivity**:
   - *Design Formulation*:
     - **Linear Topology**: Entangles adjacent qubits along an open chain: $\text{CNOT}(0,1), \text{CNOT}(1,2), \text{CNOT}(2,3)$ ($N-1 = 3$ entangling gates per layer).
     - **Circular Topology**: Adds a wrap-around entangling gate between the last and first qubit: $\text{CNOT}(0,1), \text{CNOT}(1,2), \text{CNOT}(2,3), \text{CNOT}(3,0)$ ($N = 4$ entangling gates per layer).
   - *Author's Hypothesis*: Because two-qubit entangling gates exhibit an order-of-magnitude higher error rate than single-qubit rotations on physical hardware, circular topology will experience higher cumulative noise degradation per layer than linear topology, particularly under depolarizing noise.

2. **Choice of PyTorch Adam Optimizer**:
   - *Design Formulation*: While some literature (e.g., Rahman et al.) utilized derivative-free optimizers like COBYLA in Qiskit, we choose the gradient-based **Adam optimizer** (`torch.optim.Adam`) in PyTorch.
   - *Author's Rationale*: PennyLane seamlessly integrates with PyTorch autograd via the parameter-shift rule (`interface="torch"`). Adam utilizes adaptive first and second moment estimation, which provides rapid, stable convergence on clean loss surfaces without the oscillating steps often observed with derivative-free heuristic search.

3. **Choice of Classical Baselines (Logistic Regression + Small MLP)**:
   - *Author's Rationale*: To benchmark the VQC fairly, we test a linear model (`LogisticRegressionPyTorch`, 5 parameters) and a compact non-linear model (`SmallMLPPyTorch`, 49 parameters) on the exact same 4 PCA features. This ensures the classical models match the small parameter scale of shallow NISQ circuits while remaining noise-invariant by construction.
