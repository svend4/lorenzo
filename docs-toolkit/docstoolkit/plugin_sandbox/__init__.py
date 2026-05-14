"""Plugin sandbox module for docs-toolkit (E80).

Provides safe execution of untrusted plugin code with configurable policies.

Quick-start::

    from docstoolkit.plugin_sandbox import (
        SandboxPolicy, SandboxResult, PluginSandbox,
        PluginMetadata, SandboxedPlugin, PluginLoader,
    )

    policy = SandboxPolicy(allow_builtins=["print", "len", "range"])
    sandbox = PluginSandbox(policy)
    result = sandbox.execute("_result = 1 + 2")
    assert result.return_value == 3
"""
from docstoolkit.plugin_sandbox.sandbox import SandboxPolicy, SandboxResult, PluginSandbox
from docstoolkit.plugin_sandbox.loader import PluginMetadata, SandboxedPlugin, PluginLoader

__all__ = [
    "SandboxPolicy",
    "SandboxResult",
    "PluginSandbox",
    "PluginMetadata",
    "SandboxedPlugin",
    "PluginLoader",
]
