# Обработка больших массивов — Часть 9: Автоматизация

> Как сделать так, чтобы всё работало само: оркестратор, watcher, CI/CD, MCP.

---

## Проблема ручного запуска

125 скриптов. Запускать вручную каждый раз — не вариант. Нужна система, которая:
1. **Знает порядок** — какой скрипт от чего зависит
2. **Пропускает ненужное** — если метрика уже хорошая
3. **Реагирует на изменения** — сама запускается когда файл изменился
4. **Работает в CI/CD** — на каждый push
5. **Отдаёт инструменты Claude** — через MCP

---

## Ступень 1: Оркестратор — improve_run_all.py

**Главный скрипт** — запускает все группы в правильном порядке.

```bash
# Запустить всё
python scripts/improve_run_all.py

# Только быстрые скрипты (< 5 сек каждый)
python scripts/improve_run_all.py --fast

# Умный режим: пропустить если метрика уже хорошая
python scripts/improve_run_all.py --smart

# Только конкретная группа
python scripts/improve_run_all.py --group quality
python scripts/improve_run_all.py --group deeptext
python scripts/improve_run_all.py --group meta

# Только изменённые файлы (git diff)
python scripts/improve_run_all.py --changed

# Параллельное выполнение групп
python scripts/improve_run_all.py --parallel 4

# Конкретный скрипт
python scripts/improve_run_all.py --only improve_metrics.py

# Отчёт о выполнении
python scripts/improve_run_all.py --report
```

**15 групп в порядке зависимостей:**
```
structure → index → analysis → extract → quality → graph → generate
    → reports → export → cicd → analytics → textwork → deeptext → meta → enrich
```

**SMART_CONDITIONS** — не запускать если уже хорошо:
```python
SMART_CONDITIONS = {
    "improve_metrics.py":     ("docs/METRICS.md", "Средний балл", 80),
    "improve_health.py":      ("docs/HEALTH.md",  "общий балл",   85),
    "improve_scoring.py":     ("docs/SCORING.md", "балл:",        90),
    "improve_broken_links.py":("docs/BROKEN_LINKS.md", "Найдено", 30),
    "improve_dedup.py":       ("docs/DUPLICATES.md", "Точных дублей", 0),
    "improve_spellcheck.py":  ("docs/SPELLCHECK.md", "проблем", 5),
}
```

---

## Ступень 2: Автономный Watcher — improve_watcher.py

**Следит за файлами и автоматически запускает нужные скрипты.**

```bash
python scripts/improve_watcher.py  # запустить (polling каждые 30 сек)
```

**Правила реакции:**
```python
RULES = [
    # Изменился docs-файл → обновить метрики и индекс
    Rule(pattern="docs/**/*.md",        scripts=["improve_metrics", "improve_search_index"]),
    # Новый contacts-файл → обновить приоритеты
    Rule(pattern="docs/contacts/*.md",  scripts=["improve_contact_priority", "improve_contacts"]),
    # Изменился скрипт → обновить карту зависимостей
    Rule(pattern="scripts/improve_*.py",scripts=["improve_dependency_map"]),
]
```

**Cooldown:** Каждый скрипт не чаще 1 раза в 60 секунд — защита от петель.

---

## Ступень 3: GitHub Actions CI/CD — .github/workflows/docs.yml

**Запускается при каждом push.**

```yaml
# .github/workflows/docs.yml (сгенерирован improve_ci_config.py)

on: [push]
jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt -q
      
      # Быстрые скрипты на PR
      - name: Run fast scripts
        if: github.event_name == 'pull_request'
        run: python scripts/improve_run_all.py --fast
        continue-on-error: true
      
      # Все скрипты на push в main
      - name: Run all scripts
        if: github.event_name == 'push'
        run: python scripts/improve_run_all.py --smart
        continue-on-error: true
      
      # Закоммитить обновлённые docs/
      - name: Commit updates
        run: |
          git config user.name "docs-bot"
          git add -A docs/
          git diff --staged --quiet || git commit -m "docs: auto-update [skip ci]"
          git push origin HEAD
```

```bash
python scripts/improve_ci_config.py  # сгенерировать/обновить workflow
```

---

## Ступень 4: Pre-commit хуки — .pre-commit-config.yaml

**Проверки перед каждым коммитом:**

```bash
python scripts/improve_pre_commit.py --install
# pre-commit install
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-broken-links
        name: Check broken links
        entry: python scripts/improve_broken_links.py
        language: python
      - id: validate-docs
        name: Validate docs structure
        entry: python scripts/improve_validate.py
        language: python
```

---

## Ступень 5: Dependabot — .github/dependabot.yml

**Мониторинг версий зависимостей и OSS-проектов:**

```bash
python scripts/improve_dependabot.py --generate-config
```

Отслеживает:
- `anthropic` SDK
- `beautifulsoup4`
- `mcp`
- Версии OSS-проектов (AgentFS, Yodoca) из GitHub releases

---

## Ступень 6: MCP-сервер — mcp_server.py (Claude Desktop)

**Самый высокий уровень автоматизации:** Claude сам решает когда запустить скрипт.

```python
# Claude может вызвать:
run_improve(script="improve_metrics", args=[])
search_docs(query="AgentFS concurrent access")
update_contact_status(author="kksudo", field="studied", value=True)
```

**Это означает:** Говорите Claude «обнови метрики» — он сам вызовет нужный скрипт через MCP.

---

## Ступень 7: Claude Skills (КОГДА запускать)

Skills в `.claude/skills/` — это инструкции для Claude **когда** использовать какой инструмент:

| Skill | Триггер | Действие |
|-------|---------|---------|
| `analyze-project.md` | «Расскажи про AgentFS» | Найти файл, прочитать ENTITIES/CONTACTS, синтезировать |
| `review-docs.md` | «Проверь документацию» | Запустить quality-группу, прочитать METRICS |
| `write-contact.md` | «Напиши автору kksudo» | Прочитать contacts/kksudo.md, сгенерировать письмо |
| `improve.md` | «Улучши файл X» | Запустить нужные скрипты, предложить правки |

---

## Полная цепочка автоматизации

```
Событие (push / изменение файла / запрос Claude)
    ↓
Триггер (CI/CD workflow / watcher polling / MCP вызов / Skill)
    ↓
Оркестратор (improve_run_all.py --smart --changed)
    ↓
Группа скриптов (quality / deeptext / meta / ...)
    ↓
Обновлённые docs/ + метрики
    ↓
Коммит + push (git add -A docs/ && git commit && git push)
    ↓
Уведомление (RSS фид / GitHub Pages / Obsidian sync)
```

---

## Следующий шаг

→ **Часть 10: Инновационные и ещё не придуманные подходы**
