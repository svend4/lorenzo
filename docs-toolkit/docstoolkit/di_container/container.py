"""Dependency injection container."""
from __future__ import annotations

import inspect
from typing import Any

from docstoolkit.di_container.binding import Binding, BindingScope


class DIContainer:
    """A lightweight dependency injection container.

    Supports TRANSIENT and SINGLETON scopes, tagged bindings,
    pre-built instance registration, and child containers.
    """

    def __init__(self, _parent: "DIContainer | None" = None) -> None:
        self._bindings: dict[type, Binding] = {}
        self._parent = _parent

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def bind(
        self,
        interface: type,
        implementation: type | Any,
        scope: BindingScope = BindingScope.TRANSIENT,
        tags: list[str] | None = None,
    ) -> None:
        """Register *implementation* for *interface* with the given scope."""
        self._bindings[interface] = Binding(
            interface=interface,
            implementation=implementation,
            scope=scope,
            tags=list(tags) if tags else [],
        )

    def bind_instance(
        self,
        interface: type,
        instance: Any,
        tags: list[str] | None = None,
    ) -> None:
        """Register a pre-built *instance* as a SINGLETON for *interface*."""
        binding = Binding(
            interface=interface,
            implementation=type(instance),
            scope=BindingScope.SINGLETON,
            instance=instance,
            tags=list(tags) if tags else [],
        )
        self._bindings[interface] = binding

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def _get_binding(self, interface: type) -> Binding | None:
        """Look up a binding locally, then in the parent chain."""
        if interface in self._bindings:
            return self._bindings[interface]
        if self._parent is not None:
            return self._parent._get_binding(interface)
        return None

    def resolve(self, interface: type) -> Any:
        """Resolve *interface* to a concrete instance.

        * SINGLETON — create once and cache; subsequent calls return the same
          object.
        * TRANSIENT / REQUEST — create a fresh instance on every call.
        * For callables (non-class): call with no arguments.
        * For classes: instantiate with no arguments (no auto-wiring).
        """
        binding = self._get_binding(interface)
        if binding is None:
            raise KeyError(f"No binding registered for {interface!r}")

        if binding.scope is BindingScope.SINGLETON:
            if binding.instance is None:
                binding.instance = self._create(binding.implementation)
            return binding.instance

        # TRANSIENT or REQUEST
        return self._create(binding.implementation)

    @staticmethod
    def _create(implementation: Any) -> Any:
        """Instantiate a class or call a plain callable."""
        if inspect.isclass(implementation):
            return implementation()
        # Plain callable (function, lambda, …)
        return implementation()

    # ------------------------------------------------------------------
    # Tag-based resolution
    # ------------------------------------------------------------------

    def resolve_tagged(self, tag: str) -> list:
        """Return resolved instances for every binding carrying *tag*.

        Searches local bindings only (not the parent chain), so child
        containers can narrow the result set.
        """
        # Collect all bindings reachable from this container
        all_bindings: dict[type, Binding] = {}
        # Walk up the parent chain first so local bindings win
        node: DIContainer | None = self._parent
        while node is not None:
            for iface, b in node._bindings.items():
                if iface not in all_bindings:
                    all_bindings[iface] = b
            node = node._parent
        # Local bindings override
        all_bindings.update(self._bindings)

        return [
            self.resolve(iface)
            for iface, b in all_bindings.items()
            if tag in b.tags
        ]

    # ------------------------------------------------------------------
    # Introspection / management
    # ------------------------------------------------------------------

    def is_bound(self, interface: type) -> bool:
        """Return True if *interface* has a binding (local or inherited)."""
        return self._get_binding(interface) is not None

    def unbind(self, interface: type) -> bool:
        """Remove a local binding.  Returns True if one existed."""
        if interface in self._bindings:
            del self._bindings[interface]
            return True
        return False

    # ------------------------------------------------------------------
    # Child containers
    # ------------------------------------------------------------------

    def child_container(self) -> "DIContainer":
        """Create a child container that inherits all bindings from self.

        The child may override any binding without affecting the parent.
        """
        return DIContainer(_parent=self)
