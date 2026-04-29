"""
mcp_skills_server.py — MCP-сервер lorenzo-skills.

Делает скилы из .claude/skills/ доступными как MCP-инструменты:
  list_skills(category)            — список всех скилов с описаниями
  get_skill(name)                  — полный markdown скила
  match_skill(query)               — найти лучший скилл по запросу (router)
  compose_skills(skills)           — последовательность скилов с пайплайном
  evaluate_skill(skill, scores)    — записать метрики оценки

Также читает манифесты из tasks/_generated/ для семантической связки
скилл ↔ MCP-tool ↔ шаблон.

Запуск:
  python scripts/mcp_skills_server.py
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, build_server, run_stdio, log_call

try:
    from mcp.types import Tool, Resource, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


SKILLS_DIR = ROOT / ".claude" / "skills"
TASKS_GEN = ROOT / "tasks" / "_generated"
METRICS_PATH = ROOT / ".claude" / "skill_metrics.jsonl"


# ---------------------------------------------------------------------------
# Загрузка скилов
# ---------------------------------------------------------------------------

def _load_skill(name: str) -> dict | None:
    path = SKILLS_DIR / f"{name}.md"
    if not path.exists():
        return None
    text = path.read_text(encoding='utf-8')
    return _parse_skill(name, text)


def _parse_skill(name: str, text: str) -> dict:
    """Извлекает метаданные скила: первое описание, триггеры."""
    lines = text.splitlines()

    # Первое осмысленное описание (после # заголовка)
    description = ""
    for line in lines[1:]:
        line = line.strip()
        if line and not line.startswith('#'):
            description = line[:200]
            break

    # Извлечение триггеров из секции «## Когда использовать»
    # Поддерживает: - "фраза" | - 'фраза' | - «фраза» | - фраза
    triggers: list[str] = []
    in_triggers = False
    for line in lines:
        if re.match(r'^##\s+Когда использовать', line):
            in_triggers = True
            continue
        if in_triggers and line.startswith('## '):
            break
        if in_triggers:
            stripped = line.strip()
            if not stripped.startswith('-'):
                continue
            # Пропустить bullet-маркер
            content = stripped.lstrip('-').strip()
            # Снять разные виды кавычек
            for left, right in [('"', '"'), ("'", "'"), ('«', '»'), ('"', '"')]:
                if content.startswith(left) and content.endswith(right):
                    content = content[len(left):-len(right)]
                    break
            # Убрать markdown-ссылки [текст](path)
            content = re.sub(r'\[(.+?)\]\([^)]+\)', r'\1', content)
            if content and len(content) < 200:
                triggers.append(content.strip())

    # Связанные скилы из секции "## Связанные скилы"
    related: list[str] = []
    in_related = False
    for line in lines:
        if re.match(r'^##\s+Связанные скилы', line):
            in_related = True
            continue
        if in_related and line.startswith('## '):
            break
        if in_related:
            m = re.match(r'^-\s+\[`?([\w-]+)`?\]', line)
            if m:
                related.append(m.group(1))

    return {
        'name': name,
        'description': description,
        'triggers': triggers,
        'related': related,
        'size_chars': len(text),
        'path': str((SKILLS_DIR / f"{name}.md").relative_to(ROOT)),
    }


def _list_all_skills() -> list[dict]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(
        (_parse_skill(p.stem, p.read_text(encoding='utf-8'))
         for p in SKILLS_DIR.glob('*.md')),
        key=lambda x: x['name']
    )


def _load_manifest_for_skill(skill_name: str) -> dict | None:
    """Если для скила есть манифест задачи — вернуть."""
    json_path = TASKS_GEN / f"{skill_name}.json"
    if not json_path.exists():
        return None
    try:
        return json.loads(json_path.read_text(encoding='utf-8'))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Категоризация скилов (выводимая из имени или хардкод)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "universal": {"search", "summarize", "compare", "improve", "status",
                  "analyze-project", "review-docs", "write-contact"},
    "working": {"find-contradictions", "propose-collaboration", "audit-corpus",
                "generate-rfc", "plan-mvp", "track-decisions", "find-gaps", "synthesize"},
    "domain": {"design-ensemble", "evaluate-tech", "review-architecture",
               "propose-mega-stack", "find-cinderella"},
    "composite": {"daily-routine", "new-research", "outreach-day", "weekly-review"},
    "meta": {"skill-router", "dispatch", "evaluate-skill"},
}


def _category_of(name: str) -> str:
    for cat, names in CATEGORIES.items():
        if name in names:
            return cat
    return "other"


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def tool_list_skills(category: str = "") -> str:
    skills = _list_all_skills()
    if category and category != "all":
        skills = [s for s in skills if _category_of(s['name']) == category]
    if not skills:
        return f"Нет скилов{' категории ' + category if category else ''}."

    by_cat: dict[str, list] = {}
    for s in skills:
        cat = _category_of(s['name'])
        by_cat.setdefault(cat, []).append(s)

    order = ["universal", "working", "domain", "composite", "meta", "other"]
    lines = [f"## Скилы ({len(skills)}, категорий: {len(by_cat)})\n"]
    for cat in order:
        if cat not in by_cat:
            continue
        items = by_cat[cat]
        lines.append(f"\n### {cat} ({len(items)})\n")
        for s in items:
            triggers_s = ", ".join(f'"{t}"' for t in s['triggers'][:2])
            lines.append(f"- **`{s['name']}`** — {s['description'][:100]}")
            if triggers_s:
                lines.append(f"  Триггеры: {triggers_s}")
    return "\n".join(lines)


def tool_get_skill(name: str) -> str:
    skill = _load_skill(name)
    if not skill:
        available = sorted(p.stem for p in SKILLS_DIR.glob('*.md'))
        return f"❌ Скилл '{name}' не найден.\nДоступные: {', '.join(available)}"

    path = SKILLS_DIR / f"{name}.md"
    text = path.read_text(encoding='utf-8')

    # Прикрепить манифест если есть
    manifest = _load_manifest_for_skill(name)
    suffix = ""
    if manifest:
        suffix = (f"\n\n---\n\n## Манифест задачи (`tasks/{name}.task.yaml`)\n\n"
                  f"**MCP сервер:** `{manifest.get('mcp_server', '—')}`\n"
                  f"**MCP tool:** `{manifest.get('mcp_tool', '—')}`\n"
                  f"**Шаблон:** `{manifest.get('template', '—')}`\n"
                  f"**Шагов в pipeline:** {len(manifest.get('pipeline', []))}\n")

    return text + suffix


_PLACEHOLDER_RE = re.compile(r'\b[A-ZА-Я]\b')


def _trigger_keywords(trigger: str) -> set[str]:
    """Удаляет плейсхолдеры (одиночные заглавные буквы) и возвращает значимые слова."""
    cleaned = _PLACEHOLDER_RE.sub('', trigger).lower()
    return {w for w in re.findall(r'\w+', cleaned) if len(w) >= 3}


def tool_match_skill(query: str) -> str:
    """Находит лучший скилл по запросу (поиск по триггерам + описанию)."""
    if not query:
        return "❌ Укажите query."
    skills = _list_all_skills()
    query_lower = query.lower()
    query_tokens = set(re.findall(r'\w+', query_lower))

    scored: list[tuple[float, dict, str]] = []
    for s in skills:
        score = 0.0
        reasons: list[str] = []
        best_trigger = None

        # +5 за полное совпадение фразы триггера в запросе
        # +3 за совпадение всех значимых слов триггера (с учётом плейсхолдеров)
        for t in s['triggers']:
            t_lower = t.lower()
            if t_lower in query_lower:
                score += 5.0
                best_trigger = t
                break
            keywords = _trigger_keywords(t)
            if keywords and keywords.issubset(query_tokens):
                if score < 3.0:
                    score = 3.0
                    best_trigger = t

        if best_trigger:
            reasons.append(f"trigger '{best_trigger}'")

        # +3 за совпадение имени в запросе (с учётом дефисов)
        if s['name'].replace('-', ' ') in query_lower or s['name'] in query_lower:
            score += 3.0
            reasons.append("name match")

        # +0.5 за каждое слово запроса в описании
        desc_lower = s['description'].lower()
        for token in query_tokens:
            if len(token) >= 4 and token in desc_lower:
                score += 0.5

        # +0.3 за слово в триггерах
        triggers_text = " ".join(s['triggers']).lower()
        for token in query_tokens:
            if len(token) >= 4 and token in triggers_text and token not in desc_lower:
                score += 0.3

        if score > 0:
            scored.append((score, s, ", ".join(reasons)))

    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return f"Не найдено подходящих скилов для «{query}»."

    top = scored[:5]
    lines = [f"## Лучшие скилы для «{query}»\n"]
    for score, s, reasons in top:
        lines.append(f"**`{s['name']}`** (score={score:.1f}) — {s['description'][:100]}")
        if reasons:
            lines.append(f"  Совпадения: {reasons}")
        if s['triggers'][:2]:
            triggers_s = ", ".join(f'"{t}"' for t in s['triggers'][:2])
            lines.append(f"  Триггеры: {triggers_s}")
        lines.append("")
    if len(top) > 1:
        lines.append(f"**Рекомендация:** использовать `{top[0][1]['name']}` "
                     f"(score={top[0][0]:.1f}, разрыв с #2: {top[0][0] - top[1][0]:.1f})")
    return "\n".join(lines)


def tool_compose_skills(skills_list: list[str]) -> str:
    """Возвращает план композиции из последовательности скилов."""
    if not skills_list:
        return "❌ Укажите skills (массив имён)."
    if isinstance(skills_list, str):
        skills_list = [s.strip() for s in skills_list.split(',')]

    lines = [f"## Композиция: {' → '.join(f'`{s}`' for s in skills_list)}\n"]
    total_steps = 0
    for i, name in enumerate(skills_list, 1):
        s = _load_skill(name)
        if not s:
            lines.append(f"{i}. ❌ Скилл `{name}` не найден\n")
            continue
        manifest = _load_manifest_for_skill(name)
        steps = len(manifest.get('pipeline', [])) if manifest else 0
        total_steps += steps
        lines.append(f"{i}. **`{name}`** — {s['description'][:80]}")
        if manifest:
            lines.append(f"   - Шагов pipeline: {steps}")
            lines.append(f"   - MCP: `{manifest.get('mcp_server', '—')}.{manifest.get('mcp_tool', '—')}`")
        else:
            lines.append(f"   - Без манифеста (только markdown-инструкция)")
        lines.append("")

    lines.append(f"**Итого шагов:** {total_steps}")
    lines.append(f"**Команды для последовательного запуска:**")
    lines.append("```bash")
    for name in skills_list:
        if (TASKS_GEN / f"{name}.json").exists():
            lines.append(f"python scripts/improve_workflow_run.py --task {name}")
    lines.append("```")
    return "\n".join(lines)


def tool_evaluate_skill(skill: str, scores: dict, request: str = "",
                        feedback: str = "") -> str:
    """Записывает оценку скила в .claude/skill_metrics.jsonl"""
    if not skill:
        return "❌ Укажите skill."
    if not isinstance(scores, dict):
        return "❌ scores должен быть object с ключами helpful/honest/complete/efficient (1-5)."

    valid_keys = {'helpful', 'honest', 'complete', 'efficient'}
    cleaned: dict = {}
    for k, v in scores.items():
        if k in valid_keys and isinstance(v, (int, float)) and 1 <= v <= 5:
            cleaned[k] = int(v)
    if not cleaned:
        return "❌ Нужны хотя бы один из: helpful/honest/complete/efficient (1-5)."

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        'ts': datetime.now().isoformat(timespec='seconds'),
        'skill': skill,
        'request': request[:200],
        'scores': cleaned,
        'feedback': feedback[:500],
    }
    with METRICS_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    avg = sum(cleaned.values()) / len(cleaned)
    return (f"✅ Оценка для `{skill}` записана.\n"
            f"Средняя: {avg:.1f}/5 ({', '.join(f'{k}={v}' for k, v in cleaned.items())})\n"
            f"Лог: {METRICS_PATH.relative_to(ROOT)}")


def tool_skill_metrics() -> str:
    """Сводка по skill-метрикам."""
    if not METRICS_PATH.exists():
        return "Метрик пока нет. Запустите evaluate_skill чтобы начать собирать."
    entries = []
    for line in METRICS_PATH.read_text(encoding='utf-8').splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not entries:
        return "Лог пустой."

    by_skill: dict[str, list[dict]] = {}
    for e in entries:
        by_skill.setdefault(e['skill'], []).append(e)

    lines = [f"## Skill метрики\n",
             f"**Всего оценок:** {len(entries)} ({len(by_skill)} скилов)\n",
             "\n| Скилл | Использований | Avg helpful | Avg honest | Avg complete | Avg efficient |",
             "|-------|---------------|-------------|------------|--------------|---------------|"]
    for skill, items in sorted(by_skill.items(), key=lambda x: -len(x[1])):
        n = len(items)
        sums = {'helpful': 0, 'honest': 0, 'complete': 0, 'efficient': 0}
        counts = {'helpful': 0, 'honest': 0, 'complete': 0, 'efficient': 0}
        for it in items:
            for k, v in it.get('scores', {}).items():
                if k in sums:
                    sums[k] += v
                    counts[k] += 1
        avg = {k: f"{sums[k]/counts[k]:.1f}" if counts[k] else "—"
               for k in sums}
        lines.append(f"| `{skill}` | {n} | {avg['helpful']} | {avg['honest']} | {avg['complete']} | {avg['efficient']} |")
    return "\n".join(lines)


def dispatch(name: str, args: dict) -> str:
    if name == "list_skills":
        return tool_list_skills(args.get("category", ""))
    if name == "get_skill":
        return tool_get_skill(args.get("name", ""))
    if name == "match_skill":
        return tool_match_skill(args.get("query", ""))
    if name == "compose_skills":
        return tool_compose_skills(args.get("skills", []))
    if name == "evaluate_skill":
        return tool_evaluate_skill(
            args.get("skill", ""),
            args.get("scores", {}),
            args.get("request", ""),
            args.get("feedback", ""),
        )
    if name == "skill_metrics":
        return tool_skill_metrics()
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="list_skills",
        description="Список всех скилов с категориями (universal/working/domain/composite/meta).",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {
                    "enum": ["", "all", "universal", "working", "domain", "composite", "meta", "other"],
                },
            },
        },
    ),
    Tool(
        name="get_skill",
        description="Полный markdown-контент скила + связанный манифест задачи если есть.",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    ),
    Tool(
        name="match_skill",
        description="Skill router: найти лучший скилл по запросу пользователя.",
        inputSchema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    ),
    Tool(
        name="compose_skills",
        description="План композиции из последовательности скилов.",
        inputSchema={
            "type": "object",
            "properties": {
                "skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Имена скилов в порядке выполнения",
                },
            },
            "required": ["skills"],
        },
    ),
    Tool(
        name="evaluate_skill",
        description="Записать оценку применённого скила (4 оси: helpful/honest/complete/efficient).",
        inputSchema={
            "type": "object",
            "properties": {
                "skill": {"type": "string"},
                "scores": {
                    "type": "object",
                    "properties": {
                        "helpful": {"type": "integer", "minimum": 1, "maximum": 5},
                        "honest": {"type": "integer", "minimum": 1, "maximum": 5},
                        "complete": {"type": "integer", "minimum": 1, "maximum": 5},
                        "efficient": {"type": "integer", "minimum": 1, "maximum": 5},
                    },
                },
                "request": {"type": "string"},
                "feedback": {"type": "string"},
            },
            "required": ["skill", "scores"],
        },
    ),
    Tool(
        name="skill_metrics",
        description="Сводка skill-метрик: какие скилы используются чаще, средние баллы.",
        inputSchema={"type": "object", "properties": {}},
    ),
]


RESOURCES = [
    Resource(uri="lorenzo://skills/index", name="Skills index",
             description="JSON-индекс всех скилов с метаданными",
             mimeType="application/json"),
    Resource(uri="lorenzo://docs/TASKS_INDEX.md", name="Tasks index",
             description="Каталог задач из tasks/", mimeType="text/markdown"),
]


def read_resource(uri: str) -> str:
    if uri == "lorenzo://skills/index":
        return json.dumps(_list_all_skills(), ensure_ascii=False, indent=2)
    if uri.startswith("lorenzo://docs/"):
        rel = uri[len("lorenzo://docs/"):]
        path = ROOT / "docs" / rel
        return path.read_text(encoding="utf-8") if path.exists() else ""
    return ""


PROMPTS = [
    Prompt(
        name="lorenzo-route-request",
        description="Найти лучший скилл для запроса пользователя",
        arguments=[PromptArgument(name="query", description="Запрос", required=True)],
    ),
    Prompt(
        name="lorenzo-skill-help",
        description="Объяснить что делает скилл и когда применять",
        arguments=[PromptArgument(name="skill", required=True)],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-route-request":
        q = args.get("query", "")
        return (
            f"Запрос пользователя: «{q}»\n\n"
            f"1. Вызови `match_skill` с query='{q}' для топ-5 кандидатов. "
            f"2. Если score лучшего > score #2 на 2+ — применяй автоматически. "
            f"3. Если близко — спроси пользователя выбрать. "
            f"4. После применения вызови `evaluate_skill` для записи метрик."
        )
    if name == "lorenzo-skill-help":
        skill = args.get("skill", "")
        return (
            f"1. Вызови `get_skill` с name='{skill}'. "
            f"2. Прочитай секцию 'Когда использовать' и шаги. "
            f"3. Если есть манифест — покажи pipeline. "
            f"4. Дай рекомендацию: подходит ли для задачи пользователя."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-skills",
        TOOLS,
        dispatch,
        resources_spec=RESOURCES,
        resource_reader=read_resource,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
