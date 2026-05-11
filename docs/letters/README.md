# Открытые письма авторам проектов

<!-- toc-auto -->
## Contents

- [Что это](#что-это)
- [Письма по авторам](#письма-по-авторам)
- [Как использовать](#как-использовать)
- [Смотрите также](#смотрите-также)

<!-- summary -->
> Открытые письма — черновики первых сообщений авторам OSS-проектов, которые могут войти в Svyazi 2.0.

<!-- tags: contacts, letters, outreach, collaboration -->

> [!NOTE]
> Письма — открытые черновики. Их не обязательно отправлять в исходном виде:
> можно адаптировать, сократить или дать прямую ссылку на файл как «почитайте,
> что я думаю о вашем проекте».

---

## Что это

Svyazi 2.0 — локальная community intelligence platform, которая собирается из
лучших OSS-проектов с Хабра. У каждого проекта есть автор, с которым имеет смысл
поговорить: о синергии, об открытых вопросах, о возможном сотрудничестве.

Эти письма — не шаблонные «давайте сотрудничать», а конкретные технические вопросы
к конкретным решениям, которые мы изучили детально.

## Письма по авторам

| Автор | Проект | Слой | Ключевой вопрос |
|-------|--------|------|-----------------|
| [kksudo](kksudo.md) | AgentFS | knowledge/filesystem | Где граница .agentos vs machine-only state? |
| [spbmolot](spbmolot.md) | NGT Memory | memory | Как избежать ложной ко-активации при community discovery? |
| [VitalyOborin](vitalyoborin.md) | Yodoca + Wikontic | memory + graph | Что сильнее влияет на качество памяти: decay или типизация? |
| [AnastasiyaW](anastasiyaw.md) | knowledge-space + mclaude | knowledge/orchestration | Operational vs reference cards — один слой или два? |
| [nlaik](nlaik.md) | LiteParse + research-docs | rag/evidence | Как LiteParse обрабатывает таблицы с перенесёнными ячейками? |
| [zodigancode](zodigancode.md) | Rufler | orchestration | Как Rufler управляет откатом при частичном сбое роя? |
| [Antipozitive](antipozitive.md) | MemNet | memory/research | Как оценивается точность ассоциативных связей? |
| [VitaliySemenov](vitalysemenov.md) | agent-memory-mcp | memory/MCP | Как gardener-loop решает конфликты bi-temporal фактов? |

## Как использовать

```bash
# Прочитать письмо перед отправкой
cat docs/letters/kksudo.md

# Открыть все письма
ls docs/letters/*.md

# Найти письма по теме
grep -l "memory" docs/letters/*.md
```

Каждое письмо содержит:
- **Контекст** — что именно изучили в проекте
- **Синергия** — как проект вписывается в Svyazi 2.0
- **Конкретный вопрос** — один технический вопрос, требующий экспертизы автора
- **Предложение** — что может быть интересно автору

## Смотрите также

- [CONTACTS.md](../CONTACTS.md) — сводная таблица авторов
- [CONTACT_PRIORITY.md](../CONTACT_PRIORITY.md) — приоритеты контактов
- [contacts/](../contacts/) — контактные карточки
- [05-habr-projects/](../05-habr-projects/) — детальные профили проектов
