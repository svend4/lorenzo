---
title: "Proposal: Knowledge-Space × Yodoca"
date: 2026-05-13
card_id: 32d7ac3f8fb7
card_type: proposal
state: raw
tags: [proposal, knowledge-space, yodoca, knowledge, memory, integration]
projects: [knowledge-space, yodoca]
similarity: 0.112
score: 0.412
source: proposal-gen
---

# Proposal: Knowledge-Space × Yodoca

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Интеграция knowledge-слоя (Knowledge-Space) и memory-слоя (Yodoca): Knowledge-Space обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция: epi

<!-- tags: proposal, knowledge-space, yodoca, knowledge, memory, integration -->

## Гипотеза интеграции

Knowledge-Space обеспечивает персистентную память эпизодов, Yodoca хранит структурированный граф знаний. Интеграция: episodes из Knowledge-Space как узлы графа в Yodoca — контекстно-зависимый retrieval с временно́й семантикой.

## Проекты

| Параметр | Knowledge-Space | Yodoca |
|----------|———————————————|——————|
| Слой | knowledge | memory |
| Автор | AnastasiyaW | VitalyOborin |
| Файл | `docs/05-habr-projects/knowledge/knowledge-space.md` | `docs/05-habr-projects/memory/yodoca.md` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | 0.112 |
| Комплементарность слоёв | ✅ высокая |
| Итоговый рейтинг | 0.412 |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="knowledge-space"`, edges к `yodoca`).

```json
{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["knowledge-space", "yodoca"],
  "contract": "Card Envelope §3.1",
  "layer_a": "knowledge",
  "layer_b": "memory"
}
```

## Следующие шаги

- [ ] Изучить API Knowledge-Space и Yodoca
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с AnastasiyaW и VitalyOborin
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено


---
_Сгенерировано improve_proposal_gen.py: 2026-05-13_

<!-- see-also -->

---

**Смотрите также:**
- [proposal-knowledge-space-x-ngt-memory](proposal-knowledge-space-x-ngt-memory.md)
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- [proposal-agentfs-x-yodoca](proposal-agentfs-x-yodoca.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [README](README.md)
- [proposal-01-synthesis-x-yodoca](proposal-01-synthesis-x-yodoca.md)
- [proposal-agentfs-x-yodoca](proposal-agentfs-x-yodoca.md)
- [proposal-knowledge-space-x-agent-memory-mcp](proposal-knowledge-space-x-agent-memory-mcp.md)
- [proposal-knowledge-space-x-ngt-memory](proposal-knowledge-space-x-ngt-memory.md)
- [proposal-wikontic-x-ngt-memory](proposal-wikontic-x-ngt-memory.md)
- [proposal-wikontic-x-yodoca](proposal-wikontic-x-yodoca.md)
- [READING_ORDER](../../READING_ORDER.md)
- _...ещё 1_

