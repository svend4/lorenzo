# Метаскриптинг — Часть 5: Синтез новых скриптов

<!-- summary -->
> > Как из существующих паттернов порождать новые скрипты.
**Проекты:** AgentFS

---
<!-- tags: knowledge, roadmap, self-improvement -->




> Как из существующих паттернов порождать новые скрипты.

---

## Откуда берутся паттерны

155 существующих скриптов — это обучающий датасет.
Каждый скрипт можно разложить на паттерн:

```
improve_health.py:
  паттерн = READ_MANY → AGGREGATE → WRITE_ONE_REPORT

improve_crosslink_all.py:
  паттерн = READ_MANY → TRANSFORM_EACH → WRITE_MANY_INPLACE

improve_search_index.py:
  паттерн = READ_MANY → BUILD_INDEX → WRITE_JSON

improve_llm_enrich.py:
  паттерн = READ_ONE → LLM_CALL → WRITE_ONE_ENRICHED
```

---

## Шесть базовых паттернов

| Паттерн | Читает | Делает | Пишет | Пример |
|---------|--------|--------|-------|--------|
| `REPORT` | docs/**/*.md | агрегирует | один .md отчёт | improve_health |
| `INDEX` | docs/**/*.md | строит индекс | .json файл | improve_search_index |
| `TRANSFORM` | docs/**/*.md | меняет каждый | те же файлы | improve_auto_toc |
| `EXTRACT` | docs/**/*.md | извлекает | отдельные файлы | improve_entities |
| `LLM_ENRICH` | один файл | LLM-вызов | обогащённый файл | improve_llm_enrich |
| `CROSS_READ` | scripts/*.py | анализирует код | отчёт о коде | improve_dependency_map |

---

## Три способа синтеза

### Способ A: По шаблону (без LLM)

Пользователь выбирает паттерн, заполняет параметры — скрипт генерируется:

```bash
python scripts/improve_self.py --generate \
  --pattern REPORT \
  --name improve_link_density \
  --input "docs/**/*.md" \
  --output "docs/LINK_DENSITY.md" \
  --description "плотность внутренних ссылок на 1000 слов"
```

Результат: готовый файл `scripts/improve_link_density.py` с правильной
структурой, docstring, argparse, dry-run, main() — нужно только дописать
бизнес-логику (саму формулу плотности).

### Способ B: По задаче с LLM

```bash
python scripts/improve_self.py --generate --llm \
  --task "найти файлы где упоминается AgentFS но нет ссылки на agentfs.md"
```

LLM (claude-haiku) получает:
- описание задачи
- несколько примеров существующих скриптов как образцы стиля
- структуру проекта

И пишет новый скрипт полностью.

### Способ C: Расширение существующего

```bash
python scripts/improve_self.py --extend improve_metrics.py \
  --add "подсчёт файлов без заголовка H1"
```

Читает `improve_metrics.py`, находит место где добавить новую метрику,
вставляет функцию и вызов.

---

## Защита от плохого кода

Сгенерированный код всегда:
1. Проходит `python -m py_compile` — синтаксис валиден
2. Проходит `--dry-run` — не ломает файлы при первом запуске
3. Сохраняется в `scripts/generated/` до ручного перемещения в `scripts/`
4. Получает метку `# GENERATED — проверить перед использованием`

```
scripts/
  generated/              ← карантин для новых скриптов
    improve_link_density.py  ← проверить, потом mv в scripts/
```

---

## Петля самообогащения (осторожно)

Теоретически: метаскрипт читает себя → находит что он не умеет → генерирует
дополнение → добавляет в себя. Это называется «петля самомодификации».

**Почему это опасно без контроля:**
```
Итерация 1: скрипт добавляет функцию A → OK
Итерация 2: скрипт на основе A добавляет B → возможно OK
Итерация 3: B конфликтует с чем-то → непредсказуемо
```

**Поэтому правило:** петля разрешена максимум на 1 итерацию,
каждый шаг требует `--apply` от человека или Claude.

```
человек: "улучши скрипт X"  →  Claude читает X  →  предлагает изменение
человек: "принять"          →  Claude применяет  →  стоп
                               (не идёт дальше без следующего запроса)
```

<!-- see-also -->

---

**Смотрите также:**
- [02-architecture](02-architecture.md)
- [01-concept](01-concept.md)
- [METHODOLOGY](../METHODOLOGY.md)
- [03-catalog](03-catalog.md)

