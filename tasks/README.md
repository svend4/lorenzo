# tasks/ — единый источник истины для задач

Каждый файл `*.task.yaml` — манифест задачи, который описывает все четыре слоя
(скилл / шаблон / плагин / скрипт-пайплайн) в одном месте.

## Зачем

Раньше:
- Скилл писался руками в `.claude/skills/`
- MCP-инструмент дублировал логику в `scripts/mcp_*_server.py`
- Шаблон жил отдельно в `docs/templates/`
- Скрипты вызывались через CLAUDE.md / docstring

В результате — drift между слоями. При добавлении нового триггера-фразы нужно
было редактировать 3-4 файла.

Теперь:
- Один YAML описывает всё.
- Генератор `scripts/improve_task_codegen.py` собирает остальные слои из манифеста.

## Формат

```yaml
id: write-contact
version: 1.0
description: Помогает написать первое сообщение автору проекта

trigger_phrases:
  - "напиши письмо автору"
  - "составь запрос на коллаборацию"

inputs:
  author: {type: string, required: true}
  project: {type: string, required: false}

template: contact-outreach              # докуумент-шаблон если задача создаёт документ
output_path: docs/contacts/{author}.md  # путь с переменными

mcp_server: lorenzo-contacts            # к какому серверу привязать инструмент
mcp_tool: write_contact                 # имя инструмента

pipeline:
  - read: docs/contacts/{author}.md
  - read_glob: "docs/05-habr-projects/**/*{project}*"
  - generate: "5-7 sentences personalized message"
  - write_section: "Первое сообщение"

post_checks:
  - file_exists: docs/contacts/{author}.md
  - section_exists: "Первое сообщение"

related:
  skills: [write-contact, status]
  templates: [contact-outreach]
```

## Команды

```bash
# Создать новый манифест из шаблона
python scripts/improve_task_init.py --id my-task

# Генерировать из манифестов скиллы / MCP-tools / docs ссылки
python scripts/improve_task_codegen.py
python scripts/improve_task_codegen.py --task write-contact   # один манифест
python scripts/improve_task_codegen.py --dry-run               # предпросмотр

# Список всех задач
python scripts/improve_task_codegen.py --list

# Валидация
python scripts/improve_task_codegen.py --validate
```

## Принципы

1. **Манифест read-only после генерации.** Изменения вносятся в YAML, потом codegen.
2. **Переменные везде одинаковые.** `{author}` в template, output_path, pipeline — одно и то же.
3. **Никакого drift.** Если YAML не описал триггер — скилл его не получит.
