"""
improve_qa.py — генерирует Q&A листы для каждого раздела docs/.
Вопросы строятся детерминированно из заголовков и ключевых слов.
Создаёт docs/QA.md и QA-файл в каждой подпапке.
Запуск: python scripts/improve_qa.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Шаблоны вопросов по тегам/темам
QA_TEMPLATES = {
    "memory": [
        ("Какие системы памяти описаны в этом разделе?",
         "projects", ["Yodoca", "NGT Memory", "MemNet", "agent-memory-mcp"]),
        ("Как происходит консолидация и забывание в памяти агентов?",
         "keywords", ["консолидац", "forgetting", "decay", "episod"]),
        ("Какова разница между эпизодической и семантической памятью?",
         "keywords", ["episod", "семантич", "fact", "proposal"]),
    ],
    "rag": [
        ("Как реализован forensic RAG с доказуемостью?",
         "keywords", ["liteparse", "bounding box", "page-level", "evidence"]),
        ("Что такое Evidence Envelope и зачем он нужен?",
         "keywords", ["evidence envelope", "source_id", "page", "span"]),
        ("Какие RAG-подходы сравниваются в документах?",
         "projects", ["Legal RAG", "Hybrid RAG", "Graph RAG", "LiteParse"]),
    ],
    "orchestration": [
        ("Как организована многоагентная оркестрация?",
         "projects", ["mclaude", "AI Factory", "Rufler", "Sequential"]),
        ("Что такое handoff и locks в агентных системах?",
         "keywords", ["handoff", "locks", "mailbox", "multi-session"]),
        ("Как работает spec-driven подход в AI Factory?",
         "keywords", ["spec", "patch", "skill", "self-learning"]),
    ],
    "security": [
        ("Какие инструменты обеспечивают безопасность агентов?",
         "projects", ["SENTINEL", "LiteLLM", "Tool Search", "Auto AI Router"]),
        ("Какова политика доступа по умолчанию (tool classes)?",
         "keywords", ["read-only", "allowlist", "path guard", "quarantine"]),
        ("Как организован бюджетный роутинг между моделями?",
         "keywords", ["routing", "budget", "litellm", "local model"]),
    ],
    "knowledge": [
        ("Как работает AgentFS и что такое .agentos?",
         "keywords", ["agentos", "vault", "compile", "persistent state"]),
        ("Что такое knowledge-space и для кого он предназначен?",
         "keywords", ["reference card", "agent-readable", "785", "gotcha"]),
        ("Как CardIndex хранит и версионирует карточки?",
         "keywords", ["cardindex", "card_id", "state", "hash", "dedup"]),
    ],
    "architecture": [
        ("Какие 5 архитектурных зазоров выделены в исследовании?",
         "keywords", ["зазор", "карточка", "evidence", "memory governance",
                      "agent contract", "review protocol"]),
        ("Что входит в интеграционный контракт между слоями?",
         "keywords", ["card envelope", "evidence envelope", "memory write",
                      "skill policy", "review record"]),
    ],
    "roadmap": [
        ("Каковы этапы MVP и их оценка по времени?",
         "keywords", ["mvp", "12-18", "итерац", "фаза", "неделя"]),
        ("Что входит в первую итерацию прототипа?",
         "keywords", ["evidence-first", "unified card", "page/span", "manual review"]),
    ],
    "anthropic": [
        ("Какие кластеры найма выделены у Anthropic?",
         "keywords", ["research", "gtm", "trust & safety", "inference", "product"]),
        ("Какие роли наиболее релевантны для профиля svend4?",
         "keywords", ["forward deployed", "research engineer", "developer community"]),
    ],
    "collaboration": [
        ("Кто ключевые авторы проектов для контакта?",
         "projects", ["Андрей Чуян", "Виталий Оборин", "kksudo", "spbmolot"]),
        ("Какие вопросы лучше задавать авторам при первом контакте?",
         "keywords", ["первый вопрос", "архитектурный", "шаблон", "контакт"]),
    ],
}


def check_answer(text: str, kind: str, items: list[str]) -> str:
    """Ищет ответ в тексте по ключевым словам или проектам."""
    low = text.lower()
    found = [item for item in items if item.lower() in low]
    if found:
        return "Упоминаются: " + ", ".join(f"**{f}**" for f in found[:5])
    return "_Не найдено в этом файле._"


def make_section_qa(folder: Path, tags: list[str], files: list[Path]) -> str:
    """Строит Q&A для папки на основе тегов."""
    qa_pairs = []
    all_text = "\n".join(f.read_text(encoding="utf-8") for f in files)

    for tag in tags:
        templates = QA_TEMPLATES.get(tag, [])
        for question, kind, items in templates:
            answer = check_answer(all_text, kind, items)
            qa_pairs.append((question, answer))

    if not qa_pairs:
        return ""

    lines = [f"# Q&A: {folder.name}\n",
             f"_Автоматически сгенерировано по {len(files)} файлам раздела._\n"]
    for q, a in qa_pairs:
        lines.append(f"## {q}\n")
        lines.append(f"{a}\n")
    return "\n".join(lines)


def collect_folder_tags(folder: Path) -> list[str]:
    """Собирает теги из файлов папки."""
    tag_counts: dict[str, int] = defaultdict(int)
    tag_re = re.compile(r'<!--\s*tags:\s*([^-]+)\s*-->')
    for f in folder.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = tag_re.search(text)
        if m:
            for t in m.group(1).split(","):
                tag_counts[t.strip()] += 1
    return sorted(tag_counts, key=lambda x: -tag_counts[x])


def make_global_qa(all_qa: dict[str, str]) -> str:
    """Объединённый Q&A по всему репозиторию."""
    lines = ["# Глобальный Q&A\n",
             "Вопросы и ответы по всем разделам монорепозитория.\n"]
    for section, content in all_qa.items():
        if content:
            lines.append(f"\n---\n## Раздел: {section}\n")
            # Берём только вопросы-ответы без заголовка файла
            for line in content.split("\n")[3:]:
                lines.append(line)
    return "\n".join(lines)


def main():
    all_qa = {}
    for folder in sorted(DOCS.iterdir()):
        if not folder.is_dir():
            continue
        files = [f for f in folder.rglob("*.md")
                 if f.name not in ("README.md", "QA.md")]
        if not files:
            continue

        tags = collect_folder_tags(folder)
        qa_content = make_section_qa(folder, tags, files)

        if qa_content:
            qa_file = folder / "QA.md"
            qa_file.write_text(qa_content, encoding="utf-8")
            print(f"  wrote: {qa_file.relative_to(ROOT)}")
            all_qa[folder.name] = qa_content

    global_qa = make_global_qa(all_qa)
    out = DOCS / "QA.md"
    out.write_text(global_qa, encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"Готово: {len(all_qa)} Q&A файлов создано")


if __name__ == "__main__":
    main()
