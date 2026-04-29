"""Authentication + RBAC для docs-toolkit.

3 типа auth:
  - API keys (стандартно для machine-to-machine)
  - Bearer tokens (для UI sessions)
  - None (default — для локального использования)

Scopes (RBAC):
  - read:docs       — чтение документов
  - read:search     — поиск
  - read:graph      — knowledge graph
  - write:docs      — создание/редактирование
  - write:templates — управление шаблонами
  - admin:keys      — управление API keys
  - admin:peers     — federation peers
  - admin:jobs      — работа с jobs queue

Использование:
    from docstoolkit.auth import KeyStore, require_scope

    store = KeyStore()
    key = store.create("alice", scopes=["read:*"])
    # → returns "dt_abc123..." (хранится hash в БД)

    @require_scope("write:docs")
    def my_handler(...):
        pass
"""
from docstoolkit.auth.keys import KeyStore, ApiKey, hash_key, generate_key
from docstoolkit.auth.scopes import (
    Scope, AVAILABLE_SCOPES, scope_matches, require_scope, AuthError,
)
from docstoolkit.auth.middleware import (
    extract_token, authenticate, AuthContext,
)

__all__ = [
    "KeyStore", "ApiKey", "hash_key", "generate_key",
    "Scope", "AVAILABLE_SCOPES", "scope_matches", "require_scope", "AuthError",
    "extract_token", "authenticate", "AuthContext",
]
