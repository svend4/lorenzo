# Security + routing plane

<!-- summary -->
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

**Смотрите также:**
- [E-execution-plane](docs/svyazi-2-0/ensembles/E-execution-plane.md)
- [research-docs-liteparse](docs/svyazi-2-0/components/research-docs-liteparse.md)
- [rufler](docs/svyazi-2-0/components/rufler.md)
- [yodoca](docs/svyazi-2-0/components/yodoca.md)

