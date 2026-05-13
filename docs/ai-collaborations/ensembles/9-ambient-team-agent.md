---
state: approved
---

# Ансамбль 9 — Ambient Team Agent

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. Telegram/Mattermost chat → thread context → code/RAG/AgentFS → issue/task board → agent execution → handoff/report
Telegram/Mattermost chat → thread context → code/RAG/AgentFS → issue/task board → agent execution → handoff/report
Дети этой связки:
Team Memory Bot — помнит, что обсуждали, какие решения приняли, какие задачи появились, кто ответственный.
**Проекты:** AgentFS, knowledge-space

---
<!-- tags: rag, orchestration, knowledge, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

9. Ambient Team Agent: «ассистент живёт в рабочем чате»

Родители: рабочий Telegram-ассистент + Skate + Coreness + OpenClaw/Moltbot + AgentFS.

В статье про ИИ-ассистента в рабочем Telegram-чате бот видит контекст веток обсуждений, имеет доступ к кодовой базе и может создавать GitHub issues с правильными labels по контексту разговора. Habr

Склеиваем это со Skate, где агент работает с Mattermost Boards, меняет статусы и закрывает задачи, с Coreness для мульти-тенантного self-hosted деплоя и с AgentFS/knowledge-space для долгой памяти. Habr+2Habr+2

Что рождается при склейке:

Получается агент, который живёт не в отдельном чате, а внутри команды.

Схема:

Telegram/Mattermost chat → thread context → code/RAG/AgentFS → issue/task board → agent execution → handoff/report

Дети этой связки:

Team Memory Bot — помнит, что обсуждали, какие решения приняли, какие задачи появились, кто ответственный.

Collaboration Matcher Bot — внутри сообщества видит обсуждения, навыки, проекты и предлагает «вам двоим стоит поговорить».

Operations Concierge — в чате принимает команды, создаёт задачи, запускает агентов, сообщает статусы, эскалирует человеку.

Главное новое свойство: AI перестаёт быть инструментом, который надо открывать. Он становится участником рабочего пространства.

Самые сильные связки для реального первого проекта

Если выбирать не абстрактно, а как «что можно собрать первым и получить необычное свойство», я бы ранжировал так.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Ансамбль 9 Ambient Team Agent"
```

## Смотрите также
- [7-domain-agent-app-factory](7-domain-agent-app-factory.md)
- [2-distributed-agent-workshop](2-distributed-agent-workshop.md)
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [4-web-to-knowledge-pipeline](4-web-to-knowledge-pipeline.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [2-distributed-agent-workshop](2-distributed-agent-workshop.md)
- [4-web-to-knowledge-pipeline](4-web-to-knowledge-pipeline.md)
- _...ещё 2_


<!-- similar-docs -->

---

**Похожие документы:**
- [9-ambient-team-agent](../../obsidian/ai-collaborations/ensembles/9-ambient-team-agent.md) (сходство 0.98)
- [7-domain-agent-app-factory](7-domain-agent-app-factory.md) (сходство 0.24)
- [7-domain-agent-app-factory](../../obsidian/ai-collaborations/ensembles/7-domain-agent-app-factory.md) (сходство 0.24)

