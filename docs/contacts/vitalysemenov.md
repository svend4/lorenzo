---
state: normalized
template: contact-outreach
version: "1.0"
author: "VitaliySemenov"
author_handle: "@moshael"
projects: [agent-memory-mcp, Memory OS]
platform: GitHub
status: not_started
priority: 2
created: 2026-05-10
last_contact: null
tags: [контакты, команда]
---
# Контакт: VitaliySemenov / agent-memory-mcp

<!-- toc-auto -->
## Contents

- [Профиль](#профиль)
- [Проект: agent-memory-mcp](#проект-agent-memory-mcp)
- [Вопросы для первого контакта](#вопросы-для-первого-контакта)
- [Шаблон первого сообщения](#шаблон-первого-сообщения)
- [История контактов](#история-контактов)
- [Смотрите также](#смотрите-также)


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Автор agent-memory-mcp (типизированная память для MCP + Memory OS с bi-temporal фактами). Документ содержит практические рекомендации и лучшие практики.
**Проекты:** agent-memory-mcp, Memory OS

---
<!-- tags: person, memory, mcp, contact -->

## Профиль

| Параметр | Значение |
|----------|---------|
| Ник | VitaliySemenov / moshael |
| GitHub | @moshael |
| Проекты | agent-memory-mcp, Memory OS |
| Слой в Svyazi | memory |
| Упомянут в файлах | docs/svyazi-2-0/components/agent-memory-mcp.md |
| Статус | not_started |

## Статус связи

_Контакт ещё не установлен. Приоритет: 2 (высокий)._

## Проект: agent-memory-mcp

Typed memory MCP-сервер с типами: `episodic`, `semantic`, `procedural`, `working`.  
Хранит в SQLite + WAL. Включает repo/doc search и path guard.

**Синергия с Lorenzo/Svyazi:**
- Готовый memory-слой с MCP API для Claude Desktop
- Typed memories дополняют CardEnvelope (episode → fact цикл)
- SQLite + WAL — локальный, GDPR-safe, offline-capable

## Вопросы для первого контакта

1. Есть ли публичная документация по Memory OS (bi-temporal facts, gardener-loop)?
2. Планируется ли поддержка внешних источников (CardIndex / doc-ingestion)?
3. Открыты к интеграционным PR для Svyazi 2.0?

## Первое сообщение

```

<!-- llm-contact-draft -->
## Улучшенное сообщение (LLM, 2026-05-29)

```
Hi Vitaly,

I've been following agent-memory-mcp and impressed by how you've structured typed memory contexts for MCP — the approach to semantic grounding feels like exactly what Knowledge OS needs for maintaining context coherence across heterogeneous OSS tools.

We're building Svyazi 2.0, a community intelligence platform that integrates best-in-class open projects into unified Knowledge OS architecture. Your memory layer is a critical piece: it solves the persistence and type-safety problem that most agent frameworks gloss over.

Specifically, I'm curious about your approach to memory serialization — are you planning versioning/migration strategies for schema evolution as agent systems grow more complex? We're thinking about how to handle that across different tool integrations, and your experience would be invaluable.

Would be great to discuss whether agent-memory-mcp could be positioned as the canonical memory backend in Svyazi's agent layer. Open to a quick technical sync if you're interested.
```
**Кому:** VitaliySemenov (@moshael)
**Тема:** Интеграция agent-memory-mcp в Knowledge OS (Svyazi 2.0)

Привет!

Изучил ваш agent-memory-mcp и Memory OS — очень близко к тому, 
что мы строим в Svyazi 2.0 (локальная Knowledge OS для коллаборационных сетей).

Особенно ценна идея typed memories (episodic → semantic → procedural) 
и bi-temporal facts с gardener-loop.

Работаю над интеграцией memory-слоя с CardIndex (Card Envelope) + 
AgentFS (граф знаний). Хотел бы обсудить:
- Как memory write API взаимодействует с внешними источниками?
- Планируется ли поддержка batch-ingestion из документов?

Репо: github.com/svend4/lorenzo | Спецификация: docs/PROTOTYPE_SPEC.md

С уважением,
Lorenzo / svend4
```

## История контактов

_Контакт ещё не установлен_

<!-- see-also -->

---

## Смотрите также
- [andrey-chuyan](andrey-chuyan.md)
- [antipozitive](antipozitive.md)
- [tagir-analyzes](tagir-analyzes.md)
- [cutcode](cutcode.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [agent-memory-mcp](../05-habr-projects/memory/agent-memory-mcp.md)
- [OUTLINE](../OUTLINE.md)
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [vitalysemenov](../obsidian/contacts/vitalysemenov.md) (сходство 0.86)
- [tagir-analyzes](tagir-analyzes.md) (сходство 0.39)
- [nlaik](nlaik.md) (сходство 0.37)

