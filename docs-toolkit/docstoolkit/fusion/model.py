"""Logistic regression fusion model. Pure stdlib, no sklearn/numpy."""
import json
import math
import random
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.fusion.features import FusionFeatures


@dataclass
class FusionWeights:
    """Current model weights and training metadata."""
    weights: list[float]        # one per feature in to_vector()
    bias: float = 0.0
    n_training_examples: int = 0
    accuracy: float = 0.0       # last eval accuracy


def _sigmoid(x: float) -> float:
    """Numerically stable sigmoid."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    else:
        z = math.exp(x)
        return z / (1.0 + z)


def _dot(a: list[float], b: list[float]) -> float:
    return sum(ai * bi for ai, bi in zip(a, b))


class LearnedFusion:
    """Logistic regression fusion model. Pure stdlib, no sklearn/numpy.

    Trains on (FusionFeatures, is_relevant: bool) pairs via mini-batch SGD.
    """

    def __init__(
        self,
        n_features: int = 5,   # matches FusionFeatures.to_vector() length
        lr: float = 0.1,
        regularization: float = 0.01,
        seed: int = 42,
    ):
        rng = random.Random(seed)
        self._weights = [rng.gauss(0, 0.01) for _ in range(n_features)]
        self._bias = 0.0
        self._lr = lr
        self._reg = regularization
        self._n_trained = 0

    def fit(
        self,
        training_data: list[tuple],   # list[(FusionFeatures, bool)]
        *,
        epochs: int = 20,
        batch_size: int = 32,
        seed: int = 42,
    ) -> FusionWeights:
        """Train via mini-batch SGD with L2 regularization.

        For each epoch:
        1. Shuffle training data (with seed)
        2. For each mini-batch:
           - For each (features, label): compute sigmoid(dot(weights, x) + bias)
           - gradient = (pred - label) * x_i + reg * w_i
           - Update: w_i -= lr * gradient
           - Update bias: bias -= lr * (pred - label)
        3. After all epochs: compute accuracy on training data

        Returns FusionWeights with final state.
        """
        rng = random.Random(seed)
        data = list(training_data)
        n = len(data)

        for _ in range(epochs):
            rng.shuffle(data)
            for batch_start in range(0, n, batch_size):
                batch = data[batch_start: batch_start + batch_size]
                # Accumulate gradients over the batch
                grad_w = [0.0] * len(self._weights)
                grad_b = 0.0
                for features, label in batch:
                    x = features.to_vector()
                    pred = _sigmoid(_dot(self._weights, x) + self._bias)
                    error = pred - float(label)
                    for i, xi in enumerate(x):
                        grad_w[i] += error * xi + self._reg * self._weights[i]
                    grad_b += error
                # Apply averaged gradients
                m = len(batch)
                for i in range(len(self._weights)):
                    self._weights[i] -= self._lr * grad_w[i] / m
                self._bias -= self._lr * grad_b / m

        self._n_trained = n

        # Compute accuracy on training data
        correct = 0
        for features, label in data:
            pred = self.score(features)
            predicted_label = pred >= 0.5
            if predicted_label == bool(label):
                correct += 1
        accuracy = correct / n if n > 0 else 0.0

        return FusionWeights(
            weights=list(self._weights),
            bias=self._bias,
            n_training_examples=n,
            accuracy=accuracy,
        )

    def score(self, features: FusionFeatures) -> float:
        """Predict relevance probability (0-1) for a FusionFeatures."""
        x = features.to_vector()
        return _sigmoid(_dot(self._weights, x) + self._bias)

    def explain(self, features: FusionFeatures) -> dict[str, float]:
        """SHAP-like: feature name -> contribution to score.
        contribution[i] = weight[i] * x[i]
        """
        names = ["bm25", "dense", "graph", "query_len", "passage_len"]
        x = features.to_vector()
        return {names[i]: self._weights[i] * x[i] for i in range(len(x))}

    def save(self, path: str | Path) -> None:
        """Save weights to JSON."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "weights": self._weights,
            "bias": self._bias,
            "n_trained": self._n_trained,
            "lr": self._lr,
            "regularization": self._reg,
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "LearnedFusion":
        """Load weights from JSON."""
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        n_features = len(data["weights"])
        instance = cls(
            n_features=n_features,
            lr=data.get("lr", 0.1),
            regularization=data.get("regularization", 0.01),
        )
        instance._weights = data["weights"]
        instance._bias = data["bias"]
        instance._n_trained = data.get("n_trained", 0)
        return instance

    def weights_snapshot(self) -> FusionWeights:
        """Current state as FusionWeights dataclass."""
        return FusionWeights(
            weights=list(self._weights),
            bias=self._bias,
            n_training_examples=self._n_trained,
            accuracy=0.0,
        )
