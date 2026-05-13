"""Document clustering module for docs-toolkit (E20).

Pure-stdlib TF-IDF feature extraction and K-Means clustering.
"""

from docstoolkit.clustering.features import (
    DocumentFeatures,
    FeatureExtractor,
)
from docstoolkit.clustering.distance import (
    cosine_similarity,
    cosine_distance,
    jaccard_similarity,
)
from docstoolkit.clustering.kmeans import (
    Cluster,
    KMeansConfig,
    KMeansResult,
    KMeansClustering,
)

__all__ = [
    # features
    "DocumentFeatures",
    "FeatureExtractor",
    # distance
    "cosine_similarity",
    "cosine_distance",
    "jaccard_similarity",
    # kmeans
    "Cluster",
    "KMeansConfig",
    "KMeansResult",
    "KMeansClustering",
]
