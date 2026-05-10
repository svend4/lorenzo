# Метаскриптинг — Часть 3: Автокаталог скриптов

<!-- summary -->
> > Скрипт читает все 155 скриптов и строит живой каталог.

---
<!-- tags: ingestion -->




> Скрипт читает все 155 скриптов и строит живой каталог.

---

## Что такое автокаталог

Каталог — это JSON-файл (`docs/scripts_catalog.json`), который описывает каждый
скрипт: что делает, что читает, что пишет, насколько опасен.

Он строится автоматически — не вручную. При добавлении нового скрипта
достаточно запустить `improve_self.py --catalog` и каталог обновится.

---

## Что извлекается из каждого скрипта

```
improve_health.py
├── Первый docstring:    "дашборд здоровья репозитория. Создаёт docs/HEALTH.md"
├── Импорты:            pathlib, re, datetime (стандартные → нет зависимостей)
├── Глобальные пути:    ROOT = Path(__file__).parent.parent
│                       DOCS = ROOT / "docs"
├── Файлы которые читает:   DOCS.rglob("*.md")
├── Файлы которые пишет:    DOCS / "HEALTH.md"
├── CLI-аргументы:      нет (нет argparse)
├── Функции:            count_files(), calc_score(), write_health()
└── Риск:               🟢 green (пишет только в один отдельный файл)
```

---

## Алгоритм определения риска

```python
def detect_risk(info: ScriptInfo) -> str:
    writes = info.writes

    # Красный: перезаписывает входные файлы (docs/**/*.md → docs/**/*.md)
    if any("**" in w for w in writes) and any("**" in r for r in info.reads):
        if set(writes) & set(info.reads):   # выход пересекается со входом
            return "red"

    # Жёлтый: пишет в docs/ но в конкретный файл
    if writes and all("HEALTH" in w or "METRICS" in w for w in writes):
        return "green"
    if writes:
        return "yellow"

    # Зелёный: ничего не пишет или пишет только в один отчётный файл
    return "green"
```

---

## Пример выходного каталога (фрагмент)

```json
{
  "improve_health.py": {
    "doc": "дашборд здоровья репозитория",
    "inputs": ["docs/**/*.md"],
    "outputs": ["docs/HEALTH.md"],
    "args": [],
    "risk": "green",
    "group": "quality",
    "has_dry_run": false,
    "imports_external": [],
    "lines": 89
  },
  "improve_crosslink_all.py": {
    "doc": "добавляет обратные ссылки во все docs/*.md",
    "inputs": ["docs/**/*.md"],
    "outputs": ["docs/**/*.md"],
    "args": ["--apply", "--dry-run", "--keywords"],
    "risk": "red",
    "group": "content",
    "has_dry_run": true,
    "imports_external": [],
    "lines": 312
  }
}
```

---

## Что каталог даёт на практике

**1. Автоматическое обновление CLAUDE.md**
Если добавили скрипт — каталог обновляется, CLAUDE.md можно перегенерировать.

**2. Проверка консистентности**
```
CLAUDE.md говорит: "improve_xyz.py — делает A"
AST говорит:       выходной файл — docs/B.md, не A

→ несоответствие: CLAUDE.md устарел
```

**3. Поиск по каталогу**
```bash
# Какие скрипты пишут в docs/HEALTH.md?
python scripts/improve_self.py --catalog --query "output:HEALTH.md"

# Какие скрипты без dry-run?
python scripts/improve_self.py --catalog --query "has_dry_run:false risk:red"

# Какие скрипты нет в группах run_all?
python scripts/improve_self.py --catalog --query "group:none"
```

**4. Обнаружение дублей**
Два скрипта читают одни файлы и пишут похожие выходы → вероятно дубли.

<!-- see-also -->

---

**Смотрите также:**
- [04-enrichment](04-enrichment.md)
- [01-concept](01-concept.md)
- [05-synthesis](05-synthesis.md)
- [02-architecture](02-architecture.md)

