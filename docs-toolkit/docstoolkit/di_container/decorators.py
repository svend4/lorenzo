"""Decorators for the DI container."""
from __future__ import annotations

import functools
from typing import Any

from docstoolkit.di_container.binding import BindingScope
from docstoolkit.di_container.container import DIContainer


def injectable(scope: BindingScope = BindingScope.TRANSIENT):
    """Class decorator that marks a class as injectable.

    Sets the ``__di_scope__`` attribute on the decorated class so that
    tooling / container helpers can read the intended scope.

    Usage::

        @injectable(scope=BindingScope.SINGLETON)
        class MyService: ...
    """
    def decorator(cls):
        cls.__di_scope__ = scope
        return cls
    return decorator


# Convenience shortcut
singleton = injectable(scope=BindingScope.SINGLETON)
"""Shortcut for ``@injectable(scope=BindingScope.SINGLETON)``."""


def inject(container: DIContainer):
    """Function decorator that resolves type-annotated parameters from *container*.

    For every parameter that has a type annotation AND is not supplied by the
    caller, the decorator resolves the type from *container* and passes it as
    a keyword argument.

    Parameters that have no annotation, or whose annotated type is not bound
    in the container, are left for the caller to supply.

    Usage::

        @inject(container)
        def start(service: MyService, name: str): ...

        start(name="hello")   # service resolved automatically
    """
    import inspect
    import sys

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)

            # Resolve string annotations to actual types using the function's
            # module globals (handles `from __future__ import annotations`).
            module = sys.modules.get(func.__module__, None)
            globalns = getattr(module, "__dict__", {}) if module else {}
            try:
                hints = inspect.get_annotations(func, globals=globalns, eval_str=True)
            except AttributeError:
                # Python < 3.10 fallback
                import typing
                try:
                    hints = typing.get_type_hints(func, globalns=globalns)
                except Exception:
                    hints = {}

            resolved: dict[str, Any] = {}
            for i, (param_name, param) in enumerate(sig.parameters.items()):
                # Skip already-provided positional args
                if i < len(args):
                    continue
                # Skip already-provided keyword args
                if param_name in kwargs:
                    continue
                # Skip unannotated / return annotation
                if param_name not in hints or param_name == "return":
                    continue
                param_type = hints[param_name]
                # Try to resolve from container
                if container.is_bound(param_type):
                    resolved[param_name] = container.resolve(param_type)

            kwargs = {**resolved, **kwargs}
            return func(*args, **kwargs)

        return wrapper
    return decorator
