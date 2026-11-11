"""
data.py - Data loading and preprocessing pipeline for PneumoniaMNIST.

This module prepares a low-dimensional quantum-compatible representation of
the PneumoniaMNIST medical imaging dataset.

Pipeline steps:
1. Load raw PneumoniaMNIST images and labels (binary classification:
   0 = Normal, 1 = Pneumonia).
2. Sample balanced subsets: 300 training samples (150 normal, 150 pneumonia)
   and 100 test samples (50 normal, 50 pneumonia).
3. Flatten each 28x28 grayscale image into a 784-dimensional vector.
4. Normalize pixel values from [0, 255] to [0.0, 1.0].
5. Fit Principal Component Analysis (PCA) on the training set ONLY to reduce
   dimensionality from 784 down to 4 features (one feature per qubit).
6. Transform both train and test sets using the fitted PCA model.
7. Scale the 4 PCA features to the interval [0, pi] using MinMaxScaler fitted
   on the training set ONLY. Scaling to [0, pi] is necessary for quantum angle
   encoding: an Ry(theta) gate rotates |0> to |1> as theta goes from 0 to pi.
"""

import argparse
import numpy as np
from medmnist import PneumoniaMNIST
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


def load_and_preprocess_data(seed: int = 42, n_train: int = 300, n_test: int = 100):
    """
    Loads PneumoniaMNIST, samples balanced train/test sets, flattens, normalizes,
    applies PCA to reduce to 4 features, and scales features to [0, pi].

    Args:
        seed: Random seed for reproducible class sampling and PCA initialization.
        n_train: Total number of training samples (must be even for balance).
        n_test: Total number of test samples (must be even for balance).

    Returns:
        dict containing:
            - 'X_train': (n_train, 4) scaled features in [0, pi]
            - 'y_train': (n_train,) binary labels (0 or 1)
            - 'X_test':  (n_test, 4) scaled features in [0, pi]
            - 'y_test':  (n_test,) binary labels (0 or 1)
            - 'pca': fitted PCA object
            - 'scaler': fitted MinMaxScaler object
    """
    assert n_train % 2 == 0, "n_train must be divisible by 2 for balanced classes"
    assert n_test % 2 == 0, "n_test must be divisible by 2 for balanced classes"

    n_train_per_class = n_train // 2
    n_test_per_class = n_test // 2

    # Step 1: Download/load official PneumoniaMNIST splits
    raw_train = PneumoniaMNIST(split="train", download=True)
    raw_test = PneumoniaMNIST(split="test", download=True)

    # Step 2: Deterministic balanced sampling using numpy Generator
    rng = np.random.default_rng(seed)

    # Training split sampling
    train_labels = raw_train.labels.flatten()
    train_idx_0 = np.where(train_labels == 0)[0]
    train_idx_1 = np.where(train_labels == 1)[0]

    chosen_train_0 = rng.choice(train_idx_0, size=n_train_per_class, replace=False)
    chosen_train_1 = rng.choice(train_idx_1, size=n_train_per_class, replace=False)
    train_indices = np.concatenate([chosen_train_0, chosen_train_1])
    rng.shuffle(train_indices)

    # Test split sampling
    test_labels = raw_test.labels.flatten()
    test_idx_0 = np.where(test_labels == 0)[0]
    test_idx_1 = np.where(test_labels == 1)[0]

    chosen_test_0 = rng.choice(test_idx_0, size=n_test_per_class, replace=False)
    chosen_test_1 = rng.choice(test_idx_1, size=n_test_per_class, replace=False)
    test_indices = np.concatenate([chosen_test_0, chosen_test_1])
    rng.shuffle(test_indices)

    # Step 3 & 4: Flatten (28x28 -> 784) and normalize ([0, 255] -> [0.0, 1.0])
    X_train_raw = raw_train.imgs[train_indices].reshape(-1, 28 * 28).astype(np.float32) / 255.0
    y_train = train_labels[train_indices].astype(np.int64)

    X_test_raw = raw_test.imgs[test_indices].reshape(-1, 28 * 28).astype(np.float32) / 255.0
    y_test = test_labels[test_indices].astype(np.int64)

    # Step 5: Principal Component Analysis (fit on TRAIN only to avoid data leakage)
    pca = PCA(n_components=4, random_state=seed)
    X_train_pca = pca.fit_transform(X_train_raw)
    X_test_pca = pca.transform(X_test_raw)

    # Step 6: Scale features to [0, pi] for quantum angle encoding
    # MinMaxScaler is fitted on training set only.
    scaler = MinMaxScaler(feature_range=(0.0, np.pi))
    X_train_scaled = scaler.fit_transform(X_train_pca)
    # Clip test values to [0, pi] to guarantee valid rotation angle domain
    X_test_scaled = np.clip(scaler.transform(X_test_pca), 0.0, np.pi)

    return {
        "X_train": X_train_scaled.astype(np.float32),
        "y_train": y_train,
        "X_test": X_test_scaled.astype(np.float32),
        "y_test": y_test,
        "pca": pca,
        "scaler": scaler,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PneumoniaMNIST Data Pipeline")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    data = load_and_preprocess_data(seed=args.seed)
    print("=== PneumoniaMNIST Preprocessing Summary ===")
    print(f"Random Seed:           {args.seed}")
    print(f"Train samples:         {data['X_train'].shape[0]} (Class 0: {(data['y_train'] == 0).sum()}, Class 1: {(data['y_train'] == 1).sum()})")
    print(f"Test samples:          {data['X_test'].shape[0]} (Class 0: {(data['y_test'] == 0).sum()}, Class 1: {(data['y_test'] == 1).sum()})")
    print(f"Number of features:    {data['X_train'].shape[1]}")
    print(f"Feature range train:   [{data['X_train'].min():.4f}, {data['X_train'].max():.4f}] (target: [0, pi = {np.pi:.4f}])")
    print(f"Feature range test:    [{data['X_test'].min():.4f}, {data['X_test'].max():.4f}]")
    print(f"PCA explained variance ratio sum (4 components): {data['pca'].explained_variance_ratio_.sum():.4%}")
