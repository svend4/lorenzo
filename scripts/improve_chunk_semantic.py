"""
improve_chunk_semantic.py — семантическое чанкинг документов для RAG.

Делит тексты по смысловым границам (не механически по N токенов):
  - H2/H3 заголовки = границы чанков
  - Если секция > MAX_CHUNK_WORDS — дополнительно делит по абзацам
  - Если секция < MIN_CHUNK_WORDS — объединяет с соседней

Каждый чанк содержит:
  - id, source (файл), section (заголовок), text, word_count
  - context: заголовок родительской секции для лучшего retrieval

Сохраняет docs/chunks/{section}.jsonl (один чанк = одна строка JSON).

Запуск:
    python scripts/improve_chunk_semantic.py
    python scripts/improve_chunk_semantic.py --section 05-habr-projects
    python scripts/improve_chunk_semantic.py --max-words 400 --min-words 50
    python scripts/improve_chunk_semantic.py --output docs/chunks
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MAX_CHUNK_WORDS = 300
MIN_CHUNK_WORDS = 40

if "--max-words" in sys.argv:
    idx = sys.argv.index("--max-words")
    if idx + 1 < len(sys.argv):
        MAX_CHUNK_WORDS = int(sys.argv[idx + 1])

if "--min-words" in sys.argv:
    idx = sys.argv.index("--min-words")
    if idx + 1 < len(sys.argv):
        MIN_CHUNK_WORDS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

OUTPUT_DIR = DOCS / "chunks"
if "--output" in sys.argv:
    idx = sys.argv.index("--output")
    if idx + 1 < len(sys.argv):
        OUTPUT_DIR = ROOT / sys.argv[idx + 1]

SKIP_FILES = {
    "SEARCH.md", "READABILITY.md", "SPELLCHECK.md", "CONTENT_GAPS.md",
    "LINK_PREVIEW.md", "BROKEN_LINKS.md", "COVERAGE.md", "STALENESS.md",
    "OUTLINE.md", "SOURCE_MAP.md", "DUPLICATE_ACROSS.md",
}


def _clean_text(text: str) -> str:
    """Убирает markdown-разметку, оставляет читаемый текст."""
    text = re.sub(r'```.*?```', ' [CODE BLOCK] ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', lambda m: m.group(0)[1:-1], text)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', '[URL]', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[*_~|]', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _word_count(text: str) -> int:
    return len(text.split())


def _chunk_id(source: str, section: str, idx: int) -> str:
    raw = f"{source}::{section}::{idx}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def _split_by_headings(text: str) -> list[tuple[str, str, str]]:
    """
    Делит текст по заголовкам H1-H3.
    Возвращает [(parent_heading, section_heading, section_text)].
    """
    # Паттерн: строка начинается с # (не в коде)
    pattern = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(text))

    if not matches:
        return [("", "", text)]

    chunks = []
    parent = ""
    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_text = text[start:end].strip()

        if level == 1:
            parent = heading
        chunks.append((parent, heading, section_text))

    return chunks


def _split_by_paragraphs(text: str, max_words: int) -> list[str]:
    """Дополнительно делит большие секции по абзацам."""
    paragraphs = [p.strip() for p in re.split(r'\n\n+', text) if p.strip()]
    result = []
    current = []
    current_words = 0

    for para in paragraphs:
        pw = _word_count(para)
        if current_words + pw > max_words and current:
            result.append('\n\n'.join(current))
            current = [para]
            current_words = pw
        else:
            current.append(para)
            current_words += pw

    if current:
        result.append('\n\n'.join(current))
    return result


def chunk_file(path: Path) -> list[dict]:
    """Возвращает список чанков для одного файла."""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return []

    # Убираем frontmatter
    raw = re.sub(r'^---\s*\n.*?\n---\s*\n', '', raw, flags=re.DOTALL)

    rel_path = str(path.relative_to(ROOT))
    section_name = path.relative_to(DOCS).parts[0] if path.parent != DOCS else "root"

    sections = _split_by_headings(raw)
    chunks = []
    chunk_idx = 0

    # Буфер для слияния маленьких секций
    buffer_parent = ""
    buffer_heading = ""
    buffer_text = ""
    buffer_words = 0

    def flush_buffer():
        nonlocal buffer_text, buffer_words, buffer_parent, buffer_heading, chunk_idx
        if buffer_words >= MIN_CHUNK_WORDS:
            clean = _clean_text(buffer_text)
            if _word_count(clean) >= MIN_CHUNK_WORDS:
                chunks.append({
                    "id": _chunk_id(rel_path, buffer_heading, chunk_idx),
                    "source": rel_path,
                    "section_folder": section_name,
                    "parent_heading": buffer_parent,
                    "heading": buffer_heading,
                    "text": clean,
                    "word_count": _word_count(clean),
                    "date": TODAY,
                })
                chunk_idx += 1
        buffer_text = ""
        buffer_words = 0
        buffer_parent = ""
        buffer_heading = ""

    for parent_h, heading, text in sections:
        wc = _word_count(text)

        if wc < MIN_CHUNK_WORDS:
            # Маленькая секция — копим в буфер
            if buffer_words + wc > MAX_CHUNK_WORDS:
                flush_buffer()
            buffer_text += "\n\n" + text
            buffer_words += wc
            if not buffer_heading:
                buffer_parent = parent_h
                buffer_heading = heading
        elif wc > MAX_CHUNK_WORDS:
            # Большая секция — сначала сбрасываем буфер
            flush_buffer()
            # Делим по абзацам
            parts = _split_by_paragraphs(text, MAX_CHUNK_WORDS)
            for part in parts:
                clean = _clean_text(part)
                if _word_count(clean) >= MIN_CHUNK_WORDS:
                    chunks.append({
                        "id": _chunk_id(rel_path, heading, chunk_idx),
                        "source": rel_path,
                        "section_folder": section_name,
                        "parent_heading": parent_h,
                        "heading": heading,
                        "text": clean,
                        "word_count": _word_count(clean),
                        "date": TODAY,
                    })
                    chunk_idx += 1
        else:
            flush_buffer()
            clean = _clean_text(text)
            if _word_count(clean) >= MIN_CHUNK_WORDS:
                chunks.append({
                    "id": _chunk_id(rel_path, heading, chunk_idx),
                    "source": rel_path,
                    "section_folder": section_name,
                    "parent_heading": parent_h,
                    "heading": heading,
                    "text": clean,
                    "word_count": _word_count(clean),
                    "date": TODAY,
                })
                chunk_idx += 1

    flush_buffer()
    return chunks


def main() -> None:
    print("✂️  improve_chunk_semantic.py — семантическое чанкинг для RAG")
    print(f"   Размер чанка: {MIN_CHUNK_WORDS}–{MAX_CHUNK_WORDS} слов\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "chunks" not in str(f)
             and "obsidian" not in str(f)
             and "confluence" not in str(f)]

    print(f"   Файлов: {len(files)}\n")

    all_chunks = []
    by_section: dict[str, list] = {}

    for f in files:
        chunks = chunk_file(f)
        if not chunks:
            continue
        all_chunks.extend(chunks)
        sec = f.relative_to(DOCS).parts[0] if f.parent != DOCS else "root"
        by_section.setdefault(sec, []).extend(chunks)
        print(f"  {f.relative_to(ROOT)}: {len(chunks)} чанков")

    # Сохраняем по секциям
    for sec, chunks in by_section.items():
        out = OUTPUT_DIR / f"{sec}.jsonl"
        with out.open('w', encoding='utf-8') as fh:
            for chunk in chunks:
                fh.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    # Общий файл
    all_out = OUTPUT_DIR / "all_chunks.jsonl"
    with all_out.open('w', encoding='utf-8') as fh:
        for chunk in all_chunks:
            fh.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    # Статистика
    wc_avg = sum(c["word_count"] for c in all_chunks) / max(1, len(all_chunks))
    print(f"\n  Всего чанков: {len(all_chunks)}")
    print(f"  Средний размер: {wc_avg:.0f} слов")
    print(f"  Секций: {len(by_section)}")
    print(f"  Вывод: {OUTPUT_DIR.relative_to(ROOT)}/")
    print(f"  Используйте all_chunks.jsonl для RAG-пайплайна.")


if __name__ == "__main__":
    main()
