# Сходство 1: Composite Skills паттерн уже встроен

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Чем Hermes похож на нашу архитектуру (InGit + Cowork + Nautilus)

Сходств больше, чем различий. Это надо признать честно.

Сходство 1: Composite Skills паттерн уже встроен

Hermes имеет buit-in skills system с 118 навыками в v0.10.0. Каждый навык — это специализированный инструмент. Skills Hub на agentskills.io позволяет community-shared skills.

Это очень похоже на то, что Document 7 описывает как Composite Skills Agent. Только Hermes уже реализовал концепцию, в то время как наши документы её только теоретизируют.

Но есть нюанс: skills в Hermes — это generally functional capabilities (web search, code execution, file operations, etc.), не профессиональные специализации в нашем смысле. То есть Hermes имеет «skill для поиска в интернете», но не «sub-agent для немецкого социального права». Профессиональная глубина skills в Hermes ограничена.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Сходство 1 Composite Skills паттерн уже"
```

## Смотрите также
- [07-difference-2-domain-specialization](07-difference-2-domain-specialization.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)
- [05-similarity-5-self-hosting-privacy](05-similarity-5-self-hosting-privacy.md)
- [04-similarity-4-multi-platform](04-similarity-4-multi-platform.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в базе знаний репозитория Lorenzo._ _Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [CONCEPTS](../../CONCEPTS.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [07-difference-2-domain-specialization](07-difference-2-domain-specialization.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [01-similarity-1-composite-skills](../../obsidian/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md) (сходство 0.98)
- [07-difference-2-domain-specialization](07-difference-2-domain-specialization.md) (сходство 0.40)
- [07-difference-2-domain-specialization](../../obsidian/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md) (сходство 0.40)

