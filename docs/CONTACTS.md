# Контакты и авторы

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> Я собираю прототип Svyazi 2.0 — локальной community intelligence platform.
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---

<!-- toc -->
## Содержание

- [Ключевые авторы проектов](#ключевые-авторы-проектов)
- [GitHub репозитории](#github-репозитории)
- [Email адреса](#email-адреса)
- [Шаблон первого сообщения](#шаблон-первого-сообщения)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improve, collaboration -->




## Ключевые авторы проектов

| Автор | Проект | Слой | Упомянут в файлах | Первый вопрос |
|-------|--------|------|-------------------|---------------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 90 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 61 | — |
| **Cutcode** | AIF Handoff | orchestration | 68 | — |
| **Dmitriila** | SENTINEL | security | 64 | — |
| **MiXaiLL76** | Auto AI Router | security | 56 | — |
| **Sonia_Black** | knowledge-space | knowledge | 33 | — |
| **VitalyOborin** | Yodoca | memory | 73 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 81 | — |
| **andrey_chuyan** | Svyazi | ingestion/CardIndex | 29 | Стоит ли расширять CardIndex до person/project/episode/evidence или лучше держать разные индексы? |
| **kksudo** | AgentFS | knowledge/filesystem | 138 | Что лучше класть в .agentos, а что выносить в machine-only state вне vault conventions? |
| **lee-to** | AI Factory | orchestration | 19 | — |
| **nlaik** | LiteParse / research-docs | rag | 52 | — |
| **spbmolot** | NGT Memory | memory | 131 | Где проходит практическая граница между полезной ассоциацией и ложной ко-активацией тем для community discovery? |
| **tagir_analyzes** | Legal RAG | rag | 27 | — |
| **zodigancode** | Rufler | orchestration | 70 | — |

## GitHub репозитории

| Репозиторий | Упоминается в файлах |
|-------------|---------------------|
| `github.com/github.com/AnastasiyaW` | 8 |
| `github.com/github.com/AnastasiyaW/knowledge-space` | 17 |
| `github.com/github.com/Antipozitive` | 8 |
| `github.com/github.com/Cutcode` | 7 |
| `github.com/github.com/Dmitriila` | 8 |
| `github.com/github.com/MiXaiLL76` | 7 |
| `github.com/github.com/NicholasSpisak/second-brain` | 5 |
| `github.com/github.com/Sonia` | 8 |
| `github.com/github.com/VitalyOborin` | 7 |
| `github.com/github.com/VitalyOborin/yodoca` | 9 |
| `github.com/github.com/VladSpace` | 7 |
| `github.com/github.com/andrey` | 6 |
| `github.com/github.com/anthropics/mcp` | 9 |
| `github.com/github.com/artur-gavronchuk/tg-chat-analyser` | 8 |
| `github.com/github.com/camel-ai/camel` | 10 |
| `github.com/github.com/dementev-dev/adversarial-review` | 8 |
| `github.com/github.com/github` | 4 |
| `github.com/github.com/kagvi13/HMP` | 2 |
| `github.com/github.com/kagvi13/HMP.` | 3 |
| `github.com/github.com/kksudo` | 7 |
| `github.com/github.com/kksudo/agentfs` | 10 |
| `github.com/github.com/lib4u/rufler` | 3 |
| `github.com/github.com/mcp` | 14 |
| `github.com/github.com/nlaik` | 7 |
| `github.com/github.com/ruvnet/ruflo` | 3 |
| `github.com/github.com/settings/tokens` | 10 |
| `github.com/github.com/spbmolot` | 8 |
| `github.com/github.com/spbmolot/ngt-memory` | 9 |
| `github.com/github.com/svend4` | 8 |
| `github.com/github.com/svend4/data70` | 11 |
| `github.com/github.com/svend4/info1` | 24 |
| `github.com/github.com/svend4/info40` | 9 |
| `github.com/github.com/svend4/info7` | 9 |
| `github.com/github.com/svend4/ingit` | 28 |
| `github.com/github.com/svend4/meta` | 22 |
| `github.com/github.com/svend4/n` | 3 |
| `github.com/github.com/svend4/nautilus` | 101 |
| `github.com/github.com/svend4/nautilus.` | 5 |
| `github.com/github.com/svend4/nautilus.git` | 6 |
| `github.com/github.com/svend4/pro2` | 24 |
| `github.com/github.com/tagir` | 7 |
| `github.com/github.com/tree` | 2 |
| `github.com/github.com/users/svend4` | 10 |
| `github.com/github.com/vuguzum/self-aware-mcp-server` | 9 |
| `github.com/github.com/yjs/yjs` | 5 |
| `github.com/github.com/zodigancode` | 7 |

## Email адреса

- `lorenzo@dhlab.ai`

## Шаблон первого сообщения

```
Здравствуйте!
Я собираю прототип Svyazi 2.0 — локальной community intelligence platform.
В вашем проекте [ПРОЕКТ] меня особенно интересует слой [СЛОЙ].

Один конкретный вопрос: [ВОПРОС]

Если интересно — пришлю одностраничную схему интеграции.
Если нет — спасибо за публикацию, она уже повлияла на архитектуру.
```
