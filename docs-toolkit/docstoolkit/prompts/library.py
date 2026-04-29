"""Prompt registry с versioning, deterministic A/B routing, defaults."""
import hashlib
import json
import random
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


PLACEHOLDER_RE = re.compile(r'\{(\w+)\}')


class PromptRenderError(Exception):
    """Ошибка рендеринга: missing variable, etc."""


@dataclass
class Prompt:
    """Один версионированный промпт."""
    id: str                          # canonical identifier, e.g. "rag.system"
    version: int = 1
    template: str = ""
    variables: list[str] = field(default_factory=list)
    description: str = ""
    metadata: dict = field(default_factory=dict)
    created_ts: str = ""

    def __post_init__(self):
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec='seconds')
        # auto-extract variables if not provided
        if not self.variables:
            self.variables = sorted(set(PLACEHOLDER_RE.findall(self.template)))

    def render(self, vars: dict, *, strict: bool = True) -> str:
        """Render template by substituting {name} placeholders."""
        out = self.template
        for name in self.variables:
            if name in vars:
                out = out.replace("{" + name + "}", str(vars[name]))
            elif strict:
                raise PromptRenderError(
                    f"prompt {self.id}@v{self.version}: missing variable '{name}'"
                )
        # strict: detect leftover placeholders not in `variables` (typos)
        remaining = PLACEHOLDER_RE.findall(out)
        if strict and remaining:
            unknown = [n for n in remaining if n not in self.variables]
            if unknown:
                raise PromptRenderError(
                    f"prompt {self.id}@v{self.version}: unknown placeholders {unknown}"
                )
        return out

    def fingerprint(self) -> str:
        """Стабильный hash для tracing/eval."""
        h = hashlib.sha1()
        h.update(self.id.encode())
        h.update(str(self.version).encode())
        h.update(self.template.encode())
        return h.hexdigest()[:12]


@dataclass
class _Variant:
    version: int
    weight: float = 1.0


class PromptLibrary:
    """In-memory + опц. JSON-persisted prompt registry.

    Структура: {prompt_id: {version: Prompt}} + active_variants[prompt_id] = [_Variant].
    """
    def __init__(self, *, path: Path | None = None,
                 rng_seed: int | None = None):
        self._prompts: dict[str, dict[int, Prompt]] = {}
        self._variants: dict[str, list[_Variant]] = {}
        self.path = Path(path) if path else None
        self._rng = random.Random(rng_seed) if rng_seed is not None else random.Random()
        if self.path and self.path.exists():
            self.load()

    # ---- registry ----
    def register(self, prompt: Prompt) -> None:
        self._prompts.setdefault(prompt.id, {})[prompt.version] = prompt
        # default variant: latest version with weight 1.0 if no explicit variant set
        if prompt.id not in self._variants:
            self._variants[prompt.id] = [_Variant(version=prompt.version, weight=1.0)]

    def get(self, prompt_id: str, version: int | None = None) -> Prompt | None:
        versions = self._prompts.get(prompt_id, {})
        if not versions:
            return None
        if version is None:
            version = max(versions.keys())
        return versions.get(version)

    def list_ids(self) -> list[str]:
        return sorted(self._prompts.keys())

    def list_versions(self, prompt_id: str) -> list[int]:
        return sorted(self._prompts.get(prompt_id, {}).keys())

    def remove(self, prompt_id: str, version: int | None = None) -> bool:
        if version is None:
            return self._prompts.pop(prompt_id, None) is not None
        versions = self._prompts.get(prompt_id, {})
        return versions.pop(version, None) is not None

    # ---- A/B variants ----
    def set_active_variant(self, prompt_id: str, *, version: int,
                            weight: float = 1.0,
                            additional: list[tuple[int, float]] | None = None) -> None:
        """Задаёт активные variants. additional = [(version, weight), ...]."""
        if prompt_id not in self._prompts:
            raise KeyError(f"unknown prompt id: {prompt_id}")
        variants = [_Variant(version=version, weight=weight)]
        if additional:
            for v, w in additional:
                variants.append(_Variant(version=v, weight=w))
        # validate all versions exist
        known = set(self._prompts[prompt_id].keys())
        for var in variants:
            if var.version not in known:
                raise KeyError(
                    f"prompt {prompt_id} has no version {var.version}"
                )
        self._variants[prompt_id] = variants

    def get_active_variants(self, prompt_id: str) -> list[tuple[int, float]]:
        return [(v.version, v.weight) for v in self._variants.get(prompt_id, [])]

    def _pick_variant(self, prompt_id: str) -> Prompt | None:
        variants = self._variants.get(prompt_id, [])
        if not variants:
            return self.get(prompt_id)
        if len(variants) == 1:
            return self.get(prompt_id, variants[0].version)
        total_w = sum(v.weight for v in variants) or 1.0
        # weighted choice via cumulative
        u = self._rng.random() * total_w
        acc = 0.0
        for v in variants:
            acc += v.weight
            if u <= acc:
                return self.get(prompt_id, v.version)
        return self.get(prompt_id, variants[-1].version)

    # ---- render ----
    def render(self, prompt_id: str, vars: dict | None = None,
                *, version: int | None = None, strict: bool = True
                ) -> tuple[str, Prompt]:
        """Returns (rendered_text, used_prompt). version=None → A/B pick."""
        p = self.get(prompt_id, version) if version is not None else self._pick_variant(prompt_id)
        if not p:
            raise PromptRenderError(f"unknown prompt: {prompt_id}")
        return p.render(vars or {}, strict=strict), p

    # ---- persistence ----
    def save(self, path: Path | None = None) -> None:
        target = Path(path) if path else self.path
        if not target:
            raise ValueError("no path provided for save()")
        data = {
            "prompts": [
                {
                    "id": p.id, "version": p.version, "template": p.template,
                    "variables": p.variables, "description": p.description,
                    "metadata": p.metadata, "created_ts": p.created_ts,
                }
                for versions in self._prompts.values() for p in versions.values()
            ],
            "variants": {
                pid: [{"version": v.version, "weight": v.weight} for v in vs]
                for pid, vs in self._variants.items()
            },
        }
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding='utf-8')

    def load(self, path: Path | None = None) -> None:
        target = Path(path) if path else self.path
        if not target or not target.exists():
            return
        data = json.loads(target.read_text(encoding='utf-8'))
        for pd in data.get("prompts", []):
            self.register(Prompt(
                id=pd["id"], version=pd["version"], template=pd["template"],
                variables=pd.get("variables", []),
                description=pd.get("description", ""),
                metadata=pd.get("metadata", {}),
                created_ts=pd.get("created_ts", ""),
            ))
        for pid, vlist in data.get("variants", {}).items():
            self._variants[pid] = [
                _Variant(version=v["version"], weight=v.get("weight", 1.0))
                for v in vlist
            ]

    def stats(self) -> dict:
        return {
            "ids": len(self._prompts),
            "total_versions": sum(len(v) for v in self._prompts.values()),
            "active_ab_tests": sum(1 for vs in self._variants.values() if len(vs) > 1),
        }
