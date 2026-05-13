"""Knowledge diffusion: concepts flow between corpora with provenance."""
from docstoolkit.diffusion.alignment import ConceptAlignment, align_corpora, AlignmentResult
from docstoolkit.diffusion.transfer import DiffusionTransfer, TransferRecord, TransferReport
from docstoolkit.diffusion.provenance import DiffusionProvenance, trace_origin

__all__ = [
    "ConceptAlignment", "align_corpora", "AlignmentResult",
    "DiffusionTransfer", "TransferRecord", "TransferReport",
    "DiffusionProvenance", "trace_origin",
]
