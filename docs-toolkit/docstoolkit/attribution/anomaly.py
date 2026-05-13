from dataclasses import dataclass
from docstoolkit.attribution.scorer import AttributionMap


@dataclass
class AnomalyReport:
    is_anomalous: bool
    reason: str                  # "overreliance" | "none" | "balanced"
    dominant_passage_id: str     # passage_id with highest influence, or ""
    dominant_influence: float    # 0-1
    recommendation: str          # human-readable suggestion


def detect_overreliance(
    attribution_map: AttributionMap,
    *,
    threshold: float = 0.5,
) -> AnomalyReport:
    """Detect if one passage dominates the answer.

    If max(influence) > threshold: is_anomalous=True, reason="overreliance"
    Else: is_anomalous=False, reason="balanced"

    recommendation:
    - overreliance: "Consider retrieving more diverse sources for query: {query[:50]}"
    - balanced: "Attribution looks balanced across {n} sources"
    """
    if not attribution_map.scores:
        return AnomalyReport(
            is_anomalous=False,
            reason="balanced",
            dominant_passage_id="",
            dominant_influence=0.0,
            recommendation=f"Attribution looks balanced across 0 sources",
        )

    top = attribution_map.scores[0]  # already sorted by influence desc
    dominant_influence = top.influence
    dominant_passage_id = top.passage_id
    n = len(attribution_map.scores)

    if dominant_influence > threshold:
        return AnomalyReport(
            is_anomalous=True,
            reason="overreliance",
            dominant_passage_id=dominant_passage_id,
            dominant_influence=dominant_influence,
            recommendation=(
                f"Consider retrieving more diverse sources for query: "
                f"{attribution_map.query[:50]}"
            ),
        )
    else:
        return AnomalyReport(
            is_anomalous=False,
            reason="balanced",
            dominant_passage_id=dominant_passage_id,
            dominant_influence=dominant_influence,
            recommendation=f"Attribution looks balanced across {n} sources",
        )
