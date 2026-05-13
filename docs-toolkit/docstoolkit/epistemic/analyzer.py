"""Corpus-level voice analysis."""

from dataclasses import dataclass, field
from docstoolkit.epistemic.profile import EpistemicProfile, measure_profile, aggregate_profiles
from docstoolkit.epistemic.distance import voice_distance, VoiceComparison


@dataclass
class CorpusVoice:
    """Aggregated voice model for a corpus of documents."""

    profile: EpistemicProfile
    doc_profiles: dict[str, EpistemicProfile] = field(default_factory=dict)
    outliers: list[str] = field(default_factory=list)

    def fits_voice(self, text: str, threshold: float = 0.4) -> bool:
        """Return True if *text*'s profile is within *threshold* distance of corpus."""
        doc_profile = measure_profile(text)
        cmp = voice_distance(doc_profile, self.profile)
        return cmp.distance <= threshold

    def voice_score(self, text: str) -> float:
        """Return similarity score (0–1) between *text* and the corpus voice."""
        doc_profile = measure_profile(text)
        cmp = voice_distance(doc_profile, self.profile)
        return cmp.similarity


def analyze_corpus_voice(
    docs: dict[str, str],
    *,
    outlier_threshold: float = 0.5,
) -> CorpusVoice:
    """Measure voice for each document, aggregate, and detect outliers.

    Parameters
    ----------
    docs:
        Mapping of ``{doc_id: content}``.
    outlier_threshold:
        Documents whose voice distance from the corpus profile exceeds this
        value are considered outliers.

    Returns
    -------
    CorpusVoice
        ``profile`` is the mean profile across all documents.
        ``doc_profiles`` maps each doc_id to its individual profile.
        ``outliers`` lists doc_ids whose distance from the corpus > threshold.
    """
    if not docs:
        return CorpusVoice(profile=EpistemicProfile(), doc_profiles={}, outliers=[])

    # 1. Measure each document
    doc_profiles: dict[str, EpistemicProfile] = {
        doc_id: measure_profile(content)
        for doc_id, content in docs.items()
    }

    # 2. Aggregate → corpus profile
    corpus_profile = aggregate_profiles(list(doc_profiles.values()))

    # 3. Find outliers
    outliers = [
        doc_id
        for doc_id, profile in doc_profiles.items()
        if voice_distance(profile, corpus_profile).distance > outlier_threshold
    ]

    return CorpusVoice(
        profile=corpus_profile,
        doc_profiles=doc_profiles,
        outliers=outliers,
    )
