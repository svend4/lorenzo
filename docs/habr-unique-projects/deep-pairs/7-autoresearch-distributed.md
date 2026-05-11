# Пара 7 — AutoResearch цикл × Распределённый рой

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, AutoResearch

---
<!-- tags: orchestration, ingestion, roadmap, self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 7. AutoResearch цикл × Распределённый рой

AutoResearch Карпаты на русском (https://habr.com/ru/articles/1010198/) — 630 строк кода, агент получает train.py + бюджет в минутах GPU, запускает эксперимент, измеряет, сохраняет/откатывает, повторяет. Hyperspace AI распределили его по 35 узлам p2p — за ночь 333 эксперимента. Single Grain адаптировали для маркетинга — 36 000 экспериментов за раз. Самоорганизация Дочкиной (https://habr.com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%.

Дети:

Autoresearch для prompt engineering Svyazi/legal — агент крутит варианты промпта на твоём legal-template-generator, мерит % правильно сгенерированных Stellungnahme на 100 эталонных делах, сохраняет улучшения, откатывает регрессы. То самое, чего Чуян хочет, но пока не сделал — самоулучшающийся промпт. На дешёвой карте за ночь — десятки итераций.

Distributed autoresearch over peer network — паттерн Hyperspace AI: несколько твоих знакомых юристов оставляют ноут включённым на ночь, общий agent разрабатывает шаблоны Widerspruch на их анонимизированных делах. Каждый вносит свой compute, все получают улучшенный шаблон. Этический бонус: одно дело анонимно, но улучшение приходит ко всем.

Sequential протокол для модерации inferred-фактов — у Чуяна inferred идут на ручную модерацию. Если поставить вместо одного человека Sequential-протокол из 8 малых агентов на дешёвых моделях, каждый видит результаты предшественников, — получаешь 44% качества выше координатора, и всё за стоимость одного звонка к Opus. Конкретное применение того, чего диссертация Дочкиной не показывает напрямую.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Пара 7 AutoResearch цикл Распределённый"
```

## Смотрите также
- 05-sourcecraft-cli-[claude-code-sequential-protokol-dochkinoy](../../technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)
- [05-supplementary-infrastructure](../key-findings/05-supplementary-infrastructure.md)
- [3-discovery-research](../final-ensembles/3-discovery-research.md)
- [4-riscv-privacy](../hardware-pairs/4-riscv-privacy.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [2-autoresearch-legal](../final-ensembles/2-autoresearch-legal.md)

