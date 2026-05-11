# Логика прогрессии: conservative escalation

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
<!-- tags: roadmap, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — пятиуровневая phased deployment Lorenzo (от ручного режима к полноценному network).

Логика прогрессии

Каждый уровень:

Building на previous level

Не requires next level (можно остановиться)

Имеет clear success criteria для перехода

Имеет off-ramp (можно вернуться или pivot)

Decision points:

После Уровня 0: Достаточно ли value от ручного режима? Если да, не двигаться. Если нет — Уровень 1.

После Уровня 1: Persistified Lorenzo полезен? Если да, проверить Уровень 2.

После Уровня 2: Public presence yields response? Если да, Уровень 3.

И так далее.

Это conservative escalation — escalate только если предыдущий уровень proves value.

Сейчас: продолжать экспериментировать в Уровне 0 + начать Уровень 1

Вы предложили правильный approach: продолжать экспериментировать вручную в рамках текущих сессий. Давайте структурируем это.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Логика прогрессии conservative"
```

## Смотрите также
- [00-overview](00-overview.md)
- [01-level-0-manual](01-level-0-manual.md)
- [06-level-5-full-network](06-level-5-full-network.md)
- [03-level-2-basic-lite](03-level-2-basic-lite.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документ индексирован в базе знаний репозитория.

<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [00-overview](00-overview.md)
- [01-level-0-manual](01-level-0-manual.md)
- [06-level-5-full-network](06-level-5-full-network.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [07-progression-logic](../../obsidian/lorenzo-agent/phased-deployment/07-progression-logic.md) (сходство 0.98)
- [01-level-0-manual](01-level-0-manual.md) (сходство 0.48)
- [01-level-0-manual](../../obsidian/lorenzo-agent/phased-deployment/01-level-0-manual.md) (сходство 0.47)

