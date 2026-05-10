# autofilled

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Файлов:** 1

## Содержание

- [research-summary.md](research-summary.md) — <!-- summary -->
<!-- tags: documentation, index, overview -->

## Подразделы

- [components/](components/) — components

Раздел `autofilled/` содержит документы, автоматически сформированные скриптом `improve_autofill.py` на основе данных других скриптов. Файлы заполняются из шаблонов с подстановкой актуальных значений: контактов, метрик, ссылок. При повторном запуске скрипта документы обновляются без потери структуры. Шаблоны хранятся в `docs/templates/`, данные для подстановки берутся из `docs/CONTACTS.md`, `docs/ENTITIES.md` и других источников.

## Использование

```bash
python scripts/improve_autofill.py --dry-run
```
