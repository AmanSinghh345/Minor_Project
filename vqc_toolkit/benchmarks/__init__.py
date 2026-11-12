from .datasets import load_iris_dataset, load_cancer_dataset
from .classical import evaluate_classical_suite, evaluate_classical_models, SmallMLP

__all__ = [
    "load_iris_dataset",
    "load_cancer_dataset",
    "evaluate_classical_suite",
    "evaluate_classical_models",
    "SmallMLP"
]
