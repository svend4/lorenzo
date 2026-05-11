# Мониторинг зависимостей

> [!NOTE]
> Раздел `DEPENDABOT` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: dependabot, docs -->


<!-- summary -->
> `DEPENDABOT` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

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

<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [COLLAB_SUGGESTIONS](COLLAB_SUGGESTIONS.md)
- [CONTACT_PRIORITY](CONTACT_PRIORITY.md)
- [GRAPH](GRAPH.md)
- [OUTLINE](OUTLINE.md)
- [READABILITY](READABILITY.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [TABLES](TABLES.md)
- _...ещё 2_


<!-- similar-docs -->

---

**Похожие документы:**
- [DEPENDABOT](obsidian/DEPENDABOT.md) (сходство 0.84)
- [README](badges/README.md) (сходство 0.31)
- [README](obsidian/badges/README.md) (сходство 0.29)

