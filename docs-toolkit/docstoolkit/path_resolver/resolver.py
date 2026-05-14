"""Path resolver for markdown documents (stdlib only — pathlib + posixpath)."""
from __future__ import annotations

import posixpath
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PathType(Enum):
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    ANCHOR = "anchor"
    EXTERNAL = "external"
    INVALID = "invalid"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ResolvedPath:
    original: str
    resolved: str
    path_type: PathType
    is_resolved: bool = False
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------

_EXTERNAL_PREFIXES = ("http://", "https://", "ftp://", "mailto:")


class PathResolver:
    """Resolves relative document paths and link references."""

    def __init__(self, base_dir: str = ".") -> None:
        # Normalize base directory using posix conventions
        self.base_dir = posixpath.normpath(base_dir.replace("\\", "/")) if base_dir else "."

    # ----- classification helpers --------------------------------------

    def is_absolute(self, path: str) -> bool:
        if not path:
            return False
        return path.startswith("/")

    def is_external(self, path: str) -> bool:
        if not path:
            return False
        lower = path.lower()
        return any(lower.startswith(pref) for pref in _EXTERNAL_PREFIXES)

    def is_anchor(self, path: str) -> bool:
        if not path:
            return False
        return path.startswith("#")

    # ----- low-level path operations -----------------------------------

    def normalize(self, path: str) -> str:
        """Remove `..`, `./`, and double slashes (posix style)."""
        if not path:
            return ""
        # Convert backslashes to forward slashes
        normalized = path.replace("\\", "/")
        return posixpath.normpath(normalized)

    def join(self, *parts: str) -> str:
        """Join path parts using posix conventions."""
        if not parts:
            return ""
        cleaned = [p.replace("\\", "/") for p in parts if p is not None]
        if not cleaned:
            return ""
        joined = posixpath.join(*cleaned)
        return joined

    def parent_dir(self, path: str) -> str:
        if not path:
            return ""
        return posixpath.dirname(path.replace("\\", "/"))

    def with_suffix(self, path: str, new_suffix: str) -> str:
        """Replace file extension. new_suffix may include leading dot or not."""
        if not path:
            return ""
        norm = path.replace("\\", "/")
        # Normalize suffix to start with dot (empty suffix = strip extension)
        if new_suffix and not new_suffix.startswith("."):
            suffix = "." + new_suffix
        else:
            suffix = new_suffix

        base, _, _ = norm.rpartition("/")
        last = norm.rpartition("/")[2]
        if "." in last:
            stem = last.rsplit(".", 1)[0]
        else:
            stem = last

        new_name = stem + suffix
        if "/" in norm:
            return base + "/" + new_name
        return new_name

    def extract_anchor(self, path: str) -> tuple[str, Optional[str]]:
        """Split `path#anchor` → (path, anchor)."""
        if path is None:
            return "", None
        if "#" not in path:
            return path, None
        idx = path.index("#")
        before = path[:idx]
        anchor = path[idx + 1 :]
        # anchor may be empty string after '#'; preserve empty as anchor=""
        return before, anchor

    # ----- relative-to ------------------------------------------------

    def relative_to(self, target: str, source: str) -> str:
        """Compute relative path from `source` to `target`.

        `source` is interpreted as a file path; the relative result is relative
        to source's parent directory.
        """
        if target is None or source is None:
            return target or ""
        tgt = target.replace("\\", "/")
        src = source.replace("\\", "/")
        src_dir = posixpath.dirname(src) or "."
        try:
            rel = posixpath.relpath(tgt, start=src_dir)
        except ValueError:
            return tgt
        return rel

    # ----- main resolution --------------------------------------------

    def resolve(self, path: str, from_file: str = None) -> ResolvedPath:
        original = path if path is not None else ""

        # Handle None / empty
        if path is None or path == "":
            return ResolvedPath(
                original=original,
                resolved="",
                path_type=PathType.INVALID,
                is_resolved=False,
                error="empty path",
            )

        # External URLs — left unchanged
        if self.is_external(path):
            return ResolvedPath(
                original=original,
                resolved=path,
                path_type=PathType.EXTERNAL,
                is_resolved=True,
                error=None,
            )

        # Anchor-only
        if self.is_anchor(path):
            if from_file:
                from_norm = from_file.replace("\\", "/")
                resolved = f"{from_norm}{path}"
            else:
                resolved = path
            return ResolvedPath(
                original=original,
                resolved=resolved,
                path_type=PathType.ANCHOR,
                is_resolved=True,
                error=None,
            )

        # Split path#anchor
        path_part, anchor = self.extract_anchor(path)

        # Absolute path
        if self.is_absolute(path_part):
            resolved_path = self.normalize(path_part)
            if anchor is not None:
                resolved_full = f"{resolved_path}#{anchor}"
            else:
                resolved_full = resolved_path
            return ResolvedPath(
                original=original,
                resolved=resolved_full,
                path_type=PathType.ABSOLUTE,
                is_resolved=True,
                error=None,
            )

        # Relative path — resolve against from_file directory or base_dir
        if from_file:
            from_norm = from_file.replace("\\", "/")
            from_dir = posixpath.dirname(from_norm) or "."
        else:
            from_dir = self.base_dir or "."

        try:
            joined = posixpath.join(from_dir, path_part.replace("\\", "/"))
            resolved_path = posixpath.normpath(joined)
        except Exception as exc:  # pragma: no cover - defensive
            return ResolvedPath(
                original=original,
                resolved="",
                path_type=PathType.INVALID,
                is_resolved=False,
                error=str(exc),
            )

        if anchor is not None:
            resolved_full = f"{resolved_path}#{anchor}"
        else:
            resolved_full = resolved_path

        return ResolvedPath(
            original=original,
            resolved=resolved_full,
            path_type=PathType.RELATIVE,
            is_resolved=True,
            error=None,
        )

    def resolve_all(
        self, paths: list[str], from_file: str = None
    ) -> list[ResolvedPath]:
        return [self.resolve(p, from_file=from_file) for p in paths]
