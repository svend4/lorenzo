---
state: approved
---

# Метаскриптинг — Часть 2: Архитектура

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений. 118-appendix-a-шаблон-для-header-warning 119-appendix-b-примеры-расхождений-и-их-разрешения
Смотрите также
 05-synthesis
 118-appendix-a-шаблон-для-header-warning
 119-appendix-b-примеры-расхождений-и-их-разрешения
 132-planned-v0-2-0
 --
Кто ссылается на этот документ (12):
 CONCEPTS
 METHODOLOGY
 OUTLINE
 READABILITY
 READING_TIME
 SEA

---

<!-- toc -->
## Содержание

- [Ключевой инструмент: AST](#ключевой-инструмент-ast)
- [Что можно извлечь из скрипта через AST](#что-можно-извлечь-из-скрипта-через-ast)
- [Четыре режима метаскрипта](#четыре-режима-метаскрипта)
  - [Режим 1: --audit (аудит)](#режим-1---audit-аудит)
  - [Режим 2: --enrich (обогащение)](#режим-2---enrich-обогащение)
  - [Режим 3: --generate (генерация)](#режим-3---generate-генерация)
  - [Режим 4: --cross-read (перекрёстное чтение)](#режим-4---cross-read-перекрёстное-чтение)
- [Структура данных: ScriptCatalog](#структура-данных-scriptcatalog)
- [Паттерн «читаю → понимаю → улучшаю»](#паттерн-читаю-понимаю-улучшаю)
- [Безопасность: метаскрипт не меняет чужой код без --apply](#безопасность-метаскрипт-не-меняет-чужой-код-без---apply)

---

<!-- tags: security, ingestion, architecture -->




> Как устроен скрипт, который читает другие скрипты.

---

## Ключевой инструмент: AST

**AST (Abstract Syntax Tree)** — стандартный модуль Python. Читает `.py` файл и возвращает
дерево: функции, классы, импорты, аргументы — всё как объекты, без выполнения кода.

```python
import ast

source = open("scripts/improve_health.py").read()
tree = ast.parse(source)

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"Функция: {node.name}, строка {node.lineno}")
    if isinstance(node, ast.Import):
        print(f"Импорт: {[a.name for a in node.names]}")
```

**Почему AST, а не grep?**
```
grep "def " scripts/*.py     → находит строки с текстом "def "
AST                          → понимает структуру: это функция,
                               вот её аргументы, вот что она возвращает,
                               вот её docstring
```

---

## Что можно извлечь из скрипта через AST

```python
class ScriptInfo:
    name: str           # имя файла
    module_doc: str     # первый docstring модуля ("""...""")
    functions: list     # все def, их аргументы и docstring
    imports: list       # все import / from X import Y
    constants: list     # ROOT, DOCS, OUTPUT = ... (глобальные переменные)
    reads: list         # open(), Path.read_text() — что читает
    writes: list        # .write_text(), open(..., 'w') — что пишет
    cli_args: list      # argparse / sys.argv — какие флаги принимает
    calls: list         # какие другие скрипты/функции вызывает
```

Из этих данных строится полная карта скрипта.

---

## Четыре режима метаскрипта

### Режим 1: --audit (аудит)
Читает все 155 скриптов. Выдаёт отчёт:
```
Без docstring:         23 скрипта
Без аргументов CLI:    41 скрипт
Без вывода в docs/:    12 скриптов
Дублирующие функции:   8 пар
Упомянуты в docs/ но не существуют: 5 скриптов
```

### Режим 2: --enrich (обогащение)
Берёт конкретный скрипт, читает его через AST,
добавляет или улучшает: docstring, типизацию (`->` аннотации),
примеры в комментариях, секцию `if __name__ == "__main__"`.

### Режим 3: --generate (генерация)
По шаблону и описанию задачи создаёт новый скрипт.
Все 155 скриптов — это обучающий датасет паттернов.

### Режим 4: --cross-read (перекрёстное чтение)
Читает скрипты + docs/ одновременно. Находит:
- скрипты упомянутые в docs/ которых нет в scripts/
- скрипты в scripts/ которых нет в docs/
- несоответствия между описанием в CLAUDE.md и реальным кодом

---

## Структура данных: ScriptCatalog

```python
catalog = {
    "improve_health.py": {
        "doc":     "дашборд здоровья репозитория",
        "inputs":  ["docs/**/*.md"],
        "outputs": ["docs/HEALTH.md"],
        "args":    [],
        "imports": ["pathlib", "re", "datetime"],
        "group":   "quality",
        "has_dry_run": False,
        "risk":    "green",   # green/yellow/red
        "lines":   89,
        "functions": ["count_files", "calc_score", "write_health"]
    },
    "improve_crosslink_all.py": {
        "doc":     "добавляет обратные ссылки в каждый файл",
        "inputs":  ["docs/**/*.md"],
        "outputs": ["docs/**/*.md"],   # перезаписывает входные файлы!
        "args":    ["--apply", "--dry-run", "--keywords"],
        "risk":    "red",
        ...
    }
}
```

Этот каталог — основа для всех остальных операций.

---

## Паттерн «читаю → понимаю → улучшаю»

```
ВХОД                  АНАЛИЗ                  ВЫХОД
──────────────────    ──────────────────────  ───────────────────
improve_X.py    →     AST: что делает?    →   обогащённый скрипт
                      docs: что говорим?       исправленный docstring
                      CLAUDE.md: что ждём?     новый скрипт по шаблону
                      другие скрипты: паттерн  раздел в документации
```

---

## Безопасность: метаскрипт не меняет чужой код без --apply

Как и все контентные скрипты, метаскрипт работает по правилу:
```bash
python scripts/improve_self.py --audit              # только читает
python scripts/improve_self.py --enrich --dry-run   # показывает что изменит
python scripts/improve_self.py --enrich --apply     # применяет
```

Никогда не меняет чужой файл без явного `--apply`.

<!-- see-also -->

---

## Смотрите также
- [05-synthesis](05-synthesis.md)
- [118-appendix-a-шаблон-для-header-warning](../02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)
- [119-appendix-b-примеры-расхождений-и-их-разрешения](../02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md)
- [132-planned-v0-2-0](../02-anthropic-vacancies/132-planned-v0-2-0.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (12):**
- [CONCEPTS](../CONCEPTS.md)
- [METHODOLOGY](../METHODOLOGY.md)
- [OUTLINE](../OUTLINE.md)
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)
- [01-concept](01-concept.md)
- _...ещё 4_


<!-- similar-docs -->

---

**Похожие документы:**
- [02-architecture](../obsidian/meta-scripting/02-architecture.md) (сходство 0.96)
- [05-synthesis](05-synthesis.md) (сходство 0.23)
- [03-catalog](03-catalog.md) (сходство 0.23)

