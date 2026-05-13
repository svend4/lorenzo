"""Epistemic profile: measure and compare the «voice» of text."""
from docstoolkit.epistemic.profile import (
    EpistemicProfile, measure_profile, aggregate_profiles,
)
from docstoolkit.epistemic.distance import voice_distance, VoiceComparison
from docstoolkit.epistemic.analyzer import CorpusVoice, analyze_corpus_voice

__all__ = [
    "EpistemicProfile", "measure_profile", "aggregate_profiles",
    "voice_distance", "VoiceComparison",
    "CorpusVoice", "analyze_corpus_voice",
]
