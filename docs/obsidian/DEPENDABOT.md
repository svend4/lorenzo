---
title: "Мониторинг зависимостей"
tags:
  - memory
  - knowledge
  - ingestion
  - anthropic
  - collaboration
  - general
date: 2026-05-10
---

# Мониторинг зависимостей

<!-- toc-auto -->
## Contents

- [Python-зависимости](#python-зависимости)
- [OSS-проекты (Svyazi 2.0)](#oss-проекты-svyazi-20)
- [Автоматизация](#автоматизация)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> python scripts/improve_dependabot.py --generate-config
**Проекты:** Svyazi, AgentFS, knowledge-space, Yodoca, NGT Memory

---
<!-- tags: memory, knowledge, ingestion, anthropic, collaboration -->




_Обновлено: 2026-05-10_

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

## Смотрите также
- [[GRAPH]]
- [[NETWORK]]
- [[TAGS]]
- [[MINDMAP]]

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all.

<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

