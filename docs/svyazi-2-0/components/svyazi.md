# Svyazi

<!-- toc-auto -->
## Contents

- [Описание](#описание)
- [Ключевые компоненты и паттерны](#ключевые-компоненты-и-паттерны)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **Источник:** Хабр citeturn41search0
**Проекты:** Svyazi, CardIndex

---
<!-- tags: knowledge, ingestion, architecture, roadmap, collaboration -->




- **Автор:** Андрей Чуян
- **Источник:** Хабр citeturn41search0
- **Лицензия:** код закрыт. citeturn41search0
- **Maturity:** активный закрытый авторский прототип. citeturn41search0
- **Релевантность к Svyazi‑2.0:** очень высокая — это базовый ingest/normalize/discovery‑слой.

## Описание

Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций».

## Ключевые компоненты и паттерны

- 6 слоёв (ingest, extract, normalize, dedup, index, discover)
- YAML
- SHA256‑дедупликация
- Ollama + Qwen
- LLM + детерминированный код
- CardIndex
- Privacy by design

<!-- see-also -->

---

**Смотрите также:**
- [rufler](rufler.md)
- [memnet](memnet.md)
- [knowledge-space](knowledge-space.md)
- [yodoca](yodoca.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)

