"""
improve_autocorrect.py — применяет исправления из CONSISTENCY.md:
заменяет все нестандартные написания на канонические прямо в файлах.
Запуск: python scripts/improve_autocorrect.py [--dry-run]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
DRY_RUN = "--dry-run" in sys.argv

# Замены: (вариант, канонический) — порядок важен (длинные первыми)
REPLACEMENTS = [
    # knowledge-space
    (r'\bknowledge_space\b',    "knowledge-space"),
    (r'\bknowledge space\b',    "knowledge-space"),
    # NGT Memory
    (r'\bNGT-Memory\b',         "NGT Memory"),
    (r'\bngt memory\b',         "NGT Memory"),
    # self-improvement
    (r'\bself-improve\b',       "self-improvement"),
    (r'\bselfimprovement\b',    "self-improvement"),
    # AI Factory
    (r'\bAI-Factory\b',         "AI Factory"),
    (r'\bAIFactory\b',          "AI Factory"),
    # Svyazi 2.0
    (r'\bSvyazi-2\.0\b',        "Svyazi 2.0"),
    (r'\bSvyazi2\.0\b',         "Svyazi 2.0"),
    # AgentFS
    (r'\bAgent FS\b',           "AgentFS"),
    (r'\bAgent-FS\b',           "AgentFS"),
    # local-first
    (r'\bLocal-First\b',        "local-first"),
    (r'\blocal first\b',        "local-first"),
    # CardIndex
    (r'\bCard Index\b',         "CardIndex"),
    (r'\bcard index\b',         "CardIndex"),
    (r'\bcard-index\b',         "CardIndex"),
    # Evidence Envelope
    (r'\bEvidence-Envelope\b',  "Evidence Envelope"),
    (r'\bEvidenceEnvelope\b',   "Evidence Envelope"),
    (r'\bevidence envelope\b',  "Evidence Envelope"),
    # Auto AI Router
    (r'\bAutoAI Router\b',      "Auto AI Router"),
    (r'\bAuto-AI-Router\b',     "Auto AI Router"),
    (r'\bAutoAIRouter\b',       "Auto AI Router"),
]


def fix_file(path: Path) -> int:
    """Применяет все замены к файлу. Возвращает число замен."""
    text = path.read_text(encoding="utf-8")
    original = text
    changes = 0

    for pattern, replacement in REPLACEMENTS:
        new_text = re.sub(pattern, replacement, text)
        if new_text != text:
            count = len(re.findall(pattern, text))
            changes += count
            text = new_text

    if text != original and not DRY_RUN:
        path.write_text(text, encoding="utf-8")

    return changes


def main():
    mode = "DRY RUN" if DRY_RUN else "APPLY"
    print(f"Авто-исправление терминов [{mode}]...")

    total_changes = 0
    total_files = 0

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"CONSISTENCY.md", "CHANGELOG.md", "README.md"}
        if f.name in skip:
            continue
        changes = fix_file(f)
        if changes > 0:
            total_files += 1
            total_changes += changes
            print(f"  {'+' if not DRY_RUN else '~'} {f.relative_to(ROOT)} ({changes} замен)")

    print(f"\nИтого: {total_changes} замен в {total_files} файлах")
    if DRY_RUN:
        print("(dry-run: файлы не изменены, запустите без --dry-run для применения)")


if __name__ == "__main__":
    main()
