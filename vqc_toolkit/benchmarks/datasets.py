"""
Dataset benchmarking loaders with strict train-test isolation and [0, pi] angle scaling.
"""

from typing import Tuple
import numpy as np
from sklearn.datasets import load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA


def load_iris_dataset(seed: int = 42, test_size: float = 0.25) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads 4-feature Iris dataset for binary classification (Class 0 vs Class 1+2).
    Applies MinMaxScaler fit strictly on train split, scaled to [0, pi].
    """
    iris = load_iris()
    X = iris.data  # 4 features: sepal length/width, petal length/width
    y = (iris.target > 0).astype(int)  # Binary: setosa (0) vs non-setosa (1)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )
    
    scaler = MinMaxScaler(feature_range=(0.0, np.pi))
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = np.clip(scaler.transform(X_test), 0.0, np.pi)
    
    return X_train_scaled, X_test_scaled, y_train, y_test


def load_cancer_dataset(seed: int = 42, test_size: float = 0.25) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads Breast Cancer Wisconsin dataset reduced to 4 PCA components.
    PCA and MinMaxScaler fit strictly on train split to prevent data leakage.
    """
    data = load_breast_cancer()
    X = data.data
    y = data.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )
    
    pca = PCA(n_components=4, random_state=seed)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    
    scaler = MinMaxScaler(feature_range=(0.0, np.pi))
    X_train_scaled = scaler.fit_transform(X_train_pca)
    X_test_scaled = np.clip(scaler.transform(X_test_pca), 0.0, np.pi)
    
    return X_train_scaled, X_test_scaled, y_train, y_test
