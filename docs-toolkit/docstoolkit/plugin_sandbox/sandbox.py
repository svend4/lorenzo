"""Plugin sandbox for safe execution of untrusted plugin code.

Provides restricted execution environment with:
- Builtin allowlisting
- Import blocking
- Execution timeout via threading
"""
from __future__ import annotations

import builtins
import ctypes
import threading
import time
from dataclasses import dataclass, field
from typing import Any


def _kill_thread(thread: threading.Thread) -> None:
    """Inject SystemExit into a runaway daemon thread.

    Without this, a sandbox timeout leaves a daemon thread spinning a
    busy loop (e.g. ``while True: pass``) for the rest of the process
    lifetime — fine for short-lived CLIs, but in a long test session it
    pegs CPU and slows every subsequent test linearly. Pure-Python loops
    check for pending exceptions at each bytecode boundary, so async
    injection unwinds them; threads stuck in C extensions are unaffected.
    """
    tid = thread.ident
    if tid is None or not thread.is_alive():
        return
    ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )


@dataclass
class SandboxPolicy:
    """Policy controlling what sandboxed code can do.

    Parameters
    ----------
    allow_builtins:
        List of builtin names permitted in the sandbox.  ``None`` means all
        builtins are available (default).
    allow_imports:
        List of top-level module names that ``import`` statements may load.
        ``None`` means no import restriction (default).
    max_exec_time:
        Wall-clock seconds before execution is considered timed-out. Default 5.0.
    """
    allow_builtins: list[str] | None = None
    allow_imports: list[str] | None = None
    max_exec_time: float = 5.0


@dataclass
class SandboxResult:
    """Result of sandboxed code execution.

    Parameters
    ----------
    success:
        ``True`` if execution finished without errors or timeout.
    return_value:
        Value of the ``_result`` variable from the executed globals, if set.
    error:
        Human-readable error message; empty string on success.
    duration:
        Wall-clock seconds the execution took.
    """
    success: bool
    return_value: Any = None
    error: str = ""
    duration: float = 0.0


class PluginSandbox:
    """Execute plugin code strings in a restricted environment."""

    def __init__(self, policy: SandboxPolicy | None = None) -> None:
        self.policy: SandboxPolicy = policy if policy is not None else SandboxPolicy()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_globals(self, extra_context: dict | None) -> dict:
        """Build the restricted globals dict for exec."""
        policy = self.policy

        # --- builtins ---------------------------------------------------
        if policy.allow_builtins is None:
            # All builtins allowed — pass the real builtins dict
            restricted_builtins: Any = vars(builtins).copy()
        else:
            restricted_builtins = {
                name: getattr(builtins, name)
                for name in policy.allow_builtins
                if hasattr(builtins, name)
            }

        # --- import override -------------------------------------------
        allow_imports = policy.allow_imports  # may be None

        real_import = builtins.__import__

        def _restricted_import(name, *args, **kwargs):
            top = name.split(".")[0]
            if allow_imports is not None and top not in allow_imports:
                raise ImportError(
                    f"Import of '{name}' is not allowed by sandbox policy"
                )
            return real_import(name, *args, **kwargs)

        if isinstance(restricted_builtins, dict):
            restricted_builtins["__import__"] = _restricted_import

        # --- assemble globals ------------------------------------------
        globs: dict = {
            "__builtins__": restricted_builtins,
        }
        if extra_context:
            globs.update(extra_context)
        return globs

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute(self, code: str, context: dict | None = None) -> SandboxResult:
        """Execute *code* string in a restricted environment.

        Convention: if the executed code sets a variable named ``_result``
        in its namespace, that value is returned as ``SandboxResult.return_value``.

        Parameters
        ----------
        code:
            Python source code to execute.
        context:
            Optional dict of extra names injected into the execution globals
            before running the code.

        Returns
        -------
        SandboxResult
        """
        globs = self._build_globals(context)

        exc_holder: list[BaseException] = []
        start = time.monotonic()

        def _run() -> None:
            try:
                exec(compile(code, "<sandbox>", "exec"), globs)  # noqa: S102
            except BaseException as exc:  # noqa: BLE001
                exc_holder.append(exc)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=self.policy.max_exec_time)
        duration = time.monotonic() - start

        if thread.is_alive():
            _kill_thread(thread)
            thread.join(timeout=0.5)
            return SandboxResult(success=False, error="timeout", duration=duration)

        if exc_holder:
            err = exc_holder[0]
            return SandboxResult(
                success=False,
                error=f"{type(err).__name__}: {err}",
                duration=duration,
            )

        return_value = globs.get("_result", None)
        return SandboxResult(success=True, return_value=return_value, duration=duration)

    def call_function(
        self,
        code: str,
        func_name: str,
        *args,
        context: dict | None = None,
        **kwargs,
    ) -> SandboxResult:
        """Execute *code* then call ``func_name(*args, **kwargs)`` from it.

        Parameters
        ----------
        code:
            Python source containing the function definition.
        func_name:
            Name of the function to call.
        *args:
            Positional arguments forwarded to the function.
        context:
            Extra names injected into the execution globals.
        **kwargs:
            Keyword arguments forwarded to the function.

        Returns
        -------
        SandboxResult
        """
        globs = self._build_globals(context)

        exc_holder: list[BaseException] = []
        result_holder: list[Any] = []
        start = time.monotonic()

        def _run() -> None:
            try:
                exec(compile(code, "<sandbox>", "exec"), globs)  # noqa: S102
            except BaseException as exc:  # noqa: BLE001
                exc_holder.append(exc)
                return

            if func_name not in globs:
                exc_holder.append(
                    NameError(f"Function '{func_name}' not found in plugin code")
                )
                return

            try:
                result_holder.append(globs[func_name](*args, **kwargs))
            except BaseException as exc:  # noqa: BLE001
                exc_holder.append(exc)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=self.policy.max_exec_time)
        duration = time.monotonic() - start

        if thread.is_alive():
            _kill_thread(thread)
            thread.join(timeout=0.5)
            return SandboxResult(success=False, error="timeout", duration=duration)

        if exc_holder:
            err = exc_holder[0]
            return SandboxResult(
                success=False,
                error=f"{type(err).__name__}: {err}",
                duration=duration,
            )

        return_value = result_holder[0] if result_holder else None
        return SandboxResult(success=True, return_value=return_value, duration=duration)
