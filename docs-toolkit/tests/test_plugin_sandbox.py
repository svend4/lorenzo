"""Tests for docstoolkit.plugin_sandbox (E80).

Coverage targets
----------------
- SandboxPolicy: defaults and explicit field values
- SandboxResult: fields and defaults
- PluginSandbox.execute: basic execution, _result convention, syntax errors,
  runtime errors, builtin restriction, import restriction, timeout enforcement
- PluginSandbox.call_function: calls named function, passes args/kwargs,
  handles missing function, handles runtime errors in function
- SandboxedPlugin: run delegates to sandbox, validate catches syntax errors
  and missing entry point
- PluginLoader: load_string, load_file
"""
from __future__ import annotations

import os
import tempfile
import time

import pytest

from docstoolkit.plugin_sandbox import (
    PluginLoader,
    PluginMetadata,
    PluginSandbox,
    SandboxedPlugin,
    SandboxPolicy,
    SandboxResult,
)


# ===========================================================================
# SandboxPolicy
# ===========================================================================

class TestSandboxPolicy:
    def test_defaults(self):
        p = SandboxPolicy()
        assert p.allow_builtins is None
        assert p.allow_imports is None
        assert p.max_exec_time == 5.0

    def test_allow_builtins_explicit(self):
        p = SandboxPolicy(allow_builtins=["print", "len"])
        assert p.allow_builtins == ["print", "len"]

    def test_allow_imports_explicit(self):
        p = SandboxPolicy(allow_imports=["math", "os"])
        assert p.allow_imports == ["math", "os"]

    def test_max_exec_time_explicit(self):
        p = SandboxPolicy(max_exec_time=10.0)
        assert p.max_exec_time == 10.0

    def test_all_fields_set(self):
        p = SandboxPolicy(
            allow_builtins=["print"],
            allow_imports=["math"],
            max_exec_time=2.5,
        )
        assert p.allow_builtins == ["print"]
        assert p.allow_imports == ["math"]
        assert p.max_exec_time == 2.5

    def test_empty_allow_builtins(self):
        p = SandboxPolicy(allow_builtins=[])
        assert p.allow_builtins == []

    def test_empty_allow_imports(self):
        p = SandboxPolicy(allow_imports=[])
        assert p.allow_imports == []

    def test_dataclass_is_mutable(self):
        p = SandboxPolicy()
        p.max_exec_time = 3.0
        assert p.max_exec_time == 3.0


# ===========================================================================
# SandboxResult
# ===========================================================================

class TestSandboxResult:
    def test_success_true(self):
        r = SandboxResult(success=True)
        assert r.success is True

    def test_success_false(self):
        r = SandboxResult(success=False)
        assert r.success is False

    def test_defaults(self):
        r = SandboxResult(success=True)
        assert r.return_value is None
        assert r.error == ""
        assert r.duration == 0.0

    def test_return_value(self):
        r = SandboxResult(success=True, return_value=42)
        assert r.return_value == 42

    def test_return_value_complex(self):
        r = SandboxResult(success=True, return_value={"key": [1, 2, 3]})
        assert r.return_value == {"key": [1, 2, 3]}

    def test_error_field(self):
        r = SandboxResult(success=False, error="something went wrong")
        assert r.error == "something went wrong"

    def test_duration_field(self):
        r = SandboxResult(success=True, duration=0.123)
        assert r.duration == pytest.approx(0.123)

    def test_all_fields(self):
        r = SandboxResult(success=True, return_value="hi", error="", duration=1.0)
        assert r.success is True
        assert r.return_value == "hi"
        assert r.error == ""
        assert r.duration == 1.0


# ===========================================================================
# PluginSandbox — execute
# ===========================================================================

class TestPluginSandboxExecute:

    # --- basic execution ---------------------------------------------------

    def test_execute_simple_assignment(self):
        sb = PluginSandbox()
        result = sb.execute("x = 1 + 1")
        assert result.success is True
        assert result.error == ""

    def test_execute_returns_sandbox_result(self):
        sb = PluginSandbox()
        result = sb.execute("pass")
        assert isinstance(result, SandboxResult)

    def test_execute_duration_recorded(self):
        sb = PluginSandbox()
        result = sb.execute("pass")
        assert result.duration >= 0.0

    def test_execute_no_result_var(self):
        sb = PluginSandbox()
        result = sb.execute("x = 99")
        assert result.return_value is None

    # --- _result convention ------------------------------------------------

    def test_execute_result_int(self):
        sb = PluginSandbox()
        result = sb.execute("_result = 42")
        assert result.success is True
        assert result.return_value == 42

    def test_execute_result_string(self):
        sb = PluginSandbox()
        result = sb.execute("_result = 'hello'")
        assert result.return_value == "hello"

    def test_execute_result_list(self):
        sb = PluginSandbox()
        result = sb.execute("_result = [1, 2, 3]")
        assert result.return_value == [1, 2, 3]

    def test_execute_result_dict(self):
        sb = PluginSandbox()
        result = sb.execute("_result = {'a': 1}")
        assert result.return_value == {"a": 1}

    def test_execute_result_none_explicit(self):
        sb = PluginSandbox()
        result = sb.execute("_result = None")
        assert result.success is True
        assert result.return_value is None

    def test_execute_result_computed(self):
        sb = PluginSandbox()
        result = sb.execute("_result = 3 * 7")
        assert result.return_value == 21

    def test_execute_result_from_context(self):
        sb = PluginSandbox()
        result = sb.execute("_result = x + 1", context={"x": 10})
        assert result.return_value == 11

    def test_execute_context_variable_available(self):
        sb = PluginSandbox()
        result = sb.execute("_result = msg", context={"msg": "world"})
        assert result.return_value == "world"

    # --- syntax errors -----------------------------------------------------

    def test_execute_syntax_error(self):
        sb = PluginSandbox()
        result = sb.execute("def broken(:")
        assert result.success is False
        assert "SyntaxError" in result.error

    def test_execute_syntax_error_has_duration(self):
        sb = PluginSandbox()
        result = sb.execute("def broken(:")
        assert result.duration >= 0.0

    def test_execute_syntax_error_return_value_none(self):
        sb = PluginSandbox()
        result = sb.execute("def broken(:")
        assert result.return_value is None

    # --- runtime errors ----------------------------------------------------

    def test_execute_runtime_name_error(self):
        sb = PluginSandbox()
        result = sb.execute("_result = undefined_variable")
        assert result.success is False
        assert "NameError" in result.error

    def test_execute_runtime_zero_division(self):
        sb = PluginSandbox()
        result = sb.execute("_result = 1 / 0")
        assert result.success is False
        assert "ZeroDivisionError" in result.error

    def test_execute_runtime_type_error(self):
        sb = PluginSandbox()
        result = sb.execute("_result = 'a' + 1")
        assert result.success is False
        assert "TypeError" in result.error

    def test_execute_runtime_value_error(self):
        sb = PluginSandbox()
        result = sb.execute("_result = int('not_a_number')")
        assert result.success is False
        assert "ValueError" in result.error

    # --- builtin restriction -----------------------------------------------

    def test_execute_builtin_restriction_allowed(self):
        policy = SandboxPolicy(allow_builtins=["len", "range", "list"])
        sb = PluginSandbox(policy)
        result = sb.execute("_result = len([1, 2, 3])")
        assert result.success is True
        assert result.return_value == 3

    def test_execute_builtin_restriction_blocked(self):
        policy = SandboxPolicy(allow_builtins=["len"])
        sb = PluginSandbox(policy)
        # 'print' not in allow list
        result = sb.execute("print('hello')")
        assert result.success is False

    def test_execute_builtin_empty_list_blocks_all(self):
        policy = SandboxPolicy(allow_builtins=[])
        sb = PluginSandbox(policy)
        result = sb.execute("len([1, 2, 3])")
        assert result.success is False

    def test_execute_builtin_none_allows_all(self):
        policy = SandboxPolicy(allow_builtins=None)
        sb = PluginSandbox(policy)
        result = sb.execute("_result = len('hello')")
        assert result.success is True
        assert result.return_value == 5

    def test_execute_builtin_int_allowed(self):
        policy = SandboxPolicy(allow_builtins=["int", "str"])
        sb = PluginSandbox(policy)
        result = sb.execute("_result = int('42')")
        assert result.success is True
        assert result.return_value == 42

    def test_execute_multiple_builtins_allowed(self):
        policy = SandboxPolicy(allow_builtins=["len", "list", "range", "sum"])
        sb = PluginSandbox(policy)
        result = sb.execute("_result = sum(range(5))")
        assert result.success is True
        assert result.return_value == 10

    # --- import restriction ------------------------------------------------

    def test_execute_import_allowed(self):
        policy = SandboxPolicy(allow_imports=["math"])
        sb = PluginSandbox(policy)
        result = sb.execute("import math\n_result = math.floor(3.9)")
        assert result.success is True
        assert result.return_value == 3

    def test_execute_import_blocked(self):
        policy = SandboxPolicy(allow_imports=["math"])
        sb = PluginSandbox(policy)
        result = sb.execute("import os")
        assert result.success is False
        assert "ImportError" in result.error or "not allowed" in result.error

    def test_execute_import_none_allows_all(self):
        policy = SandboxPolicy(allow_imports=None)
        sb = PluginSandbox(policy)
        result = sb.execute("import math\n_result = math.pi")
        assert result.success is True
        assert result.return_value == pytest.approx(3.14159, rel=1e-4)

    def test_execute_import_empty_list_blocks_all(self):
        policy = SandboxPolicy(allow_imports=[])
        sb = PluginSandbox(policy)
        result = sb.execute("import math")
        assert result.success is False

    def test_execute_import_submodule_blocked_by_parent(self):
        policy = SandboxPolicy(allow_imports=["os"])
        sb = PluginSandbox(policy)
        # submodule "os.path" has top-level "os" which is allowed
        result = sb.execute("import os.path\n_result = True")
        assert result.success is True

    def test_execute_import_disallowed_submodule(self):
        policy = SandboxPolicy(allow_imports=["math"])
        sb = PluginSandbox(policy)
        result = sb.execute("import os.path")
        assert result.success is False

    # --- timeout enforcement -----------------------------------------------

    def test_execute_timeout(self):
        policy = SandboxPolicy(max_exec_time=0.2)
        sb = PluginSandbox(policy)
        result = sb.execute("while True: pass")
        assert result.success is False
        assert result.error == "timeout"

    def test_execute_timeout_duration_reasonable(self):
        policy = SandboxPolicy(max_exec_time=0.2)
        sb = PluginSandbox(policy)
        t0 = time.monotonic()
        result = sb.execute("while True: pass")
        elapsed = time.monotonic() - t0
        assert result.error == "timeout"
        # Should not take much longer than the timeout
        assert elapsed < 2.0

    def test_execute_no_timeout_fast_code(self):
        policy = SandboxPolicy(max_exec_time=5.0)
        sb = PluginSandbox(policy)
        result = sb.execute("_result = 1")
        assert result.success is True


# ===========================================================================
# PluginSandbox — call_function
# ===========================================================================

class TestPluginSandboxCallFunction:

    def test_call_function_basic(self):
        sb = PluginSandbox()
        code = "def greet(): return 'hello'"
        result = sb.call_function(code, "greet")
        assert result.success is True
        assert result.return_value == "hello"

    def test_call_function_with_args(self):
        sb = PluginSandbox()
        code = "def add(a, b): return a + b"
        result = sb.call_function(code, "add", 3, 4)
        assert result.success is True
        assert result.return_value == 7

    def test_call_function_with_kwargs(self):
        sb = PluginSandbox()
        code = "def greet(name='world'): return 'hello ' + name"
        result = sb.call_function(code, "greet", name="Alice")
        assert result.success is True
        assert result.return_value == "hello Alice"

    def test_call_function_mixed_args_kwargs(self):
        sb = PluginSandbox()
        code = "def compute(x, y, factor=1): return (x + y) * factor"
        result = sb.call_function(code, "compute", 2, 3, factor=10)
        assert result.success is True
        assert result.return_value == 50

    def test_call_function_missing_function(self):
        sb = PluginSandbox()
        code = "x = 1"
        result = sb.call_function(code, "nonexistent")
        assert result.success is False
        assert "nonexistent" in result.error

    def test_call_function_syntax_error_in_code(self):
        sb = PluginSandbox()
        code = "def broken(:"
        result = sb.call_function(code, "broken")
        assert result.success is False
        assert "SyntaxError" in result.error

    def test_call_function_runtime_error_in_function(self):
        sb = PluginSandbox()
        code = "def bad(): return 1 / 0"
        result = sb.call_function(code, "bad")
        assert result.success is False
        assert "ZeroDivisionError" in result.error

    def test_call_function_returns_none(self):
        sb = PluginSandbox()
        code = "def noop(): pass"
        result = sb.call_function(code, "noop")
        assert result.success is True
        assert result.return_value is None

    def test_call_function_with_context(self):
        sb = PluginSandbox()
        code = "def double(): return value * 2"
        result = sb.call_function(code, "double", context={"value": 21})
        assert result.success is True
        assert result.return_value == 42

    def test_call_function_timeout(self):
        policy = SandboxPolicy(max_exec_time=0.2)
        sb = PluginSandbox(policy)
        code = "def infinite(): \n    while True: pass"
        result = sb.call_function(code, "infinite")
        assert result.success is False
        assert result.error == "timeout"

    def test_call_function_returns_list(self):
        sb = PluginSandbox()
        code = "def items(): return [1, 2, 3]"
        result = sb.call_function(code, "items")
        assert result.success is True
        assert result.return_value == [1, 2, 3]

    def test_call_function_returns_dict(self):
        sb = PluginSandbox()
        code = "def config(): return {'key': 'value'}"
        result = sb.call_function(code, "config")
        assert result.success is True
        assert result.return_value == {"key": "value"}

    def test_call_function_duration_recorded(self):
        sb = PluginSandbox()
        code = "def fast(): return 1"
        result = sb.call_function(code, "fast")
        assert result.duration >= 0.0

    def test_call_function_nested_function(self):
        sb = PluginSandbox()
        code = (
            "def outer():\n"
            "    def inner(x): return x * 2\n"
            "    return inner(5)\n"
        )
        result = sb.call_function(code, "outer")
        assert result.success is True
        assert result.return_value == 10


# ===========================================================================
# PluginMetadata
# ===========================================================================

class TestPluginMetadata:
    def test_defaults(self):
        m = PluginMetadata(name="my-plugin")
        assert m.name == "my-plugin"
        assert m.version == "0.0.1"
        assert m.description == ""
        assert m.entry_point == "run"

    def test_explicit_fields(self):
        m = PluginMetadata(
            name="test",
            version="1.2.3",
            description="A test plugin",
            entry_point="main",
        )
        assert m.version == "1.2.3"
        assert m.description == "A test plugin"
        assert m.entry_point == "main"

    def test_name_required(self):
        with pytest.raises(TypeError):
            PluginMetadata()  # type: ignore[call-arg]


# ===========================================================================
# SandboxedPlugin
# ===========================================================================

class TestSandboxedPlugin:

    # --- run ---------------------------------------------------------------

    def test_run_delegates_to_sandbox(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(): return 'ok'"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        result = plugin.run()
        assert result.success is True
        assert result.return_value == "ok"

    def test_run_passes_args(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(x, y): return x + y"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        result = plugin.run(10, 20)
        assert result.return_value == 30

    def test_run_passes_kwargs(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(greeting='hi'): return greeting"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        result = plugin.run(greeting="hello")
        assert result.return_value == "hello"

    def test_run_returns_sandbox_result(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(): pass"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        result = plugin.run()
        assert isinstance(result, SandboxResult)

    def test_run_custom_entry_point(self):
        meta = PluginMetadata(name="test", entry_point="execute")
        code = "def execute(): return 'custom'"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        result = plugin.run()
        assert result.success is True
        assert result.return_value == "custom"

    def test_run_uses_provided_sandbox(self):
        policy = SandboxPolicy(allow_builtins=["len"])
        sandbox = PluginSandbox(policy)
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(): return len([1, 2])"
        plugin = SandboxedPlugin(metadata=meta, code=code, sandbox=sandbox)
        result = plugin.run()
        assert result.success is True
        assert result.return_value == 2

    def test_run_error_propagated(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(): raise ValueError('boom')"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        result = plugin.run()
        assert result.success is False
        assert "ValueError" in result.error

    # --- validate ----------------------------------------------------------

    def test_validate_valid_plugin(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(): return 1"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        errors = plugin.validate()
        assert errors == []

    def test_validate_syntax_error(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(:"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        errors = plugin.validate()
        assert len(errors) == 1
        assert "SyntaxError" in errors[0]

    def test_validate_missing_entry_point(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def other_function(): pass"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        errors = plugin.validate()
        assert len(errors) == 1
        assert "run" in errors[0]

    def test_validate_missing_custom_entry_point(self):
        meta = PluginMetadata(name="test", entry_point="process")
        code = "def run(): pass"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        errors = plugin.validate()
        assert any("process" in e for e in errors)

    def test_validate_returns_list(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def run(): pass"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        assert isinstance(plugin.validate(), list)

    def test_validate_syntax_error_skips_entry_point_check(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def broken(:"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        errors = plugin.validate()
        # Only one error (syntax), not two
        assert len(errors) == 1

    def test_validate_empty_code_missing_entry_point(self):
        meta = PluginMetadata(name="test", entry_point="run")
        plugin = SandboxedPlugin(metadata=meta, code="")
        errors = plugin.validate()
        assert len(errors) == 1
        assert "run" in errors[0]

    def test_validate_multiple_functions_entry_present(self):
        meta = PluginMetadata(name="test", entry_point="run")
        code = "def helper(): pass\ndef run(): return helper()"
        plugin = SandboxedPlugin(metadata=meta, code=code)
        assert plugin.validate() == []


# ===========================================================================
# PluginLoader
# ===========================================================================

class TestPluginLoader:

    def test_load_string_returns_sandboxed_plugin(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_string("def run(): return 1", meta)
        assert isinstance(plugin, SandboxedPlugin)

    def test_load_string_code_stored(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        code = "def run(): return 1"
        plugin = loader.load_string(code, meta)
        assert plugin.code == code

    def test_load_string_metadata_stored(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="my-plugin", version="2.0.0")
        plugin = loader.load_string("def run(): pass", meta)
        assert plugin.metadata is meta

    def test_load_string_default_sandbox(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_string("def run(): pass", meta)
        assert isinstance(plugin.sandbox, PluginSandbox)

    def test_load_string_custom_sandbox(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        policy = SandboxPolicy(max_exec_time=1.0)
        sandbox = PluginSandbox(policy)
        plugin = loader.load_string("def run(): pass", meta, sandbox=sandbox)
        assert plugin.sandbox is sandbox

    def test_load_string_runnable(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_string("def run(): return 'loaded'", meta)
        result = plugin.run()
        assert result.success is True
        assert result.return_value == "loaded"

    def test_load_file_returns_sandboxed_plugin(self, tmp_path):
        path = tmp_path / "myplugin.py"
        path.write_text("def run(): return 99\n", encoding="utf-8")
        loader = PluginLoader()
        meta = PluginMetadata(name="file-plugin")
        plugin = loader.load_file(str(path), meta)
        assert isinstance(plugin, SandboxedPlugin)

    def test_load_file_code_matches_file(self, tmp_path):
        code = "def run(): return 'from file'\n"
        path = tmp_path / "plugin.py"
        path.write_text(code, encoding="utf-8")
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_file(str(path), meta)
        assert plugin.code == code

    def test_load_file_runnable(self, tmp_path):
        path = tmp_path / "plugin.py"
        path.write_text("def run(x): return x * 3\n", encoding="utf-8")
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_file(str(path), meta)
        result = plugin.run(7)
        assert result.success is True
        assert result.return_value == 21

    def test_load_file_missing_raises(self, tmp_path):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        with pytest.raises(OSError):
            loader.load_file(str(tmp_path / "nonexistent.py"), meta)

    def test_load_string_validate_valid(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_string("def run(): pass", meta)
        assert plugin.validate() == []

    def test_load_string_validate_invalid(self):
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        plugin = loader.load_string("def broken(:", meta)
        errors = plugin.validate()
        assert len(errors) > 0

    def test_load_file_custom_sandbox(self, tmp_path):
        path = tmp_path / "plugin.py"
        path.write_text("def run(): return 1\n", encoding="utf-8")
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        policy = SandboxPolicy(max_exec_time=2.0)
        sb = PluginSandbox(policy)
        plugin = loader.load_file(str(path), meta, sandbox=sb)
        assert plugin.sandbox is sb


# ===========================================================================
# Integration / edge-case tests
# ===========================================================================

class TestIntegration:

    def test_full_workflow(self):
        """End-to-end: load, validate, run."""
        loader = PluginLoader()
        meta = PluginMetadata(name="adder", entry_point="run")
        code = "def run(a, b): return a + b"
        plugin = loader.load_string(code, meta)
        assert plugin.validate() == []
        result = plugin.run(5, 6)
        assert result.success is True
        assert result.return_value == 11

    def test_policy_applied_through_loader(self):
        """Policy restrictions propagate from sandbox to loaded plugin."""
        policy = SandboxPolicy(allow_imports=[])
        sandbox = PluginSandbox(policy)
        loader = PluginLoader()
        meta = PluginMetadata(name="test")
        code = "def run(): import os; return os.getcwd()"
        plugin = loader.load_string(code, meta, sandbox=sandbox)
        result = plugin.run()
        assert result.success is False

    def test_execute_multiline_code(self):
        sb = PluginSandbox()
        code = (
            "total = 0\n"
            "for i in range(10):\n"
            "    total += i\n"
            "_result = total\n"
        )
        result = sb.execute(code)
        assert result.success is True
        assert result.return_value == 45

    def test_execute_function_defined_and_called(self):
        sb = PluginSandbox()
        code = (
            "def square(x): return x * x\n"
            "_result = square(7)\n"
        )
        result = sb.execute(code)
        assert result.success is True
        assert result.return_value == 49

    def test_default_policy_used_when_none(self):
        sb = PluginSandbox(policy=None)
        assert isinstance(sb.policy, SandboxPolicy)

    def test_sandboxed_plugin_default_sandbox(self):
        meta = PluginMetadata(name="test")
        plugin = SandboxedPlugin(metadata=meta, code="def run(): pass")
        assert isinstance(plugin.sandbox, PluginSandbox)

    def test_call_function_with_all_allowed_imports(self):
        policy = SandboxPolicy(allow_imports=["math"])
        sb = PluginSandbox(policy)
        code = "import math\ndef compute(r): return math.pi * r * r"
        result = sb.call_function(code, "compute", 1)
        assert result.success is True
        assert result.return_value == pytest.approx(3.14159, rel=1e-4)
