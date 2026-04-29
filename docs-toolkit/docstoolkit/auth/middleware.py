"""Auth middleware для serve.py."""
from dataclasses import dataclass


@dataclass
class AuthContext:
    """Текущий пользователь / API key."""
    name: str
    scopes: list[str]
    key_id: int = 0
    is_admin: bool = False


def extract_token(headers: dict) -> str | None:
    """Извлекает Bearer / X-API-Key из headers.

    Поддерживает:
      - Authorization: Bearer dt_xxx
      - X-API-Key: dt_xxx
    """
    auth = headers.get("Authorization", "") or headers.get("authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()

    api_key = headers.get("X-API-Key", "") or headers.get("x-api-key", "")
    if api_key:
        return api_key.strip()

    return None


def authenticate(token: str | None, store=None) -> AuthContext | None:
    """Возвращает AuthContext или None.

    Если token пустой — None (handler решает как реагировать).
    """
    if not token:
        return None

    if store is None:
        from docstoolkit.auth.keys import KeyStore
        store = KeyStore()

    api_key = store.verify(token)
    if not api_key:
        return None

    is_admin = "*" in api_key.scopes or "admin:*" in api_key.scopes
    return AuthContext(
        name=api_key.name,
        scopes=api_key.scopes,
        key_id=api_key.id,
        is_admin=is_admin,
    )
