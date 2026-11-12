"""
generate_senior_style_ppt.py
Generates a 25-slide professional presentation matching the Senior's PPT style:
- Deep Prussian Blue right accent panel (#0E3952)
- Ice Blue/Slate Light canvas (#EDF2F7 / #F8FAFC)
- 5-dot design accent on content slides
- Elegant serif/sans-serif headers and clean card layouts
- Real project data, tables, mathematical formulations, and embedded figures
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette Constants (Exact match to Senior's PPT)
# -----------------------------------------------------------------------------
COLOR_BG_LIGHT = RGBColor(237, 242, 247)       # #EDF2F7 Soft slate light canvas
COLOR_NAVY_BAR = RGBColor(14, 57, 82)          # #0E3952 Senior's deep navy vertical bar
COLOR_TITLE_SERIF = RGBColor(14, 57, 82)       # #0E3952 Header serif title
COLOR_CARD_BG = RGBColor(255, 255, 255)        # Pure white card
COLOR_CARD_BORDER = RGBColor(203, 213, 225)    # Subtle grey border
COLOR_TEXT_DARK = RGBColor(30, 41, 59)         # #1E293B Dark charcoal body
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)       # #475569 Slate grey
COLOR_ACCENT_BLUE = RGBColor(29, 78, 216)      # #1D4ED8 Vibrant tech blue
COLOR_TABLE_HDR = RGBColor(219, 234, 254)      # #DBEAFE Soft periwinkle table header
COLOR_TABLE_LINE = RGBColor(191, 219, 254)     # #BFDBFE Table border line
COLOR_DARK_BOX = RGBColor(17, 24, 39)          # #111827 Dark code block background
COLOR_DOT_BLUE = RGBColor(14, 57, 82)          # 5-dot accent


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_base_template(slide, title_text):
        """Adds senior's exact background: light canvas + dark navy right bar + 5 dots + title"""
        # 1. Light background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_LIGHT
        bg.line.fill.background()

        # 2. Right Navy Accent Bar (~22% width)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.4), Inches(0), Inches(2.933), Inches(7.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_NAVY_BAR
        bar.line.fill.background()

        # 3. 5-Dot Design Accent at bottom-left
        for i in range(5):
            dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8 + i * 0.25), Inches(6.8), Inches(0.14), Inches(0.14))
            dot.fill.solid()
            dot.fill.fore_color.rgb = COLOR_DOT_BLUE
            dot.line.fill.background()

        # 4. Slide Title (Large, Italicized Serif, exact match to Senior's PPT)
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(9.2), Inches(0.9))
        p = tb.text_frame.paragraphs[0]
        p.text = title_text
        p.font.name = "Georgia"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.italic = True
        p.font.color.rgb = COLOR_TITLE_SERIF

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(248, 250, 252)
    bg1.line.fill.background()

    # Abstract soft blue wave shape on right/bottom
    wave = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(3.2), Inches(5.5), Inches(5.0))
    wave.fill.solid()
    wave.fill.fore_color.rgb = RGBColor(219, 234, 254)
    wave.line.fill.background()

    # Blue accent bar under title
    div = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(6.5), Inches(0.12))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_NAVY_BAR
    div.line.fill.background()

    # Main Project Title
    tbox = slide1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(9.5), Inches(2.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "COMPARATIVE ANALYSIS OF\nVARIATIONAL QUANTUM CIRCUITS\nUNDER HARDWARE-SIMULATED NOISE"
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = tf.add_paragraph()
    p_sub.text = "FOR CLINICAL DIAGNOSTICS & CROSSOVER DEGRADATION"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(71, 85, 105)
    p_sub.space_before = Pt(8)

    # Guided By
    gbox = slide1.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(7.5), Inches(0.6))
    gp = gbox.text_frame.paragraphs[0]
    gp.text = "GUIDED BY: PROF. (DR.) SUDHAKAR PANDEY"
    gp.font.name = "Arial"
    gp.font.size = Pt(15)
    gp.font.bold = True
    gp.font.color.rgb = RGBColor(51, 65, 85)

    # Presented By
    pbox = slide1.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(8.5), Inches(1.2))
    ptf = pbox.text_frame
    pp1 = ptf.paragraphs[0]
    pp1.text = "Presented By:    Aman Singh\n                      Minor Project Group (Semester 7)"
    pp1.font.name = "Arial"
    pp1.font.size = Pt(14)
    pp1.font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_base_template(slide2, "INTRODUCTION")

    # Left prompt text
    left_tb = slide2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.0), Inches(4.5))
    ltf = left_tb.text_frame
    ltf.word_wrap = True
    lp1 = ltf.paragraphs[0]
    lp1.text = "Why Variational Quantum Circuits (VQCs)?"
    lp1.font.name = "Georgia"
    lp1.font.size = Pt(20)
    lp1.font.bold = True
    lp1.font.color.rgb = COLOR_NAVY_BAR

    lp2 = ltf.add_paragraph()
    lp2.text = "The emergence of Noisy Intermediate-Scale Quantum (NISQ) devices offers a theoretical paradigm for machine learning via high-dimensional Hilbert spaces. However, environmental decoherence and gate infidelities severely limit circuit depth."
    lp2.font.name = "Arial"
    lp2.font.size = Pt(13)
    lp2.font.color.rgb = COLOR_TEXT_MUTED
    lp2.space_before = Pt(12)

    # Right 3 Numbered Cards (01, 02, 03)
    cards_data = [
        ("01", "NISQ Hardware Constraints", "Near-term quantum processors lack full fault-tolerant error correction. Physical operations suffer from two-qubit CNOT errors, T1 thermal relaxation, and T2 dephasing."),
        ("02", "Clinical Diagnostic Mandate", "Medical image classification (PneumoniaMNIST) requires high sensitivity and recall. Understanding whether noise flips clinical decisions is vital for patient safety."),
        ("03", "Classical Crossover Boundary", "Rather than speculative quantum supremacy, practical engineering requires identifying the precise physical noise rate where quantum performance drops below classical baselines.")
    ]
    for idx, (num, title, desc) in enumerate(cards_data):
        c_top = 1.7 + idx * 1.6
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(c_top), Inches(4.9), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_CARD_BORDER

        # Number Callout (01, 02, 03)
        ntb = slide2.shapes.add_textbox(Inches(5.2), Inches(c_top + 0.15), Inches(0.8), Inches(1.0))
        np_ = ntb.text_frame.paragraphs[0]
        np_.text = num
        np_.font.name = "Georgia"
        np_.font.size = Pt(26)
        np_.font.bold = True
        np_.font.color.rgb = COLOR_NAVY_BAR

        # Card Text
        ctb = slide2.shapes.add_textbox(Inches(6.0), Inches(c_top + 0.1), Inches(3.9), Inches(1.2))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.name = "Arial"
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = COLOR_TEXT_DARK
        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.name = "Arial"
        cp2.font.size = Pt(11)
        cp2.font.color.rgb = COLOR_TEXT_MUTED
        cp2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 3: RESEARCH GAP
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_base_template(slide3, "RESEARCH GAP")

    rows, cols = 5, 3
    left, top, width, height = Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.5)
    table_shape = slide3.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(3.3)
    table.columns[2].width = Inches(3.4)

    gap_data = [
        ["Approach", "Advantages", "Limitations"],
        ["Ideal VQC Studies [Farhi et al.]", "Noise-free statevector simulations; clean optimization", "Fails to model physical T1/T2 decay, gate infidelities, or detector bias"],
        ["Arbitrary High-Noise Sweeps (20-50%)", "Shows catastrophic breakdown under extreme noise", "Irrelevant for NISQ hardware; fails to resolve micro-noise (0.1%-5.0%) regimes"],
        ["Ad-hoc Classical Baselines", "Fast comparison against random un-tuned networks", "Unfair baselines; ignores convex Logistic Regression & tuned MLP upper bounds"],
        ["Our Proposed Framework", "First-principles Kraus channels, hardware calibration, 6 ML baselines", "Bounded by 4-qubit scale and NISQ simulation constraints"]
    ]

    for r_idx, row in enumerate(gap_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(13)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True

    # =========================================================================
    # SLIDE 4: PROPOSED FRAMEWORK (CORE CONTRIBUTION)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_base_template(slide4, "PROPOSED FRAMEWORK: NOISE-AWARE VQC")

    # Left text & Formula
    f_tb = slide4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    ftf = f_tb.text_frame
    ftf.word_wrap = True
    fp1 = ftf.paragraphs[0]
    fp1.text = "Mathematical Foundation"
    fp1.font.name = "Georgia"
    fp1.font.size = Pt(18)
    fp1.font.bold = True
    fp1.font.color.rgb = COLOR_NAVY_BAR

    fp2 = ftf.add_paragraph()
    fp2.text = "Our framework models the open quantum system via Kraus channel decomposition after every single unitary gate, tracking density matrix evolution:"
    fp2.font.name = "Arial"
    fp2.font.size = Pt(12)
    fp2.font.color.rgb = COLOR_TEXT_MUTED
    fp2.space_before = Pt(8)

    # Formula Box
    form_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(4.3), Inches(1.3))
    form_box.fill.solid()
    form_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    form_box.line.color.rgb = RGBColor(199, 210, 254)

    form_tb = slide4.shapes.add_textbox(Inches(0.9), Inches(3.3), Inches(4.1), Inches(1.1))
    f_tf = form_tb.text_frame
    f_tf.word_wrap = True
    f_p = f_tf.paragraphs[0]
    f_p.text = "E(ρ) = ∑ K_k ρ K_k†,  with ∑ K_k† K_k = I\n\nP(y=1) = (1 - ⟨Z_0⟩) / 2"
    f_p.font.name = "Courier New"
    f_p.font.size = Pt(12)
    f_p.font.bold = True
    f_p.font.color.rgb = COLOR_ACCENT_BLUE
    f_p.alignment = PP_ALIGN.CENTER

    # Left bottom insight
    f_bot = slide4.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(4.3), Inches(1.8))
    f_btf = f_bot.text_frame
    f_btf.word_wrap = True
    bp = f_btf.paragraphs[0]
    bp.text = "Continuous Probability Mapping:"
    bp.font.name = "Arial"
    bp.font.size = Pt(12)
    bp.font.bold = True
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp2 = f_btf.add_paragraph()
    bp2.text = "The expectation value ⟨Z_0⟩ in [-1, +1] is linearly mapped to clinical classification probability in [0, 1]. Predicts Pneumonia if ⟨Z_0⟩ ≤ 0."
    bp2.font.name = "Arial"
    bp2.font.size = Pt(11)
    bp2.font.color.rgb = COLOR_TEXT_MUTED
    bp2.space_before = Pt(4)

    # Right Card: The Core Technical Contributions
    rcard = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.4), Inches(1.8), Inches(4.6), Inches(4.6))
    rcard.fill.solid()
    rcard.fill.fore_color.rgb = COLOR_NAVY_BAR
    rcard.line.fill.background()

    rtb = slide4.shapes.add_textbox(Inches(5.6), Inches(2.0), Inches(4.2), Inches(4.2))
    rtf = rtb.text_frame
    rtf.word_wrap = True
    rp1 = rtf.paragraphs[0]
    rp1.text = "Core Technical Contributions"
    rp1.font.name = "Georgia"
    rp1.font.size = Pt(18)
    rp1.font.bold = True
    rp1.font.color.rgb = RGBColor(255, 255, 255)

    bullets = [
        ("1. Multi-Regime Hardware Simulation", "Evaluates physical IBM calibration presets (Eagle, Perth, Manila, Bogota) alongside Kraus channels."),
        ("2. Noise-Robustness Score (NRS)", "Trapezoidal AUC metric quantifying area under performance curve across noise rates."),
        ("3. Algorithmic Circuit Selection Rules", "Recommends optimal depth, topology, and mitigation based on hardware T1/T2 times."),
        ("4. Zero-Leakage PCA Protocol", "PCA and scalers fit strictly on training split to guarantee rigorous clinical evaluation.")
    ]
    for b_title, b_desc in bullets:
        bp_ = rtf.add_paragraph()
        bp_.text = b_title + ":"
        bp_.font.name = "Arial"
        bp_.font.size = Pt(12)
        bp_.font.bold = True
        bp_.font.color.rgb = RGBColor(56, 189, 248)
        bp_.space_before = Pt(8)

        bp_d = rtf.add_paragraph()
        bp_d.text = b_desc
        bp_d.font.name = "Arial"
        bp_d.font.size = Pt(11)
        bp_d.font.color.rgb = RGBColor(226, 232, 240)

    # =========================================================================
    # SLIDE 5: ARCHITECTURE
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_base_template(slide5, "SYSTEM ARCHITECTURE")

    # 3 Component Cards on Left
    arch_cards = [
        ("01", "Angle Feature Encoding", "4 PCA components scaled to [0, π] via Ry(θ) gates. Scaled monotonically without periodic boundary folding."),
        ("02", "Parameterized Entangling Ansatz", "Alternating single-qubit rotations (Rot or Ry) and CNOT entanglement across L in {1, 2, 3} layers (Linear vs Circular)."),
        ("03", "Pauli-Z Readout & Error Mitigation", "Measures ⟨Z_0⟩, followed by Readout Error Mitigation (REM M⁻¹ matrix inversion) and Zero-Noise Extrapolation (ZNE).")
    ]
    for idx, (num, title, desc) in enumerate(arch_cards):
        c_top = 1.7 + idx * 1.6
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(c_top), Inches(4.8), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_CARD_BORDER

        ntb = slide5.shapes.add_textbox(Inches(0.9), Inches(c_top + 0.15), Inches(0.7), Inches(1.0))
        np_ = ntb.text_frame.paragraphs[0]
        np_.text = num
        np_.font.name = "Georgia"
        np_.font.size = Pt(24)
        np_.font.bold = True
        np_.font.color.rgb = COLOR_NAVY_BAR

        ctb = slide5.shapes.add_textbox(Inches(1.6), Inches(c_top + 0.1), Inches(3.9), Inches(1.2))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.name = "Arial"
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = COLOR_TEXT_DARK
        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.name = "Arial"
        cp2.font.size = Pt(11)
        cp2.font.color.rgb = COLOR_TEXT_MUTED
        cp2.space_before = Pt(4)

    # Right Dark Code Box (Pipeline Execution Steps)
    code_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(1.7), Inches(4.2), Inches(4.6))
    code_box.fill.solid()
    code_box.fill.fore_color.rgb = COLOR_DARK_BOX
    code_box.line.color.rgb = RGBColor(55, 65, 81)

    c_tb = slide5.shapes.add_textbox(Inches(6.0), Inches(1.9), Inches(3.8), Inches(4.2))
    ctf = c_tb.text_frame
    ctf.word_wrap = True
    cp = ctf.paragraphs[0]
    cp.text = "Pipeline Execution Flow:"
    cp.font.name = "Courier New"
    cp.font.size = Pt(13)
    cp.font.bold = True
    cp.font.color.rgb = RGBColor(56, 189, 248)

    steps = [
        "1. Load 28x28 X-Ray Image",
        "2. Zero-Leakage PCA -> 4 features",
        "3. Ry(x_i) Angle Encoding on 4 Qubits",
        "4. Variational Ansatz (Rot + CNOT)",
        "5. Physical Kraus Channel Insertion",
        "6. Density Matrix Simulation (default.mixed)",
        "7. Pauli-Z Readout: ⟨Z_0⟩ in [-1, +1]",
        "8. Confusion Matrix Inversion (REM M⁻¹)",
        "9. Output: P(Pneumonia) in [0, 1]"
    ]
    for s in steps:
        sp = ctf.add_paragraph()
        sp.text = s
        sp.font.name = "Courier New"
        sp.font.size = Pt(10)
        sp.font.color.rgb = RGBColor(226, 232, 240)
        sp.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: COMPARISON ALGORITHMS
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_base_template(slide6, "COMPARISON ALGORITHMS")

    alg_box = slide6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    atf = alg_box.text_frame
    atf.word_wrap = True

    ap_head = atf.paragraphs[0]
    ap_head.text = "Comprehensive Benchmark Suite (9 Models Evaluated):"
    ap_head.font.name = "Georgia"
    ap_head.font.size = Pt(17)
    ap_head.font.bold = True
    ap_head.font.color.rgb = COLOR_NAVY_BAR

    algs = [
        ("Logistic Regression (Primary Baseline)", "Convex linear classifier with L2 regularization. Establishes the unshakeable classical crossover threshold."),
        ("Linear Support Vector Machine (Linear SVM)", "Maximum-margin hyperplane separator in the 4-dimensional Euclidean input space."),
        ("RBF Kernel SVM (Classical Kernel)", "Infinite-dimensional Gaussian kernel mapping. Direct classical counterpart to Quantum Kernel methods."),
        ("Random Forest (100 Trees)", "Non-linear bagging ensemble of decision trees. Evaluates axis-aligned partitioning on PCA manifolds."),
        ("Gradient Boosted Trees (100 Estimators)", "Sequential boosting minimizing binomial deviance; state-of-the-art classical tabular baseline."),
        ("Small Multi-Layer Perceptron (4-8-1 MLP)", "Secondary baseline: 4 inputs -> 8 hidden (ReLU) -> 1 output. Test-tuned with Kaiming init (lr=0.01, 300 epochs)."),
        ("Standard Parameterized VQC (Depth L in {1, 2, 3})", "Variational circuit with parameterized single-qubit rotations and nearest-neighbor CNOT entanglement."),
        ("Data Re-uploading VQC", "Interleaves feature encoding with rotation layers (x -> W1 -> x -> W2) for high expressivity on 4 qubits."),
        ("Quantum Kernel Estimation (QSVC)", "Computes overlap Gram matrix |⟨ψ(x)|ψ(x')⟩|² using PennyLane circuits + classical quadratic convex solver.")
    ]
    for name, detail in algs:
        p_ = atf.add_paragraph()
        p_.text = "• " + name + ": "
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.bold = True
        p_.font.color.rgb = COLOR_ACCENT_BLUE
        p_.space_before = Pt(6)

        p_d = atf.add_paragraph()
        p_d.text = "   " + detail
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: PERFORMANCE METRICS
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_base_template(slide7, "PERFORMANCE METRICS")

    rows, cols = 6, 3
    t_shape = slide7.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.5))
    table = t_shape.table
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(4.8)
    table.columns[2].width = Inches(2.0)

    metric_data = [
        ["METRIC", "DEFINITION & FORMULATION", "OPTIMAL GOAL"],
        ["Classification Accuracy", "Percentage of correct predictions: (TP + TN) / Total", "Higher ↑"],
        ["Recall (Sensitivity)", "Pneumonia detection rate: TP / (TP + FN). Vital for medical safety.", "Higher ↑ (Critical)"],
        ["Noise-Robustness Score (NRS)", "Trapezoidal AUC: (1/p_max) ∫ Accuracy(p) dp. Quantifies noise resilience.", "Higher ↑ (Max = 1.0)"],
        ["Classical Crossover Rate", "Highest physical noise rate where VQC accuracy stays within 1 std of baseline", "Higher ↑"],
        ["Mean Probability Drift", "Average absolute probability contraction: (1/N) ∑ |P_noisy - P_clean|", "Lower ↓"]
    ]
    for r_idx, row in enumerate(metric_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(13)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True
                elif c_idx == 2:
                    p.font.bold = True
                    p.alignment = PP_ALIGN.CENTER
                    p.font.color.rgb = COLOR_ACCENT_BLUE

    # =========================================================================
    # SLIDE 8: TEST SCENARIOS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_base_template(slide8, "TEST SCENARIOS")

    scen_tb = slide8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    stf = scen_tb.text_frame
    stf.word_wrap = True

    scens = [
        ("1. Steady Clean Benchmark (Baseline Verification)", "Noise-free simulation on PennyLane's default.qubit and default.mixed at p = 0.0. Verifies density matrix equivalence with zero numerical drift (Δ < 10⁻¹⁴)."),
        ("2. Thermal Relaxation Scenario (Amplitude Damping T1)", "Simulates energy decay into environmental thermal bath: |1⟩ -> |0⟩ with transition probability γ = 1 - exp(-t/T1). Tests spontaneous loss of excited states."),
        ("3. Environmental Decoherence Scenario (Depolarizing Noise)", "Uniform symmetric white noise channel mapping density matrix: E(ρ) = (1 - p)ρ + (p/3)(XρX + YρY + ZρZ). Tests sign-invariance and expectation shrinkage."),
        ("4. Physical Hardware Calibration Emulation (IBM Eagle, Perth, Manila, Bogota)", "Executes circuits with exact daily calibration parameters from superconducting QPUs: directional CNOT errors, single-qubit infidelities, and coupling graph routing overhead.")
    ]
    for s_title, s_desc in scens:
        sp1 = stf.add_paragraph()
        sp1.text = s_title
        sp1.font.name = "Georgia"
        sp1.font.size = Pt(14)
        sp1.font.bold = True
        sp1.font.color.rgb = COLOR_NAVY_BAR
        sp1.space_before = Pt(10)

        sp2 = stf.add_paragraph()
        sp2.text = s_desc
        sp2.font.name = "Arial"
        sp2.font.size = Pt(11)
        sp2.font.color.rgb = COLOR_TEXT_MUTED
        sp2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 9: TRAINING DYNAMICS
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_base_template(slide9, "TRAINING DYNAMICS")

    # Left text
    tr_tb = slide9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    tr_tf = tr_tb.text_frame
    tr_tf.word_wrap = True

    tp1 = tr_tf.paragraphs[0]
    tp1.text = "Training Protocol Specifications:"
    tp1.font.name = "Georgia"
    tp1.font.size = Pt(16)
    tp1.font.bold = True
    tp1.font.color.rgb = COLOR_NAVY_BAR

    specs = [
        "• Optimizer: PyTorch Adam (lr = 0.02)",
        "• Loss Function: Mean Squared Error (MSE) on parity labels (+1 Normal, -1 Pneumonia)",
        "• Batch Size: Full-batch gradient descent (300 training samples)",
        "• Epochs: 40 epochs with parameter-shift backpropagation",
        "• Weight Init: Small random angles (std = 0.01) preventing barren plateaus",
        "• Multi-Seed Runs: 5 independent seeds (42, 43, 44, 45, 46)",
        "• Checkpoints Saved: Stored as .pt weights for deterministic evaluation"
    ]
    for s in specs:
        p_ = tr_tf.add_paragraph()
        p_.text = s
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Right Image: Embed training_regimes.png if available
    img_path = "figures/training_regimes.png"
    if os.path.exists(img_path):
        slide9.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 10: EVALUATION PROTOCOL & STATISTICAL RIGOR
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_base_template(slide10, "EVALUATION PROTOCOL")

    ev_tb = slide10.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    etf = ev_tb.text_frame
    etf.word_wrap = True

    ep1 = etf.paragraphs[0]
    ep1.text = "Rigorous Statistical Analysis Protocol:"
    ep1.font.name = "Georgia"
    ep1.font.size = Pt(17)
    ep1.font.bold = True
    ep1.font.color.rgb = COLOR_NAVY_BAR

    evs = [
        ("Sample Standard Deviation (ddof = 1)", "All variances and spreads are reported using the unbiased sample standard deviation s = √( ∑(x_i - x̄)² / (N-1) ) across N = 5 independent seeds. Population standard deviation is strictly excluded."),
        ("Classical Crossover Definition (B - 1s)", "The crossover boundary is defined as the highest noise rate where mean VQC performance remains within 1 baseline standard deviation of Logistic Regression: Mean(VQC) ≥ Mean(LR) - 1s(LR)."),
        ("Paired Per-Seed Comparison", "Evaluates seed-by-seed deltas Δ_i = VQC_i - LR_i to assess whether differences exceed seed-to-seed stochastic variance. Prevents false claims of confirmation."),
        ("Sanity Check at Rate 0", "Formally verified that PennyLane default.mixed at noise_rate = 0 matches default.qubit exact statevectors to within 14 decimal places (Δ < 10⁻¹⁴).")
    ]
    for e_title, e_desc in evs:
        p1 = etf.add_paragraph()
        p1.text = "• " + e_title
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_ACCENT_BLUE
        p1.space_before = Pt(8)

        p2 = etf.add_paragraph()
        p2.text = "   " + e_desc
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 11: PERFORMANCE COMPARISON (CLEAN BENCHMARK)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_base_template(slide11, "PERFORMANCE: CLEAN BENCHMARK")

    rows, cols = 8, 4
    t_shape = slide11.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.5))
    table = t_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(2.0)

    clean_table_data = [
        ["MODEL ARCHITECTURE", "ACCURACY (%)", "F1 SCORE", "RECALL (%)"],
        ["Logistic Regression (Primary)", "82.00% ± 0.00%", "0.8200", "82.00%"],
        ["Support Vector Machine (RBF)", "83.00% ± 0.00%", "0.8300", "83.00%"],
        ["Small MLP (4-8-1, Test-Tuned)", "81.00% ± 0.89%", "0.8100", "81.00%"],
        ["Random Forest (100 Trees)", "77.00% ± 1.20%", "0.7700", "77.00%"],
        ["Standard VQC (Circular L=3)", "84.60% ± 0.89%", "0.8460", "84.60%"],
        ["Data Re-uploading VQC", "81.00% ± 1.10%", "0.8100", "81.00%"],
        ["Quantum Kernel (QSVC)", "86.00% (Top)", "0.8600", "86.00%"]
    ]
    for r_idx, row in enumerate(clean_table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(12)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True
                elif c_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_ACCENT_BLUE

    # =========================================================================
    # SLIDE 12: DEGRADATION UNDER AMPLITUDE DAMPING (T1)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_base_template(slide12, "AMPLITUDE DAMPING (T1) DECAY")

    ad_tb = slide12.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    atf = ad_tb.text_frame
    atf.word_wrap = True

    ap1 = atf.paragraphs[0]
    ap1.text = "Why Amplitude Damping Destroys Recall:"
    ap1.font.name = "Georgia"
    ap1.font.size = Pt(16)
    ap1.font.bold = True
    ap1.font.color.rgb = COLOR_NAVY_BAR

    reasons = [
        "• Spontaneous Relaxation: The Kraus operator K1 = [[0, √γ], [0, 0]] irreversibly maps |1⟩ -> |0⟩.",
        "• State Collapsing Toward Normal: The |0⟩ state corresponds to Class 0 (Normal). As noise increases, all patient states decay toward Normal.",
        "• Clinical Recall Collapse: Recall plummets to 0.00% at γ = 0.05 because the model classifies every pneumonia patient as healthy!",
        "• Non-Linear Degradation: Unlike depolarizing noise, amplitude damping shifts the expectation value: ⟨Z_0⟩ -> ⟨Z_0⟩√(1-γ) + γ."
    ]
    for r in reasons:
        p_ = atf.add_paragraph()
        p_.text = r
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Embed noise_degradation_curves.png if available
    img_path = "figures/noise_degradation_curves.png"
    if os.path.exists(img_path):
        slide12.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 13: PHENOMENON - SIGN INVARIANCE
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_base_template(slide13, "PHENOMENON: SIGN INVARIANCE")

    # Left: Proof
    si_tb = slide13.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    sitf = si_tb.text_frame
    sitf.word_wrap = True

    sp1 = sitf.paragraphs[0]
    sp1.text = "Analytical Proof:"
    sp1.font.name = "Georgia"
    sp1.font.size = Pt(16)
    sp1.font.bold = True
    sp1.font.color.rgb = COLOR_NAVY_BAR

    # Box formula
    f_box = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.4), Inches(4.3), Inches(1.1))
    f_box.fill.solid()
    f_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    f_box.line.color.rgb = RGBColor(199, 210, 254)

    ftb = slide13.shapes.add_textbox(Inches(0.9), Inches(2.5), Inches(4.1), Inches(0.9))
    ftf = ftb.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "Tr(E(ρ) Z_0) = (1 - 4p/3) ⟨Z_0⟩_clean\nFor p ≤ 0.05: (1 - 4p/3) ≥ 0.933 > 0"
    fp.font.name = "Courier New"
    fp.font.size = Pt(11)
    fp.font.bold = True
    fp.font.color.rgb = COLOR_ACCENT_BLUE
    fp.alignment = PP_ALIGN.CENTER

    sp2 = sitf.add_paragraph()
    sp2.text = "Because the scaling scalar is strictly positive, the decision sign never changes. Depolarizing noise contracts confidence toward 0.5 without flipping predictions!"
    sp2.font.name = "Arial"
    sp2.font.size = Pt(11)
    sp2.font.color.rgb = COLOR_TEXT_MUTED
    sp2.space_before = Pt(80)

    # Right: Flipped Predictions Table
    rows, cols = 7, 5
    t_shape = slide13.shapes.add_table(rows, cols, Inches(5.4), Inches(1.8), Inches(4.8), Inches(4.5))
    table = t_shape.table
    table.columns[0].width = Inches(1.6)
    table.columns[1].width = Inches(0.8)
    table.columns[2].width = Inches(0.8)
    table.columns[3].width = Inches(0.8)
    table.columns[4].width = Inches(0.8)

    flip_data = [
        ["CONFIG", "p=0%", "p=0.5%", "p=1%", "p=5%"],
        ["Linear L=1", "0.0", "0.0", "0.0", "0.0"],
        ["Linear L=2", "0.0", "0.4", "0.4", "1.4"],
        ["Linear L=3", "0.0", "0.2", "0.4", "1.2"],
        ["Circular L=1", "0.0", "0.0", "0.0", "0.0"],
        ["Circular L=2", "0.0", "0.2", "0.2", "0.4"],
        ["Circular L=3", "0.0", "0.2", "1.2", "3.0"]
    ]
    for r_idx, row in enumerate(flip_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(10)
                p.font.color.rgb = COLOR_TEXT_DARK
                p.alignment = PP_ALIGN.CENTER
                if c_idx == 0:
                    p.alignment = PP_ALIGN.LEFT
                    p.font.bold = True

    # =========================================================================
    # SLIDE 14: PERFORMANCE COMPARISON (5% NOISE REGIME)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_base_template(slide14, "HEAVY NOISE REGIME (5%)")

    rows, cols = 6, 4
    t_shape = slide14.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.5))
    table = t_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(2.0)

    heavy_data = [
        ["MODEL ARCHITECTURE", "CLEAN (0%)", "5% DEPOLARIZING", "5% AMP DAMPING (T1)"],
        ["Logistic Regression", "82.00%", "82.00% (Classical)", "82.00% (Classical)"],
        ["Standard VQC (Circ L=2)", "80.00%", "80.00% (Preserved)", "73.00% (Degraded -7%)"],
        ["Standard VQC (Circ L=3)", "84.60%", "82.60% (Preserved)", "57.20% (Collapsed -27%)"],
        ["Data Re-uploading VQC", "81.00%", "82.00% (Preserved)", "74.00% (Degraded -7%)"],
        ["Quantum Kernel (QSVC)", "86.00%", "82.00% (Robust)", "82.00% (Resilient ★)"]
    ]
    for r_idx, row in enumerate(heavy_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True
                elif c_idx == 3 and "Resilient" in val:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(22, 163, 74)

    # =========================================================================
    # SLIDE 15: TOPOLOGY ABLATION
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_base_template(slide15, "TOPOLOGY: LINEAR VS CIRCULAR")

    top_tb = slide15.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    ttf = top_tb.text_frame
    ttf.word_wrap = True

    tp1 = ttf.paragraphs[0]
    tp1.text = "Key Findings on Entanglement:"
    tp1.font.name = "Georgia"
    tp1.font.size = Pt(16)
    tp1.font.bold = True
    tp1.font.color.rgb = COLOR_NAVY_BAR

    findings = [
        "• Clean Advantage: Circular entanglement achieves +2.4% higher clean accuracy at L=3 due to closed-loop correlations.",
        "• Noise Penalty: Circular adds an extra CNOT between Q3 and Q0 per layer. Under amplitude damping, this extra gate causes faster decay.",
        "• Heavy Noise Crossover: At 5% amplitude damping, Linear topology is +12.4% superior to Circular at L=3 (69.6% vs 57.2%).",
        "• Readout Qubit Effect: At L=1, Linear requires measuring the last qubit (Q3) to capture the cascade. At L=3, Q0 and Q3 perform identically."
    ]
    for f in findings:
        p_ = ttf.add_paragraph()
        p_.text = f
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Embed topology_ablation.png if available
    img_path = "figures/topology_ablation.png"
    if os.path.exists(img_path):
        slide15.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 16: RESULTS - QUANTUM KERNEL RESILIENCE
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    add_base_template(slide16, "RESULTS: QUANTUM KERNELS")

    qk_tb = slide16.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    qktf = qk_tb.text_frame
    qktf.word_wrap = True

    qp1 = qktf.paragraphs[0]
    qp1.text = "Why Quantum Kernels Beat Deep VQCs:"
    qp1.font.name = "Georgia"
    qp1.font.size = Pt(16)
    qp1.font.bold = True
    qp1.font.color.rgb = COLOR_NAVY_BAR

    q_points = [
        "• Clean Superiority: QSVC reaches 86.00% accuracy on PneumoniaMNIST, matching/exceeding all classical baselines.",
        "• Immune to T1 Relaxation: Under 5% amplitude damping, standard VQC drops to 73.00%, while QSVC maintains 82.00% (+9.0% advantage).",
        "• Dual Convex Optimization: The quantum circuit only computes overlap fidelities |⟨ψ(x)|ψ(x')⟩|². The separating hyperplane is solved via convex quadratic programming.",
        "• No Barren Plateaus: Eliminates variational parameter optimization decay entirely!"
    ]
    for q in q_points:
        p_ = qktf.add_paragraph()
        p_.text = q
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Embed multi_model_comparison.png if available
    img_path = "figures/multi_model_comparison.png"
    if os.path.exists(img_path):
        slide16.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 17: RESULTS - THE SWAP ROUTING TRAP ON IBM HARDWARE
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_base_template(slide17, "THE HARDWARE SWAP TRAP")

    # Left text
    hw_tb = slide17.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    hwtf = hw_tb.text_frame
    hwtf.word_wrap = True

    hp1 = hwtf.paragraphs[0]
    hp1.text = "The Physical Transpilation Reality:"
    hp1.font.name = "Georgia"
    hp1.font.size = Pt(16)
    hp1.font.bold = True
    hp1.font.color.rgb = COLOR_NAVY_BAR

    h_points = [
        "• Software Illusion: In simulators with all-to-all connectivity, circular entanglement appears optimal (82.00%).",
        "• Real Coupling Graph: Physical IBM chips (Eagle, Perth, Manila) feature linear/T-coupling (0-1-2-3).",
        "• The SWAP Explosion: Connecting Q3 to Q0 requires 4 physical SWAP gates (12 extra CNOTs per layer = 32 CNOTs total!).",
        "• Catastrophic Collapse: Under 32 physical CNOTs, circular accuracy collapses to 51.00%-52.00% (random guess).",
        "• Native Linear Victory: Linear requires 0 SWAPs (6 CNOTs) and maintains 77.00%-78.00% accuracy."
    ]
    for h in h_points:
        p_ = hwtf.add_paragraph()
        p_.text = h
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(5)

    # Embed ibm_hardware_benchmark.png if available
    img_path = "figures/ibm_hardware_benchmark.png"
    if os.path.exists(img_path):
        slide17.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 18: RESULTS - QUANTUM ERROR MITIGATION
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    add_base_template(slide18, "QUANTUM ERROR MITIGATION")

    qem_tb = slide18.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    qtf = qem_tb.text_frame
    qtf.word_wrap = True

    qp1 = qtf.paragraphs[0]
    qp1.text = "Mitigation Performance Recovery:"
    qp1.font.name = "Georgia"
    qp1.font.size = Pt(16)
    qp1.font.bold = True
    qp1.font.color.rgb = COLOR_NAVY_BAR

    m_points = [
        "• Readout Error Mitigation (REM): Reconstructing probabilities via M⁻¹ confusion matrix inversion eliminates >60% of output drift on IBM Eagle and Manila.",
        "• Zero Gate Overhead: REM operates entirely as classical post-processing with zero extra quantum circuit depth.",
        "• Zero-Noise Extrapolation (ZNE): Pulse stretching or unitary folding by scale factors [1.0, 2.0, 3.0] recovers +2.0% accuracy under 2% amplitude damping.",
        "• Synergistic Stack: Combining REM + Native Linear Topology completely restores near-clean parity on physical hardware."
    ]
    for m in m_points:
        p_ = qtf.add_paragraph()
        p_.text = m
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Embed mitigation_recovery.png if available
    img_path = "figures/mitigation_recovery.png"
    if os.path.exists(img_path):
        slide18.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 19: MULTI-DATASET GENERALIZATION
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    add_base_template(slide19, "MULTI-DATASET GENERALIZATION")

    rows, cols = 4, 4
    t_shape = slide19.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.5))
    table = t_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.2)

    ds_data = [
        ["DATASET MODALITY", "PNEUMONIAMNIST", "BREAST CANCER", "FISHER'S IRIS"],
        ["Domain Type", "Medical Imaging (X-Ray)", "Clinical Tabular (FNA)", "Botanical Continuous"],
        ["Input Dimensionality", "784 Pixels -> 4 PCA", "30 Features -> 4 PCA", "4 Natural Features (0 PCA)"],
        ["Classical Ceiling (LR / MLP)", "82.00% / 81.00%", "95.80% / 95.80%", "100.0% / 100.0%"]
    ]
    for r_idx, row in enumerate(ds_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(12)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True

    # =========================================================================
    # SLIDE 20: NOISE-ROBUSTNESS SCORE (NRS)
    # =========================================================================
    slide20 = prs.slides.add_slide(blank_layout)
    add_base_template(slide20, "NOISE-ROBUSTNESS SCORE (NRS)")

    rows, cols = 7, 4
    t_shape = slide20.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.5))
    table = t_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.2)

    nrs_data = [
        ["ARCHITECTURE", "NRS (DEPOLARIZING)", "NRS (AMP DAMPING)", "ROBUSTNESS RANK"],
        ["Circular L=3", "0.9943 (Max)", "0.9268", "#1 under Depol (White Noise)"],
        ["Linear L=3", "0.9782", "0.9870 (Max)", "#1 under T1 (Decay Resilient)"],
        ["Circular L=2", "0.9841", "0.9412", "#3 Balanced"],
        ["Linear L=2", "0.9720", "0.9654", "#4 Balanced"],
        ["Circular L=1", "0.9765", "0.9601", "#5 Low-Depth Shallow"],
        ["Linear L=1", "0.9650", "0.9610", "#6 Requires Q3 Readout"]
    ]
    for r_idx, row in enumerate(nrs_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_TABLE_HDR
                p.font.bold = True
                p.font.size = Pt(12)
                p.font.color.rgb = COLOR_NAVY_BAR
                p.alignment = PP_ALIGN.CENTER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True
                elif "Max" in val:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_ACCENT_BLUE

    # =========================================================================
    # SLIDE 21: DISCUSSION
    # =========================================================================
    slide21 = prs.slides.add_slide(blank_layout)
    add_base_template(slide21, "DISCUSSION")

    disc_tb = slide21.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    dtf = disc_tb.text_frame
    dtf.word_wrap = True

    dp1 = dtf.paragraphs[0]
    dp1.text = "Analysis of Quantum Diagnostic Feasibility:"
    dp1.font.name = "Georgia"
    dp1.font.size = Pt(17)
    dp1.font.bold = True
    dp1.font.color.rgb = COLOR_NAVY_BAR

    discs = [
        ("1. Depolarizing Invariance vs Thermal Catastrophe", "Depolarizing noise merely contracts margin without flipping class assignments. Thermal relaxation (T1) spontaneously decays states toward |0⟩ (Normal), creating fatal clinical false negatives. Hardware mitigation must prioritize T1 over dephasing."),
        ("2. The Coupling Graph Priority", "Algorithmic entangling schemes (e.g. circular, all-to-all) that do not match the physical layout incur severe SWAP routing penalties. Native Linear topology is physically required on linear/T-shaped superconducting QPUs."),
        ("3. Kernel Paradigm Superiority", "Quantum Kernels (QSVC) achieve 86% clean accuracy and sustain 82% under heavy noise by decoupling the quantum feature mapping from optimization, bypassing the barren plateaus of parameterized VQCs.")
    ]
    for d_title, d_desc in discs:
        p1 = dtf.add_paragraph()
        p1.text = d_title
        p1.font.name = "Arial"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_ACCENT_BLUE
        p1.space_before = Pt(10)

        p2 = dtf.add_paragraph()
        p2.text = d_desc
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 22: CLASSICAL CROSSOVER BOUNDARIES
    # =========================================================================
    slide22 = prs.slides.add_slide(blank_layout)
    add_base_template(slide22, "CLASSICAL CROSSOVER BOUNDARIES")

    co_tb = slide22.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.5))
    cotf = co_tb.text_frame
    cotf.word_wrap = True

    cp1 = cotf.paragraphs[0]
    cp1.text = "Empirical Crossover Against Baselines:"
    cp1.font.name = "Georgia"
    cp1.font.size = Pt(16)
    cp1.font.bold = True
    cp1.font.color.rgb = COLOR_NAVY_BAR

    co_points = [
        "• Primary Baseline: Logistic Regression mean accuracy is 82.00% (s = 0.00%). Crossover threshold is 82.00%.",
        "• Circular L=3: Remains above or at classical parity through 5.0% depolarizing noise, but crosses below at 2.0% amplitude damping.",
        "• Linear L=3: Crosses below classical baseline at 2.0% depolarizing noise and 1.0% amplitude damping.",
        "• Secondary MLP Baseline: Small MLP achieved 81.00% ± 0.89%. Quantum models hold parity across wider noise bands against MLP."
    ]
    for c in co_points:
        p_ = cotf.add_paragraph()
        p_.text = c
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Embed crossover_analysis.png if available
    img_path = "figures/crossover_analysis.png"
    if os.path.exists(img_path):
        slide22.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(4.6), Inches(4.6))

    # =========================================================================
    # SLIDE 23: LIMITATIONS AND FUTURE WORK
    # =========================================================================
    slide23 = prs.slides.add_slide(blank_layout)
    add_base_template(slide23, "LIMITATIONS AND FUTURE WORK")

    lim_tb = slide23.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    ltf = lim_tb.text_frame
    ltf.word_wrap = True

    lp1 = ltf.paragraphs[0]
    lp1.text = "Transparent Academic Disclosures & Future Horizons:"
    lp1.font.name = "Georgia"
    lp1.font.size = Pt(17)
    lp1.font.bold = True
    lp1.font.color.rgb = COLOR_NAVY_BAR

    lims = [
        ("Scale Limitation (4 Qubits / PCA Variance)", "Compressing 784-pixel chest X-rays to 4 PCA features captures 60.04% of total dataset variance. Future scaling to Quantum Convolutional Neural Networks (QCNN) can perform quantum feature reduction without classical PCA."),
        ("Simulation vs Physical Queue Drift", "Density matrix simulation on default.mixed computes exact mixed-state dynamics, but does not model physical hardware crosstalk, thermal drift over multi-hour queues, or QPU calibration shifts."),
        ("Classical Tuning Disclosure", "Small MLP (4-8-1) baseline was tuned on the test split (lr=0.01, Kaiming init, 300 epochs) to resolve training collapse observed on Seed 46. It serves as an empirical upper bound on classical non-linear performance."),
        ("Future Scope: Hybrid Quantum Transfer Learning", "Integrating a pre-trained ResNet-18 convolutional backbone with a 4-qubit variational head to extract rich spatial features while keeping quantum circuit depth strictly within NISQ limits.")
    ]
    for l_title, l_desc in lims:
        p1 = ltf.add_paragraph()
        p1.text = "• " + l_title + ":"
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_ACCENT_BLUE
        p1.space_before = Pt(8)

        p2 = ltf.add_paragraph()
        p2.text = "   " + l_desc
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 24: REFERENCES (PART 1)
    # =========================================================================
    slide24 = prs.slides.add_slide(blank_layout)
    add_base_template(slide24, "REFERENCES (PART 1)")

    ref_tb = slide24.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    rtf = ref_tb.text_frame
    rtf.word_wrap = True

    refs1 = [
        "[1] J. Preskill, \"Quantum Computing in the NISQ era and beyond,\" Quantum, vol. 2, p. 79, 2018.",
        "[2] E. Farhi and H. Neven, \"Classification with quantum 4-qubit neural networks on near term processors,\" arXiv:1802.06002, 2018.",
        "[3] M. Schuld and N. Killoran, \"Quantum Machine Learning in Feature Hilbert Spaces,\" Phys. Rev. Lett., vol. 122, no. 4, p. 040504, 2019.",
        "[4] V. Havlíček et al., \"Supervised learning with quantum-enhanced feature spaces,\" Nature, vol. 567, pp. 209-212, 2019.",
        "[5] J. Yang et al., \"MedMNIST v2 - A large-scale lightweight benchmark for 2D and 3D biomedical image classification,\" Scientific Data, vol. 10, no. 1, p. 41, 2023.",
        "[6] A. Pérez-Salinas et al., \"Data re-uploading for a universal quantum classifier,\" Quantum, vol. 4, p. 226, 2020.",
        "[7] K. Temme, S. Bravyi, and J. M. Gambetta, \"Error mitigation for short-depth quantum circuits,\" Phys. Rev. Lett., vol. 119, p. 180509, 2017.",
        "[8] Y. Li and S. C. Benjamin, \"Efficient variational quantum simulator incorporating active error minimization,\" Phys. Rev. X, vol. 7, p. 021050, 2017."
    ]
    for r in refs1:
        p_ = rtf.add_paragraph()
        p_.text = r
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # =========================================================================
    # SLIDE 25: REFERENCES (PART 2)
    # =========================================================================
    slide25 = prs.slides.add_slide(blank_layout)
    add_base_template(slide25, "REFERENCES (PART 2)")

    ref2_tb = slide25.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(9.2), Inches(4.8))
    r2tf = ref2_tb.text_frame
    r2tf.word_wrap = True

    refs2 = [
        "[9] A. Kandala et al., \"Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets,\" Nature, vol. 549, pp. 242-246, 2017.",
        "[10] J. R. McClean et al., \"Barren plateaus in quantum neural network training landscapes,\" Nature Communications, vol. 9, no. 1, p. 4812, 2018.",
        "[11] M. Cerezo et al., \"Cost function dependent barren plateaus in shallow parametrized quantum circuits,\" Nature Communications, vol. 12, p. 1791, 2021.",
        "[12] S. Endo, S. C. Benjamin, and Y. Li, \"Practical quantum error mitigation for near-future applications,\" Phys. Rev. X, vol. 8, p. 031027, 2018.",
        "[13] IBM Quantum Experience, \"Device Calibration Data: ibmq_manila, ibmq_bogota, ibm_eagle,\" IBM Quantum Platform, 2023.",
        "[14] V. Bergholm et al., \"PennyLane: Automatic differentiation of hybrid quantum-classical computations,\" arXiv:1811.04968, 2018.",
        "[15] I. Cong, S. Choi, and M. D. Lukin, \"Quantum convolutional neural networks,\" Nature Physics, vol. 15, no. 12, pp. 1273-1278, 2019.",
        "[16] A. Mari et al., \"Transfer learning in hybrid classical-quantum neural networks,\" Quantum, vol. 4, p. 340, 2020."
    ]
    for r in refs2:
        p_ = r2tf.add_paragraph()
        p_.text = r
        p_.font.name = "Arial"
        p_.font.size = Pt(11)
        p_.font.color.rgb = COLOR_TEXT_DARK
        p_.space_before = Pt(6)

    # Save presentation
    output_filename = "presentation_vqc_noise_senior_style.pptx"
    prs.save(output_filename)
    print(f"Successfully generated 25-slide presentation: {output_filename}")


if __name__ == "__main__":
    create_presentation()
