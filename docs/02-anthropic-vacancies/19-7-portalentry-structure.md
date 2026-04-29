# 7. PortalEntry Structure
<!-- tags: ingestion, architecture, anthropic -->


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Унифицированная структура данных, возвращаемая адаптерами.

---



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

<!-- similar-docs -->

---

**Похожие документы:**
- [82-7-portalentry-structure](82-7-portalentry-structure.md) (сходство 0.25)


<!-- see-also -->

---

**Смотрите также:**
- [82-7-portalentry-structure](82-7-portalentry-structure.md)
- [123-portal-mcp-py](123-portal-mcp-py.md)
- [08-3-registry-nautilus-json](08-3-registry-nautilus-json.md)
- [81-6-adapter-interface](81-6-adapter-interface.md)

<!-- backlinks-auto -->
## Упоминается в

- [11. Security Considerations](23-11-security-considerations.md)
- [2. Terminology](07-2-terminology.md)
- [2. Terminology](77-2-terminology.md)
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md)
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md)
- [3. Принципы консолидации (Фаза C)](109-3-принципы-консолидации-фаза-c.md)
- [4. Passport (`passport.md`)](79-4-passport-passport-md.md)
- [5. Compatibility Levels](80-5-compatibility-levels.md)
- [6. Adapter Interface](18-6-adapter-interface.md)
- [6. Adapter Interface](81-6-adapter-interface.md)
- [7. PortalEntry Structure](82-7-portalentry-structure.md)
- [8. Q6 Space (Normative)](83-8-q6-space-normative.md)
- [Abstract](74-abstract.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [⬡](69-section.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [7. PortalEntry Structure](82-7-portalentry-structure.md) _48%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _33%_
- [2. Terminology](07-2-terminology.md) _25%_
- [2. Terminology](77-2-terminology.md) _25%_
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md) _25%_
- [6. Adapter Interface](18-6-adapter-interface.md) _21%_
- [4. Passport (`passport.md`)](79-4-passport-passport-md.md) _21%_
- [5. Compatibility Levels](80-5-compatibility-levels.md) _21%_
## Связанные документы

- [7. PortalEntry Structure](82-7-portalentry-structure.md) _42%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _29%_
- [2. Terminology](77-2-terminology.md) _29%_
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md) _29%_
- [2. Terminology](07-2-terminology.md) _21%_
- [6. Adapter Interface](18-6-adapter-interface.md) _21%_
- [⬡](69-section.md) _21%_
- [Abstract](74-abstract.md) _21%_
