# Метаскриптинг — Часть 4: Обогащение скриптов

<!-- summary -->
> > Как скрипт улучшает другой скрипт, не зная заранее что в нём написано.

---

<!-- toc -->
## Содержание

- [Что значит «обогатить скрипт»](#что-значит-обогатить-скрипт)
- [Пять уровней обогащения](#пять-уровней-обогащения)
  - [Уровень 1: Docstring (без LLM)](#уровень-1-docstring-без-llm)
  - [Уровень 2: Типизация (без LLM)](#уровень-2-типизация-без-llm)
  - [Уровень 3: --dry-run флаг (без LLM)](#уровень-3---dry-run-флаг-без-llm)
  - [Уровень 4: Умный docstring (с LLM, ~$0.001)](#уровень-4-умный-docstring-с-llm-0001)
  - [Уровень 5: Кросс-обогащение (с LLM)](#уровень-5-кросс-обогащение-с-llm)
- [Алгоритм обогащения (пошагово)](#алгоритм-обогащения-пошагово)
- [Пример: было → стало](#пример-было-стало)

---

<!-- tags: ingestion -->




> Как скрипт улучшает другой скрипт, не зная заранее что в нём написано.

---

## Что значит «обогатить скрипт»

Существующий скрипт (`improve_xyz.py`) уже работает. Обогащение — это:

```
До:                              После:
────────────────────             ────────────────────────────────
нет docstring                →   docstring с входами/выходами
нет типизации                →   def func(path: Path) -> dict:
нет --dry-run                →   if args.dry_run: print(plan); return
нет примера запуска          →   # python scripts/improve_xyz.py --dry-run
нет if __name__ == "__main__"→   стандартный блок запуска
разные стили кода            →   унифицирован под проектный стиль
```

---

## Пять уровней обогащения

### Уровень 1: Docstring (без LLM)
Если у скрипта нет docstring — сгенерировать его из:
- имени файла (`improve_health` → «дашборд здоровья»)
- глобальных констант (`OUTPUT = DOCS / "HEALTH.md"` → «создаёт docs/HEALTH.md»)
- имён функций (`calc_score`, `write_health`)

```python
# Сгенерированный docstring без LLM:
"""
improve_health.py — дашборд здоровья репозитория.
Читает: docs/**/*.md
Пишет:  docs/HEALTH.md
Запуск: python scripts/improve_health.py
"""
```

### Уровень 2: Типизация (без LLM)
AST находит функции без аннотаций типов. По паттернам добавляет:
```python
# Было:
def count_files(docs_path):

# Стало:
def count_files(docs_path: Path) -> dict:
```

### Уровень 3: --dry-run флаг (без LLM)
Если скрипт пишет в файлы но не имеет `--dry-run` — добавить шаблонный блок:
```python
parser.add_argument("--dry-run", action="store_true",
                    help="Показать что изменится, не применять")
```

### Уровень 4: Умный docstring (с LLM, ~$0.001)
Передаём исходный код в claude-haiku. Он пишет осмысленный docstring
с пониманием что скрипт делает по смыслу, а не по имени файла.

```python
prompt = f"""
Вот Python-скрипт:
{source_code}

Напиши docstring в первые 6 строк файла. Формат:
\"\"\"
<имя файла> — <одна строка: что делает>.
Читает: <что читает>
Пишет:  <что пишет>
Запуск: python scripts/<имя> [--флаги]
\"\"\"
"""
```

### Уровень 5: Кросс-обогащение (с LLM)
Передаём скрипту контекст из других скриптов и docs/:
```
«Вот improve_health.py. Вот improve_metrics.py. Они оба читают docs/*.md.
Найди что health.py мог бы переиспользовать из metrics.py.
Предложи конкретные изменения.»
```

---

## Алгоритм обогащения (пошагово)

```
1. Прочитать скрипт через AST
2. Проверить: есть ли docstring?
   → нет: сгенерировать (уровень 1)
3. Проверить: есть ли типизация у > 50% функций?
   → нет: добавить (уровень 2)
4. Проверить: скрипт пишет файлы?
   → да: есть ли --dry-run?
     → нет: добавить шаблон (уровень 3)
5. Если --llm: отправить в claude-haiku (уровень 4)
6. Показать diff (если --dry-run) или применить (если --apply)
```

---

## Пример: было → стало

**До:**
```python
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

def count_words(f):
    return len(f.read_text().split())

def main():
    for f in DOCS.rglob("*.md"):
        print(f, count_words(f))

main()
```

**После (уровень 1-3, без LLM):**
```python
"""
improve_word_count.py — подсчёт слов в каждом документе.
Читает: docs/**/*.md
Пишет:  stdout (отчёт)
Запуск: python scripts/improve_word_count.py [--dry-run]
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def count_words(f: Path) -> int:
    return len(f.read_text(encoding="utf-8").split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files = list(DOCS.rglob("*.md"))
    if args.dry_run:
        print(f"[dry-run] обработаю {len(files)} файлов")
        return

    for f in files:
        print(f"{f.relative_to(ROOT)}: {count_words(f)} слов")


if __name__ == "__main__":
    main()
```

<!-- see-also -->

---

**Смотрите также:**
- [03-catalog](docs/meta-scripting/03-catalog.md)
- [02-architecture](docs/meta-scripting/02-architecture.md)
- [05-synthesis](docs/meta-scripting/05-synthesis.md)
- [07-llm](docs/processing-guide/07-llm.md)

