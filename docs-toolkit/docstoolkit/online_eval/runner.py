"""Continuous online evaluation: мониторинг качества RAG в production."""
import json
import re
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.online_eval.sampler import OnlineEvalSampler
from docstoolkit.rag.types import AnswerResult


# ---- Dataclasses ----

@dataclass
class OnlineEvalRun:
    """Запись одного оценённого запроса."""
    id: str
    query: str
    ts: str
    precision: float
    recall: float
    f1: float
    citation_precision: float
    answer_score: float
    retriever: str
    answerer: str
    duration_ms: int


@dataclass
class DriftReport:
    """Отчёт об отклонении метрики от базовой линии."""
    metric: str
    baseline_value: float
    current_value: float
    delta: float
    significant: bool       # abs(delta) > 0.1
    window_days: int


# ---- SQLite Store ----

_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    ts TEXT NOT NULL,
    precision REAL NOT NULL DEFAULT 0.0,
    recall REAL NOT NULL DEFAULT 0.0,
    f1 REAL NOT NULL DEFAULT 0.0,
    citation_precision REAL NOT NULL DEFAULT 0.0,
    answer_score REAL NOT NULL DEFAULT 0.0,
    retriever TEXT NOT NULL DEFAULT '',
    answerer TEXT NOT NULL DEFAULT '',
    duration_ms INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_runs_ts ON runs(ts);
"""


class OnlineEvalStore:
    """SQLite-хранилище результатов онлайн-оценки."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "online_eval.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def save_run(self, run: OnlineEvalRun) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO runs "
            "(id, query, ts, precision, recall, f1, citation_precision, "
            " answer_score, retriever, answerer, duration_ms) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                run.id, run.query, run.ts,
                run.precision, run.recall, run.f1,
                run.citation_precision, run.answer_score,
                run.retriever, run.answerer, run.duration_ms,
            ),
        )
        self.conn.commit()

    def recent_runs(self, days: int = 7) -> list[OnlineEvalRun]:
        cutoff = (datetime.now(tz=timezone.utc) - timedelta(days=days)).isoformat()
        rows = self.conn.execute(
            "SELECT * FROM runs WHERE ts >= ? ORDER BY ts DESC", (cutoff,)
        ).fetchall()
        return [self._row_to_run(r) for r in rows]

    def baseline_stats(
        self,
        days_ago_start: int = 14,
        days_ago_end: int = 7,
    ) -> dict[str, float]:
        """Среднее по метрикам для baseline окна [now-days_ago_start, now-days_ago_end]."""
        now = datetime.now(tz=timezone.utc)
        start = (now - timedelta(days=days_ago_start)).isoformat()
        end = (now - timedelta(days=days_ago_end)).isoformat()
        return self._mean_stats(
            "SELECT * FROM runs WHERE ts >= ? AND ts < ?", (start, end)
        )

    def current_stats(self, days: int = 7) -> dict[str, float]:
        """Среднее по метрикам за последние days дней."""
        cutoff = (datetime.now(tz=timezone.utc) - timedelta(days=days)).isoformat()
        return self._mean_stats(
            "SELECT * FROM runs WHERE ts >= ?", (cutoff,)
        )

    def _mean_stats(self, sql: str, params: tuple) -> dict[str, float]:
        rows = self.conn.execute(sql, params).fetchall()
        if not rows:
            return {
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "citation_precision": 0.0,
                "answer_score": 0.0,
            }
        n = len(rows)
        metrics = ["precision", "recall", "f1", "citation_precision", "answer_score"]
        return {m: sum(r[m] for r in rows) / n for m in metrics}

    @staticmethod
    def _row_to_run(row) -> OnlineEvalRun:
        return OnlineEvalRun(
            id=row["id"],
            query=row["query"],
            ts=row["ts"],
            precision=row["precision"],
            recall=row["recall"],
            f1=row["f1"],
            citation_precision=row["citation_precision"],
            answer_score=row["answer_score"],
            retriever=row["retriever"],
            answerer=row["answerer"],
            duration_ms=row["duration_ms"],
        )


# ---- Runner ----

def _tokenize(text: str) -> set[str]:
    """Простая токенизация для сравнения запросов."""
    return set(re.findall(r'[а-яёa-z]{3,}', text.lower()))


def _token_overlap(a: str, b: str) -> float:
    """Jaccard-подобное сходство: |A ∩ B| / |A ∪ B|."""
    ta, tb = _tokenize(a), _tokenize(b)
    union = ta | tb
    if not union:
        return 0.0
    return len(ta & tb) / len(union)


class OnlineEvalRunner:
    """Оркестрирует онлайн-оценку: сэмплирует запросы, матчит golden, сохраняет."""

    def __init__(
        self,
        store: OnlineEvalStore,
        golden_dataset_path: Path | None = None,
        sampler: OnlineEvalSampler | None = None,
    ):
        self.store = store
        self.golden_dataset_path = golden_dataset_path
        self.sampler = sampler or OnlineEvalSampler(sample_rate=0.01)
        self._golden: list | None = None

    def _load_golden(self) -> list:
        """Загружает golden dataset из файла (YAML или JSON)."""
        if self._golden is not None:
            return self._golden

        if self.golden_dataset_path is None:
            self._golden = []
            return self._golden

        path = Path(self.golden_dataset_path)
        if not path.exists():
            self._golden = []
            return self._golden

        suffix = path.suffix.lower()
        try:
            if suffix == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
                items_raw = data.get("items", []) if isinstance(data, dict) else data
            else:
                # YAML via frontmatter parser (already in stdlib-friendly utils)
                from docstoolkit.frontmatter import parse_yaml
                data = parse_yaml(path.read_text(encoding="utf-8"))
                items_raw = data.get("items", []) if isinstance(data, dict) else []

            from docstoolkit.eval.golden import GoldenItem
            items: list[GoldenItem] = []
            for x in items_raw:
                if isinstance(x, str):
                    items.append(GoldenItem(question=x))
                elif isinstance(x, dict):
                    items.append(GoldenItem(
                        question=x.get("question", ""),
                        expected_answer_contains=x.get("expected_answer_contains", []),
                        expected_doc_ids=x.get("expected_doc_ids", []),
                        forbidden_phrases=x.get("forbidden_phrases", []),
                        weight=float(x.get("weight", 1.0)),
                        notes=x.get("notes", ""),
                    ))
            self._golden = items
        except Exception:
            self._golden = []

        return self._golden

    def _find_matching_golden(self, query: str):
        """Ищет наиболее похожий golden item по token overlap."""
        from docstoolkit.eval.golden import GoldenItem

        golden = self._load_golden()
        if not golden:
            return None

        best_item = None
        best_score = 0.0
        for item in golden:
            sim = _token_overlap(query, item.question)
            if sim > best_score:
                best_score = sim
                best_item = item

        # Требуем минимальное сходство для матча
        if best_score < 0.1:
            return None
        return best_item

    def _evaluate_against_golden(
        self,
        result: AnswerResult,
        golden_item,
    ) -> tuple[float, float, float, float, float]:
        """Возвращает (precision, recall, f1, citation_precision, answer_score)."""
        from docstoolkit.eval.golden import score_answer, score_citations

        # Citation scoring
        actual_doc_ids = [c.get("doc_id", "") for c in result.citations]
        expected_doc_ids = getattr(golden_item, "expected_doc_ids", [])
        precision, recall, f1 = score_citations(actual_doc_ids, expected_doc_ids)

        # Citation precision (same as precision here for consistency)
        citation_precision = precision

        # Answer scoring
        expected_contains = getattr(golden_item, "expected_answer_contains", [])
        answer_score = score_answer(result.answer, expected_contains) / 100.0  # normalise 0-1

        return precision, recall, f1, citation_precision, answer_score

    def maybe_run(self, query: str, result: AnswerResult) -> OnlineEvalRun | None:
        """Решает: оценивать ли запрос. Если да — оценивает и сохраняет.

        Возвращает OnlineEvalRun или None (если не попал в сэмпл).
        """
        if not self.sampler.maybe_sample(query):
            return None

        golden_item = self._find_matching_golden(query)

        if golden_item is None:
            # Нет матча — создаём dummy golden с пустыми ожиданиями
            from docstoolkit.eval.golden import GoldenItem
            golden_item = GoldenItem(
                question=query,
                expected_answer_contains=[],
                expected_doc_ids=[],
            )

        precision, recall, f1, citation_precision, answer_score = (
            self._evaluate_against_golden(result, golden_item)
        )

        run = OnlineEvalRun(
            id=uuid.uuid4().hex[:16],
            query=query,
            ts=datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
            precision=precision,
            recall=recall,
            f1=f1,
            citation_precision=citation_precision,
            answer_score=answer_score,
            retriever=getattr(result, "method", "") or "",
            answerer=getattr(result, "answerer", "") or "",
            duration_ms=result.duration_ms,
        )
        self.store.save_run(run)
        return run

    def compute_drift(self, window_days: int = 7) -> list[DriftReport]:
        """Сравнивает текущую неделю с предыдущей baseline неделей.

        DriftReport.significant = True когда abs(delta) > 0.1.
        """
        baseline = self.store.baseline_stats(
            days_ago_start=window_days * 2,
            days_ago_end=window_days,
        )
        current = self.store.current_stats(days=window_days)

        metrics = ["precision", "recall", "f1", "citation_precision", "answer_score"]
        reports: list[DriftReport] = []
        for metric in metrics:
            b = baseline.get(metric, 0.0)
            c = current.get(metric, 0.0)
            delta = c - b
            reports.append(DriftReport(
                metric=metric,
                baseline_value=b,
                current_value=c,
                delta=delta,
                significant=abs(delta) > 0.1,
                window_days=window_days,
            ))
        return reports
