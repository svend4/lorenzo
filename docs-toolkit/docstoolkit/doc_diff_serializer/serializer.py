"""E413 DocDiffSerializer — serialize, parse, store and apply document diffs.

Pure stdlib implementation. Thread-safe via ``threading.Lock``.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field, asdict
from typing import Optional


VALID_OPS = ("insert", "delete", "replace")


@dataclass
class DiffOp:
    """A single diff operation."""

    op: str
    position: int
    length: int = 0
    text: str = ""


@dataclass
class SerializedDiff:
    """A complete serialized diff payload."""

    doc_id: str
    from_version: str
    to_version: str
    ops: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class SerializerStats:
    """Aggregate statistics for a :class:`DocDiffSerializer`."""

    total_diffs: int
    total_ops_serialized: int
    total_ops_parsed: int


class DocDiffSerializer:
    """Serialize/parse/apply document diff payloads."""

    def __init__(self) -> None:
        self._stored: dict = {}
        self._total_ops_serialized: int = 0
        self._total_ops_parsed: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def serialize(self, diff: SerializedDiff) -> str:
        """Serialize ``diff`` into a JSON string."""
        if not isinstance(diff, SerializedDiff):
            raise TypeError("diff must be a SerializedDiff instance")
        with self._lock:
            payload = {
                "doc_id": diff.doc_id,
                "from_version": diff.from_version,
                "to_version": diff.to_version,
                "ops": [asdict(op) if isinstance(op, DiffOp) else dict(op) for op in diff.ops],
                "metadata": dict(diff.metadata),
            }
            self._total_ops_serialized += len(diff.ops)
            return json.dumps(payload, ensure_ascii=False, sort_keys=True)

    def parse(self, json_str: str) -> SerializedDiff:
        """Parse ``json_str`` into a :class:`SerializedDiff`."""
        if not isinstance(json_str, str):
            raise ValueError("json_str must be a string")
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("Top-level JSON must be an object")
        for required in ("doc_id", "from_version", "to_version"):
            if required not in data:
                raise ValueError(f"Missing required field: {required}")
            if not isinstance(data[required], str):
                raise ValueError(f"Field {required} must be a string")
        ops_raw = data.get("ops", [])
        if not isinstance(ops_raw, list):
            raise ValueError("Field 'ops' must be a list")
        ops: list = []
        for entry in ops_raw:
            if not isinstance(entry, dict):
                raise ValueError("Each op must be an object")
            if "op" not in entry or "position" not in entry:
                raise ValueError("Each op requires 'op' and 'position'")
            op_kind = entry["op"]
            if op_kind not in VALID_OPS:
                raise ValueError(f"Unknown op kind: {op_kind}")
            position = entry["position"]
            if not isinstance(position, int) or isinstance(position, bool):
                raise ValueError("Field 'position' must be int")
            length = entry.get("length", 0)
            if not isinstance(length, int) or isinstance(length, bool):
                raise ValueError("Field 'length' must be int")
            text = entry.get("text", "")
            if not isinstance(text, str):
                raise ValueError("Field 'text' must be a string")
            ops.append(DiffOp(op=op_kind, position=position, length=length, text=text))
        metadata = data.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ValueError("Field 'metadata' must be an object")
        with self._lock:
            self._total_ops_parsed += len(ops)
        return SerializedDiff(
            doc_id=data["doc_id"],
            from_version=data["from_version"],
            to_version=data["to_version"],
            ops=ops,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------
    def store(self, diff: SerializedDiff) -> SerializedDiff:
        """Store ``diff`` keyed by (doc_id, from_version, to_version)."""
        if not isinstance(diff, SerializedDiff):
            raise TypeError("diff must be a SerializedDiff instance")
        key = (diff.doc_id, diff.from_version, diff.to_version)
        with self._lock:
            self._stored[key] = diff
        return diff

    def retrieve(self, doc_id: str, from_version: str, to_version: str) -> Optional[SerializedDiff]:
        with self._lock:
            return self._stored.get((doc_id, from_version, to_version))

    def delete(self, doc_id: str, from_version: str, to_version: str) -> bool:
        key = (doc_id, from_version, to_version)
        with self._lock:
            if key in self._stored:
                del self._stored[key]
                return True
            return False

    def diffs_for_doc(self, doc_id: str) -> list:
        with self._lock:
            matches = [d for (did, _f, _t), d in self._stored.items() if did == doc_id]
        return sorted(matches, key=lambda d: (d.from_version, d.to_version))

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    def apply_diff(self, content: str, diff: SerializedDiff) -> str:
        """Apply ``diff`` ops to ``content`` in order."""
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if not isinstance(diff, SerializedDiff):
            raise TypeError("diff must be a SerializedDiff instance")
        result = content
        for op in diff.ops:
            if op.position < 0 or op.position > len(result):
                raise ValueError(
                    f"Op position {op.position} out of bounds for content length {len(result)}"
                )
            if op.op == "insert":
                result = result[: op.position] + op.text + result[op.position :]
            elif op.op == "delete":
                end = op.position + op.length
                if end > len(result):
                    raise ValueError(
                        f"Delete extends past end: position={op.position}, length={op.length}"
                    )
                result = result[: op.position] + result[end:]
            elif op.op == "replace":
                end = op.position + op.length
                if end > len(result):
                    raise ValueError(
                        f"Replace extends past end: position={op.position}, length={op.length}"
                    )
                result = result[: op.position] + op.text + result[end:]
            else:
                raise ValueError(f"Unknown op kind: {op.op}")
        return result

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_diff(self, diff: SerializedDiff) -> list:
        """Return list of validation errors (empty = valid)."""
        errors: list = []
        if not isinstance(diff, SerializedDiff):
            return ["diff must be a SerializedDiff instance"]
        if not isinstance(diff.doc_id, str) or not diff.doc_id:
            errors.append("doc_id must be a non-empty string")
        if not isinstance(diff.from_version, str) or not diff.from_version:
            errors.append("from_version must be a non-empty string")
        if not isinstance(diff.to_version, str) or not diff.to_version:
            errors.append("to_version must be a non-empty string")
        for idx, op in enumerate(diff.ops):
            if not isinstance(op, DiffOp):
                errors.append(f"op[{idx}] is not a DiffOp instance")
                continue
            if op.op not in VALID_OPS:
                errors.append(f"op[{idx}] has unknown op kind: {op.op}")
            if not isinstance(op.position, int) or op.position < 0:
                errors.append(f"op[{idx}] position must be int >= 0")
            if not isinstance(op.length, int) or op.length < 0:
                errors.append(f"op[{idx}] length must be int >= 0")
            if op.op == "insert":
                if not isinstance(op.text, str):
                    errors.append(f"op[{idx}] insert requires text str")
                if op.length != 0:
                    errors.append(f"op[{idx}] insert must have length == 0")
            elif op.op == "delete":
                if op.length <= 0:
                    errors.append(f"op[{idx}] delete must have length > 0")
                if op.text:
                    errors.append(f"op[{idx}] delete must have empty text")
            elif op.op == "replace":
                if op.length <= 0:
                    errors.append(f"op[{idx}] replace must have length > 0")
                if not isinstance(op.text, str):
                    errors.append(f"op[{idx}] replace requires text str")
        return errors

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------
    def clear(self) -> int:
        with self._lock:
            count = len(self._stored)
            self._stored.clear()
            return count

    def stats(self) -> SerializerStats:
        with self._lock:
            return SerializerStats(
                total_diffs=len(self._stored),
                total_ops_serialized=self._total_ops_serialized,
                total_ops_parsed=self._total_ops_parsed,
            )
