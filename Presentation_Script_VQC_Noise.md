# Complete Presentation & Speaker Defense Script
## *Comparative Analysis of Variational Quantum Circuits under Hardware-Simulated Noise for Clinical Diagnostics*

---

### **Presentation Overview & Execution Guide**
* **Total Duration:** 12–15 Minutes (~30–40 seconds per slide + transitions)
* **Team Members:**
  * **Speaker 1:** **Aditya Soni** (Roll No: `23118004`) — Slides 01 to 12 *(Problem, Motivation, Theory, Setup, Clean Results & Thermal Decay)*
  * **Speaker 2:** **Aman Singh** (Roll No: `23118008`) — Slides 13 to 25 *(Sign Invariance, IBM Hardware SWAP Trap, Error Mitigation, Multi-Dataset & Defense)*
* **Project Supervisor:** **Dr. Kapil Kumar Soni**, Assistant Professor, Department of Information Technology, NIT Raipur
* **Slide Deck:** `presentation_vqc_noise_senior_style.pptx` (25 Widescreen Slides)

---

## **Part 1: Speaker 1 — Aditya Soni (Slides 01 – 12)**

---

### **Slide 01: Title Slide & Introduction**
> *[Slide text: Comparative Analysis of Variational Quantum Circuits under Hardware-Simulated Noise]*

**Spoken Script (Aditya Soni):**
> "Respected supervisor Dr. Kapil Kumar Soni Sir, respected external examiners, and dear faculty members:
> 
> Good morning. I am **Aditya Soni** (Roll No: 23118004), and together with my project partner **Aman Singh** (Roll No: 23118008), we present our Semester 7 Minor Project entitled:
> 
> **'Comparative Analysis of Variational Quantum Circuits under Hardware-Simulated Noise for Clinical Diagnostics & Crossover Degradation'**.
> 
> Today, we examine whether Noisy Intermediate-Scale Quantum (NISQ) algorithms can deliver viable diagnostic performance in medical imaging, and we identify the exact physical hardware noise boundaries where quantum circuits break down relative to classical machine learning."

---

### **Slide 02: Introduction & Motivation**
> *[Slide text: Why Variational Quantum Circuits (VQCs)? NISQ Hardware Constraints, Clinical Diagnostic Mandate, Classical Crossover Boundary]*

**Spoken Script (Aditya Soni):**
> "Moving to Slide 2: In recent literature, Variational Quantum Circuits—or VQCs—have been widely celebrated for their potential to process medical data in exponentially large Hilbert spaces.
> 
> However, today's quantum computers exist in the **NISQ era**—Noisy Intermediate-Scale Quantum. They lack fault-tolerant quantum error correction. Every physical two-qubit gate, every microsecond of thermal relaxation, and every detector readout introduces errors.
> 
> In safety-critical domains like pneumonia detection from chest X-rays, clinical sensitivity and recall are paramount. A false negative can cost a patient's life. 
> 
> Therefore, rather than chasing speculative 'quantum supremacy', our project asks a fundamental engineering question: **At what precise physical noise threshold does a quantum classifier cross below classical machine learning baselines?**"

---

### **Slide 03: Research Gap & Related Work**
> *[Slide text: Table comparing Ideal VQC studies, Arbitrary High-Noise sweeps, Ad-hoc classical baselines, and Our Proposed Framework]*

**Spoken Script (Aditya Soni):**
> "Slide 3 highlights the critical gaps in prior literature:
> 
> First, seminal papers like Farhi and Neven evaluate VQCs using **noise-free statevector simulators**. While useful for theoretical proof-of-concept, they completely ignore physical gate infidelities and $T_1/T_2$ relaxation times.
> 
> Second, studies that do test noise frequently simulate unrealistic, uniform noise rates of 20% to 50%. On real superconducting processors, gate error rates sit between 0.1% and 5%. Extreme noise tests fail to observe micro-noise dynamics.
> 
> Third, many quantum papers benchmark against weak, un-tuned classical heuristics. 
> 
> Our framework bridges these gaps by combining **first-principles Kraus operator modeling**, **real daily calibration snapshots from physical IBM Quantum processors**, and a rigorous suite of **six tuned classical machine learning baselines**."

---

### **Slide 04: Proposed Framework: Noise-Aware VQC**
> *[Slide text: Mathematical Foundation: $\mathcal{E}(\rho) = \sum K_k \rho K_k^\dagger$, Probability Mapping, Core Contributions]*

**Spoken Script (Aditya Soni):**
> "On Slide 4, we present the mathematical foundation of our Noise-Aware VQC toolkit.
> 
> To capture open quantum system dynamics, we model quantum states using density operators $\rho$. Every quantum gate is followed by a **Kraus channel map**:
> $$\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger, \quad \text{where} \quad \sum_k K_k^\dagger K_k = I$$
> 
> At the final stage, we measure the expectation value of the Pauli-Z operator on qubit 0: $\langle Z_0 \rangle \in [-1, +1]$. We then apply a continuous probability mapping:
> $$P(y=1) = \frac{1 - \langle Z_0 \rangle}{2}$$
> A patient is classified as Pneumonia if $\langle Z_0 \rangle \le 0$, corresponding to a probability greater than 50%.
> 
> Our core technical contributions include an integrated **Trapezoidal Noise-Robustness Score (NRS)**, strict **zero-leakage PCA feature pre-processing**, and **closed-form algorithmic selection rules** for NISQ hardware."

---

### **Slide 05: System Architecture & Pipeline**
> *[Slide text: 3 numbered cards: Angle Encoding, Parameterized Ansatz, Pauli-Z Readout & Error Mitigation + 9-step execution flow]*

**Spoken Script (Aditya Soni):**
> "Slide 5 illustrates our end-to-end operational pipeline across nine sequential stages:
> 
> 1. We take 28x28 chest X-rays from the **PneumoniaMNIST** benchmark.
> 2. We apply zero-leakage PCA, fitting strictly on the training partition to reduce dimensionality from 784 pixels to 4 dominant orthogonal components.
> 3. These 4 features are mapped into quantum state space via **$R_y$ angle feature encoding**, scaled monotonically to $[0, \pi]$.
> 4. The state enters a parameterized variational ansatz composed of parameterized single-qubit rotations and entangling CNOT gates across depths $L \in \{1, 2, 3\}$.
> 5. Physical Kraus noise channels are injected after each gate.
> 6. We simulate full density matrix propagation on PennyLane's `default.mixed` device.
> 7. We compute the $\langle Z_0 \rangle$ expectation value.
> 8. We apply **Readout Error Mitigation (REM)** via confusion matrix inversion $M^{-1}$.
> 9. Finally, the system outputs the calibrated clinical diagnosis."

---

### **Slide 06: Comparison Algorithms (Classical & Quantum Suite)**
> *[Slide text: 9 evaluated models: Logistic Regression, Linear SVM, RBF SVM, Random Forest, GBDT, Small MLP, Standard VQC, Data Re-uploading, QSVC]*

**Spoken Script (Aditya Soni):**
> "On Slide 6, we detail our benchmark suite of nine distinct algorithms.
> 
> To ensure scientific rigor, we evaluated **six classical paradigms**:
> - Our primary classical ceiling is **Logistic Regression**, which provides a strictly convex linear baseline.
> - We also evaluate **Linear SVM**, **RBF Kernel SVM**, **Random Forest** (100 trees), **Gradient Boosted Decision Trees**, and a test-tuned **Small MLP** (4-8-1 architecture with Kaiming initialization).
> 
> On the quantum side, we evaluate three paradigms:
> - **Standard Parameterized VQC** across layers $L=1, 2, 3$ in both Linear and Circular topologies.
> - **Data Re-uploading VQC**, which interleaves data encoding between variational rotation layers.
> - **Quantum Support Vector Classifier (QSVC)**, which evaluates quantum kernel overlap matrices combined with a classical quadratic program solver."

---

### **Slide 07: Performance Metrics**
> *[Slide text: Table: Accuracy, Recall (Sensitivity), Noise-Robustness Score (NRS), Classical Crossover Rate, Mean Probability Drift]*

**Spoken Script (Aditya Soni):**
> "Slide 7 outlines the five evaluation metrics chosen specifically for medical safety:
> 
> While overall **Classification Accuracy** measures total correctness, in clinical diagnostics, **Recall (or Sensitivity)** is our most critical metric. Missing a pneumonia case carries far higher cost than a false alarm.
> 
> To quantify noise resilience holistically, we formulated the **Noise-Robustness Score (NRS)**. This is a normalized trapezoidal integral computing the Area Under the Performance Curve across all tested noise rates, where $1.0$ represents a completely noise-immune architecture.
> 
> We also measure **Mean Probability Drift**, which quantifies how severely noise shrinks the model's confidence away from its ideal decision boundary."

---

### **Slide 08: Test Scenarios & Physical Noise Channels**
> *[Slide text: 4 test scenarios: Clean Benchmark, Thermal Relaxation (T1), Environmental Decoherence (Depolarizing), IBM Hardware Calibration]*

**Spoken Script (Aditya Soni):**
> "Slide 8 details the four environmental noise scenarios we modeled:
> 
> 1. **Clean Benchmark ($p=0.0$):** Used to verify our density matrix simulator matches exact analytic statevectors to within $10^{-14}$.
> 2. **Thermal Relaxation ($T_1$ Amplitude Damping):** Models irreversible energy loss where excited states $|1\rangle$ spontaneously decay to ground state $|0\rangle$ with transition probability $\gamma = 1 - e^{-t/T_1}$.
> 3. **Environmental Decoherence (Depolarizing Noise):** Models isotropic white noise where the qubit state is uniformly scrambled by Pauli $X$, $Y$, and $Z$ errors.
> 4. **Physical IBM Hardware Calibration:** Emulates daily calibration snapshots of real superconducting chips—IBM Eagle, Perth, Manila, and Bogota—incorporating real gate durations, coupling graph constraints, and asymmetric readout confusion."

---

### **Slide 09: Training Dynamics & Optimization**
> *[Slide text: PyTorch Adam lr=0.02, MSE parity loss, Full-batch 300 samples, 40 epochs, Parameter-Shift, 5 independent seeds]*

**Spoken Script (Aditya Soni):**
> "Slide 9 presents our training methodology.
> 
> All variational circuits were trained using **PyTorch Adam** with a learning rate of $0.02$, minimizing Mean Squared Error on parity targets over 40 epochs.
> 
> Quantum gradients were computed using the **analytic Parameter-Shift Rule**, which executes circuit shifts at $\pm \frac{\pi}{2}$ to evaluate exact hardware gradients without numerical finite-difference errors.
> 
> To prevent barren plateaus, angles were initialized with small random distributions ($\sigma = 0.01$). Crucially, every experiment was repeated across **5 independent random seeds**—42, 43, 44, 45, and 46—with all checkpoints saved for fully reproducible validation."

---

### **Slide 10: Evaluation Protocol & Statistical Rigor**
> *[Slide text: Sample Standard Deviation ddof=1, Classical Crossover Definition (B - 1s), Paired Seed Comparison, Sanity Check at Rate 0]*

**Spoken Script (Aditya Soni):**
> "Slide 10 outlines our statistical protocol.
> 
> In compliance with strict academic standards, all experimental spreads and error bars report the **unbiased sample standard deviation $s$ with degrees of freedom $\text{ddof}=1$**:
> $$s = \sqrt{\frac{1}{N-1} \sum_{i=1}^N (x_i - \bar{x})^2}$$
> Population standard deviation was strictly disallowed.
> 
> Furthermore, we established a mathematically formal definition of the **Classical Crossover Boundary**: it is the highest noise rate where mean VQC accuracy remains within one standard deviation of the classical Logistic Regression ceiling:
> $$\text{Mean}(\text{VQC}) \ge \text{Mean}(\text{LR}) - 1s(\text{LR})$$
> We also conducted paired seed-by-seed analysis to verify whether observed performance variations reflect genuine quantum behavior rather than stochastic initialization luck."

---

### **Slide 11: Performance under Clean Benchmark**
> *[Slide text: Performance Table: LR 82%, RBF SVM 83%, Small MLP 81%, RF 77%, VQC Circ L=3 84.6%, QSVC 86%]*

**Spoken Script (Aditya Soni):**
> "Turning to our results on Slide 11:
> 
> In the ideal, noise-free regime, classical Logistic Regression sets a strong baseline at **82.00% accuracy** and 82.00% recall. The non-linear classical Small MLP achieves **81.00%**.
> 
> Standard VQC with Circular entanglement at depth $L=3$ achieved **84.60% ± 0.89%**, successfully outperforming classical Logistic Regression by $+2.6\%$.
> 
> Most impressively, **Quantum Kernel Estimation (QSVC)** achieved the highest overall clean accuracy at **86.00%**, surpassing all classical and variational competitors.
> 
> This proves that under ideal conditions, quantum feature spaces can indeed capture subtle clinical correlations in medical data."

---

### **Slide 12: The Thermal Relaxation Catastrophe ($T_1$ Decay)**
> *[Slide text: Why Amplitude Damping Destroys Recall: Spontaneous Relaxation $K_1$, State Collapsing Toward Normal $|0\rangle$, Recall Collapse to 0.00%]*

**Spoken Script (Aditya Soni):**
> "However, Slide 12 reveals the most critical clinical discovery of our study: **The Thermal Relaxation Catastrophe**.
> 
> When we introduce Amplitude Damping ($T_1$), the Kraus operator $K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}$ irreversibly decays excited states $|1\rangle$ to ground state $|0\rangle$.
> 
> In our clinical encoding, ground state $|0\rangle$ corresponds to Class 0, which represents 'Normal' (healthy) lungs. As thermal relaxation increases, all patient states artificially decay toward Normal.
> 
> Consequently, at a noise rate of just $\gamma = 0.05$, **clinical recall collapses to exactly 0.00%**. The model classifies every single sick patient as healthy. 
> 
> In an automated hospital triage system, this would lead to catastrophic, undetected pneumonia. This proves that for clinical NISQ deployment, thermal relaxation is vastly more dangerous than simple dephasing.
> 
> At this point, I would like to hand over to my teammate, **Aman Singh**, who will present our findings on depolarizing sign invariance, the physical IBM hardware transpilation trap, and quantum error mitigation."

---

## **Part 2: Speaker 2 — Aman Singh (Slides 13 – 25)**

---

### **Slide 13: Phenomenon: Sign Invariance under Depolarizing Noise**
> *[Slide text: Analytical Proof: $\text{Tr}(\mathcal{E}(\rho) Z_0) = (1 - \frac{4p}{3}) \langle Z_0 \rangle_{\text{clean}}$, Table showing flipped predictions]*

**Spoken Script (Aman Singh):**
> "Thank you, Aditya. Respected panel, I am **Aman Singh** (Roll No: 23118008), and I will walk you through our empirical discoveries and hardware validation.
> 
> On Slide 13, we present a remarkable contrast to the thermal catastrophe: **The Phenomenon of Sign Invariance under Depolarizing Noise**.
> 
> We analytically proved that under isotropic depolarizing noise of rate $p$, the expectation value of any traceless observable scales by an exact scalar factor:
> $$\text{Tr}(\mathcal{E}(\rho) Z_0) = \left(1 - \frac{4p}{3}\right) \langle Z_0 \rangle_{\text{clean}}$$
> 
> Notice that for all physical noise rates $p \le 0.05$, the coefficient $(1 - \frac{4p}{3}) \ge 0.933$, which is **strictly positive**.
> 
> This means that while depolarizing noise shrinks the magnitude of model confidence toward 0.5, it **never flips the sign** of the decision boundary!
> 
> As our table demonstrates, across 100 clinical test samples, shallow circuits flipped **0.0 samples**, and even at $L=3$ under heavy 5% noise, only 3 out of 100 samples flipped. Depolarizing noise degrades confidence, but preserves diagnostic classification."

---

### **Slide 14: Heavy Noise Regime (5%) Comparative Breakdown**
> *[Slide text: Table comparing Clean, 5% Depolarizing, and 5% Amplitude Damping across models]*

**Spoken Script (Aman Singh):**
> "Slide 14 compares our architectures under the heavy 5% noise regime:
> 
> Look at Standard VQC at depth $L=3$: Under 5% depolarizing noise, accuracy is preserved at **82.60%**. But under 5% amplitude damping, it suffers a devastating collapse to **57.20%**—a drop of 27.4 percentage points!
> 
> Meanwhile, classical Logistic Regression stands completely impervious at **82.00%**.
> 
> However, look at the bottom row: **Quantum Kernel Estimation (QSVC)** holds firm at **82.00%** under both 5% depolarizing and 5% amplitude damping noise, proving that convex dual optimization possesses superior structural resilience over parameterized circuits."

---

### **Slide 15: Entanglement Topology: Linear vs. Circular**
> *[Slide text: Key Findings on Entanglement: Clean Advantage (+2.4%), Noise Penalty, Heavy Noise Crossover (+12.4% for Linear), Readout Qubit Effect]*

**Spoken Script (Aman Singh):**
> "Slide 15 analyzes entanglement topology: Linear versus Circular.
> 
> In clean simulations, Circular entanglement held a $+2.4\%$ advantage at $L=3$ because its closed loop allows correlations between Qubit 3 and Qubit 0.
> 
> However, that closed loop requires an extra CNOT gate per layer. In noisy environments, every additional two-qubit gate acts as an open door for decoherence.
> 
> Under 5% amplitude damping, the tables turn dramatically: **Linear topology outperforms Circular by $+12.4\%$** (69.6% vs 57.2%).
> 
> Furthermore, we proved that for shallow Linear circuits ($L=1$), the readout must be placed on the final qubit (Q3) to capture the entangling cascade, whereas at $L=3$, information spreads uniformly across all qubits."

---

### **Slide 16: Results: Quantum Kernel (QSVC) Superiority**
> *[Slide text: 4 cards: Clean Superiority (86%), Immune to T1 Relaxation, Dual Convex Optimization, No Barren Plateaus]*

**Spoken Script (Aman Singh):**
> "On Slide 16, we explain why Quantum Kernels decisively outperform Deep VQCs under physical noise.
> 
> In a parameterized VQC, noise corrupts both the forward pass and the parameter-shift gradients during backpropagation, leading to noise-induced barren plateaus.
> 
> In contrast, QSVC uses quantum circuits **only to evaluate state overlaps**: $|\langle \psi(x) | \psi(x') \rangle|^2$. Once this Gram matrix is computed, the decision hyperplane is solved via a **classical quadratic programming solver**.
> 
> Because the optimization is globally convex and handled entirely on classical hardware, QSVC completely eliminates barren plateaus, delivering **86% clean accuracy** and holding **82% under thermal decay**."

---

### **Slide 17: The Hardware Transpilation SWAP Routing Trap**
> *[Slide text: Publication Figure: Eagle, Perth, Manila, Bogota. Simulated vs Physical CNOTs: Circular explodes to 32 CNOTs -> collapses to 51%]*

**Spoken Script (Aman Singh):**
> "Slide 17 reveals the second major discovery of our research: **The Hardware SWAP Routing Trap**.
> 
> In idealized simulators, researchers assume all-to-all connectivity. On physical superconducting processors like **IBM Eagle, Perth, Manila, and Bogota**, physical qubits are arranged on a linear or heavy-hexagonal lattice: Q0 is connected to Q1, Q1 to Q2, and Q2 to Q3.
> 
> There is **no physical wire between Q3 and Q0**.
> 
> To execute a Circular entanglement gate between Q3 and Q0, the IBM transpiler must insert **4 SWAP gates**, which equals **12 additional physical CNOTs per layer**.
> 
> Over a 2-layer circuit, the CNOT count explodes from 8 to **32 physical CNOTs**. Under real device calibration errors, Circular accuracy collapses to **51% to 52%**—no better than a random coin toss!
> 
> In contrast, **Native Linear entanglement requires exactly 0 SWAPs** (6 CNOTs total) and sustains **77% to 78% accuracy** across all IBM processors. This proves that designing circuits without accounting for QPU coupling graphs leads to complete algorithmic failure."

---

### **Slide 18: Quantum Error Mitigation (REM & ZNE)**
> *[Slide text: Readout Error Mitigation via $M^{-1}$, Zero Gate Overhead, ZNE +2% recovery, Synergistic Stack]*

**Spoken Script (Aman Singh):**
> "On Slide 18, we present our Error Mitigation results.
> 
> First, we implemented **Readout Error Mitigation (REM)** by characterizing the $2 \times 2$ detector confusion matrix $M = \begin{pmatrix} 1-p_{01} & p_{10} \\ p_{01} & 1-p_{10} \end{pmatrix}$ and inverting it via $M^{-1}$.
> 
> Because REM is pure classical post-processing, it incurs **zero additional quantum gate overhead**. On IBM Eagle and Manila, REM eliminated over **60% of output probability drift**, reducing drift from 0.0075 down to 0.0029.
> 
> Second, we implemented **Zero-Noise Extrapolation (ZNE)** using unitary folding at scale factors $c \in \{1, 2, 3\}$, recovering $+2.0\%$ accuracy under 2% amplitude damping.
> 
> When combined, **Native Linear Topology + REM** fully restores near-clean parity on real hardware."

---

### **Slide 19: Multi-Dataset Generalization**
> *[Slide text: Table comparing PneumoniaMNIST, Breast Cancer Wisconsin, and Fisher's Iris across dimensions and models]*

**Spoken Script (Aman Singh):**
> "To prove our conclusions are not an artifact of a single dataset, Slide 19 shows our multi-dataset benchmark across three distinct domains:
> 
> 1. **PneumoniaMNIST** (Medical Imaging, 784 pixels $\to$ 4 PCA components).
> 2. **Breast Cancer Wisconsin** (Clinical Tabular FNA, 30 features $\to$ 4 PCA components).
> 3. **Fisher's Iris** (Continuous Botanical, 4 raw physical measurements with zero PCA compression).
> 
> On Breast Cancer Wisconsin, VQC achieved **93.71% accuracy**, coming within 2% of the classical ceiling (95.80%). On Iris, VQC achieved **96.67%**, proving robust multi-class separability.
> 
> Most importantly, the hierarchy of noise vulnerability—where amplitude damping severely outperforms depolarizing in destruction rate—was strictly replicated across all three datasets."

---

### **Slide 20: Noise-Robustness Score (NRS) Ranking**
> *[Slide text: Ranking Table: Circular L=3 #1 under Depol (0.9943), Linear L=3 #1 under T1 (0.9870)]*

**Spoken Script (Aman Singh):**
> "Slide 20 synthesizes our results into the **Noise-Robustness Score (NRS)** ranking table:
> 
> - Under isotropic depolarizing noise, **Circular $L=3$ ranks #1** with an exceptional score of **0.9943**, thanks to closed-loop sign invariance.
> - However, under thermal amplitude damping ($T_1$), **Linear $L=3$ takes the #1 position** with a score of **0.9870**, because its lower CNOT count limits spontaneous energy decay.
> 
> This table provides a rigorous selection guide for quantum engineers: If your QPU is dephasing-dominated, use Circular entanglement; if your QPU is $T_1$-relaxation-dominated, Linear topology is mandatory."

---

### **Slide 21: Discussion & Key Empirical Discoveries**
> *[Slide text: 3 numbered summary cards: Depolarizing Invariance vs Thermal Catastrophe, Coupling Graph Priority, Kernel Paradigm Superiority]*

**Spoken Script (Aman Singh):**
> "Slide 21 summarizes our three core scientific takeaways:
> 
> 1. **Depolarizing Noise is Clinically Benign, but Thermal Relaxation is Lethal:** Depolarizing noise merely contracts margin confidence without flipping labels. Thermal relaxation irreversibly biases readouts toward $|0\rangle$, destroying clinical recall and generating fatal false negatives.
> 2. **Hardware Topology Dictates Algorithmic Viability:** Simulating non-native entangling circuits is a fallacy on NISQ chips. The transpilation SWAP penalty destroys any theoretical entanglement advantage.
> 3. **Kernel Methods Triumph over Parameterized Circuits:** Quantum Kernels eliminate variational optimization noise and barren plateaus entirely, representing the most viable path to near-term quantum utility."

---

### **Slide 22: Classical Crossover Boundaries & Deployment Rules**
> *[Slide text: Empirical Crossover Against Baselines: LR 82% threshold, Circular L=3 crosses at 2% T1, Linear L=3 crosses at 1% T1]*

**Spoken Script (Aman Singh):**
> "Slide 22 formalizes our **Classical Crossover Boundaries**:
> 
> Benchmarked against our primary classical ceiling—Logistic Regression at 82.00%:
> - Circular $L=3$ holds classical parity up to 5% depolarizing noise, but crosses below classical performance at **2.0% amplitude damping**.
> - Linear $L=3$ crosses below at **1.0% amplitude damping**.
> 
> We formulate three practical deployment rules for quantum practitioners:
> - **Rule 1:** When physical two-qubit gate error exceeds 2.5%, default to classical ML.
> - **Rule 2:** Always match ansatz connectivity to the hardware coupling graph (use Linear on linear QPUs).
> - **Rule 3:** Implement Readout Error Mitigation by default—it is free of circuit depth penalties."

---

### **Slide 23: Limitations and Future Work**
> *[Slide text: 4 cards: 4-Qubit Scale (60% variance), Simulation vs Hardware Drift, Classical Tuning Disclosure, Hybrid Quantum Transfer Learning]*

**Spoken Script (Aman Singh):**
> "Slide 23 presents our transparent academic disclosures and future roadmap:
> 
> - **Dimensionality Scale:** Compressing 784-pixel chest X-rays to 4 PCA components captured 60.04% of dataset variance. To transcend this, our future work will implement **Quantum Convolutional Neural Networks (QCNN)** for native quantum feature reduction.
> - **Multi-Hour Queue Drift:** While our IBM calibration snapshots faithfully emulate device physics, real cloud QPU execution suffers from calibration drift during multi-hour job queues.
> - **Hybrid Quantum Transfer Learning:** Our next milestone combines a pre-trained classical **ResNet-18 backbone** to extract high-dimensional clinical embeddings, feeding directly into a calibrated 4-qubit quantum classifier head."

---

### **Slides 24 & 25: References & Conclusion**
> *[Slide text: 16 Core IEEE Citations: Preskill, Farhi, Schuld, Havlíček, Yang, Pérez-Salinas, Temme, Kandala, McClean, Cerezo, IBM Calibration]*

**Spoken Script (Aman Singh):**
> "Slides 24 and 25 list our key literature references, including seminal works by John Preskill on NISQ theory, Maria Schuld on Quantum Hilbert Spaces, Havlíček on Quantum Kernels, and official IBM Quantum calibration documentation.
> 
> All our codebase, pre-trained weights, hardware emulation suite, and interactive verification dashboards are open-source and publicly accessible on GitHub.
> 
> We express our heartfelt gratitude to our guide, **Dr. Kapil Kumar Soni Sir**, for his invaluable guidance, insights, and continuous encouragement throughout this project.
> 
> Thank you very much for your time and attention. We are now open to your questions and feedback."

---

## **Part 3: Master Q&A Defense Guide (Top 6 Panel Questions)**

---

### **Question 1: "Why did Circular Entanglement perform well in clean simulation but completely collapse on the IBM hardware benchmark?"**
* **Who Answers:** Aman Singh
* **Spoken Response:**
  > "Thank you, Sir, that is a central finding of our work. In unconstrained software simulators, qubits have virtual all-to-all connectivity. In that setting, Circular entanglement achieves 84.6% accuracy because the closed loop allows two-way correlation between Qubit 3 and Qubit 0.
  > 
  > However, physical superconducting chips like IBM Eagle, Perth, and Manila have a **linear coupling graph** ($Q_0 - Q_1 - Q_2 - Q_3$). There is no physical bus connecting $Q_3$ to $Q_0$.
  > 
  > When we transpile Circular entanglement to the physical device, the compiler must insert **4 SWAP gates** to route quantum information from $Q_3$ back to $Q_0$. Since each SWAP gate decomposes into 3 physical CNOTs, that adds **12 extra CNOTs per layer**, exploding circuit depth to 32 CNOTs total.
  > 
  > Because physical two-qubit CNOT gates have an error rate of $\sim 10^{-2}$, accumulated gate infidelity and $T_1$ decay completely depolarize the state, dropping Circular accuracy to $51\% \sim 52\%$. In contrast, Linear topology requires **0 SWAP gates** (6 CNOTs) and sustains 77% to 78% accuracy on real hardware."

---

### **Question 2: "Can you explain mathematically why Depolarizing noise does not flip classification predictions?"**
* **Who Answers:** Aditya Soni
* **Spoken Response:**
  > "Certainly, Sir. An isotropic depolarizing channel with parameter $p$ maps a density matrix $\rho$ as:
  > $$\mathcal{E}(\rho) = (1 - p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)$$
  > 
  > Since the Pauli matrices anticommute and the Pauli-Z observable $Z_0$ is traceless, taking the expectation value yields:
  > $$\text{Tr}(\mathcal{E}(\rho) Z_0) = \left(1 - \frac{4p}{3}\right) \text{Tr}(\rho Z_0) = \left(1 - \frac{4p}{3}\right) \langle Z_0 \rangle_{\text{clean}}$$
  > 
  > For any physical noise rate $p \le 0.05$, the contraction factor $\left(1 - \frac{4p}{3}\right) \ge 0.933$, which is strictly positive.
  > 
  > In our classification rule, we predict Pneumonia when $\langle Z_0 \rangle \le 0$ and Normal when $\langle Z_0 \rangle > 0$. Multiplying $\langle Z_0 \rangle$ by a positive scalar contracts the output probability towards $0.5$, reducing confidence, but **never alters the mathematical sign**. Hence, the decision boundary remains invariant."

---

### **Question 3: "Why did clinical Recall collapse to 0.00% under Amplitude Damping ($T_1$), and why is that dangerous?"**
* **Who Answers:** Aditya Soni
* **Spoken Response:**
  > "Yes, Sir. Unlike depolarizing noise which is symmetric white noise, Amplitude Damping models thermal relaxation into the environment. Its primary Kraus operator is:
  > $$K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}$$
  > This operator non-unitarily maps the excited state $|1\rangle$ down to ground state $|0\rangle$.
  > 
  > In our clinical encoding, $|0\rangle$ corresponds to Class 0 ('Normal' healthy lung), and $|1\rangle$ corresponds to Class 1 ('Pneumonia'). As the thermal relaxation parameter $\gamma$ grows, the quantum state collapses towards $|0\rangle$ regardless of the input chest X-ray.
  > 
  > Consequently, the circuit outputs $\langle Z_0 \rangle \to +1$, which maps to $P(\text{Pneumonia}) \to 0$. The model predicts that every single patient is healthy, driving True Positives to zero and False Negatives to 100%. In medical triage, this would cause all pneumonia patients to be sent home without treatment, which is clinically fatal."

---

### **Question 4: "Why does Quantum Support Vector Classifier (QSVC) beat Parameterized VQC under thermal noise?"**
* **Who Answers:** Aman Singh
* **Spoken Response:**
  > "Great question, Sir. The key difference lies in **where the optimization takes place**.
  > 
  > In a Parameterized VQC, both the forward quantum circuit and the gradient computation (via the Parameter-Shift Rule) are executed on the noisy quantum processor. Noise distorts the cost landscape, flattens gradients, and induces **noise-induced barren plateaus**.
  > 
  > In QSVC, the quantum processor is only used as an **inner-product evaluation engine** to compute the kernel Gram matrix $K_{ij} = |\langle \psi(x_i) | \psi(x_j) \rangle|^2$. Once that matrix is evaluated, the support vectors and decision boundary are computed using a **classical quadratic programming solver** on a standard CPU.
  > 
  > Because the classical solver optimizes a globally convex dual objective, it has no local minima and no barren plateaus. Even if the Gram matrix elements are slightly degraded by noise, the classical convex solver finds the optimal robust separating hyperplane, maintaining 82% accuracy."

---

### **Question 5: "How does Readout Error Mitigation (REM) work without adding circuit depth?"**
* **Who Answers:** Aman Singh
* **Spoken Response:**
  > "Sir, on physical quantum hardware, state measurement is asymmetric: preparing a $|0\rangle$ state might be misclassified as $|1\rangle$ with probability $p_{01}$, and $|1\rangle$ misclassified as $|0\rangle$ with probability $p_{10}$.
  > 
  > Prior to running the clinical circuits, we calibrate the detector by preparing known basis states $|0\rangle$ and $|1\rangle$ and recording measurement counts. This yields the detector confusion matrix:
  > $$M = \begin{pmatrix} 1 - p_{01} & p_{10} \\ p_{01} & 1 - p_{10} \end{pmatrix}$$
  > 
  > When we execute the diagnostic circuits, we observe a noisy probability vector $\vec{P}_{\text{noisy}} = M \vec{P}_{\text{ideal}}$.
  > 
  > To recover the true state, we simply invert this $2 \times 2$ matrix classically on the computer:
  > $$\vec{P}_{\text{mitigated}} = M^{-1} \vec{P}_{\text{noisy}}$$
  > This operation is executed entirely in classical post-processing after measurement. It requires zero additional gates or circuit depth on the quantum chip."

---

### **Question 6: "What is your sample standard deviation protocol and why did you use $\text{ddof}=1$?"**
* **Who Answers:** Aditya Soni
* **Spoken Response:**
  > "Sir, in many applied machine learning papers, authors mistakenly use population standard deviation ($N$ in the denominator) across a small number of seeds, which underestimates variance by 10% to 20%.
  > 
  > Because we trained across $N=5$ independent seeds, Bessel's correction is mathematically necessary to provide an unbiased estimator of true population variance. We therefore strictly calculated:
  > $$s = \sqrt{\frac{1}{N-1} \sum_{i=1}^N (x_i - \bar{x})^2}$$
  > Every table, confidence interval, and crossover boundary in our presentation and report uses $s$ with $\text{ddof}=1$, ensuring our reported spreads are scientifically defensible."
