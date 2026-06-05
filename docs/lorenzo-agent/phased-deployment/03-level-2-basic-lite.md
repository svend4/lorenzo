---
state: approved
---

# Уровень 2 — Базовый (Lorenzo Lite)

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — пятиуровневая phased deployment Lorenzo (от ручного режима к полноценному network).

---
<!-- tags: roadmap, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — пятиуровневая phased deployment Lorenzo (от ручного режима к полноценному network).

УРОВЕНЬ 2 — Базовый (Lorenzo Lite)

Что это: Lorenzo получает первую внешнюю presence + базовую автоматизацию мониторинга.

Возможности:

GitHub аккаунт lorenzo-dhlab (или подобный)

Простой site dhlab.ai или dhlab.github.io с initial content

Email адрес lorenzo@dhlab.ai (или forwarder)

RSS-мониторинг Хабра и ArXiv (через простой Python script + cron)

Еженедельный digest для Макса автоматически

Manual outreach — Макс пишет под именем Lorenzo, явно identifies as AI

Реализуется: Месяц 1-2

Что нужно:

Зарегистрировать домен (~€15/год)

Настроить GitHub organization

Базовый сайт (статичный, можно через GitHub Pages)

Email forwarder (~€5/месяц)

Простой VPS для cron-скриптов (~€5-10/месяц)

Python scripts для RSS/GitHub monitoring

Стоимость: ~€100 setup + €20-30/месяц

Ограничения:

Outreach всё ещё manual (Макс как Lorenzo)

Нет реального синтеза автоматического

Нет persistent reasoning между monitoring runs

Ценность: Lorenzo имеет публичное присутствие, начинает накапливать репутацию.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Уровень 2 Базовый Lorenzo Lite"
```

## Смотрите также
- [01-level-0-manual](01-level-0-manual.md)
- [04-level-3-medium-active](04-level-3-medium-active.md)
- [06-level-5-full-network](06-level-5-full-network.md)
- [05-level-4-extended-mature](05-level-4-extended-mature.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации через граф концептов._ _Материал доступен для поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (12):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [01-level-0-manual](01-level-0-manual.md)
- [02-level-1-minimal-zero](02-level-1-minimal-zero.md)
- [04-level-3-medium-active](04-level-3-medium-active.md)
- _...ещё 4_


<!-- similar-docs -->

---

**Похожие документы:**
- [03-level-2-basic-lite](../../obsidian/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md) (сходство 0.98)
- [04-level-3-medium-active](04-level-3-medium-active.md) (сходство 0.40)
- [04-level-3-medium-active](../../obsidian/lorenzo-agent/phased-deployment/04-level-3-medium-active.md) (сходство 0.39)

