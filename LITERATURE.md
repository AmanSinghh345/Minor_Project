# LITERATURE.md - Research Foundations & Citations

This document catalogues all literature and technical references directly consulted, analyzed, and used to guide the design, modeling choices, noise parameters, and baseline architectures of this project.

---

## 1. Papers from Local Research Repository (`papers/`)

### Paper 1: Noise Analysis in QML for Extreme IoT Environments
- **Full Citation**: Sritam Kumar Satpathy, Vallabh Vibhu, Bikash K. Behera, Saif Al-Kuwari, Shahid Mumtaz, and Ahmed Farouk. *"Analysis of Quantum Machine Learning Algorithms in Noisy Channels for Classification Tasks in the IoT Extreme Environment."* *IEEE Internet of Things Journal*, vol. 11, no. 3, pp. 3840-3849, February 2024. [DOI: 10.1109/JIOT.2023.3308855](https://doi.org/10.1109/JIOT.2023.3308855).
- **Core Findings**:
  - Investigated QML performance under multiple quantum noise channels: depolarizing, amplitude damping, phase damping, bit-flip, and phase-flip.
  - Demonstrated that deep quantum circuits suffer catastrophic accuracy drops under noise (dropping from ~98% to ~26%), while shallow circuits exhibit much more predictable, gradual degradation.
- **Influence on this Project**:
  - Directly justifies restricting our variational ansatz to shallow depths ($L \in \{1, 2, 3\}$) to prevent premature noise saturation.
  - Guided our selection of depolarizing and amplitude damping channels as the primary benchmark noise models.

---

### Paper 2: Data Re-Uploading Single-Qubit Classifier Depth and Noise
- **Full Citation**: Philip Easom-McCaldin, Ahmed Bouridane, et al. *"On Depth, Robustness and Performance Using the Data Re-Uploading Single-Qubit Classifier."* *IEEE Access*, vol. 9, pp. 65127-65139, April 2021. [DOI: 10.1109/ACCESS.2021.3075492](https://doi.org/10.1109/ACCESS.2021.3075492).
- **Core Findings**:
  - Evaluated single-qubit quantum classification robustness against amplitude damping and depolarizing noise.
  - Found that performance suffers a sharp collapse beyond a critical damping probability ($\gamma \approx 0.4$), demonstrating that a clear noise-induced failure threshold exists.
- **Influence on this Project**:
  - Motivated the mathematical search for an empirical "crossover point" where quantum accuracy drops below classical baseline performance.

---

### Paper 3: Variational Quantum Classifier on Real vs. Synthetic Data
- **Full Citation**: Danyal Maheshwari et al. *"Variational Quantum Classifier for Binary Classification: Real vs Synthetic Dataset."* *IEEE Access*, vol. 10, pp. 4569-4578, December 2021. [DOI: 10.1109/ACCESS.2021.3139323](https://doi.org/10.1109/ACCESS.2021.3139323).
- **Core Findings**:
  - Evaluated VQCs against classical benchmarks (SVM, Logistic Regression) across both synthetic and real-world datasets.
  - Concluded that on real tabular and reduced-dimension image datasets, well-tuned classical baselines often match or outperform VQCs.
- **Influence on this Project**:
  - Establishes that Logistic Regression is not a "strawman" but a rigorous, standard, and highly credible classical baseline.
  - Emphasizes the need for fair, noise-free classical reporting alongside noisy quantum models.

---

### Paper 4: Noise-Resilient Quantum Neural Networks (NR-QNN)
- **Full Citation**: Sohrab Sajadimanesh, Hanieh Aghaee Rad, and Jean Paul Latyr Faye. *"NR-QNN: Noise-Resilient Quantum Neural Network."* *IEEE Access*, vol. 13, pp. 38550-38562, March 2025. [DOI: 10.1109/ACCESS.2025.3546956](https://doi.org/10.1109/ACCESS.2025.3546956).
- **Core Findings**:
  - Showed that deep parameterized quantum circuits (PQCs) suffer exponential fidelity decay driven by environmental $T_1$ (relaxation) and $T_2$ (dephasing) timescales.
  - Proposed architectural strategies to limit two-qubit gate counts, as entangling gates are the dominant source of NISQ noise.
- **Influence on this Project**:
  - Influenced our comparison of linear CNOT topology (which uses $N-1 = 3$ two-qubit gates per layer) versus circular CNOT topology ($N = 4$ two-qubit gates per layer).

---

### Paper 5: Layerwise Noise Sensitivity in QNNs for NISQ Devices
- **Full Citation**: Prerana M N et al. *"Layerwise Noise Sensitivity in Quantum Neural Networks for NISQ Devices."* PES University, Bangalore, 2024.
- **Core Findings**:
  - Studied the location-dependent effect of noise insertion within QNN layers.
  - Demonstrated that noise occurring in entangling layers causes significantly higher degradation than noise in single-qubit rotation gates.
- **Influence on this Project**:
  - Informs our ablation study comparing circular vs. linear entanglement: circular entanglement introduces an additional entangling gate and closure loop, amplifying sensitivity to depolarizing noise.

---

### Paper 6: Fine-Tuned VQCs and Optimizers for Cyber Attack Detection
- **Full Citation**: Md Abdur Rahman. *"Fine-Tuned Variational Quantum Classifiers for Cyber Attacks Detection Based on Parameterized Quantum Circuits and Optimizers."* University of West Florida, 2024.
- **Core Findings**:
  - Systematically evaluated Adam, COBYLA, and RMSProp optimizers on parameterized quantum circuits.
  - Found that Adam consistently yields superior gradient stability and convergence speed when training parameterized quantum circuits with angle encoding.
- **Influence on this Project**:
  - Solidified the choice of PyTorch Adam optimizer for training our VQC parameters noise-free before hardware noise injection.

---

### Paper 7: Quantum Machine Learning: Recent Advances, Challenges, and Perspectives
- **Full Citation**: Pradeep Lamichhane and Danda B. Rawat. *"Quantum Machine Learning: Recent Advances, Challenges, and Perspectives."* *IEEE Access*, vol. 13, 2025. [DOI: 10.1109/ACCESS.2025.3573244](https://doi.org/10.1109/ACCESS.2025.3573244).
- **Core Findings**:
  - Comprehensive survey of NISQ barriers: barren plateaus, hardware decoherence, gate infidelity, and input encoding bottlenecks.
  - Highlighted that dimensionality reduction (such as PCA) followed by angle encoding is the most viable strategy for mapping classical image data to NISQ circuits.
- **Influence on this Project**:
  - Direct justification for using PCA (784 dimensions $\rightarrow$ 4 dimensions) and $[0, \pi]$ $R_y$ angle encoding on 4 qubits.

---

### Paper 8: Minor Project Proposal & Presentation (Aditya Soni & Aman Singh)
- **Full Citation**: Aditya Soni and Aman Singh (Guided by Dr. Kapil Kumar Soni). *"Comparative Performance Analysis of Variational Quantum Classifiers Under Simulated Hardware Noise."* B.Tech Minor Project Proposal & Presentation, 2024. (Files: `papers/minor pdf.pdf` and `papers/Comparative-Performance-Analysis-of-Variational-Quantum-Classifiers-Under-Simulated-Hardware-Noise G2.pdf`).
- **Core Findings / Project Goals**:
  - Evaluates 4-qubit VQC vs. PyTorch classical baselines on MedMNIST binary classification.
  - Focuses on the micro-noise regime ($0.1\%$ to $1.0\%$) and studies linear vs. circular entanglement, depth vs. noise, and crossover identification.
- **Influence on this Project**:
  - Defines the core problem statement, research methodology, and milestone deliverables for this implementation.

---

## 2. Online Sources, Hardware Calibration Data & Framework Documentation

### Source 1: IBM Quantum Hardware Calibration Reports
- **Source / Citation**: IBM Quantum Systems Calibration Data (IBM Falcon, Eagle, and Heron QPUs via IBM Quantum Platform / Qiskit documentation). [Link: https://quantum.ibm.com/](https://quantum.ibm.com/).
- **Key Hardware Figures**:
  - **Single-qubit gate error ($e_{1q}$)**: typically $1.0 \times 10^{-4}$ to $5.0 \times 10^{-4}$ ($0.01\% - 0.05\%$).
  - **Two-qubit gate error (CNOT / ECR)**: typically $5.0 \times 10^{-3}$ to $1.5 \times 10^{-2}$ ($0.5\% - 1.5\%$).
  - **Readout / measurement error**: typically $1.0 \times 10^{-2}$ to $3.0 \times 10^{-2}$ ($1\% - 3\%$).
- **Influence on this Project**:
  - Justifies our chosen noise rate sweep: `[0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]` ($0\%$ to $5\%$).
  - The micro-range $0.1\%$ to $1.0\%$ is precisely where physical superconducting qubits operate today.

---

### Source 2: PennyLane Mixed-State & Quantum Noise Documentation
- **Source / Citation**: Xanadu. *"PennyLane: Mixed States and Noise Channels (`qml.DepolarizingChannel`, `qml.AmplitudeDamping`, `default.mixed`)."* PennyLane Official Documentation, 2024. [Link: https://docs.pennylane.ai/en/stable/introduction/operations.html#noisy-channels](https://docs.pennylane.ai/en/stable/introduction/operations.html#noisy-channels).
- **Key Concepts**:
  - Mixed states represented as density operators $\rho$.
  - Operation of noise channels via Kraus operator decomposition: $\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$ with completeness $\sum_k K_k^\dagger K_k = I$.
- **Influence on this Project**:
  - Used in Stage 3 to verify our hand-written NumPy Kraus operators against PennyLane's analytical implementations on `default.mixed`.

---

### Source 3: Quantum Computing in the NISQ Era and Beyond
- **Source / Citation**: John Preskill. *"Quantum Computing in the NISQ Era and Beyond."* *Quantum*, vol. 2, p. 79, August 2018. [DOI: 10.22331/q-2018-08-06-79](https://doi.org/10.22331/q-2018-08-06-79).
- **Key Findings**:
  - Coined the term Noisy Intermediate-Scale Quantum (NISQ).
  - Outlined that 50–100 qubit systems without fault tolerance will be heavily constrained by gate infidelity and short decoherence times.
- **Influence on this Project**:
  - Theoretical framework motivating why NISQ models must be benchmarked with realistic noise rather than assumed to be perfect.
