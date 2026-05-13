---
state: normalized
---

# habr-unique-projects/ — поиск уникальных проектов на Хабре

<!-- toc-auto -->
## Содержание




<!-- summary -->
> Уникальные проекты с Хабра: память, граф знаний, инструменты и авторы для коллаборации.

<!-- tags: habr, projects, overview -->

> [!TIP]
> Раздел содержит несколько документов. Используйте содержание для навигации.


## Источник

Файлы в корне репозитория:

- `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (MHTML)
- `… - Claude (1)` — почти идентичная вторая копия (MHTML)

## Подпапки

| Подпапка | О чём |
|---|---|
| [`analogues/`](analogues/) | Прямые аналоги Svyazi (K2-18, Wikontic, NGT Memory) и смежные проекты |
| [`key-findings/`](key-findings/) | Ключевые находки: Yodoca, MemNet, PDA-бот, Дочкина, инфраструктурные кусочки, синтез блок-карты |
| [`hardware-pairs/`](hardware-pairs/) | Пять hardware-near родительских пар + бонус (RRAM) и метафора |
| [`software-pairs/`](software-pairs/) | Пять софтверных родительских пар |
| [`deep-pairs/`](deep-pairs/) | Восемь углублённых софтверных пар (третья итерация) |
| [`final-ensembles/`](final-ensembles/) | Три финальных ансамбля + сводный список авторов |
| [`extra-examples/`](extra-examples/) | Расширенные примеры с Хабра по варианту D — 13 файлов: Svyazi (детально), ВШЭ нетворкинг, BrainBox, Claude subagents, HW-NL2Workflow, профессиональные платформы, knowledge workspace, multi-agent hub, federated platform, profession-specific workflows, конкретные next steps |
| [`search-strategy/`](search-strategy/) | Каркас стратегии поиска (заполняется по необходимости) |
| [`evaluation/`](evaluation/) | Каркас оценки уникальности и зрелости |

## Главная мысль диалога

> На Хабре за последние полгода кристаллизовалась полная экосистема софтверных кубиков для one-man-AI-company, где каждый автор закрывает свой узкий кусок.

Имена, которые стоит держать в голове: Дмитрий Дементьев (adversarial-review), Никита Списак (second-brain skill-pack для Obsidian), vuguzum (self-aware MCP), автор «Деревни» (tmux-агенты), автор «9 агентов», Андрей Чуян (Svyazi), Аскольд Романов (K2-18), Алла Чепурова (Wikontic), автор Yodoca, автор NGT Memory, автор PDA-бота. См. [`final-ensembles/4-summary-authors.md`](final-ensembles/4-summary-authors.md).

## Использование

```bash
python scripts/improve_semantic_search.py --query "habr unique projects поиск уникальных пр" --section habr-unique-projects
```

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов.

<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](../OUTLINE.md)
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)
- [4-summary-authors](final-ensembles/4-summary-authors.md)
- [README](search-strategy/README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [README](../obsidian/habr-unique-projects/README.md) (сходство 0.99)
- [4-summary-authors](../obsidian/habr-unique-projects/final-ensembles/4-summary-authors.md) (сходство 0.28)
- [4-summary-authors](final-ensembles/4-summary-authors.md) (сходство 0.28)

