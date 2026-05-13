---
title: "Примеры запросов (в Claude)"
tags:
  - collaboration
  - anthropic-vacancies
date: 2026-05-13
---

# Примеры запросов (в Claude)

<!-- toc-auto -->
## Contents

- [Примеры запросов (в Claude)](#примеры-запросов-в-claude)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (10)](#кто-ссылается-на-этот-документ-10)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> После подключения Claude может использовать tools автоматически.

---
<!-- tags: collaboration -->




## Примеры запросов (в Claude)

После подключения Claude может использовать tools автоматически. 
Примеры фраз, которые триггерят вызовы:

- «Найди в моей экосистеме svend4 всё про синтез» → `nautilus_query`
- «Какие репо есть в Nautilus?» → `nautilus_list_repos`
- «Проверь, согласован ли концепт 'bidir' между репо» → 
  `nautilus_consensus_check`
- «Покажи Q6-соседей для координаты 010100 на расстоянии 1» → 
  `nautilus_q6_neighbors`

<!-- similar-docs -->

---

## Похожие документы
- [[128-доступные-инструменты]] (сходство 0.21)
- 91-16-[[91-16-mcp-extension-informative|mcp-extension-informative]] (сходство 0.14)
- [[05-0-status-of-this-document]] (сходство 0.11)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Примеры запросов в Claude"
```

## Смотрите также
- [[128-доступные-инструменты]]
- 91-16-[[91-16-mcp-extension-informative|mcp-extension-informative]]
- [[05-0-status-of-this-document]]
- [[03-portal-protocol-md]]

<!-- backlinks-auto -->
## Упоминается в

- [[05-0-status-of-this-document|0. Status of This Document]]
- [[24-12-versioning-policy|12. Versioning Policy]]
- [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]
- [[92-17-versioning-policy|17. Versioning Policy]]
- [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]
- [[84-9-consensus-algorithm|9. Consensus Algorithm]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[128-доступные-инструменты|Доступные инструменты]]
- [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]
- [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[128-доступные-инструменты|Доступные инструменты]] _33%_
- [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]] _29%_
- [[05-0-status-of-this-document|0. Status of This Document]] _25%_
- [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] _21%_
- [[93-18-reference-implementation|18. Reference Implementation]] _21%_
- [[25-13-reference-implementation|13. Reference Implementation]] _17%_
- [[42-author-contact|Author & Contact]] _17%_
- [[48-content-overview|Content Overview]] _17%_
## Связанные документы

- [[128-доступные-инструменты|Доступные инструменты]] _48%_
- [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]] _42%_
- [[05-0-status-of-this-document|0. Status of This Document]] _29%_
- [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] _29%_
- [[42-author-contact|Author & Contact]] _25%_
- [[75-0-status-of-this-document|0. Status of This Document]] _25%_
- [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] _21%_
- [[24-12-versioning-policy|12. Versioning Policy]] _21%_

<!-- backlinks -->

---

## Кто ссылается на этот документ (10)
- [[03-portal-protocol-md]]
- [[05-0-status-of-this-document]]
- 124-конфигурация-для-[[124-конфигурация-для-claude-desktop|claude-desktop]]
- [[128-доступные-инструменты]]
- [[131-ограничения-текущей-версии-0-1-0-draft]]
- [[24-12-versioning-policy]]
- [[42-author-contact]]
- [[75-0-status-of-this-document]]
- _...ещё 2_

