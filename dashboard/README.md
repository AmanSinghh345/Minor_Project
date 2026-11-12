# VQC Noise Presentation Dashboard

A standalone, projector-friendly React viewer for benchmarking Variational Quantum Classifiers (VQCs) under hardware-simulated noise on PneumoniaMNIST.

### Quick Start

```bash
cd dashboard
npm install
npm run dev
```

Open [http://localhost:5174](http://localhost:5174) in your browser.

### Features
1. **Interactive Sidebar Controls**:
   - Noise Channel: Depolarizing (white noise) vs. Amplitude Damping (T1 relaxation).
   - Gate Noise Rate: 0.0%, 0.1%, 0.2%, 0.5%, 1.0%, 2.0%, 5.0%.
   - Layers: Depth L = 1, 2, 3.
   - Entanglement Scheme: Circular (4 CNOTs/L) vs. Linear (3 CNOTs/L).
2. **Metric Cards**:
   - VQC Accuracy, Precision, Recall, F1 (mean ± sample std, ddof=1).
   - Logistic Regression primary baseline comparison.
   - Small MLP 4-8-1 secondary baseline comparison.
3. **Accuracy vs. Noise Rate Chart**:
   - Shaded ±1s standard deviation error bands.
   - Horizontal reference lines for classical baselines.
   - Vertical marker for the currently selected noise level.
4. **Try an Image (12 Test Cases)**:
   - Real chest X-ray scans (6 Normal, 6 Pneumonia).
   - Real VQC expectation value $\langle Z \rangle$ and probability of pneumonia.
   - Direct side-by-side comparison with Logistic Regression and Small MLP predictions.
5. **About & Methodology**:
   - Project research question.
   - Full hybrid quantum-classical pipeline diagram.
   - Honest scientific disclosures and limitations.

*Note: Pure client-side viewer. No Python backend required at runtime.*
