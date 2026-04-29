"""RBAC scopes."""
from dataclasses import dataclass


# Все доступные scopes — точечные права
AVAILABLE_SCOPES = {
    "read:docs": "Читать документы",
    "read:search": "Поиск по корпусу",
    "read:graph": "Knowledge graph и метаданные",
    "read:templates": "Список шаблонов",
    "read:health": "Health/dashboard endpoints",
    "write:docs": "Создание/редактирование документов",
    "write:templates": "Управление шаблонами",
    "write:rag": "Запуск RAG (стоит денег)",
    "write:agent": "Запуск agent loop",
    "admin:keys": "Управление API keys",
    "admin:peers": "Federation peers",
    "admin:jobs": "Background jobs queue",
    "admin:config": "Изменение docstoolkit.toml",
    "admin:*": "Полный admin доступ",
    "*": "Полный root доступ",
}


@dataclass
class Scope:
    name: str
    description: str = ""


class AuthError(Exception):
    """Auth/permission ошибка."""


def scope_matches(required: str, granted: list[str]) -> bool:
    """Проверяет, удовлетворяют ли granted scopes required scope.

    Wildcards: 'read:*' даёт все 'read:X'; '*' даёт всё.
    """
    if "*" in granted:
        return True
    if required in granted:
        return True
    # Wildcard в granted: 'read:*' matches 'read:docs'
    if ":" in required:
        prefix, _ = required.split(":", 1)
        if f"{prefix}:*" in granted:
            return True
    return False


def require_scope(scope: str):
    """Декоратор: требует чтобы AuthContext был с указанным scope.

    Использование:
        @require_scope("write:docs")
        def my_handler(ctx: AuthContext, ...):
            ...

    Если auth disabled (нет AuthContext) — пропускает.
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            ctx = kwargs.get("ctx")
            if ctx is None:
                # Try first positional arg
                if args and hasattr(args[0], "scopes"):
                    ctx = args[0]
            if ctx is None:
                # No auth context — assume open mode
                return fn(*args, **kwargs)
            if not scope_matches(scope, ctx.scopes):
                raise AuthError(f"Недостаточно прав: требуется {scope}, "
                                f"granted={ctx.scopes}")
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        return wrapper
    return decorator
