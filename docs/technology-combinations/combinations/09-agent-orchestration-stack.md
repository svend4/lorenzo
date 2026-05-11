# Комбинация 9: Agent Orchestration Stack

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: orchestration, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Agent-Bridge (habr.com/ru/articles/1016456/) - визуальное управление десятками CLI агентов из браузера, персистентные сессии

Conductor (habr.com/ru/articles/1001478/) - $2.8M YC, macOS-native parallel agent manager, 250% рост/месяц

Sequential Protocol (Dochkina's 8-16 small agents, 44% quality boost)

Дети:

Visual Multi-Agent IDE с persistent workspace

Agent-Bridge предоставляет infinite canvas для визуализации

Conductor управляет параллельным выполнением (workspace per task)

Sequential обеспечивает chain-of-agents без coordinator

Итог: один разработчик видит 10-20 агентов на доске, каждый в своём контейнере, работающих цепочкой

Cross-machine distributed agents с браузерным dashboard

Agent-Bridge + несколько нод (home PC + VPS + Cloud)

Conductor orchestrates tasks distribution

Sequential ensures chain completion across machines

ROI: Full stack development на $700/мес вместо $20k/мес team

Уникальность: Conductor — macOS only, Agent-Bridge — browser-based + multi-machine. Вместе = remote development paradise. Sequential устраняет bottleneck координатора.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 9 Agent Orchestration Stack"
```

## Смотрите также
- [05-benchmarks](../../03-technology-combinations/05-benchmarks.md)
- [12-multi-agent-observability-stack](12-multi-agent-observability-stack.md)
- 05-sourcecraft-cli-[claude-code-sequential-protokol-dochkinoy](05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)
- [32-consensus-based-multi-agent-coordination](32-consensus-based-multi-agent-coordination.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [09-14-extended](../synthesis-tables/09-14-extended.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ доступен для семантического поиска, BM25 и навигации через граф связей репозитория._ _Индексировано в поисковой базе репозитория Lorenzo._ _Индексировано._
