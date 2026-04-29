# 7. PortalEntry Structure

## 7. PortalEntry Structure

Унифицированная структура данных, возвращаемая адаптерами.

```python
class PortalEntry:
    repo_name: str           # REQUIRED: откуда пришло
    native_id: str           # REQUIRED: id в native формате
    title: str               # REQUIRED: человекочитаемое имя
    summary: str             # REQUIRED: до 280 символов
    content: str             # REQUIRED: полный текст
    tags: list[str]          # OPTIONAL: ключевые слова
    confidence: float        # OPTIONAL: 0.0–1.0, default 1.0
    native_metadata: dict    # OPTIONAL: любые native-специфичные поля
    url: str | None          # OPTIONAL: прямая ссылка на источник
```

### 7.1. Field Semantics

- `repo_name` MUST совпадать с `name` в registry
- `native_id` MUST быть уникален в пределах Repo
- `title` SHOULD быть до 120 символов
- `summary` MUST быть до 280 символов (для предпросмотров)
- `content` MAY быть большим, но implementation MAY trimming при 
  transport
- `confidence` — субъективная оценка адаптера о релевантности entry 
  к query
- `native_metadata` — escape hatch для данных, не ложащихся в 
  стандартные поля

---
