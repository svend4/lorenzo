"""E324 DocAttachmentStore — manage file attachments for documents.

Public API
----------
:class:`Attachment`        — a file attachment to a document
:class:`AttachmentStats`   — aggregate statistics
:class:`DocAttachmentStore` — main interface for attachment management
"""

from .store import Attachment, AttachmentStats, DocAttachmentStore

__all__ = ["Attachment", "AttachmentStats", "DocAttachmentStore"]
