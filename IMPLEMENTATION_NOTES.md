# IMPLEMENTATION_NOTES.md - Original Implementation vs. Library Dependencies

To ensure academic transparency and prepare for a rigorous viva examination, this document delineates between code and mathematical formulations authored directly in this project versus standard utility functions provided by external libraries.

---

## Detailed Breakdown Table

| Component | What I Implemented Myself | Library Provided Utility | Library Used |
| :--- | :--- | :--- | :--- |
| **Data Pipeline (`data.py`)** | • Balanced class subsampling logic using NumPy seed generators<br>• Custom feature flattening and normalization pipeline<br>• Scaler pipeline bounding features strictly to $[0, \pi]$ for $R_y$ angle rotations<br>• Leakage prevention architecture (fitting PCA and Scaler strictly on train split) | • Raw PneumoniaMNIST dataset download and storage<br>• Low-level SVD decomposition for PCA (`PCA.fit_transform`)<br>• Bounding transforms (`MinMaxScaler`) | `medmnist`, `scikit-learn`, `numpy` |
| **Classical Baselines (`baseline.py`)** | • `LogisticRegressionPyTorch` network module<br>• `SmallMLPPyTorch` (4-8-1) non-linear neural network module<br>• Full training loop with gradient descent, loss backpropagation, and metric calculation<br>• Multi-seed evaluation harness | • PyTorch `nn.Module`, `nn.Linear`, `nn.ReLU`<br>• Autograd engine (`loss.backward()`)<br>• Adam optimizer (`torch.optim.Adam`)<br>• Evaluation metric calculations (`accuracy_score`, `f1_score`, etc.) | `torch`, `scikit-learn` |
| **Variational Quantum Classifier (`model.py` - Stage 2)** | • Custom parameterized quantum circuit architecture in PennyLane<br>• Angle encoding layer for $N=4$ qubits<br>• Layered variational ansatz with configurable layer depth ($L \in \{1, 2, 3\}$)<br>• Configurable CNOT entanglement topologies (linear vs. circular)<br>• PauliZ expectation value extraction on qubit 0 and mapping to binary prediction probabilities | • Quantum device simulator (`default.qubit`)<br>• PennyLane QNode decorator (`qml.qnode`)<br>• Quantum gate primitives (`qml.RY`, `qml.CNOT`, `qml.expval`, `qml.PauliZ`) | `pennylane`, `torch` |
| **Noise Channels & Verification (`noise.py` - Stage 3)** | • **Hand-written Kraus operators** in NumPy from first-principles density matrix physics for Depolarizing and Amplitude Damping channels<br>• Explicit Kraus map verification routine: $\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$<br>• Completeness verification test ($\sum_k K_k^\dagger K_k = I$)<br>• Direct fidelity comparison asserting numerical equivalence with PennyLane's built-in operators on pure and mixed test states<br>• Gate-level noise injection pipeline applying channels after every gate across all qubits | • Mixed state simulator (`default.mixed`)<br>• Reference built-in channel primitives (`qml.DepolarizingChannel`, `qml.AmplitudeDamping`) | `numpy`, `pennylane` |
| **Experiment Sweep (`run_experiments.py` - Stage 4)** | • Automated experiment matrix orchestrating 5 seeds $\times$ 2 noise types $\times$ 7 noise rates $\times$ 3 layer depths $\times$ 2 topologies ($= 420$ evaluation runs)<br>• Cached QNode management on `default.mixed` to eliminate redundant compilation overhead<br>• Checkpoint saving/loading (.pt) and incremental CSV persistence with auto-resumption<br>• Real-time progress and ETA tracking | • Standard Python I/O and CSV formatting | `pandas`, `numpy`, `time` |
| **Plotting & Crossover (`plot.py` - Stage 5)** | • Custom crossover rate interpolation algorithm (locating the exact physical noise rate where noisy VQC intersects classical baseline)<br>• Comparative degradation curves with $\pm 1\sigma$ error bands<br>• Depth ablation and topology ablation visualizations<br>• Automated markdown summary report generation | • Matplotlib 2D plotting engine (`plt.subplots`, `plt.errorbar`)<br>• Scientific interpolation (`numpy.interp` / piecewise linear) | `matplotlib`, `numpy` |
| **Demo Notebook & Docs (`demo.ipynb`, README - Stage 6)** | • Interactive end-to-end inference verification comparing clean ($0\%$) vs. noisy ($1\%$) performance without re-training<br>• Comprehensive viva defense guide covering 15 rigorous academic questions and answers | • Jupyter notebook kernel execution environment | `jupyter` |

---

## Summary of Verification Checks

1. **Completeness Relation**:
   $$\sum_{k} K_k^\dagger K_k = I_{2 \times 2} \quad (\text{Residual Norm} < 10^{-15})$$
2. **Trace Preservation**:
   $$\text{Tr}(\mathcal{E}(\rho)) = 1.000000 \quad (\text{Absolute Deviation} < 10^{-14})$$
3. **PennyLane Numerical Parity**:
   $$\max |\rho_{\text{hand-written}} - \rho_{\text{pennylane}}| < 10^{-14}$$
   Verified across ground state $|0\rangle\langle0|$, excited state $|1\rangle\langle1|$, superposition state $|+\rangle\langle+|$, and mixed density matrix $0.7|0\rangle\langle0| + 0.3|1\rangle\langle1|$.
