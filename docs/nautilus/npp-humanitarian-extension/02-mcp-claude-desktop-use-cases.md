---
state: approved
---

# Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — применение NPP к гуманитарным документам (юридические, социальные).

---
<!-- tags: roadmap, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — применение NPP к гуманитарным документам (юридические, социальные).

Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы типа:

«Найди все нормы SGB IX, упоминающие Persönliches Budget» → legal_query с format_type filter

«Какие решения Sozialgericht Dresden за 2024–2026 касались Eingliederungshilfe для психиатрических пациентов?» → legal_query с jurisdiction�/SN + topic_tags

«Соответствует ли содержание Bescheid от Sozialamt Dresden 15.11.2025 требованиям SGB XII § 62?» → legal_consensus_check между двумя источниками

«Какой срок Widerspruch на Bescheid от Y-Datum?» → автоматический расчёт через deadline metadata

«Покажи timeline кейса S 6 SO 58/26 ER» → nautilus_case_timeline

Это конкретно решает проблемы, с которыми вы работаете ежедневно в Sozialgericht-proceedings.

8. Коммерческая перспектива

Позволю себе отметить нечто важное. Legal-tech в Германии — большой и не до конца насыщенный рынок. Существующие решения (LexisNexis Advance, Beck-Online, JurionRS) — массивные корпоративные системы. AI-инструменты (Noxtua, PRIME LEGAL AI, Libra) — закрытые проприетарные.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Что он даёт вам на практике Через MCP"
```

## Смотрите также
- [03-what-doesnt-exist-on-market](03-what-doesnt-exist-on-market.md)
- [05-which-combination-more-valuable](05-which-combination-more-valuable.md)
- [04-section-4-sgb-pilot](../../anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md)
- 16-[mcp-extension](../npp-v1-1/16-mcp-extension.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации по графу._ _Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [02-mcp-claude-desktop-use-cases](../../obsidian/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md) (сходство 0.96)
- [11-relevance-ranking](../npp-v1-1/11-relevance-ranking.md) (сходство 0.27)
- [11-relevance-ranking](../../obsidian/nautilus/npp-v1-1/11-relevance-ranking.md) (сходство 0.27)

