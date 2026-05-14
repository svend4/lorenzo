---
state: approved
---

# Различие 1: Структурированная подложка отсутствует

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

Различие 1: Структурированная подложка отсутствует

Hermes не imposes структуру на ваши файлы и проекты. Каждый пользователь хранит данные как ему удобно. Hermes adapts to whatever структура есть.

InGit specifically provides структуру (00_inbox через 90_exports, YAML metadata schemas). Это:

Делает кросс-проектное сравнение возможным

Стандартизирует team collaboration (когда станет доступным)

Обеспечивает predictable patterns для Hermes (или Cowork) к работе с

Делает migration между systems easier

То есть InGit + Hermes могло бы быть лучшей комбинацией, чем Hermes alone. Hermes как агентский слой, InGit как структурный слой. Точно так же, как InGit + Cowork.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Различие 1 Структурированная подложка"
```

## Смотрите также
- [08-difference-3-federation-missing](08-difference-3-federation-missing.md)
- 03-similarity-3-[mcp-support](03-similarity-3-mcp-support.md)
- [05-similarity-5-self-hosting-privacy](05-similarity-5-self-hosting-privacy.md)
- [04-similarity-4-multi-platform](04-similarity-4-multi-platform.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all.

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [08-difference-3-federation-missing](08-difference-3-federation-missing.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [06-difference-1-structured-substrate-missing](../../obsidian/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md) (сходство 0.98)
- [03-similarity-3-mcp-support](03-similarity-3-mcp-support.md) (сходство 0.55)
- [03-similarity-3-mcp-support](../../obsidian/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md) (сходство 0.54)

