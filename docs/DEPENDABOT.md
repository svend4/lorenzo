# Мониторинг зависимостей

> [!NOTE]
> Документ `DEPENDABOT` создаётся автоматически.

<!-- alert-added -->
<!-- tags: dependabot, docs, analysis -->


<!-- summary -->
> Автоматически сформированный документ: `DEPENDABOT`.


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

**Кто ссылается на этот документ (7):**
- [OUTLINE](OUTLINE.md)
- [READABILITY](READABILITY.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [SEE_ALSO](SEE_ALSO.md)
- [TABLES](TABLES.md)
- [QA](svyazi-2-0/QA.md)

