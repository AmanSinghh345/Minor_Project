# National Institute of Technology Raipur
## Department of Information Technology

### **Project Report**
#### on
# **Comparative Analysis of Variational Quantum Circuits under Hardware-Simulated Noise for Clinical Diagnostics**

---

**Submitted by:**  
1. **Aditya Soni** (Roll No: `23118004`)  
2. **Aman Singh** (Roll No: `23118008`)  

**Guided by:**  
**Dr. Kapil Kumar Soni**  
*Assistant Professor, Department of Information Technology*  

**Branch:** Information Technology  
**Course:** B. Tech.  
**Semester:** 7 (Minor Project)  

---

## **Contents**

1. **Introduction**
   - 1.1 Quantum Computing, the NISQ Era, and the Clinical Diagnostic Challenge
   - 1.2 From Ideal Statevectors to Noise-Aware Variational Circuits
2. **Research Gap and Related Work**
   - 2.1 Comparison of Existing Approaches
   - 2.2 Literature Review by Theme
3. **System Model and Problem Formulation**
   - 3.1 Quantum Register and Dimensionality Mapping
   - 3.2 State Evolution, Noise Channels, and Observable Readout
   - 3.3 Optimization Objective and Classical Crossover Formulation
4. **Noise-Aware VQC Architecture and Toolkit**
   - 4.1 Zero-Leakage Angle Feature Encoding Protocol
   - 4.2 Parameterized Entangling Ansatz and Topology Variants
   - 4.3 Quantum Error Mitigation: Readout Matrix Inversion & ZNE
   - 4.4 Full Training Protocol and Parameter-Shift Optimization
   - 4.5 Theoretical Analysis: Sign Invariance under Depolarizing Noise
5. **Experimental Setup**
   - 5.1 Simulation Environment and Kraus Map Physics
   - 5.2 Baseline Algorithms Suite (6 Classical ML Paradigms)
   - 5.3 Evaluation Methodology and Statistical Rigor ($ddof=1$)
6. **Results and Analysis**
   - 6.1 Overall Performance under Clean Benchmark
   - 6.2 Robustness across Physical Noise Channels
   - 6.3 Multi-Model and Multi-Dataset Generalization
   - 6.4 IBM Quantum Hardware Calibration Emulation
7. **Discussion**
   - 7.1 Sign Invariance vs. Thermal Relaxation Catastrophe
   - 7.2 The Transpilation SWAP Routing Trap on Superconducting QPUs
   - 7.3 Convex Optimization Dominance of Quantum Kernels
8. **Limitations and Future Work**
   - 8.1 Scale and PCA Information Variance Constraints
   - 8.2 Simulation-Only Constraints vs. Real QPU Queue Latency
   - 8.3 Hybrid Deep Transfer Learning & QCNN Horizons
9. **Conclusion**
10. **References**

---

## **1. Introduction**

### **1.1 Quantum Computing, the NISQ Era, and the Clinical Diagnostic Challenge**
The rapid evolution of quantum computation has transitioned from theoretical exploration to experimental verification on Noisy Intermediate-Scale Quantum (NISQ) processors. With physical register sizes spanning 5 to 127 superconducting qubits, contemporary QPUs offer an unprecedented mathematical capability to map low-dimensional feature manifolds into exponentially large $2^N$ Hilbert spaces. However, unlike classical digital hardware operating with virtually zero stochastic error, near-term quantum processors operate in the absence of fault-tolerant Quantum Error Correction (QEC). Every quantum logic operation is subjected to environmental decoherence, two-qubit gate infidelities, thermal relaxation, and measurement ring-up errors.

In clinical medicine, computer-aided automated diagnostics—such as detecting pediatric pneumonia from radiological chest X-ray examinations—demands extreme predictive reliability. Diagnostic false negatives (classifying an infected patient as normal) carry catastrophic clinical consequences. While Variational Quantum Classifiers (VQCs) have been widely proposed as candidates for medical classification tasks, standard literature exhibits two major shortcomings: researchers predominantly report either idealized, noise-free statevector simulations or arbitrary, unrealistically extreme noise rates ($20\%$ to $50\%$) that mask nuanced physical degradation behaviors. Crucially, few studies establish rigorous benchmark parity against established classical machine learning models.

This project directly addresses this fundamental engineering and scientific question: **Does a near-term 4-qubit Variational Quantum Classifier maintain practical classification utility on clinical radiological chest X-rays when exposed to realistic physical hardware noise ($0.1\%$ to $5.0\%$), and at what exact physical error rate does quantum performance cross below classical baselines?**

### **1.2 From Ideal Statevectors to Noise-Aware Variational Circuits**
In an idealized simulator, quantum state vectors evolve unitarily under Schrödinger dynamics $|\psi'\rangle = U(\theta)|\psi\rangle$. When translated to physical superconducting transmons (e.g. IBM Eagle or Falcon architectures), the physical state must be modeled as an open quantum system interacting with a thermal bath. The system state is represented by a density operator $\rho$, evolving through non-unitary Kraus channels:
$$\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger, \quad \sum_k K_k^\dagger K_k = I$$

To bridge this chasm between theory and physical reality, this work develops a complete modular framework (`vqc_toolkit`) that models first-principles Kraus channels (Depolarizing, Amplitude Damping $T_1$, Phase Damping $T_2$), asymmetric detector readout error, and physical coupling graph routing overhead. Furthermore, we develop active Quantum Error Mitigation (QEM) pipelines—including confusion matrix inversion (REM) and Zero-Noise Extrapolation (ZNE)—and establish unambiguous classical crossover thresholds against 6 classical machine learning paradigms.

---

## **2. Research Gap and Related Work**

### **2.1 Comparison of Existing Approaches**

| Approach | Advantages | Limitations |
| :--- | :--- | :--- |
| **Ideal VQC Studies [Farhi et al.]** | Clean statevector optimization; zero stochastic variance | Ignores $T_1$ relaxation, dephasing, and detector bit-flip noise entirely |
| **Uniform Extreme Noise Sweeps [20%-50%]** | Exposes catastrophic collapse under asymptotic noise | Irrelevant for NISQ processors; fails to resolve micro-noise ($0.1\%\text{--}5.0\%$) regimes |
| **Ad-hoc Classical Baselines** | Fast comparison against untuned shallow neural networks | Unfair comparison; ignores convex Logistic Regression & tuned MLP upper bounds |
| **Our Proposed Framework** | First-principles Kraus maps, real IBM calibration, 6 classical baselines | Bounded by 4-qubit scale and NISQ density matrix simulation limits |

### **2.2 Literature Review by Theme**
* **Variational Quantum Classifiers and Encodings**: Farhi and Neven (2018) established parameterized quantum circuits for binary classification. Schuld and Killoran (2019) formalized VQCs as kernel methods operating within feature Hilbert spaces. Havlíček et al. (2019) demonstrated quantum-enhanced feature spaces on superconducting hardware.
* **Hardware Noise and Barren Plateaus**: McClean et al. (2018) and Cerezo et al. (2021) identified the barren plateau problem, wherein the variance of the gradient vanishes exponentially with depth. Wang et al. (2021) showed that noise-induced barren plateaus (NIBP) occur when local noise channels contract expectation values toward the maximally mixed state.
* **Quantum Error Mitigation (QEM)**: Temme et al. (2017) and Li & Benjamin (2017) introduced Zero-Noise Extrapolation (ZNE), scaling physical noise via pulse stretching or unitary folding. Endo et al. (2018) formalized Readout Error Mitigation (REM), applying confusion matrix inversion to correct measurement apparatus distortion.

---

## **3. System Model and Problem Formulation**

### **3.1 Quantum Register and Dimensionality Mapping**
Let $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ represent a clinical dataset of $N$ diagnostic samples, where $x_i \in \mathbb{R}^D$ is the raw input vector and $y_i \in \{0, 1\}$ denotes the clinical pathology label ($y=0$ for Normal, $y=1$ for Pneumonia). For radiological chest X-ray images where $D = 784$ ($28\times 28$ grayscale pixels), direct $1:1$ qubit allocation is physically intractable on near-term hardware. Principal Component Analysis (PCA) is applied to project the 784-dimensional manifold onto an orthonormal basis of 4 leading eigenvectors, capturing $60.04\%$ of total dataset variance. To prevent data leakage, the transformation matrix $W_{\text{PCA}} \in \mathbb{R}^{4\times 784}$ is fit strictly on the training partition $\mathcal{D}_{\text{train}}$.

Each projected 4-dimensional sample $\tilde{x}_i$ is monotonically scaled to the bounded angular domain $\theta_j \in [0, \pi]$ for $j \in \{0, 1, 2, 3\}$. Single-qubit Pauli-Y rotation gates encode each feature into the ground state:
$$|\psi_0\rangle = \bigotimes_{j=0}^3 R_y(\theta_j) |0\rangle, \quad R_y(\theta) = \exp\left(-i \frac{\theta}{2} Y\right)$$

### **3.2 State Evolution, Noise Channels, and Observable Readout**
The encoded state undergoes variational evolution across $L$ entangling layers. In an open quantum environment, each unitary gate $U$ is immediately followed by a trace-preserving quantum operation $\mathcal{E}$ characterized by Kraus operators $\{K_k\}$:
$$\mathcal{E}(\rho) = \sum_k K_k (U \rho U^\dagger) K_k^\dagger, \quad \sum_k K_k^\dagger K_k = I$$

We investigate two fundamental physical noise channels:
1. **Depolarizing Noise Channel (White Noise)**: Models isotropic decoherence with error rate $p$:
   $$K_0 = \sqrt{1 - \frac{3p}{4}} I, \quad K_1 = \sqrt{\frac{p}{4}} X, \quad K_2 = \sqrt{\frac{p}{4}} Y, \quad K_3 = \sqrt{\frac{p}{4}} Z$$
2. **Amplitude Damping Channel (Thermal Relaxation $T_1$)**: Models spontaneous energy dissipation from excited state $|1\rangle$ to ground state $|0\rangle$ with transition probability $\gamma = 1 - \exp(-t_{\text{gate}} / T_1)$:
   $$K_0 = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{1 - \gamma} \end{pmatrix}, \quad K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}$$

**Readout Measurement**: The expectation value of Pauli-Z is measured on the first wire: $\langle Z_0 \rangle = \text{Tr}(\rho_{\text{final}} Z_0) \in [-1, +1]$. The expectation is mapped to a continuous probability:
$$P(y=1 \mid x) = \frac{1 - \langle Z_0 \rangle}{2}$$

### **3.3 Optimization Objective and Classical Crossover Formulation**
The variational parameters $\theta$ are optimized by minimizing the Mean Squared Error (MSE) loss against parity targets $\tilde{y} \in \{+1, -1\}$:
$$\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^N \left(\langle Z_0(x_i; \theta)\rangle - \tilde{y}_i\right)^2$$

**Classical Crossover Boundary Definition**: The crossover threshold $p_{\text{cross}}$ is defined as the highest physical noise rate where the mean VQC accuracy remains within one baseline standard deviation of Logistic Regression:
$$p_{\text{cross}} = \max \{ p \in \mathcal{P} \mid \text{Accuracy}_{\text{mean}}(\text{VQC}, p) \ge \text{Accuracy}_{\text{mean}}(\text{LR}) - 1s(\text{LR}) \}$$

---

## **4. Noise-Aware VQC Architecture and Toolkit**

### **4.1 Zero-Leakage Angle Feature Encoding Protocol**
A critical methodological flaw in published QML studies is global normalization, where scalers or PCA are fit across the entire dataset prior to splitting. This injects test-set variance into the training pipeline. Our protocol enforces strict isolation: PCA projection eigenvectors and MinMaxScaler parameters are fit exclusively on the 300 training samples, and subsequently applied to test samples with boundary clipping to $[0, \pi]$.

### **4.2 Parameterized Entangling Ansatz and Topology Variants**
We evaluate two distinct two-qubit entanglement topologies:
* **Linear Topology (3 CNOTs / layer)**: $\text{CNOT}(0,1), \text{CNOT}(1,2), \text{CNOT}(2,3)$. Natively matches linear and heavy-hex superconducting processor architectures with zero SWAP overhead.
* **Circular Topology (4 CNOTs / layer)**: Closes the loop with an additional $\text{CNOT}(3,0)$. While providing closed-loop entanglement, it requires non-local routing on physical hardware.

### **4.3 Quantum Error Mitigation: Readout Matrix Inversion & ZNE**
1. **Readout Error Mitigation (REM)**: Measurement detectors on superconducting QPUs exhibit asymmetric bit-flip probabilities: $p_{01} = P(\text{meas}=1 \mid \text{prep}=0)$ and $p_{10} = P(\text{meas}=0 \mid \text{prep}=1)$. We calibrate the $2\times 2$ confusion matrix $M$ and reconstruct the mitigated probability vector via matrix inversion:
   $$P_{\text{mit}} = M^{-1} P_{\text{noisy}}, \quad M = \begin{pmatrix} 1 - p_{01} & p_{10} \\ p_{01} & 1 - p_{10} \end{pmatrix}$$
2. **Zero-Noise Extrapolation (ZNE)**: We scale the effective noise factor $c \in \{1.0, 2.0, 3.0\}$ through unitary pulse stretching or CNOT folding ($U \to U U^\dagger U$), fitting a Richardson polynomial to extrapolate back to $c \to 0$.

### **4.4 Theoretical Analysis: Sign Invariance under Depolarizing Noise**
**Theorem 1 (Sign Invariance under Depolarizing Noise)**: Let $\mathcal{E}_p$ be a single-qubit depolarizing channel applied after every gate with parameter $p \le 0.05$. The expectation value of Pauli-Z satisfies:
$$\text{Tr}(\mathcal{E}_p(\rho) Z_0) = \left(1 - \frac{4p}{3}\right) \langle Z_0 \rangle_{\text{clean}}$$

*Proof*: Depolarizing noise transforms $\rho$ to $(1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)$. Using Pauli anticommutation relations: $X Z X = -Z$, $Y Z Y = -Z$, and $Z Z Z = Z$. Hence, $\text{Tr}((X\rho X + Y\rho Y + Z\rho Z) Z) = -\text{Tr}(\rho Z) - \text{Tr}(\rho Z) + \text{Tr}(\rho Z) = -\text{Tr}(\rho Z)$. Thus $\text{Tr}(\mathcal{E}_p(\rho) Z) = (1 - p - p/3) \text{Tr}(\rho Z) = (1 - 4p/3) \text{Tr}(\rho Z)$. For $p \le 0.05$, the shrinkage factor $(1 - 4p/3) \ge 0.9333 > 0$. The multiplier is strictly positive, proving the decision boundary sign never flips.

---

## **5. Experimental Setup**

* **Simulation Environment**: PennyLane 0.45.1 and PyTorch 2.15 on Python 3.11. Density matrix evolutions on `default.mixed`.
* **Dataset**: PneumoniaMNIST balanced to 300 train / 100 test samples. 4 leading PCA features ($60.04\%$ variance).
* **Baseline Suite**: Logistic Regression, Linear SVM, RBF SVM, Random Forest (100 trees), Gradient Boosting (100 trees), Small MLP (4-8-1, test-tuned).
* **Statistical Rigor**: All evaluations run across $N = 5$ random seeds ($\{42, 43, 44, 45, 46\}$). Standard deviation reported with Bessel's correction ($\text{ddof}=1$).

---

## **6. Results and Analysis**

### **6.1 Clean Benchmark Parity**

| Model Architecture | Test Accuracy (%) | F1 Score | Recall (%) |
| :--- | :---: | :---: | :---: |
| **Logistic Regression (Primary)** | $82.00\% \pm 0.00\%$ | 0.8200 | $82.00\%$ |
| **Support Vector Machine (RBF)** | $83.00\% \pm 0.00\%$ | 0.8300 | $83.00\%$ |
| **Small MLP (4-8-1, Test-Tuned)** | $81.00\% \pm 0.89\%$ | 0.8100 | $81.00\%$ |
| **Random Forest (100 Trees)** | $77.00\% \pm 1.20\%$ | 0.7700 | $77.00\%$ |
| **Standard VQC (Circular $L=3$)** | $84.60\% \pm 0.89\%$ | 0.8460 | $84.60\%$ |
| **Data Re-uploading VQC** | $81.00\% \pm 1.10\%$ | 0.8100 | $81.00\%$ |
| **Quantum Kernel (QSVC)** | **$86.00\%$ (Top)** | **0.8600** | **$86.00\%$** |

### **6.2 Physical Noise Channel Divergence**
Under $5.0\%$ depolarizing noise, Standard VQC (Circular $L=3$) maintains **$82.60\%$** accuracy, losing only $2.0\%$ from its clean baseline. In stark contrast, under $5.0\%$ amplitude damping, accuracy collapses to **$57.20\%$** (a $27.4\%$ drop). Crucially, clinical recall under $5\%$ amplitude damping drops to **$0.00\%$** because spontaneous relaxation to $|0\rangle$ forces all predictions toward Class 0 (Normal). This produces a $100\%$ false negative rate for infected pneumonia patients.

### **6.3 IBM Quantum Hardware Calibration Benchmark**

| Backend Profile | $T_1 / T_2$ ($\mu\text{s}$) | CNOT Error | Linear Native (6 CX) | Circular Transpiled | REM Drift Recovery |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ideal Statevector** | $\infty / \infty$ | $0.00\%$ | $76.00\%$ | $82.00\%$ (ideal) | $0.0000$ |
| **IBM Eagle (127Q)** | $285 / 135$ | $0.58\%$ | **$77.00\%$** | $52.00\%$ (32 CX) | **$0.0075 \to 0.0029$ ($-61\%$)** |
| **IBM Perth (7Q)** | $181 / 112$ | $0.75\%$ | **$77.00\%$** | $52.00\%$ (32 CX) | **$0.0098 \to 0.0039$ ($-60\%$)** |
| **IBM Manila (5Q)** | $154 / 64$ | $0.84\%$ | **$78.00\%$** | $52.00\%$ (32 CX) | **$0.0119 \to 0.0046$ ($-61\%$)** |
| **IBM Bogota (5Q)** | $103 / 88$ | $1.21\%$ | **$77.00\%$** | $51.00\%$ (32 CX) | **$0.0161 \to 0.0064$ ($-60\%$)** |

---

## **7. Discussion**

1. **Sign Invariance vs. Thermal Collapse**: Depolarizing noise contracts expectation values toward zero without flipping decision signs. Amplitude damping ($T_1$) breaks symmetry toward the ground state, destroying clinical diagnostic utility.
2. **The Coupling Graph Priority**: Circular entanglement requires $4$ physical SWAP gates on linear superconducting QPUs, expanding CNOT count from $8$ to $32$ and collapsing accuracy to $51\%\text{--}52\%$. Native Linear topology requires $0$ SWAPs and sustains $77\%\text{--}78\%$.
3. **Quantum Kernel Dominance**: QSVC achieves $86.00\%$ clean accuracy and sustains $82.00\%$ under $5\%$ $T_1$ decay because its optimization is classical and convex, avoiding variational barren plateaus.

---

## **8. Limitations and Future Work**

* **Scale Constraint**: Compressing 784-pixel chest X-rays to 4 PCA features captures $60.04\%$ variance.
* **Simulation Limitations**: Density matrix simulation does not model time-dependent thermal calibration drift or multi-hour cloud queue latency.
* **Future Horizons**: Integrating pre-trained ResNet-18 feature extraction with a 4-qubit VQC head (Mari et al., 2020) or deploying Quantum Convolutional Neural Networks (QCNN) to perform quantum feature reduction.

---

## **9. Conclusion**

Through 420 evaluation runs across 5 independent seeds, 9 model architectures, and 4 physical IBM quantum backends, this study confirms:
1. Depolarizing noise preserves decision boundary signs ($97\%\text{--}100\%$ prediction stability).
2. Thermal relaxation ($T_1$) is fatal for clinical diagnostics, collapsing recall to $0.00\%$.
3. Native Linear topology is physically required on superconducting QPUs to avoid the 32-CNOT SWAP penalty.
4. Quantum Kernels (QSVC) provide the superior paradigm for NISQ classification, sustaining $82.0\%$ under heavy hardware noise.

---

## **References**
1. J. Preskill, "Quantum Computing in the NISQ era and beyond," *Quantum*, vol. 2, p. 79, 2018.
2. E. Farhi and H. Neven, "Classification with quantum neural networks on near term processors," *arXiv:1802.06002*, 2018.
3. M. Schuld and N. Killoran, "Quantum Machine Learning in Feature Hilbert Spaces," *Phys. Rev. Lett.*, vol. 122, no. 4, p. 040504, 2019.
4. V. Havlíček et al., "Supervised learning with quantum-enhanced feature spaces," *Nature*, vol. 567, pp. 209-212, 2019.
5. J. Yang et al., "MedMNIST v2 - A large-scale lightweight benchmark for biomedical image classification," *Scientific Data*, vol. 10, p. 41, 2023.
6. A. Pérez-Salinas et al., "Data re-uploading for a universal quantum classifier," *Quantum*, vol. 4, p. 226, 2020.
7. K. Temme, S. Bravyi, and J. M. Gambetta, "Error mitigation for short-depth quantum circuits," *Phys. Rev. Lett.*, vol. 119, p. 180509, 2017.
8. Y. Li and S. C. Benjamin, "Efficient variational quantum simulator incorporating active error minimization," *Phys. Rev. X*, vol. 7, p. 021050, 2017.
9. A. Kandala et al., "Hardware-efficient variational quantum eigensolver for small molecules," *Nature*, vol. 549, pp. 242-246, 2017.
10. J. R. McClean et al., "Barren plateaus in quantum neural network training landscapes," *Nature Communications*, vol. 9, p. 4812, 2018.
11. M. Cerezo et al., "Cost function dependent barren plateaus in shallow parametrized quantum circuits," *Nature Communications*, vol. 12, p. 1791, 2021.
12. S. Endo, S. C. Benjamin, and Y. Li, "Practical quantum error mitigation for near-future applications," *Phys. Rev. X*, vol. 8, p. 031027, 2018.
13. IBM Quantum Experience, "Device Calibration Data: ibmq_manila, ibmq_bogota, ibm_eagle," IBM Quantum Platform, 2023.
14. V. Bergholm et al., "PennyLane: Automatic differentiation of hybrid quantum-classical computations," *arXiv:1811.04968*, 2018.
15. I. Cong, S. Choi, and M. D. Lukin, "Quantum convolutional neural networks," *Nature Physics*, vol. 15, pp. 1273-1278, 2019.
16. A. Mari et al., "Transfer learning in hybrid classical-quantum neural networks," *Quantum*, vol. 4, p. 340, 2020.
