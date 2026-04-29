"""
utils_chunker.py — утилиты разбивки больших текстов на части.
Stage 0: детерминировано, без LLM, $0.

Импортируется другими скриптами:
    from utils_chunker import chunk_by_headers, chunk_fixed, chunk_overlap
    from utils_chunker import iter_md_files_chunked
"""
import re
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# Базовые стратегии чанкинга
# ---------------------------------------------------------------------------

def chunk_fixed(text: str, words: int = 1500) -> list[str]:
    """Фиксированные чанки по N слов. Быстро, грубо."""
    parts = text.split()
    return [' '.join(parts[i:i + words]) for i in range(0, len(parts), words)]


def chunk_overlap(text: str, words: int = 1500, overlap: int = 200) -> list[str]:
    """Скользящее окно с перекрытием — сохраняет контекст на границах."""
    parts = text.split()
    step = max(1, words - overlap)
    chunks = []
    for i in range(0, len(parts), step):
        chunk = ' '.join(parts[i:i + words])
        if chunk:
            chunks.append(chunk)
        if i + words >= len(parts):
            break
    return chunks


def chunk_by_headers(text: str, max_words: int = 2000) -> list[str]:
    """Разбивка по заголовкам Markdown (## и ###).

    Если секция длиннее max_words — дополнительно разбивает chunk_fixed.
    Лучшая стратегия для структурированных документов.
    """
    sections = re.split(r'\n(?=#{1,3} )', text)
    result = []
    for section in sections:
        if not section.strip():
            continue
        if len(section.split()) <= max_words:
            result.append(section)
        else:
            result.extend(chunk_fixed(section, max_words))
    return result


def chunk_by_paragraphs(text: str, max_words: int = 800) -> list[str]:
    """Разбивка по абзацам с объединением коротких."""
    paragraphs = re.split(r'\n{2,}', text)
    result: list[str] = []
    current: list[str] = []
    current_words = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        w = len(para.split())
        if current_words + w > max_words and current:
            result.append('\n\n'.join(current))
            current = [para]
            current_words = w
        else:
            current.append(para)
            current_words += w

    if current:
        result.append('\n\n'.join(current))
    return result


# ---------------------------------------------------------------------------
# Итераторы для больших коллекций файлов
# ---------------------------------------------------------------------------

def iter_md_files(root: Path, skip_names: set[str] | None = None) -> Iterator[Path]:
    """Обходит все .md файлы в docs/, пропуская служебные."""
    skip = skip_names or {
        "README.md", "QA.md", "TAGS.md", "SIMILAR.md", "CONTACTS.md",
        "DECISIONS.md", "ACTION_ITEMS.md", "ENTITIES.md", "METRICS.md",
        "HEALTH.md", "SCORING.md", "CLUSTERS.md", "BACKLINKS.md",
    }
    docs = root / "docs"
    for path in sorted(docs.rglob("*.md")):
        if path.name in skip:
            continue
        yield path


def iter_md_files_chunked(
    root: Path,
    strategy: str = "headers",
    max_words: int = 1500,
    skip_names: set[str] | None = None,
) -> Iterator[tuple[Path, int, str]]:
    """Итератор: (path, chunk_index, chunk_text).

    strategy: "headers" | "fixed" | "overlap" | "paragraphs"
    """
    fn = {
        "headers":    lambda t: chunk_by_headers(t, max_words),
        "fixed":      lambda t: chunk_fixed(t, max_words),
        "overlap":    lambda t: chunk_overlap(t, max_words),
        "paragraphs": lambda t: chunk_by_paragraphs(t, max_words),
    }.get(strategy, lambda t: chunk_by_headers(t, max_words))

    for path in iter_md_files(root, skip_names):
        text = path.read_text(encoding="utf-8")
        chunks = fn(text)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                yield path, i, chunk


# ---------------------------------------------------------------------------
# Утилиты оценки
# ---------------------------------------------------------------------------

def word_count(text: str) -> int:
    return len(text.split())


def estimate_tokens(text: str) -> int:
    """Грубая оценка токенов: ~1.3 токена на слово для смешанного RU/EN текста."""
    return int(word_count(text) * 1.3)


def fits_context(text: str, max_tokens: int = 180_000) -> bool:
    return estimate_tokens(text) <= max_tokens


def summarize_plan(paths: list[Path], strategy: str = "headers", max_words: int = 1500) -> None:
    """Печатает план чанкинга без реального запуска."""
    total_chunks = 0
    total_tokens = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        chunks = chunk_by_headers(text, max_words) if strategy == "headers" else chunk_fixed(text, max_words)
        n = len(chunks)
        t = sum(estimate_tokens(c) for c in chunks)
        total_chunks += n
        total_tokens += t
        if n > 1:
            print(f"  {path.name}: {n} чанков, ~{t:,} токенов")
    print(f"Итого: {total_chunks} чанков, ~{total_tokens:,} токенов")
    cost_haiku = total_tokens / 1_000_000 * 0.25
    print(f"Стоимость (haiku input): ~${cost_haiku:.3f}")
