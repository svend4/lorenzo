---
template: template-of-templates
version: "1.0"
new_template_name: "[имя нового шаблона]"
created: 2026-04-29
tags: [шаблоны, мета]
---

# [имя нового шаблона]

Это мета-шаблон для создания новых шаблонов в `docs/templates/`.

## Что делать

1. Скопируйте этот файл в `docs/templates/<имя-нового-шаблона>.md`
2. Обновите frontmatter:
   - `template: <имя-нового-шаблона>`
   - `new_template_name` → удалить
3. Создайте JSON-схему `docs/templates/_schemas/<имя-нового-шаблона>.json`
4. Запустите валидацию: `python scripts/improve_validate_templates.py`

## Обязательные блоки шаблона

### 1. Frontmatter (YAML)

```yaml
---
template: <имя>
version: "1.0"
[обязательные поля для этого типа документа]
created: 2026-04-29
tags: [тег1, тег2]
---
```

### 2. Заголовок 1-го уровня

```markdown
# [Заголовок]
```

### 3. HTML-комментарии (для совместимости со скриптами)

```markdown
<!-- summary: краткое описание -->
<!-- tags: тег1, тег2 -->
```

### 4. Секции 2-го уровня (`##`)

Минимум 3-4 секции для содержательного шаблона.

### 5. Подвал

```markdown
---
_Создано: 2026-04-29_

<!-- see-also -->

---

**Смотрите также:**
- [связанный-шаблон](docs/templates/связанный.md)
```

## Обязательные поля JSON-Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "<имя>",
  "description": "[однострочное описание]",
  "type": "object",
  "required": ["template", "version", "..."],
  "properties": {
    "template": {"const": "<имя>"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
    ...
  },
  "required_sections": ["[Секция 1]", "[Секция 2]"]
}
```

## Чеклист добавления нового шаблона

- [ ] Создан `docs/templates/<имя>.md` с frontmatter
- [ ] Создана `docs/templates/_schemas/<имя>.json`
- [ ] Все required-секции присутствуют в шаблоне
- [ ] Все enum-значения в схеме покрывают плейсхолдеры
- [ ] Шаблон проверен через `improve_validate_templates.py` (не должен падать)
- [ ] init работает: `python scripts/improve_template_init.py --type <имя> --slug /tmp/test.md`
- [ ] Добавлено упоминание в `docs/templates/README.md`

## Типичные паттерны

### Поле статуса (enum)

```yaml
status: draft  # draft | proposed | accepted | rejected | superseded
```

### Поле даты (формат)

```yaml
created: 2026-04-29  # YYYY-MM-DD
```

### Поле списка тегов

```yaml
tags: [тег1, тег2, тег3]
```

### Поле ссылки на другой шаблон

```yaml
related: ["docs/templates/other.md"]
```

### ID с регулярным выражением

```yaml
some_id: "PREFIX-NNNN"  # схема: pattern: "^PREFIX-\\d{4}$"
```

---
_Создано: 2026-04-29_

<!-- see-also -->

---

**Смотрите также:**
- [research-note](docs/templates/research-note.md)
- [decision-record](docs/templates/decision-record.md)
- [`scripts/improve_validate_templates.py`](../../scripts/improve_validate_templates.py)
- [`scripts/improve_template_init.py`](../../scripts/improve_template_init.py)
