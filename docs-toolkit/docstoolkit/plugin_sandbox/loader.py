"""Plugin loader for sandboxed plugin code.

Provides metadata-driven loading of plugin code strings or files,
with pre-validation before execution.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass

from docstoolkit.plugin_sandbox.sandbox import PluginSandbox, SandboxResult


@dataclass
class PluginMetadata:
    """Descriptive metadata for a sandboxed plugin.

    Parameters
    ----------
    name:
        Unique plugin name.
    version:
        Semantic version string. Defaults to ``"0.0.1"``.
    description:
        Human-readable description of what the plugin does.
    entry_point:
        Name of the callable inside the plugin code to invoke on ``run()``.
        Defaults to ``"run"``.
    """
    name: str
    version: str = "0.0.1"
    description: str = ""
    entry_point: str = "run"


class SandboxedPlugin:
    """A validated, sandbox-ready plugin."""

    def __init__(
        self,
        metadata: PluginMetadata,
        code: str,
        sandbox: PluginSandbox | None = None,
    ) -> None:
        self.metadata = metadata
        self.code = code
        self.sandbox: PluginSandbox = sandbox if sandbox is not None else PluginSandbox()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, *args, **kwargs) -> SandboxResult:
        """Call ``metadata.entry_point(*args, **kwargs)`` inside the sandbox.

        Returns
        -------
        SandboxResult
        """
        return self.sandbox.call_function(
            self.code,
            self.metadata.entry_point,
            *args,
            **kwargs,
        )

    def validate(self) -> list[str]:
        """Return a list of validation error messages.

        Checks performed
        ----------------
        1. Syntax check via ``ast.parse``.
        2. Presence of the entry-point function name as a top-level definition.

        Returns
        -------
        list[str]
            Empty list means the plugin is valid.
        """
        errors: list[str] = []

        # 1. Syntax
        try:
            tree = ast.parse(self.code)
        except SyntaxError as exc:
            errors.append(f"SyntaxError: {exc}")
            # Can't check entry point without a valid parse tree
            return errors

        # 2. Entry-point presence (top-level defs and assignments)
        defined_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
            elif isinstance(node, (ast.AnnAssign,)):
                if isinstance(node.target, ast.Name):
                    defined_names.add(node.target.id)

        if self.metadata.entry_point not in defined_names:
            errors.append(
                f"entry_point '{self.metadata.entry_point}' not found in plugin code"
            )

        return errors


class PluginLoader:
    """Factory for creating :class:`SandboxedPlugin` instances."""

    def load_string(
        self,
        code: str,
        metadata: PluginMetadata,
        sandbox: PluginSandbox | None = None,
    ) -> SandboxedPlugin:
        """Create a :class:`SandboxedPlugin` from a code string.

        Parameters
        ----------
        code:
            Python source code for the plugin.
        metadata:
            Plugin metadata including the entry-point name.
        sandbox:
            Optional pre-configured :class:`PluginSandbox`. A default
            sandbox is created if not provided.

        Returns
        -------
        SandboxedPlugin
        """
        return SandboxedPlugin(metadata=metadata, code=code, sandbox=sandbox)

    def load_file(
        self,
        path: str,
        metadata: PluginMetadata,
        sandbox: PluginSandbox | None = None,
    ) -> SandboxedPlugin:
        """Create a :class:`SandboxedPlugin` by reading code from a file.

        Parameters
        ----------
        path:
            Filesystem path to the ``.py`` plugin file.
        metadata:
            Plugin metadata including the entry-point name.
        sandbox:
            Optional pre-configured :class:`PluginSandbox`.

        Returns
        -------
        SandboxedPlugin

        Raises
        ------
        OSError
            If the file cannot be read.
        """
        with open(path, encoding="utf-8") as fh:
            code = fh.read()
        return self.load_string(code=code, metadata=metadata, sandbox=sandbox)
