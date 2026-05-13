---
title: "Proposal: Research-Docs-Liteparse × Agentfs"
date: 2026-05-13
card_id: 42118a818e41
card_type: proposal
state: raw
tags: [proposal, research-docs-liteparse, agentfs, ingestion, knowledge, integration]
projects: [research-docs-liteparse, agentfs]
similarity: 0.182
score: 0.432
source: proposal-gen
---

# Proposal: Research-Docs-Liteparse × Agentfs

<!-- summary -->
> Интеграция ingestion-слоя (Research-Docs-Liteparse) и knowledge-слоя (Agentfs): Research-Docs-Liteparse хранит знания в виде графа документов, Agentfs парсит и извлекает структуру из сырых источников.

<!-- tags: proposal, research-docs-liteparse, agentfs, ingestion, knowledge, integration -->

## Гипотеза интеграции

Research-Docs-Liteparse хранит знания в виде графа документов, Agentfs парсит и извлекает структуру из сырых источников. Интеграция: Agentfs → Card Envelope → Research-Docs-Liteparse — автоматическое обогащение графа из внешних источников.

## Проекты

| Параметр | Research-Docs-Liteparse | Agentfs |
|----------|———————————————————————|———————|
| Слой | ingestion | knowledge |
| Автор | nlaik | kksudo |
| Файл | `docs/05-habr-projects/knowledge/research-docs-liteparse.md` | `docs/05-habr-projects/knowledge/agentfs.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.182 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.432 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="research-docs-liteparse"`, edges к `agentfs`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["research-docs-liteparse", "agentfs"],
  "contract": "Card Envelope §3.1",
  "layer_a": "ingestion",
  "layer_b": "knowledge"
}
```

## Следующие шаги

- [ ] Изучить API Research-Docs-Liteparse и Agentfs
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с nlaik и kksudo
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_
