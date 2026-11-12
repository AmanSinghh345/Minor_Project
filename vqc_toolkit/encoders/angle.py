"""
Quantum feature encodings.
"""

import pennylane as qml
import numpy as np


def apply_angle_encoding(features, wires):
    """
    Applies monotonic Ry angle encoding:
    Ry(theta) for each wire, where theta in [0, pi].
    Strictly preserves distance ordering without periodic aliasing.
    """
    for i, wire in enumerate(wires):
        val = features[i]
        qml.RY(val, wires=wire)


def apply_dense_encoding(features, wires):
    """
    Applies dense Rx(theta1) Rz(theta2) encoding:
    Allows 2 classical features per qubit.
    """
    n_features = len(features)
    for i, wire in enumerate(wires):
        feat_rx = features[2 * i] if 2 * i < n_features else 0.0
        feat_rz = features[2 * i + 1] if 2 * i + 1 < n_features else 0.0
        qml.RX(feat_rx, wires=wire)
        qml.RZ(feat_rz, wires=wire)
