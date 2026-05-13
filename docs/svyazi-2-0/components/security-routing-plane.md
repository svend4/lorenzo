---
state: normalized
---

# Security + routing plane

<!-- toc-auto -->
## Contents

- [Описание](#описание)
- [Ключевые компоненты и паттерны](#ключевые-компоненты-и-паттерны)
- [Числовые наблюдения](#числовые-наблюдения)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->

> [!WARNING]
> Документ описывает ограничения, риски или требования безопасности. Читайте внимательно.

> - **Авторы:** Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig
**Проекты:** Svyazi, SENTINEL, LiteLLM, Auto AI Router, Tool Search

---
<!-- tags: orchestration, security, ingestion, collaboration -->




- **Авторы:** Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig
- **Источник:** Хабр + GitHub/docs citeturn20view10turn11search2turn19search5turn39view0turn39view1turn20view18
- **Лицензия:** смешанная — SENTINEL — неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2.0. citeturn20view10turn19search5turn28search3
- **Maturity:** активный operational stack. citeturn20view10turn11search2turn39view0turn39view1
- **Релевантность к Svyazi‑2.0:** очень высокая — без этого Svyazi‑2.0 будет либо дорогой, либо небезопасной.

## Описание

Рантайм‑безопасность и бюджетный execution plane для агентных систем.

## Ключевые компоненты и паттерны

- **SENTINEL** — micro‑model swarm для защиты агентной поверхности
- **LiteLLM** — unified API
- **Auto AI Router** — Go‑sidecar для rate limits и failover
- **Tool Search** — lazy MCP loading
- **RLM‑Toolkit** — budget / privacy presets

## Числовые наблюдения

- Tool Search: MCP‑overhead падает с 82k до 5.7k токенов; свободное окно растёт на 76k. citeturn39view1
- Auto AI Router: lightweight sidecar на Go с 30–80 MB RAM, OpenAI‑совместимый endpoint. citeturn39view0

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Security routing plane"
```

## Смотрите также
- [E-execution-plane](../ensembles/E-execution-plane.md)
- [research-docs-liteparse](research-docs-liteparse.md)
- [rufler](rufler.md)
- [yodoca](yodoca.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория._ _Доступен поиск._

<!-- similar-docs -->

---

**Похожие документы:**
- [security-routing-plane](../../obsidian/svyazi-2-0/components/security-routing-plane.md) (сходство 0.97)
- [E-execution-plane](../ensembles/E-execution-plane.md) (сходство 0.30)
- [E-execution-plane](../../obsidian/svyazi-2-0/ensembles/E-execution-plane.md) (сходство 0.29)

