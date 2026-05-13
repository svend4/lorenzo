# LLM Gap Analysis — семантические пробелы
<!-- tags: llm-gaps, docs -->


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> _Модель: claude-haiku-4-5 · Анализ структуры и связей документации_

---



_Модель: claude-haiku-4-5 · Анализ структуры и связей документации_

_API недоступен. Запустите с ANTHROPIC_API_KEY._


## Что анализируется

- Темы упомянутые, но не задокументированные
- Противоречия между документами
- Устаревшие планы и утверждения
- Недостающие перекрёстные ссылки
- Приоритеты для развития документации

---

_Источник: docs/ (первые 60 файлов) + архитектурные документы_


<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [DIGEST_AUTO](DIGEST_AUTO.md)
- [READABILITY](READABILITY.md)
- [SEARCH](SEARCH.md)


<!-- see-also -->

---

**Смотрите также:**
- [CONCEPT_GRAPH](CONCEPT_GRAPH.md)
- [LLM_SUMMARIES](LLM_SUMMARIES.md)
- [57-native-format](02-anthropic-vacancies/57-native-format.md)
- [CROSS_SECTION](CROSS_SECTION.md)



## Использование
```bash
# Запуск
python scripts/improve_llm_gaps.py
```
