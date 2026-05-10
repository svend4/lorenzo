"""
utils_card_envelope.py — реализация интеграционных контрактов Svyazi 2.0.

Содержит пять data-классов из PROTOTYPE_SPEC.md:
  CardEnvelope     — базовая единица хранения (любой документ/факт/проект)
  EvidenceEnvelope — доказательная цепочка для retrieval-ответа
  MemoryWrite      — типизированная запись в память (episode/fact/proposal/decay)
  SkillPolicy      — политика вызова инструмента/скилла
  ReviewRecord     — запись о проверке факта или предложения

Применение:
  from utils_card_envelope import CardEnvelope, EvidenceEnvelope, MemoryWrite

  card = CardEnvelope.from_file(Path("docs/05-habr-projects/memory/yodoca.md"))
  card.add_edge("docs/04-ai-collaborations/01-overview.md", "references")
  card.save(Path("cards/"))
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


# ─────────────────────────────────────────────────────────────────────
# Типы
# ─────────────────────────────────────────────────────────────────────

CardType  = Literal["doc", "note", "fact", "person", "project", "unknown"]
CardState = Literal["raw", "normalized", "inferred", "approved", "rejected", "decayed"]
EdgeRel   = Literal["references", "contradicts", "extends", "related", "mentions", "authored_by"]
WriteType = Literal["episode", "fact", "proposal", "decay_event"]
ToolClass = Literal["read", "annotate", "plan", "mutate", "publish", "external_send"]
ApprovalMode = Literal["auto", "review", "blocked"]


# ─────────────────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def _card_id_for(source: str) -> str:
    return _sha256(source)


def _detect_card_type(path: Path, text: str = "") -> CardType:
    """Определяет тип карточки из нескольких источников по убыванию приоритета:

    1. YAML frontmatter (``type:`` или ``card_type:``)
    2. <!-- tags: ... --> с type-словами
    3. Имя файла
    4. H1-заголовок (первая строка # ...)
    5. Контентные сигналы (имена известных проектов)
    """
    name = path.stem.lower()

    # 0. Имена файлов авто-генерируемых/мета-документов — всегда doc
    _META_NAMES = {
        "qa", "readme", "summary", "scoring", "health", "metrics", "toc",
        "knowledge_map", "knowledge-map", "index", "backlinks", "crossrefs",
        "orphans", "digest", "digest_auto", "changelog", "report", "similar",
        "similar_passages", "tags", "glossary", "faq", "timeline", "decisions",
        "content_gaps", "reading_time", "topic_model", "citation_index",
        "version_diff", "github_issues", "questions", "entities", "sitemap",
        "mindmap", "abbreviations", "progress", "narrative", "heatmap",
        "sentiment", "registry", "collab_suggestions", "broken_links",
        # Spec / planning / dashboard docs
        "prototype_spec", "script_eval_report", "collab_suggestions",
        "knowledge_map", "cross_section", "concept_graph", "dedup",
        "consistency", "coverage", "priorities", "action_items", "cost",
        "word_freq", "language_stats", "passive_voice", "heading_audit",
        "empty_sections", "reading_list", "reading_order", "network",
        "component_matrix", "projects-map", "projects_map",
        "tech_radar", "onboarding", "risk_register", "dependency_map",
        "kpi_history", "digest_weekly", "executive-summary",
    }
    if name in _META_NAMES:
        return "doc"

    # 1. YAML frontmatter — самый точный источник
    fm_match = re.search(r'^---\s*\n(.*?)\n---', text, re.DOTALL | re.MULTILINE)
    if fm_match:
        fm = fm_match.group(1)
        for key in ("card_type", "type"):
            km = re.search(rf'^{key}\s*:\s*(\S+)', fm, re.MULTILINE)
            if km:
                v = km.group(1).strip().strip('"').strip("'").lower()
                if v in ("person", "author", "contact"):
                    return "person"
                if v in ("project",):
                    return "project"
                if v in ("note",):
                    return "note"
                if v in ("fact",):
                    return "fact"
                if v in ("doc", "document", "article"):
                    return "doc"

    # 2. <!-- tags: ... --> с type-хинтами
    tag_match = re.search(r'<!--\s*tags:\s*([^>]+)-->', text)
    if tag_match:
        tag_str = tag_match.group(1).lower()
        if any(t in tag_str for t in ("person", "author", "contact")):
            return "person"
        if "project" in tag_str:
            return "project"

    # 3. Имя файла — надёжный быстрый сигнал
    if any(k in name for k in ("contact", "author", "person", "автор")):
        return "person"
    if any(k in name for k in ("project", "проект", "yodoca", "agentfs",
                                "memnet", "cardindex", "svyazi", "rufler",
                                "wikontic", "knowledge-space", "ngt-memory",
                                "liteparse", "mclaude", "firecrawl")):
        return "project"
    if any(k in name for k in ("note", "заметка", "запись")):
        return "note"
    if any(k in name for k in ("fact", "факт")):
        return "fact"

    # 4. H1 — если заголовок содержит имя проекта
    if text:
        for line in text.splitlines()[:5]:
            if line.startswith("# "):
                h1 = line[2:].lower()
                # Пропускаем мета-документы с известными H1-префиксами
                if any(h1.startswith(p) for p in (
                        "q&a:", "резюме", "summary:", "тема:", "chapter",
                        "схема", "индекс", "отчёт", "аудит", "метрики",
                )):
                    return "doc"
                if any(k in h1 for k in ("автор", "author", "contact", "контакт")):
                    return "person"
                # Проекты с фиксированными именами в H1
                _PROJ_NAMES = [
                    "yodoca", "agentfs", "memnet", "svyazi", "wikontic",
                    "ngt memory", "knowledge-space", "cardindex", "rufler",
                    "liteparsе", "mclaude", "firecrawl", "litellm",
                    "agent-memory-mcp", "sentinel",
                ]
                if any(p in h1 for p in _PROJ_NAMES):
                    return "project"
                break

    # 5. Контент: если файл в memory/ или knowledge/ подпапке — вероятно проект
    parts = [p.name.lower() for p in path.parents]
    if any(p in parts for p in ("memory", "knowledge", "ensembles")):
        # Дополнительный сигнал: короткий файл об одном проекте
        if text and len(text.split()) < 600:
            return "project"

    return "doc"


# ─────────────────────────────────────────────────────────────────────
# CardEnvelope
# ─────────────────────────────────────────────────────────────────────

@dataclass
class CardEdge:
    to: str
    rel: EdgeRel = "related"
    note: str = ""

    def to_dict(self) -> dict:
        d = {"to": self.to, "rel": self.rel}
        if self.note:
            d["note"] = self.note
        return d


@dataclass
class CardEnvelope:
    """Базовая единица хранения знания.

    Любой документ, заметка или факт сначала превращается в CardEnvelope.
    card_id — контентный хэш (SHA-256 от source), обеспечивает идемпотентность.
    """
    card_id:      str
    card_type:    CardType  = "doc"
    state:        CardState = "raw"
    sources:      list[str] = field(default_factory=list)
    edges:        list[CardEdge] = field(default_factory=list)
    created_at:   str = field(default_factory=_now_iso)
    updated_at:   str = field(default_factory=_now_iso)
    payload_hash: str = ""
    payload:      dict[str, Any] = field(default_factory=dict)

    # ── Конструкторы ─────────────────────────────────────────────

    @classmethod
    def from_file(cls, path: Path, root: Path | None = None) -> "CardEnvelope":
        """Создаёт CardEnvelope из markdown-файла."""
        text = path.read_text(encoding="utf-8")
        source = str(path.relative_to(root)) if root else str(path)
        card_id = _card_id_for(source)

        # Извлекаем заголовок
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title:
            title = path.stem.replace("-", " ").replace("_", " ")

        # Краткое резюме — первый абзац не-заголовок
        summary = ""
        for line in text.splitlines():
            if not line.startswith("#") and not line.startswith("|") and len(line.strip()) > 40:
                summary = line.strip()[:300]
                break

        # Теги из YAML frontmatter или <!-- tags: ... -->
        tags: list[str] = []
        tag_match = re.search(r'<!--\s*tags:\s*([^>]+)-->', text)
        if tag_match:
            tags = [t.strip() for t in tag_match.group(1).split(",") if t.strip()]

        # Упомянутые проекты
        KNOWN_PROJECTS = [
            "Svyazi", "CardIndex", "AgentFS", "knowledge-space", "mclaude",
            "AI Factory", "Rufler", "LiteParse", "Legal RAG", "Hybrid RAG",
            "Graph RAG", "Yodoca", "NGT Memory", "MemNet", "agent-memory-mcp",
            "SENTINEL", "LiteLLM", "Auto AI Router", "Tool Search", "AutoResearch",
            "Wikontic", "Firecrawl",
        ]
        mentioned = [p for p in KNOWN_PROJECTS if p.lower() in text.lower()]

        return cls(
            card_id=card_id,
            card_type=_detect_card_type(path, text),
            state="raw",
            sources=[source],
            payload={
                "title":    title,
                "summary":  summary,
                "tags":     tags,
                "projects": mentioned,
                "wc":       len(text.split()),
                "path":     source,
            },
            payload_hash=_sha256(text[:1000]),
        )

    @classmethod
    def from_text(cls, text: str, source: str,
                  card_type: CardType = "note") -> "CardEnvelope":
        """Создаёт CardEnvelope из произвольного текста."""
        card_id = _card_id_for(source)
        return cls(
            card_id=card_id,
            card_type=card_type,
            state="raw",
            sources=[source],
            payload={"text": text[:2000]},
            payload_hash=_sha256(text[:1000]),
        )

    @classmethod
    def from_dict(cls, d: dict) -> "CardEnvelope":
        edges = [CardEdge(**e) for e in d.get("edges", [])]
        return cls(
            card_id=d["card_id"],
            card_type=d.get("card_type", "doc"),
            state=d.get("state", "raw"),
            sources=d.get("sources", []),
            edges=edges,
            created_at=d.get("created_at", _now_iso()),
            updated_at=d.get("updated_at", _now_iso()),
            payload_hash=d.get("payload_hash", ""),
            payload=d.get("payload", {}),
        )

    # ── Мутации ──────────────────────────────────────────────────

    def add_edge(self, target: str, rel: EdgeRel = "related", note: str = "") -> None:
        for e in self.edges:
            if e.to == target and e.rel == rel:
                return  # уже есть
        self.edges.append(CardEdge(to=target, rel=rel, note=note))
        self.updated_at = _now_iso()

    def transition(self, new_state: CardState) -> None:
        self.state = new_state
        self.updated_at = _now_iso()

    def decay(self) -> None:
        self.transition("decayed")

    # ── Сериализация ─────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "card_id":      self.card_id,
            "card_type":    self.card_type,
            "state":        self.state,
            "sources":      self.sources,
            "edges":        [e.to_dict() for e in self.edges],
            "created_at":   self.created_at,
            "updated_at":   self.updated_at,
            "payload_hash": self.payload_hash,
            "payload":      self.payload,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_markdown(self) -> str:
        """Сериализует карточку как markdown-файл с YAML frontmatter."""
        p = self.payload
        title = p.get("title", self.card_id[:12])
        tags  = ", ".join(p.get("tags", []))
        lines = [
            f"---",
            f"card_id: {self.card_id}",
            f"card_type: {self.card_type}",
            f"state: {self.state}",
            f"created_at: {self.created_at}",
            f"updated_at: {self.updated_at}",
        ]
        if tags:
            lines.append(f"tags: [{tags}]")
        lines += ["---", "", f"# {title}", ""]
        if p.get("summary"):
            lines += [f"> {p['summary']}", ""]
        if p.get("projects"):
            lines.append(f"**Проекты:** {', '.join(p['projects'])}")
            lines.append("")
        if self.edges:
            lines.append("## Связи\n")
            for e in self.edges:
                lines.append(f"- [{e.to}]({e.to})  _{e.rel}_")
            lines.append("")
        return "\n".join(lines)

    def save(self, directory: Path, fmt: str = "json") -> Path:
        """Сохраняет карточку. fmt = 'json' | 'md'."""
        directory.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r'[^a-z0-9_\-]', '_', self.card_id.replace("sha256:", ""))
        if fmt == "md":
            out = directory / f"{slug}.md"
            out.write_text(self.to_markdown(), encoding="utf-8")
        else:
            out = directory / f"{slug}.json"
            out.write_text(self.to_json(), encoding="utf-8")
        return out


# ─────────────────────────────────────────────────────────────────────
# EvidenceEnvelope
# ─────────────────────────────────────────────────────────────────────

@dataclass
class EvidenceEnvelope:
    """Доказательная цепочка для любого retrieval-ответа.

    Прикрепляется к результату поиска / рекомендации / суммаризации.
    Без Evidence нельзя построить ни ручной review, ни объяснение рекомендации.
    """
    source_id:        str
    page_or_span:     str     = ""
    bbox_or_offset:   list    = field(default_factory=list)
    retrieval_method: Literal["bm25", "semantic", "graph", "hybrid", "exact"] = "bm25"
    confidence:       float   = 1.0
    supporting_nodes: list[str] = field(default_factory=list)
    text_excerpt:     str     = ""

    def to_dict(self) -> dict:
        return {
            "source_id":        self.source_id,
            "page_or_span":     self.page_or_span,
            "bbox_or_offset":   self.bbox_or_offset,
            "retrieval_method": self.retrieval_method,
            "confidence":       round(self.confidence, 3),
            "supporting_nodes": self.supporting_nodes,
            "text_excerpt":     self.text_excerpt[:200],
        }

    @classmethod
    def from_bm25_hit(cls, hit: dict) -> "EvidenceEnvelope":
        """Создаёт Evidence из результата BM25 (формат passages.json)."""
        source = hit.get("file", hit.get("source", ""))
        score  = hit.get("score", 1.0)
        confidence = min(1.0, score / 20.0)  # нормализуем BM25-score
        return cls(
            source_id=source,
            retrieval_method="bm25",
            confidence=confidence,
            text_excerpt=hit.get("text", "")[:200],
        )


# ─────────────────────────────────────────────────────────────────────
# MemoryWrite
# ─────────────────────────────────────────────────────────────────────

@dataclass
class MemoryWrite:
    """Типизированная операция записи в память.

    Записать «что-то в память» — никогда не одна операция.
    Различаем: episode (сырое) / fact (подтверждённое) / proposal (гипотеза) / decay.
    """
    write_type:      WriteType
    card_id:         str
    content:         str
    confidence:      float = 1.0
    review_required: bool  = False
    promotion_rule:  str   = ""
    decay_policy:    str   = "ttl:30d"
    written_at:      str   = field(default_factory=_now_iso)
    written_by:      str   = "agent"

    # Автоматически выставляем review_required
    def __post_init__(self) -> None:
        if self.write_type == "proposal" and not self.review_required:
            self.review_required = True
        if self.write_type == "fact" and self.confidence >= 0.9:
            self.review_required = False

    @classmethod
    def episode(cls, card_id: str, content: str, **kw) -> "MemoryWrite":
        return cls(write_type="episode", card_id=card_id, content=content, **kw)

    @classmethod
    def fact(cls, card_id: str, content: str, confidence: float = 0.95, **kw) -> "MemoryWrite":
        return cls(write_type="fact", card_id=card_id, content=content,
                   confidence=confidence, **kw)

    @classmethod
    def proposal(cls, card_id: str, content: str, confidence: float = 0.6, **kw) -> "MemoryWrite":
        return cls(write_type="proposal", card_id=card_id, content=content,
                   confidence=confidence, review_required=True, **kw)

    @classmethod
    def decay(cls, card_id: str, reason: str = "ttl_expired", **kw) -> "MemoryWrite":
        return cls(write_type="decay_event", card_id=card_id, content=reason,
                   confidence=1.0, review_required=False, **kw)

    def to_dict(self) -> dict:
        return asdict(self)


# ─────────────────────────────────────────────────────────────────────
# SkillPolicy
# ─────────────────────────────────────────────────────────────────────

@dataclass
class SkillPolicy:
    """Политика вызова скилла или MCP-инструмента.

    Определяет класс доступа, требует ли ревью, ограничения по пути и сети.
    """
    tool_name:    str
    tool_class:   ToolClass   = "read"
    approval_mode: ApprovalMode = "auto"
    path_scope:   Literal["local", "project", "global"] = "local"
    network_scope: Literal["offline", "internal", "internet"] = "offline"
    description:  str = ""

    def allows_auto(self) -> bool:
        return self.approval_mode == "auto"

    def is_destructive(self) -> bool:
        return self.tool_class in ("mutate", "publish", "external_send")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def read_only(cls, tool_name: str, **kw) -> "SkillPolicy":
        return cls(tool_name=tool_name, tool_class="read",
                   approval_mode="auto", **kw)

    @classmethod
    def mutate(cls, tool_name: str, require_review: bool = True, **kw) -> "SkillPolicy":
        mode = "review" if require_review else "auto"
        return cls(tool_name=tool_name, tool_class="mutate",
                   approval_mode=mode, **kw)


# ─────────────────────────────────────────────────────────────────────
# ReviewRecord
# ─────────────────────────────────────────────────────────────────────

@dataclass
class ReviewRecord:
    """Запись о проверке факта, предложения или действия агента.

    Отделяет machine suggestion от accepted truth.
    """
    card_id:      str
    reviewer_role: Literal["human", "agent", "auto"] = "human"
    decision:     Literal["approved", "rejected", "deferred"] = "deferred"
    reason:       str = ""
    evidence_refs: list[str] = field(default_factory=list)
    follow_up:    str = ""
    reviewed_at:  str = field(default_factory=_now_iso)

    def approve(self, reason: str = "") -> None:
        self.decision    = "approved"
        self.reason      = reason
        self.reviewed_at = _now_iso()

    def reject(self, reason: str = "") -> None:
        self.decision    = "rejected"
        self.reason      = reason
        self.reviewed_at = _now_iso()

    def to_dict(self) -> dict:
        return asdict(self)


# ─────────────────────────────────────────────────────────────────────
# CardStore — простое файловое хранилище
# ─────────────────────────────────────────────────────────────────────

class CardStore:
    """Минимальное файловое хранилище для CardEnvelope.

    Хранит карточки как JSON-файлы в директории.
    Поддерживает поиск по card_id, type, state и keyword.
    """

    def __init__(self, directory: Path) -> None:
        self.dir = directory
        self.dir.mkdir(parents=True, exist_ok=True)

    def put(self, card: CardEnvelope) -> Path:
        return card.save(self.dir, fmt="json")

    def get(self, card_id: str) -> CardEnvelope | None:
        slug = re.sub(r'[^a-z0-9_\-]', '_', card_id.replace("sha256:", ""))
        path = self.dir / f"{slug}.json"
        if not path.exists():
            return None
        return CardEnvelope.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def all(self) -> list[CardEnvelope]:
        cards = []
        for f in sorted(self.dir.glob("*.json")):
            try:
                cards.append(CardEnvelope.from_dict(
                    json.loads(f.read_text(encoding="utf-8"))
                ))
            except Exception:
                pass
        return cards

    def search(self, query: str, top: int = 10) -> list[tuple[float, CardEnvelope]]:
        """Keyword-поиск по payload (каждый токен считается отдельно)."""
        tokens = re.findall(r'[а-яёa-z]{3,}', query.lower())
        if not tokens:
            return []
        results = []
        for card in self.all():
            text = json.dumps(card.payload, ensure_ascii=False).lower()
            score = sum(text.count(t) for t in tokens)
            if score > 0:
                results.append((float(score), card))
        results.sort(key=lambda x: -x[0])
        return results[:top]

    def count(self) -> dict[str, int]:
        cards = self.all()
        by_type:  dict[str, int] = {}
        by_state: dict[str, int] = {}
        for c in cards:
            by_type[c.card_type]   = by_type.get(c.card_type, 0) + 1
            by_state[c.card_state] = by_state.get(c.card_state, 0) + 1  # type: ignore
        return {"total": len(cards), "by_type": by_type, "by_state": by_state}

    def stats(self) -> str:
        cards = self.all()
        if not cards:
            return "CardStore пуст."
        from collections import Counter
        types  = Counter(c.card_type  for c in cards)
        states = Counter(c.state      for c in cards)
        lines = [f"CardStore: {len(cards)} карточек", ""]
        lines.append("По типу:")
        for t, n in types.most_common():
            lines.append(f"  {t:<12} {n}")
        lines.append("\nПо статусу:")
        for s, n in states.most_common():
            lines.append(f"  {s:<12} {n}")
        return "\n".join(lines)
