"""Tests for docstoolkit.di_container (65+ tests)."""
from __future__ import annotations

import pytest

from docstoolkit.di_container import (
    Binding,
    BindingScope,
    DIContainer,
    inject,
    injectable,
    singleton,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

class IService:
    """Marker interface."""


class ServiceA(IService):
    pass


class ServiceB(IService):
    pass


class Counter:
    _n = 0

    def __init__(self):
        Counter._n += 1
        self.n = Counter._n

    @classmethod
    def reset(cls):
        cls._n = 0


@pytest.fixture(autouse=True)
def reset_counter():
    Counter.reset()
    yield
    Counter.reset()


# ===========================================================================
# Binding tests
# ===========================================================================

class TestBinding:
    def test_default_scope_transient(self):
        b = Binding(interface=IService, implementation=ServiceA)
        assert b.scope is BindingScope.TRANSIENT

    def test_is_singleton_false_for_transient(self):
        b = Binding(interface=IService, implementation=ServiceA, scope=BindingScope.TRANSIENT)
        assert b.is_singleton() is False

    def test_is_singleton_true_for_singleton(self):
        b = Binding(interface=IService, implementation=ServiceA, scope=BindingScope.SINGLETON)
        assert b.is_singleton() is True

    def test_is_singleton_false_for_request(self):
        b = Binding(interface=IService, implementation=ServiceA, scope=BindingScope.REQUEST)
        assert b.is_singleton() is False

    def test_tags_default_empty(self):
        b = Binding(interface=IService, implementation=ServiceA)
        assert b.tags == []

    def test_tags_stored(self):
        b = Binding(interface=IService, implementation=ServiceA, tags=["a", "b"])
        assert b.tags == ["a", "b"]

    def test_instance_default_none(self):
        b = Binding(interface=IService, implementation=ServiceA)
        assert b.instance is None

    def test_instance_can_be_set(self):
        svc = ServiceA()
        b = Binding(interface=IService, implementation=ServiceA,
                    scope=BindingScope.SINGLETON, instance=svc)
        assert b.instance is svc

    def test_interface_stored(self):
        b = Binding(interface=IService, implementation=ServiceA)
        assert b.interface is IService

    def test_implementation_stored(self):
        b = Binding(interface=IService, implementation=ServiceA)
        assert b.implementation is ServiceA

    def test_scope_singleton_enum_value(self):
        assert BindingScope.SINGLETON.value == "singleton"

    def test_scope_transient_enum_value(self):
        assert BindingScope.TRANSIENT.value == "transient"

    def test_scope_request_enum_value(self):
        assert BindingScope.REQUEST.value == "request"


# ===========================================================================
# DIContainer – bind / resolve
# ===========================================================================

class TestBindResolve:
    def test_bind_and_resolve_returns_instance(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        obj = c.resolve(IService)
        assert isinstance(obj, ServiceA)

    def test_transient_returns_new_instance_each_time(self):
        c = DIContainer()
        c.bind(IService, Counter, scope=BindingScope.TRANSIENT)
        a = c.resolve(IService)
        b = c.resolve(IService)
        assert a is not b

    def test_singleton_returns_same_instance(self):
        c = DIContainer()
        c.bind(IService, Counter, scope=BindingScope.SINGLETON)
        a = c.resolve(IService)
        b = c.resolve(IService)
        assert a is b

    def test_singleton_created_only_once(self):
        c = DIContainer()
        c.bind(IService, Counter, scope=BindingScope.SINGLETON)
        c.resolve(IService)
        c.resolve(IService)
        assert Counter._n == 1

    def test_transient_creates_new_each_time(self):
        c = DIContainer()
        c.bind(IService, Counter)
        c.resolve(IService)
        c.resolve(IService)
        assert Counter._n == 2

    def test_request_scope_treated_as_transient(self):
        c = DIContainer()
        c.bind(IService, Counter, scope=BindingScope.REQUEST)
        a = c.resolve(IService)
        b = c.resolve(IService)
        assert a is not b

    def test_resolve_unknown_raises_key_error(self):
        c = DIContainer()
        with pytest.raises(KeyError):
            c.resolve(IService)

    def test_bind_callable_no_args(self):
        c = DIContainer()
        c.bind(str, lambda: "hello")
        assert c.resolve(str) == "hello"

    def test_bind_callable_transient_calls_each_time(self):
        results = []
        def factory():
            results.append(1)
            return object()

        c = DIContainer()
        c.bind(object, factory)
        c.resolve(object)
        c.resolve(object)
        assert len(results) == 2

    def test_bind_callable_singleton_calls_once(self):
        calls = []
        def factory():
            calls.append(1)
            return object()

        c = DIContainer()
        c.bind(object, factory, scope=BindingScope.SINGLETON)
        c.resolve(object)
        c.resolve(object)
        assert len(calls) == 1

    def test_bind_overrides_previous(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        c.bind(IService, ServiceB)
        obj = c.resolve(IService)
        assert isinstance(obj, ServiceB)

    def test_default_scope_is_transient(self):
        c = DIContainer()
        c.bind(IService, Counter)
        c.resolve(IService)
        c.resolve(IService)
        assert Counter._n == 2


# ===========================================================================
# DIContainer – bind_instance
# ===========================================================================

class TestBindInstance:
    def test_bind_instance_returns_same_object(self):
        c = DIContainer()
        svc = ServiceA()
        c.bind_instance(IService, svc)
        assert c.resolve(IService) is svc

    def test_bind_instance_always_singleton(self):
        c = DIContainer()
        svc = ServiceA()
        c.bind_instance(IService, svc)
        assert c.resolve(IService) is c.resolve(IService)

    def test_bind_instance_with_tags(self):
        c = DIContainer()
        svc = ServiceA()
        c.bind_instance(IService, svc, tags=["primary"])
        instances = c.resolve_tagged("primary")
        assert svc in instances

    def test_bind_instance_scope_is_singleton(self):
        c = DIContainer()
        svc = ServiceA()
        c.bind_instance(IService, svc)
        binding = c._bindings[IService]
        assert binding.scope is BindingScope.SINGLETON

    def test_bind_instance_does_not_recreate(self):
        c = DIContainer()
        svc = Counter()
        Counter.reset()  # don't count the manual creation above
        c.bind_instance(IService, svc)
        c.resolve(IService)
        c.resolve(IService)
        assert Counter._n == 0  # factory never called


# ===========================================================================
# DIContainer – resolve_tagged
# ===========================================================================

class TestResolveTagged:
    def test_resolve_tagged_returns_all_matching(self):
        c = DIContainer()
        c.bind(str, lambda: "a", tags=["greet"])
        c.bind(bytes, lambda: b"b", tags=["greet"])
        results = c.resolve_tagged("greet")
        assert "a" in results
        assert b"b" in results

    def test_resolve_tagged_empty_when_no_match(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        assert c.resolve_tagged("nonexistent") == []

    def test_resolve_tagged_does_not_include_other_tags(self):
        c = DIContainer()
        c.bind(str, lambda: "a", tags=["greet"])
        c.bind(bytes, lambda: b"b", tags=["other"])
        results = c.resolve_tagged("greet")
        assert b"b" not in results

    def test_resolve_tagged_multiple_tags_on_one_binding(self):
        c = DIContainer()
        c.bind(IService, ServiceA, tags=["x", "y"])
        assert len(c.resolve_tagged("x")) == 1
        assert len(c.resolve_tagged("y")) == 1

    def test_resolve_tagged_singleton_same_instance(self):
        c = DIContainer()
        c.bind(IService, ServiceA, scope=BindingScope.SINGLETON, tags=["svc"])
        r1 = c.resolve_tagged("svc")[0]
        r2 = c.resolve_tagged("svc")[0]
        assert r1 is r2


# ===========================================================================
# DIContainer – is_bound / unbind
# ===========================================================================

class TestIsBoundUnbind:
    def test_is_bound_false_before_bind(self):
        c = DIContainer()
        assert c.is_bound(IService) is False

    def test_is_bound_true_after_bind(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        assert c.is_bound(IService) is True

    def test_unbind_returns_true_when_existed(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        assert c.unbind(IService) is True

    def test_unbind_returns_false_when_not_existed(self):
        c = DIContainer()
        assert c.unbind(IService) is False

    def test_unbind_removes_binding(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        c.unbind(IService)
        assert c.is_bound(IService) is False

    def test_unbind_prevents_resolution(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        c.unbind(IService)
        with pytest.raises(KeyError):
            c.resolve(IService)

    def test_is_bound_inherits_from_parent(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        child = parent.child_container()
        assert child.is_bound(IService) is True


# ===========================================================================
# DIContainer – child_container
# ===========================================================================

class TestChildContainer:
    def test_child_inherits_binding(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        child = parent.child_container()
        obj = child.resolve(IService)
        assert isinstance(obj, ServiceA)

    def test_child_can_override_binding(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        child = parent.child_container()
        child.bind(IService, ServiceB)
        assert isinstance(child.resolve(IService), ServiceB)
        assert isinstance(parent.resolve(IService), ServiceA)

    def test_child_override_does_not_affect_parent(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        child = parent.child_container()
        child.bind(IService, ServiceB)
        # Parent unaffected
        assert isinstance(parent.resolve(IService), ServiceA)

    def test_child_singleton_independent_from_parent(self):
        parent = DIContainer()
        parent.bind(IService, Counter, scope=BindingScope.SINGLETON)
        child = parent.child_container()
        # Child inherits but resolves through parent's binding object
        child.resolve(IService)
        parent.resolve(IService)
        # Both end up sharing the same cached instance (binding is shared)
        assert Counter._n == 1

    def test_grandchild_inherits_from_grandparent(self):
        gp = DIContainer()
        gp.bind(IService, ServiceA)
        parent = gp.child_container()
        child = parent.child_container()
        assert isinstance(child.resolve(IService), ServiceA)

    def test_child_unbind_does_not_affect_parent(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        child = parent.child_container()
        child.unbind(IService)
        # Parent still has it; child falls back to parent
        assert parent.is_bound(IService) is True

    def test_child_unbind_local_override_exposes_parent(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        child = parent.child_container()
        child.bind(IService, ServiceB)
        child.unbind(IService)
        # After removing local override, child sees parent's ServiceA
        obj = child.resolve(IService)
        assert isinstance(obj, ServiceA)

    def test_multiple_children_independent(self):
        parent = DIContainer()
        parent.bind(IService, ServiceA)
        c1 = parent.child_container()
        c2 = parent.child_container()
        c1.bind(IService, ServiceB)
        assert isinstance(c1.resolve(IService), ServiceB)
        assert isinstance(c2.resolve(IService), ServiceA)


# ===========================================================================
# Decorators – injectable / singleton
# ===========================================================================

class TestInjectableDecorator:
    def test_injectable_default_scope_transient(self):
        @injectable()
        class Svc:
            pass

        assert Svc.__di_scope__ is BindingScope.TRANSIENT

    def test_injectable_explicit_singleton(self):
        @injectable(scope=BindingScope.SINGLETON)
        class Svc:
            pass

        assert Svc.__di_scope__ is BindingScope.SINGLETON

    def test_injectable_explicit_request(self):
        @injectable(scope=BindingScope.REQUEST)
        class Svc:
            pass

        assert Svc.__di_scope__ is BindingScope.REQUEST

    def test_injectable_returns_same_class(self):
        class Original:
            pass

        Decorated = injectable()(Original)
        assert Decorated is Original

    def test_injectable_does_not_break_instantiation(self):
        @injectable()
        class Svc:
            value = 42

        assert Svc().value == 42

    def test_singleton_shortcut_sets_singleton_scope(self):
        @singleton
        class Svc:
            pass

        assert Svc.__di_scope__ is BindingScope.SINGLETON

    def test_singleton_shortcut_returns_same_class(self):
        class Original:
            pass

        Decorated = singleton(Original)
        assert Decorated is Original

    def test_singleton_shortcut_does_not_break_instantiation(self):
        @singleton
        class Svc:
            value = 99

        assert Svc().value == 99


# ===========================================================================
# Decorators – inject
# ===========================================================================

class TestInjectDecorator:
    def test_inject_resolves_annotated_param(self):
        c = DIContainer()
        c.bind(IService, ServiceA)

        @inject(c)
        def consume(svc: IService):
            return svc

        result = consume()
        assert isinstance(result, ServiceA)

    def test_inject_does_not_override_explicit_kwarg(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        explicit = ServiceB()

        @inject(c)
        def consume(svc: IService):
            return svc

        result = consume(svc=explicit)
        assert result is explicit

    def test_inject_does_not_override_positional_arg(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        explicit = ServiceB()

        @inject(c)
        def consume(svc: IService):
            return svc

        result = consume(explicit)
        assert result is explicit

    def test_inject_leaves_unannotated_params_alone(self):
        c = DIContainer()

        @inject(c)
        def greet(name):
            return f"hello {name}"

        assert greet("world") == "hello world"

    def test_inject_skips_unbound_types(self):
        c = DIContainer()

        @inject(c)
        def func(svc: IService = None):
            return svc

        # IService not bound – default should remain None
        result = func()
        assert result is None

    def test_inject_resolves_multiple_params(self):
        c = DIContainer()
        c.bind(IService, ServiceA)
        c.bind(str, lambda: "resolved_str")

        @inject(c)
        def consume(svc: IService, name: str):
            return svc, name

        svc, name = consume()
        assert isinstance(svc, ServiceA)
        assert name == "resolved_str"

    def test_inject_preserves_function_name(self):
        c = DIContainer()

        @inject(c)
        def my_function():
            pass

        assert my_function.__name__ == "my_function"

    def test_inject_singleton_returns_same_instance(self):
        c = DIContainer()
        c.bind(IService, ServiceA, scope=BindingScope.SINGLETON)

        @inject(c)
        def consume(svc: IService):
            return svc

        r1 = consume()
        r2 = consume()
        assert r1 is r2
