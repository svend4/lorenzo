---
title: "Мониторинг зависимостей"
tags:
  - general
date: 2026-04-29
---

# Мониторинг зависимостей

<!-- summary -->
> title: "Мониторинг зависимостей"
**Проекты:** Svyazi, AgentFS, knowledge-space, Yodoca, NGT Memory

---
<!-- tags: memory, knowledge, ingestion, anthropic, collaboration -->




_Обновлено: 2026-04-29_

## Python-зависимости

| Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в |
|-------|------------|-----------------|--------|----------------|
| `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` |
| `mcp` | `1.0.0` | `—` | — | `scripts/mcp_server.py` |
| `pre-commit` | `3.0.0` | `—` | — | `.pre-commit-config.yaml` |
| `pyspellchecker` | `0.8.0` | `—` | — | `scripts/improve_spellcheck.py` |

## OSS-проекты (Svyazi 2.0)

| Проект | Репозиторий | Статус |
|--------|------------|--------|
| AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — |
| NGT Memory | [https://github.com/spbmolot/ngt-memory](https://github.com/spbmolot/ngt-memory) | — |
| Yodoca | [https://github.com/VitalyOborin/yodoca](https://github.com/VitalyOborin/yodoca) | — |
| knowledge-space | [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | — |

## Автоматизация

```bash
# Генерировать .github/dependabot.yml
python scripts/improve_dependabot.py --generate-config

# Проверить актуальные версии PyPI
python scripts/improve_dependabot.py --check-pypi
```

После `--generate-config` Dependabot автоматически откроет PR
при выходе новых версий зависимостей.

<!-- see-also -->

---

**Смотрите также:**
- [[ENTITIES]]
- [[CONTACT_PRIORITY]]
- [[vladspace]]
- [[cutcode]]


<!-- similar-docs -->

---

**Похожие документы:**
- [DEPENDABOT](docs/DEPENDABOT.md) (сходство 0.83)
- [GRAPH](docs/obsidian/GRAPH.md) (сходство 0.21)
- [NETWORK](docs/obsidian/NETWORK.md) (сходство 0.21)

