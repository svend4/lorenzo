# Changelog

Все важные изменения в `docs-toolkit` записываются в этот файл.

Формат: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
версионирование: [Semantic Versioning 2.0.0](https://semver.org/).

## [Unreleased]

### Added
- Persistent SQLite кэш embeddings (`docstoolkit/embeddings/cache.py`)
  с TF-IDF IDF и vectors, content-hash cache invalidation
- CLI команды: `docstoolkit index build/update/clear/stats`
- Skill testing framework (`docstoolkit/skills/testing.py`)
  с golden tests формата `*.test.yaml`
- CLI команды: `docstoolkit skills list/test`
- Skills registry: discovery от `.claude/skills/` + entry_points плагинов

### Changed
- TFIDFProvider принимает опциональный `cache=` для persistent IDF

### Performance
- TF-IDF.fit() с кэшем: 25x speedup на повторных вызовах
- Index build для 1194 документов: 1.4s (853 doc/sec)

## [0.1.0] - 2026-04-29

### Added
- Базовое ядро: `Config`, `load_config`, `write_doc`, `extract_frontmatter`, `parse_yaml`
- CLI команды: `init`, `doc new/validate/list-templates`, `ingest`, `serve`, `doctor`,
  `search`, `plugins list/inspect`
- Embeddings провайдеры: `TFIDFProvider`, `SentenceTransformersProvider` (опц.)
- HybridSearcher с RRF и weighted-fusion
- 7 ingest плагинов: markdown, html, mhtml, jupyter (stdlib);
  pdf (pypdf), epub (ebooklib), docx (python-docx) — опциональные
- Web ingest: url, arxiv, hackernews, habr (всё на stdlib)
- Plugin system через PEP 621 entry_points (6 групп)
- Multi-language: detect, i18n (RU+EN, 10 ключей), readability (Flesch-Kincaid)
- Doctor: 8 типов проверок системы
- Встроенный HTTP dashboard (`serve`) на stdlib
- Dockerfile (multi-stage), GitHub Action template, PyPI publish workflow
- Example plugin pack с 4 типами расширений

[Unreleased]: https://github.com/svend4/lorenzo/compare/toolkit-v0.1.0...HEAD
[0.1.0]: https://github.com/svend4/lorenzo/releases/tag/toolkit-v0.1.0
