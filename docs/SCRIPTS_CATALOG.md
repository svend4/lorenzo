# Каталог скриптов

_Обновлено: 2026-04-29_

**Всего скриптов:** 146


## По группам


### analysis (9)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_clusters.py` | кластеризует файлы по тематической близости |  |
| `improve_complexity.py` | оценка читаемости документов. |  |
| `improve_dedup.py` | находит дублирующиеся файлы и похожие абзацы. | `--threshold` |
| `improve_density.py` | карта плотности тем по всем документам. |  |
| `improve_heatmap.py` | тепловая карта тем по разделам и файлам. |  |
| `improve_priorities.py` | ранжирует файлы по важности через TF-IDF. |  |
| `improve_sentiment.py` | тональный анализ документов. |  |
| `improve_similar.py` | для каждого документа находит топ-3 похожих. |  |
| `improve_word_freq.py` | частотный анализ слов по разделам. |  |

### analytics (6)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_citation_index.py` | индекс внешних URL по частоте цитирования. | `--domain`, `--min-citations` |
| `improve_cross_section.py` | граф концептов между секциями. | `--format`, `--min-secs`, `--top` |
| `improve_digest_auto.py` | автодайджест изменений за N дней. | `--days`, `--format`, `--since` |
| `improve_reading_time.py` | оценивает время чтения каждого документа. | `--section`, `--wpm` |
| `improve_topic_model.py` | тематическое моделирование без ML-зависимостей. | `--section`, `--top-words`, `--topics` |
| `improve_version_diff.py` | показывает содержательные изменения docs/ между коммитами. | `--from`, `--last`, `--to` |

### cicd (4)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_ci_config.py` | генерирует GitHub Actions workflow для docs. | `--dry-run`, `--minimal` |
| `improve_dependabot.py` | мониторинг версий OSS-компонентов Svyazi 2.0. | `--check-pypi`, `--generate-config` |
| `improve_github_issues.py` | создаёт GitHub Issues из ACTION_ITEMS.md и TODO-блоков. | `--create`, `--dry-run`, `--label` |
| `improve_pre_commit.py` | генерирует .pre-commit-config.yaml для проекта. | `--dry-run`, `--install` |

### content (4)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_abstract.py` | генерирует структурированный абстракт для каждого документа. | `--apply`, `--dry-run`, `--min-words`, `--section` |
| `improve_auto_linker.py` | автоматические внутренние ссылки в документах. | `--apply`, `--dry-run`, `--min-mentions`, `--section`, `--types` |
| `improve_auto_toc.py` | автоматически добавляет таблицу содержания (TOC) в файлы. | `--apply`, `--depth`, `--dry-run`, `--min-headings`, `--section` |
| `improve_gap_filler.py` | заполняет пустые секции найденным контентом (BM25). | `--apply`, `--dry-run`, `--mode`, `--section`, `--top` |

### deeptext (10)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_chunk_semantic.py` | семантическое чанкинг документов для RAG. | `--max-words`, `--min-words`, `--output`, `--section` |
| `improve_concept_graph.py` | граф концептов из базы знаний. | `--format`, `--min-weight`, `--section`, `--top-concepts` |
| `improve_contradiction_check.py` | поиск противоречивых утверждений в базе знаний. | `--min-confidence`, `--section` |
| `improve_keyword_index.py` | инвертированный индекс: слово → файлы. | `--min-df`, `--query`, `--section`, `--top` |
| `improve_named_entity_index.py` | индекс именованных сущностей из всей базы. | `--min-mentions`, `--section`, `--type` |
| `improve_paragraph_quality.py` | находит проблемные абзацы в документах. | `--section`, `--verbose` |
| `improve_passage_retrieval.py` | BM25-поиск на уровне абзацев. | `--context`, `--index`, `--min-words`, `--query`, `--section`, `--top` |
| `improve_text_segmenter.py` | разбивает большие файлы на логические части. | `--apply`, `--dry-run`, `--max-words`, `--part-size`, `--section` |
| `improve_timeline_events.py` | извлекает даты и события из базы знаний. | `--format`, `--from`, `--section`, `--to` |
| `improve_vocabulary_richness.py` | метрики богатства словаря документов. | `--section`, `--top`, `--window` |

### export (7)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_confluence.py` | конвертирует docs/*.md в формат Confluence Wiki Markup. | `--dry-run`, `--section` |
| `improve_export_csv.py` | экспортирует метаданные всех docs/ в CSV. |  |
| `improve_export_html.py` | экспортирует все docs/ в единый HTML-сайт. |  |
| `improve_export_json.py` | экспортирует всю структуру docs/ в structured JSON. |  |
| `improve_export_report.py` | единый сводный отчёт по всей базе знаний. | `--no-projects`, `--sections`, `--title` |
| `improve_obsidian.py` | готовит docs/ для импорта в Obsidian. | `--dry-run`, `--in-place`, `--section` |
| `improve_rss.py` | генерирует RSS/Atom фид из истории git-коммитов. | `--base-url`, `--max-items` |

### extract (9)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_abbreviations.py` | словарь аббревиатур и сокращений из docs/. |  |
| `improve_action_items.py` | извлекает задачи, риски, решения и TODO из docs/. |  |
| `improve_concepts.py` | извлекает определения понятий прямо из текстов. |  |
| `improve_decisions.py` | извлекает ключевые выводы и решения из всех файлов. |  |
| `improve_entities.py` | извлечение именованных сущностей из docs/. |  |
| `improve_extract_code.py` | извлекает все code-блоки из docs/. |  |
| `improve_extract_tables.py` | извлекает все Markdown-таблицы из docs/ |  |
| `improve_kpi.py` | извлекает числовые KPI и метрики из docs/. |  |
| `improve_questions.py` | извлекает открытые вопросы из docs/. |  |

### generate (7)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_autofill.py` | заполняет шаблоны данными из уже сгенерированных скриптов. | `--dry-run` |
| `improve_badges.py` | генерирует SVG-бейджи для README. |  |
| `improve_faq.py` | строит FAQ из QA-паттернов в документах. |  |
| `improve_footnotes.py` | автоматически связывает технические термины с глоссарием. |  |
| `improve_see_also.py` | добавляет блок "See Also / Смотрите также" |  |
| `improve_templates.py` | генерирует шаблоны документов для каждого раздела. |  |
| `improve_word_cloud.py` | генерирует SVG word cloud из топ-слов репозитория. |  |

### graph (4)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_graph.py` | строит граф связей между проектами. |  |
| `improve_mindmap.py` | строит майндмап всего репозитория в формате Mermaid mindmap. |  |
| `improve_narrative.py` | строит нарративную линию проекта. |  |
| `improve_network.py` | анализ сети авторов и проектов. |  |

### index (6)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_backlinks.py` | индекс обратных ссылок. |  |
| `improve_crossrefs.py` | строит карту перекрёстных ссылок между файлами. |  |
| `improve_glossary.py` | извлекает все проекты, авторов и URL из docs/, |  |
| `improve_index_update.py` | инкрементальное обновление search_index.json. |  |
| `improve_search_index.py` | строит полнотекстовый JSON-индекс всех docs/. |  |
| `improve_timeline.py` | извлекает даты и временные маркеры из всех docs/, |  |

### nlpplus (10)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_empty_sections.py` | поиск и заполнение пустых секций. | `--fill`, `--min-content`, `--report`, `--section`, `--suggest` |
| `improve_faceted_search.py` | фасетный поиск по базе знаний. | `--after`, `--entity`, `--format`, `--min-words`, `--query`, `--section`, … |
| `improve_heading_audit.py` | аудит иерархии заголовков. | `--section`, `--verbose` |
| `improve_knowledge_map.py` | единый дашборд всей базы знаний. |  |
| `improve_language_split.py` | анализ языкового состава документов. | `--min-mix`, `--report`, `--section`, `--split` |
| `improve_passive_voice.py` | детектор пассивного залога и номинализаций (RU/EN). | `--section`, `--top`, `--verbose` |
| `improve_question_extractor.py` | извлечение вопросов, гипотез и TODO. | `--min-words`, `--section`, `--type` |
| `improve_reading_list.py` | персонализированный список чтения по теме. | `--format`, `--query`, `--section`, `--top` |
| `improve_similar_passages.py` | поиск похожих абзацев между файлами (TF-IDF cosine). | `--min-sim`, `--min-words`, `--section`, `--top` |
| `improve_textrank.py` | извлекательное резюме через TextRank (без LLM). | `--apply`, `--query`, `--section`, `--sentences` |

### quality (10)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_alerts.py` | добавляет GitHub Markdown callout-блоки в ключевые файлы. |  |
| `improve_broken_links.py` | проверяет внутренние ссылки в docs/. | `--dry-run`, `--fix` |
| `improve_consistency.py` | находит разные написания одного термина, |  |
| `improve_content_gaps.py` | находит темы, упомянутые в docs/, но без собственного документа. | `--min-mentions`, `--section` |
| `improve_metrics.py` | метрики качества документации. |  |
| `improve_missing.py` | находит темы/проекты упомянутые в документах |  |
| `improve_orphans.py` | находит документы без входящих ссылок (orphan docs). |  |
| `improve_readability_v2.py` | индекс читаемости текстов. | `--section` |
| `improve_spellcheck.py` | проверка орфографии в docs/. | `--fix`, `--section` |
| `improve_validate.py` | валидация структуры репозитория. |  |

### reports (19)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_benchmark.py` | замеряет и записывает время выполнения скриптов. | `--group`, `--report`, `--script` |
| `improve_changelog.py` | генерирует CHANGELOG из git-истории репозитория. |  |
| `improve_compare.py` | сравнивает текущее состояние docs/ с предыдущим коммитом. |  |
| `improve_contact_priority.py` | ранжирует авторов по приоритету для контакта. |  |
| `improve_contacts.py` | извлекает email, Telegram, GitHub, Habr-ники |  |
| `improve_cost.py` | оценка стоимости разработки MVP. |  |
| `improve_coverage.py` | матрица покрытия: какие файлы имеют summary, теги, TOC, crossrefs, статус. | `--section` |
| `improve_digest.py` | дайджест недавних изменений репозитория. |  |
| `improve_health.py` | дашборд здоровья репозитория. |  |
| `improve_progress.py` | трекер прогресса MVP-проекта. |  |
| `improve_progress_sync.py` | синхронизирует PROGRESS.md с реальным состоянием файлов. | `--dry-run` |
| `improve_qa.py` | генерирует Q&A листы для каждого раздела docs/. |  |
| `improve_reading_order.py` | строит рекомендуемый порядок чтения документов |  |
| `improve_report.py` | итоговый executive report о состоянии репозитория. |  |
| `improve_schedule.py` | строит расписание проекта из ACTION_ITEMS и временных маркеров. |  |
| `improve_scoring.py` | система оценки готовности проекта к запуску (Go/No-Go). |  |
| `improve_sitemap.py` | генерирует навигационную карту репозитория. |  |
| `improve_staleness.py` | находит документы которые давно не обновлялись или неполные. | `--days`, `--no-git` |
| `improve_stats.py` | детальная статистика по каждому разделу docs/. |  |

### structure (6)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_autocorrect.py` | применяет исправления из CONSISTENCY.md: | `--dry-run` |
| `improve_merge_short.py` | сливает слишком короткие файлы с предыдущим соседом. |  |
| `improve_readmes.py` | создаёт README.md для каждой подпапки docs/. |  |
| `improve_summaries.py` | добавляет краткую аннотацию в начало каждого файла. |  |
| `improve_tags.py` | тегирует каждый файл по темам, создаёт docs/TAGS.md |  |
| `improve_toc.py` | добавляет Table of Contents в начало файлов длиннее 500 слов. |  |

### textwork (8)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_compare_docs.py` | сравнивает два документа: общее, различия, пересечения. | `--a`, `--b`, `--batch`, `--out`, `--section`, `--top` |
| `improve_crosslink_all.py` | прописывает обратные ссылки (backlinks) во все файлы. | `--apply`, `--dry-run`, `--keywords`, `--min-refs` |
| `improve_duplicate_across.py` | поиск похожих текстов между репозиториями/папками. | `--internal`, `--other-dir`, `--other-repo`, `--section`, `--threshold` |
| `improve_merge_by_topic.py` | склеивает файлы-фрагменты одной темы в единый документ. | `--apply`, `--dry-run`, `--min-group`, `--section`, `--threshold` |
| `improve_outline.py` | строит иерархический outline всей базы знаний. | `--depth`, `--format`, `--section` |
| `improve_reclassify.py` | раскладывает файлы по подпапкам на основе TF-IDF тематики. | `--apply`, `--dry-run`, `--section`, `--topics` |
| `improve_source_map.py` | строит карту происхождения текстов. | `--authors`, `--format`, `--section`, `--show-imported` |
| `improve_subtopic_fill.py` | дополняет файлы-заглушки контентом из базы знаний. | `--apply`, `--dry-run`, `--min-words`, `--section` |

### без группы (27)

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_changelog_auto.py` | автоматический changelog из git-истории. |  |
| `improve_component_matrix.py` | матрица совместимости и возможностей компонентов. |  |
| `improve_contact_status.py` | обновляет статус контакта в docs/contacts/<slug>.md. | `--agreed`, `--author`, `--list`, `--messaged`, `--note`, `--replied`, … |
| `improve_dependency_map.py` | карта зависимостей: скрипты → выходные файлы. |  |
| `improve_digest_weekly.py` | еженедельный дайджест изменений репозитория. |  |
| `improve_epub.py` | собирает docs/ в EPUB через pandoc. | `--check`, `--output`, `--section`, `--title` |
| `improve_external_compare.py` | сравнивает документы базы с внешними источниками. | `--auto`, `--file`, `--limit`, `--query`, `--section`, `--url` |
| `improve_index_master.py` | главный навигационный хаб docs/. |  |
| `improve_kpi_snapshot.py` | исторические снапшоты ключевых метрик. |  |
| `improve_link_preview.py` | проверяет внешние ссылки в docs/ и кэширует их статус. | `--refresh`, `--section`, `--timeout` |
| `improve_llm_contact.py` | генерирует персонализированное первое сообщение автору через LLM. | `--all`, `--author`, `--dry-run` |
| `improve_llm_enrich.py` | семантическое обогащение проектных файлов через Claude API. | `--dry-run`, `--file`, `--force`, `--model`, `--section` |
| `improve_llm_gaps.py` | семантический поиск пробелов через Claude API. |  |
| `improve_llm_qa.py` | ответы на вопросы по всей базе знаний Lorenzo через Claude API. | `--batch`, `--clear-cache`, `--dry-run`, `--no-cache`, `--question`, `--save` |
| `improve_llm_summary.py` | каскадная суммаризация больших документов через Claude API. | `--dry-run`, `--file`, `--section` |
| `improve_mcp_dashboard.py` | статистика вызовов MCP-серверов. |  |
| `improve_mcp_test.py` | smoke-тесты для всех MCP-серверов. |  |
| `improve_onboarding.py` | руководство для новых участников проекта. |  |
| `improve_risk_register.py` | реестр рисков проекта Svyazi 2.0. |  |
| `improve_run_all.py` | мастер-скрипт для запуска всех improve_*.py. | `--changed`, `--dry-run`, `--fast`, `--group`, `--only`, `--parallel`, … |
| `improve_task_codegen.py` | генератор слоёв (скилл / MCP-tool / index) из манифестов tasks/*.task.yaml. | `--dry-run`, `--list`, `--task`, `--validate` |
| `improve_tech_radar.py` | tech radar для технологий проекта Svyazi 2.0. |  |
| `improve_template_init.py` | инициализация нового документа из шаблона. | `--list`, `--show`, `--slug`, `--type`, `--vars` |
| `improve_template_migrate.py` | миграции frontmatter при изменении схемы шаблона. | `--all`, `--apply`, `--dry-run`, `--template` |
| `improve_validate_templates.py` | валидация документов по схемам шаблонов. | `--file`, `--report`, `--section`, `--strict` |
| `improve_watch.py` | следит за изменениями в docs/ и перезапускает нужные скрипты. | `--changed`, `--fast`, `--group`, `--interval` |
| `improve_watcher.py` | автономный агент-наблюдатель (Ступень 6). | `--once` |

## Подробно


### `improve_abbreviations.py` _(группа: extract)_

**словарь аббревиатур и сокращений из docs/.**

Ищет: "ABC — это ...", "ABC (от англ. ...)", "ABC: ...", капс-слова. Создаёт docs/ABBREVIATIONS.md.


### `improve_abstract.py` _(группа: content)_

**генерирует структурированный абстракт для каждого документа.**

Без LLM, по паттернам в тексте определяет: - Проблема/контекст (предложения с «проблем», «задач», «нужно», «требует») - Подход/метод    (предложения с «решени», «метод», «алгоритм», «подход») - Результат       (предложения с «результат», «достигн», «получен», «вывод») - Ключевые слова  (TF-IDF топ-8)

**Флаги:** `--apply`, `--dry-run`, `--min-words`, `--section`


### `improve_action_items.py` _(группа: extract)_

**извлекает задачи, риски, решения и TODO из docs/.**

Создаёт docs/ACTION_ITEMS.md.


### `improve_alerts.py` _(группа: quality)_

**добавляет GitHub Markdown callout-блоки в ключевые файлы.**

Форматы: > [!NOTE], > [!WARNING], > [!TIP], > [!IMPORTANT]. Анализирует содержимое и вставляет подходящий callout в начало файла.


### `improve_auto_linker.py` _(группа: content)_

**автоматические внутренние ссылки в документах.**

Находит упоминания проектов/технологий/людей из named_entities.json и превращает их в markdown-ссылки на соответствующие файлы. Алгоритм: 1. Загружает named_entities.json → словарь {имя: best_file} 2. Для каждого файла ищет plain-text упоминания сущностей

**Флаги:** `--apply`, `--dry-run`, `--min-mentions`, `--section`, `--types`


### `improve_auto_toc.py` _(группа: content)_

**автоматически добавляет таблицу содержания (TOC) в файлы.**

Вставляет ## Contents после первого H1 заголовка. Идемпотентно: обновляет существующий TOC по маркеру. Пропускает файлы с менее чем 3 подзаголовками. Режимы:

**Флаги:** `--apply`, `--depth`, `--dry-run`, `--min-headings`, `--section`


### `improve_autocorrect.py` _(группа: structure)_

**применяет исправления из CONSISTENCY.md:**

заменяет все нестандартные написания на канонические прямо в файлах.

**Флаги:** `--dry-run`


### `improve_autofill.py` _(группа: generate)_

**заполняет шаблоны данными из уже сгенерированных скриптов.**

Нулевая стоимость ($0), детерминировано. Требует предварительного запуска: improve_contacts.py, improve_tags.py, improve_similar.py, improve_entities.py Создаёт: docs/contacts/  — заполненные contact-outreach.md для каждого автора (15 файлов)

**Флаги:** `--dry-run`


### `improve_backlinks.py` _(группа: index)_

**индекс обратных ссылок.**

Для каждого файла показывает, какие другие файлы на него ссылаются. Добавляет блок "Кто ссылается" в конец файла и создаёт docs/BACKLINKS.md.


### `improve_badges.py` _(группа: generate)_

**генерирует SVG-бейджи для README.**

Показывает: здоровье репо, скоринг, кол-во документов, скриптов, слов. Создаёт docs/badges/ и вставляет бейджи в корневой README.md.


### `improve_benchmark.py` _(группа: reports)_

**замеряет и записывает время выполнения скриптов.**

Хранит историю в docs/benchmark.json, показывает тренды.

**Флаги:** `--group`, `--report`, `--script`


### `improve_broken_links.py` _(группа: quality)_

**проверяет внутренние ссылки в docs/.**

Находит ссылки на несуществующие файлы и якоря. Создаёт docs/BROKEN_LINKS.md. Новое: --fix автоматически исправляет ссылки с неправильным регистром или лишними ../.

**Флаги:** `--dry-run`, `--fix`


### `improve_changelog.py` _(группа: reports)_

**генерирует CHANGELOG из git-истории репозитория.**

Группирует коммиты по типам (feat/fix/chore/improve) и датам. Создаёт docs/CHANGELOG.md и CHANGELOG.md в корне.


### `improve_changelog_auto.py` _(группа: без группы)_

**автоматический changelog из git-истории.**

Группирует коммиты по типу (feat/fix/docs/chore), строит версионированный лог. Создаёт docs/CHANGELOG_AUTO.md.


### `improve_chunk_semantic.py` _(группа: deeptext)_

**семантическое чанкинг документов для RAG.**

Делит тексты по смысловым границам (не механически по N токенов): - H2/H3 заголовки = границы чанков - Если секция > MAX_CHUNK_WORDS — дополнительно делит по абзацам - Если секция < MIN_CHUNK_WORDS — объединяет с соседней Каждый чанк содержит:

**Флаги:** `--max-words`, `--min-words`, `--output`, `--section`


### `improve_ci_config.py` _(группа: cicd)_

**генерирует GitHub Actions workflow для docs.**

Создаёт: .github/workflows/docs.yml       — основной CI для docs .github/workflows/docs_check.yml — быстрая проверка при PR

**Флаги:** `--dry-run`, `--minimal`


### `improve_citation_index.py` _(группа: analytics)_

**индекс внешних URL по частоте цитирования.**

Для каждого внешнего URL показывает: - сколько файлов его цитируют - в каких секциях - насколько «авторитетен» домен в контексте проекта Создаёт docs/CITATION_INDEX.md.

**Флаги:** `--domain`, `--min-citations`


### `improve_clusters.py` _(группа: analysis)_

**кластеризует файлы по тематической близости**

через TF-IDF вектора и косинусное сходство (без внешних ML-библиотек). Создаёт docs/CLUSTERS.md.


### `improve_compare.py` _(группа: reports)_

**сравнивает текущее состояние docs/ с предыдущим коммитом.**

Показывает: новые файлы, удалённые, изменившиеся, рост/падение слов. Создаёт docs/COMPARE.md.


### `improve_compare_docs.py` _(группа: textwork)_

**сравнивает два документа: общее, различия, пересечения.**

Анализирует: - Общие темы (по ключевым словам TF) - Уникальные разделы (заголовки есть в одном, нет в другом) - Словарное пересечение (Jaccard) - Структурное сходство

**Флаги:** `--a`, `--b`, `--batch`, `--out`, `--section`, `--top`


### `improve_complexity.py` _(группа: analysis)_

**оценка читаемости документов.**

Метрики: длина предложений, плотность терминов, глубина вложенности заголовков. Создаёт docs/COMPLEXITY.md.


### `improve_component_matrix.py` _(группа: без группы)_

**матрица совместимости и возможностей компонентов.**

Показывает какие компоненты поддерживают какие функции (memory, search, MCP, ...). Создаёт docs/COMPONENT_MATRIX.md.


### `improve_concept_graph.py` _(группа: deeptext)_

**граф концептов из базы знаний.**

Строит граф: узлы = ключевые концепты, рёбра = совместное упоминание в одном файле. Экспортирует в: - Mermaid (встраивается в markdown) - DOT (для Graphviz) - JSON (для d3.js или других инструментов)

**Флаги:** `--format`, `--min-weight`, `--section`, `--top-concepts`


### `improve_concepts.py` _(группа: extract)_

**извлекает определения понятий прямо из текстов.**

Ищет паттерны: "X — это ...", "X представляет собой ...", "X: ...", "X (англ. ...)" Создаёт docs/CONCEPTS.md.


### `improve_confluence.py` _(группа: export)_

**конвертирует docs/*.md в формат Confluence Wiki Markup.**

Создаёт docs/confluence/ с файлами .wiki. Основные преобразования: # H1 → h1. **bold** → *bold* `code` → {{code}}

**Флаги:** `--dry-run`, `--section`


### `improve_consistency.py` _(группа: quality)_

**находит разные написания одного термина,**

предлагает канонический вариант, создаёт docs/CONSISTENCY.md.


### `improve_contact_priority.py` _(группа: reports)_

**ранжирует авторов по приоритету для контакта.**

Формула: score = упоминания × 3 + (4 - статус_шаг) × 5 + слой_буст слой_буст: memory=3, knowledge=2, orchestration=2, graph=1, остальные=1 Создаёт docs/CONTACT_PRIORITY.md с топом авторов и рекомендуемым порядком.


### `improve_contact_status.py` _(группа: без группы)_

**обновляет статус контакта в docs/contacts/<slug>.md.**

Удобная альтернатива ручному редактированию файла. Использование: Поддерживает частичное имя: --author kk ищет kksudo если он единственный совпадающий.

**Флаги:** `--agreed`, `--author`, `--list`, `--messaged`, `--note`, `--replied`, `--studied`


### `improve_contacts.py` _(группа: reports)_

**извлекает email, Telegram, GitHub, Habr-ники**

из всех docs/ и создаёт docs/CONTACTS.md.


### `improve_content_gaps.py` _(группа: quality)_

**находит темы, упомянутые в docs/, но без собственного документа.**

Логика: 1. Собирает «упоминания» — слова/словосочетания, встречающиеся >= MIN_MENTIONS раз в разных файлах, похожие на названия проектов/концепций. 2. Проверяет, есть ли документ, посвящённый этой теме. 3. Выдаёт список пробелов с частотой и рекомендуемым местом создания файла.

**Флаги:** `--min-mentions`, `--section`


### `improve_contradiction_check.py` _(группа: deeptext)_

**поиск противоречивых утверждений в базе знаний.**

Ищет предложения, содержащие одни и те же сущности, но противоположные утверждения: - Числа: «X имеет 5 компонентов» vs «X имеет 8 компонентов» - Булевы: «X поддерживает Y» vs «X не поддерживает Y» - Версии: «версия 1.0» vs «версия 2.0» (об одном и том же) - Факты с «является/это» vs «не является/не это»

**Флаги:** `--min-confidence`, `--section`


### `improve_cost.py` _(группа: reports)_

**оценка стоимости разработки MVP.**

Извлекает временные оценки из документов, конвертирует в человеко-часы, рассчитывает ориентировочный бюджет. Создаёт docs/COST.md.


### `improve_coverage.py` _(группа: reports)_

**матрица покрытия: какие файлы имеют summary, теги, TOC, crossrefs, статус.**

Для каждого файла в целевых секциях показывает какие признаки присутствуют. Создаёт docs/COVERAGE.md.

**Флаги:** `--section`


### `improve_cross_section.py` _(группа: analytics)_

**граф концептов между секциями.**

Показывает какие ключевые понятия встречаются сразу в нескольких секциях и насколько сильна их связь: 1. TF-IDF веса ключевых слов по каждой секции 2. Matrise пересечений (косинусное сходство секций) 3. Mermaid-граф секций с весами рёбер

**Флаги:** `--format`, `--min-secs`, `--top`


### `improve_crosslink_all.py` _(группа: textwork)_

**прописывает обратные ссылки (backlinks) во все файлы.**

Алгоритм: 1. Сканирует все .md файлы и строит граф: кто на кого ссылается 2. Для каждого файла добавляет раздел "## Упоминается в" (обратные ссылки) 3. Идемпотентно: обновляет существующий блок по маркеру Дополнительно:

**Флаги:** `--apply`, `--dry-run`, `--keywords`, `--min-refs`


### `improve_crossrefs.py` _(группа: index)_

**строит карту перекрёстных ссылок между файлами.**

Создаёт docs/CROSSREFS.md: какой файл упоминает какие проекты, и для каждого проекта — список файлов где он встречается.


### `improve_decisions.py` _(группа: extract)_

**извлекает ключевые выводы и решения из всех файлов.**

Ищет паттерны: "главный вывод", "лучший выбор", "рекомендуется" и т.д. Создаёт docs/DECISIONS.md.


### `improve_dedup.py` _(группа: analysis)_

**находит дублирующиеся файлы и похожие абзацы.**

Создаёт docs/DUPLICATES.md с отчётом. НЕ удаляет файлы автоматически — только сообщает о них. Новое: для каждой пары похожих файлов показывает сами совпавшие абзацы (до 3 штук).

**Флаги:** `--threshold`


### `improve_density.py` _(группа: analysis)_

**карта плотности тем по всем документам.**

Считает упоминания ключевых тем в каждом разделе. Показывает: какие темы раскрыты подробно, какие слабо. Создаёт docs/DENSITY.md.


### `improve_dependabot.py` _(группа: cicd)_

**мониторинг версий OSS-компонентов Svyazi 2.0.**

Извлекает упоминания проектов + версий из docs/, сверяет с PyPI/GitHub и сообщает об устаревших зависимостях. Дополнительно: генерирует .github/dependabot.yml для автоматических PR. Создаёт docs/DEPENDABOT.md.

**Флаги:** `--check-pypi`, `--generate-config`


### `improve_dependency_map.py` _(группа: без группы)_

**карта зависимостей: скрипты → выходные файлы.**

Показывает что каждый improve_*.py производит и от чего зависит. Создаёт docs/DEPENDENCY_MAP.md.


### `improve_digest.py` _(группа: reports)_

**дайджест недавних изменений репозитория.**

Собирает из git log: новые файлы, изменённые, ключевые коммиты. Создаёт docs/DIGEST.md.


### `improve_digest_auto.py` _(группа: analytics)_

**автодайджест изменений за N дней.**

Анализирует git-лог и содержимое изменённых файлов: 1. Какие файлы добавлены / изменены / удалены за период 2. Ключевые слова из изменений (TF-IDF на diff) 3. Статистика: сколько слов добавлено/удалено 4. Самые активные секции

**Флаги:** `--days`, `--format`, `--since`


### `improve_digest_weekly.py` _(группа: без группы)_

**еженедельный дайджест изменений репозитория.**

Показывает: новые файлы, изменённые, топ-активные папки, прирост слов. Создаёт docs/DIGEST_WEEKLY.md.


### `improve_duplicate_across.py` _(группа: textwork)_

**поиск похожих текстов между репозиториями/папками.**

Сравнивает docs/ с: a) Другой локальной папкой (--other-dir /path/to/repo2/docs) b) Другим git-репозиторием (--other-repo /path/to/other-repo) c) Поддиректориями внутри docs/ (--internal — сравнивает секции между собой) Алгоритм сравнения:

**Флаги:** `--internal`, `--other-dir`, `--other-repo`, `--section`, `--threshold`


### `improve_empty_sections.py` _(группа: nlpplus)_

**поиск и заполнение пустых секций.**

Находит заголовки с минимальным содержимым (заглушки): - H2/H3 с менее чем MIN_CONTENT слов под ними - Секции только с одним вложенным заголовком и никакого текста - Файлы с >50% пустых секций Режимы:

**Флаги:** `--fill`, `--min-content`, `--report`, `--section`, `--suggest`


### `improve_entities.py` _(группа: extract)_

**извлечение именованных сущностей из docs/.**

Категории: люди, проекты, организации, технологии, URL/репозитории. Создаёт docs/ENTITIES.md.


### `improve_epub.py` _(группа: без группы)_

**собирает docs/ в EPUB через pandoc.**

Объединяет все .md файлы секции в один EPUB с оглавлением. Требует: pandoc (apt install pandoc / brew install pandoc)

**Флаги:** `--check`, `--output`, `--section`, `--title`


### `improve_export_csv.py` _(группа: export)_

**экспортирует метаданные всех docs/ в CSV.**

Создаёт docs/export.csv — удобно для анализа в Excel / Google Sheets.


### `improve_export_html.py` _(группа: export)_

**экспортирует все docs/ в единый HTML-сайт.**

Создаёт docs/index.html с навигацией и содержимым всех файлов.


### `improve_export_json.py` _(группа: export)_

**экспортирует всю структуру docs/ в structured JSON.**

Каждый файл: путь, заголовок, слова, теги, summary, первые 500 символов. Создаёт docs/export_full.json (для API/программного доступа).


### `improve_export_report.py` _(группа: export)_

**единый сводный отчёт по всей базе знаний.**

Собирает ключевые данные из всех отчётных файлов и создаёт один документ, пригодный для: - презентации инвесторам / авторам проектов - отправки в виде PDF/EPUB через pandoc - быстрого ввода нового участника в контекст

**Флаги:** `--no-projects`, `--sections`, `--title`


### `improve_external_compare.py` _(группа: без группы)_

**сравнивает документы базы с внешними источниками.**

Для заданной темы или файла: 1. Скачивает внешний URL (HTML → plain text) 2. Сравнивает с вашим документом (ключевые слова, уникальное, общее) 3. Показывает что есть у них, чего нет у вас — и наоборот Также поддерживает --auto: сканирует docs/ на URL-ссылки и сравнивает

**Флаги:** `--auto`, `--file`, `--limit`, `--query`, `--section`, `--url`


### `improve_extract_code.py` _(группа: extract)_

**извлекает все code-блоки из docs/.**

Разделяет по языкам: mermaid, python, yaml, bash, json, другие. Создаёт docs/CODE_BLOCKS.md.


### `improve_extract_tables.py` _(группа: extract)_

**извлекает все Markdown-таблицы из docs/**

в один файл docs/TABLES.md для быстрого просмотра.


### `improve_faceted_search.py` _(группа: nlpplus)_

**фасетный поиск по базе знаний.**

Поиск с фильтрами (фасетами) поверх keyword_index.json + named_entities.json: Сохраняет последний результат в docs/SEARCH_RESULTS.md.

**Флаги:** `--after`, `--entity`, `--format`, `--min-words`, `--query`, `--section`, `--top`, `--type`


### `improve_faq.py` _(группа: generate)_

**строит FAQ из QA-паттернов в документах.**

Ищет: "Вопрос/Ответ", "Q:", "A:", "—" после вопроса, секции ## FAQ. Создаёт docs/FAQ.md.


### `improve_footnotes.py` _(группа: generate)_

**автоматически связывает технические термины с глоссарием.**

Добавляет сноски [^term] к первому вхождению каждого термина в файле. Создаёт docs/FOOTNOTES.md (отчёт), не ломает оригинальные файлы.


### `improve_gap_filler.py` _(группа: content)_

**заполняет пустые секции найденным контентом (BM25).**

Для каждой пустой секции (< MIN_CONTENT слов): 1. Использует заголовок как поисковый запрос (BM25) 2. Находит релевантные абзацы из других файлов 3. Вставляет их как цитату-подсказку или сноску Режимы:

**Флаги:** `--apply`, `--dry-run`, `--mode`, `--section`, `--top`


### `improve_github_issues.py` _(группа: cicd)_

**создаёт GitHub Issues из ACTION_ITEMS.md и TODO-блоков.**

Без GitHub API: генерирует docs/GITHUB_ISSUES.md с готовым списком задач в формате, пригодном для ручного или API-создания. Опционально: если установлен gh CLI и задан --create, создаёт Issues через gh. Создаёт docs/GITHUB_ISSUES.md.

**Флаги:** `--create`, `--dry-run`, `--label`


### `improve_glossary.py` _(группа: index)_

**извлекает все проекты, авторов и URL из docs/,**

создаёт docs/GLOSSARY.md и docs/AUTHORS.md.


### `improve_graph.py` _(группа: graph)_

**строит граф связей между проектами.**

Создаёт docs/GRAPH.md с диаграммой Mermaid и матрицей совместных упоминаний.


### `improve_heading_audit.py` _(группа: nlpplus)_

**аудит иерархии заголовков.**

Проверяет: - H3/H4 без родительского H2 (нарушение иерархии) - Пустые секции: заголовок + <MIN_CONTENT слов под ним - Одиночные заголовки: H2 с одним единственным дочерним абзацем - Дублирующиеся заголовки в одном файле

**Флаги:** `--section`, `--verbose`


### `improve_health.py` _(группа: reports)_

**дашборд здоровья репозитория.**

Агрегирует метрики из всех improve_*.md файлов в один отчёт. Создаёт docs/HEALTH.md.


### `improve_heatmap.py` _(группа: analysis)_

**тепловая карта тем по разделам и файлам.**

ASCII-визуализация: строки = темы, столбцы = разделы. Создаёт docs/HEATMAP.md.


### `improve_index_master.py` _(группа: без группы)_

**главный навигационный хаб docs/.**

Собирает все ключевые документы, статистику, ссылки в один docs/INDEX.md. Служит точкой входа для навигации по всей документации.


### `improve_index_update.py` _(группа: index)_

**инкрементальное обновление search_index.json.**

Обновляет только файлы, изменившиеся с момента последней индексации (по mtime или git diff).


### `improve_keyword_index.py` _(группа: deeptext)_

**инвертированный индекс: слово → файлы.**

Строит инвертированный индекс без поискового движка: - word → [{file, count, positions, section}] - Быстрый offline-поиск без search_index.json - Поддержка биграмм (двусловных фраз) - Статистика: уникальных слов, охват файлов

**Флаги:** `--min-df`, `--query`, `--section`, `--top`


### `improve_knowledge_map.py` _(группа: nlpplus)_

**единый дашборд всей базы знаний.**

Агрегирует данные из всех отчётных файлов и строит единую карту: - Общая статистика корпуса - Топ файлов по важности (из PRIORITIES.md / SCORING.md) - Состояние по секциям (файлов, слов, качество) - Граф ключевых связей (из CONCEPT_GRAPH.md)


### `improve_kpi.py` _(группа: extract)_

**извлекает числовые KPI и метрики из docs/.**

Ищет: числа с единицами, проценты, временные оценки, бюджеты, размеры команд. Создаёт docs/KPI.md.


### `improve_kpi_snapshot.py` _(группа: без группы)_

**исторические снапшоты ключевых метрик.**

Читает текущие метрики из docs/, добавляет запись с датой в историю, строит таблицу трендов. Создаёт docs/KPI_HISTORY.md.


### `improve_language_split.py` _(группа: nlpplus)_

**анализ языкового состава документов.**

Для каждого файла определяет: - Долю русского текста (кириллица) - Долю английского текста (латиница) - Классификацию: RU / EN / MIX / CODE - Файлы с неожиданным языком (EN в RU-секции и наоборот)

**Флаги:** `--min-mix`, `--report`, `--section`, `--split`


### `improve_link_preview.py` _(группа: без группы)_

**проверяет внешние ссылки в docs/ и кэширует их статус.**

Для каждой уникальной URL: - HEAD-запрос (timeout 8с) → HTTP-статус - Если 200: извлекает <title> из HTML - Кэш в docs/link_cache.json (повторные проверки пропускаются если < CACHE_DAYS) Создаёт docs/LINK_PREVIEW.md.

**Флаги:** `--refresh`, `--section`, `--timeout`


### `improve_llm_contact.py` _(группа: без группы)_

**генерирует персонализированное первое сообщение автору через LLM.**

Читает: - docs/contacts/<author>.md — профиль и черновик сообщения - docs/05-habr-projects/**/<project>.md — детали проекта - docs/CONTACTS.md — слой архитектуры Создаёт обогащённый вариант первого сообщения с конкретными техническими деталями.

**Флаги:** `--all`, `--author`, `--dry-run`


### `improve_llm_enrich.py` _(группа: без группы)_

**семантическое обогащение проектных файлов через Claude API.**

Stage 3a: скрипт управляет процессом, LLM заполняет то, что regex не может. Что делает: Для каждого файла в docs/05-habr-projects/ и docs/04-ai-collaborations/: 1. Детерминированно извлекает факты (теги, упоминания, чанки) 2. Вызывает Claude для генерации структурированного описания

**Флаги:** `--dry-run`, `--file`, `--force`, `--model`, `--section`


### `improve_llm_gaps.py` _(группа: без группы)_

**семантический поиск пробелов через Claude API.**

Анализирует структуру документации и находит темы, которые упомянуты но не раскрыты, противоречия, устаревшие утверждения. Создаёт docs/LLM_GAPS.md.


### `improve_llm_qa.py` _(группа: без группы)_

**ответы на вопросы по всей базе знаний Lorenzo через Claude API.**

Stage 3c: RAG без векторной БД — поиск по search_index.json + LLM-синтез. Режимы: 1. Интерактивный: задаёшь вопросы в терминале, получаешь ответы с источниками 2. Batch: читает вопросы из файла, пишет ответы в docs/QA_ANSWERS.md 3. Single: ответ на один вопрос через --question "..."

**Флаги:** `--batch`, `--clear-cache`, `--dry-run`, `--no-cache`, `--question`, `--save`


### `improve_llm_summary.py` _(группа: без группы)_

**каскадная суммаризация больших документов через Claude API.**

Stage 3b: map-reduce для документов любого размера. Алгоритм: 1. chunk_by_headers() — разбивка на секции 2. LLM: summarize(chunk) → мини-резюме (map) 3. LLM: synthesize(мини-резюме) → финальное резюме (reduce)

**Флаги:** `--dry-run`, `--file`, `--section`


### `improve_mcp_dashboard.py` _(группа: без группы)_

**статистика вызовов MCP-серверов.**

Читает .claude/mcp_calls.jsonl и формирует docs/MCP_DASHBOARD.md: - сколько вызовов на каждый сервер - топ-инструменты по частоте - средняя длительность - ошибки


### `improve_mcp_test.py` _(группа: без группы)_

**smoke-тесты для всех MCP-серверов.**

Проверяет: 1. Что каждый сервер импортируется без ошибок 2. Что dispatch() возвращает строку для известных инструментов 3. Что dispatch() обрабатывает unknown tool gracefully Не запускает stdio_server (требует MCP-клиента).


### `improve_merge_by_topic.py` _(группа: textwork)_

**склеивает файлы-фрагменты одной темы в единый документ.**

Обнаруживает «цепочки» файлов принадлежащих одной теме по: - сходству заголовков (Jaccard по словам) - нумерации в имени файла (01-x, 02-x...) - общим TF-IDF ключевым словам Режимы:

**Флаги:** `--apply`, `--dry-run`, `--min-group`, `--section`, `--threshold`


### `improve_merge_short.py` _(группа: structure)_

**сливает слишком короткие файлы с предыдущим соседом.**


### `improve_metrics.py` _(группа: quality)_

**метрики качества документации.**

Считает: индекс покрытия, плотность ссылок, насыщенность примерами, баланс разделов, индекс связности. Создаёт docs/METRICS.md.


### `improve_mindmap.py` _(группа: graph)_

**строит майндмап всего репозитория в формате Mermaid mindmap.**

Создаёт docs/MINDMAP.md.


### `improve_missing.py` _(группа: quality)_

**находит темы/проекты упомянутые в документах**

но слабо раскрытые (мало файлов, мало слов). Создаёт docs/MISSING.md — карту пробелов знаний.


### `improve_named_entity_index.py` _(группа: deeptext)_

**индекс именованных сущностей из всей базы.**

Извлекает без ML (по паттернам и словарям): - Люди: CamelCase имена, известные авторы из CONTACTS.md - Проекты/Продукты: слова из ENTITIES.md + CamelCase + GitHub-ссылки - Технологии: из словаря tech-терминов - Организации: Inc, Ltd, GmbH, LLC + известные

**Флаги:** `--min-mentions`, `--section`, `--type`


### `improve_narrative.py` _(группа: graph)_

**строит нарративную линию проекта.**

Извлекает: ключевые решения, этапы, цитаты-выводы и строит связный рассказ. Создаёт docs/NARRATIVE.md.


### `improve_network.py` _(группа: graph)_

**анализ сети авторов и проектов.**

Строит: матрицу ко-упоминаний, центральность, кластеры авторов. Создаёт docs/NETWORK.md + docs/network.dot (Graphviz).


### `improve_obsidian.py` _(группа: export)_

**готовит docs/ для импорта в Obsidian.**

Преобразования: 1. Добавляет YAML frontmatter (title, tags, date) если нет 2. Заменяет [Text](../path/file.md) → [[file]] (wikilinks) 3. Создаёт docs/obsidian/ с готовыми файлами (не перезаписывает оригиналы)

**Флаги:** `--dry-run`, `--in-place`, `--section`


### `improve_onboarding.py` _(группа: без группы)_

**руководство для новых участников проекта.**

Собирает: структуру repo, первые шаги, ключевые файлы, скрипты, контакты. Создаёт docs/ONBOARDING.md.


### `improve_orphans.py` _(группа: quality)_

**находит документы без входящих ссылок (orphan docs).**

Такие файлы изолированы от навигации и могут быть потеряны. Создаёт docs/ORPHANS.md.


### `improve_outline.py` _(группа: textwork)_

**строит иерархический outline всей базы знаний.**

Генерирует два вида оглавления: 1. По структуре папок + заголовкам H1/H2 каждого файла 2. По темам (TF-IDF кластеры) — тематическая карта Создаёт docs/OUTLINE.md.

**Флаги:** `--depth`, `--format`, `--section`


### `improve_paragraph_quality.py` _(группа: deeptext)_

**находит проблемные абзацы в документах.**

Проверяет: - Слишком короткие абзацы (< MIN_SENTENCES предложений) - Копипаста: абзац почти идентичен другому в том же файле (Jaccard > 0.8) - «Водяные» абзацы: много союзов/местоимений, мало ключевых слов - «Оборванные»: заканчиваются без знака препинания

**Флаги:** `--section`, `--verbose`


### `improve_passage_retrieval.py` _(группа: deeptext)_

**BM25-поиск на уровне абзацев.**

В отличие от полнотекстового поиска по файлам, ищет релевантный АБЗАЦ внутри документа — точнее и удобнее для RAG. Алгоритм: BM25 (Okapi BM25, k1=1.5, b=0.75). Режимы:

**Флаги:** `--context`, `--index`, `--min-words`, `--query`, `--section`, `--top`


### `improve_passive_voice.py` _(группа: nlpplus)_

**детектор пассивного залога и номинализаций (RU/EN).**

Находит: - Пассивный залог RU: «был создан», «является», «используется», «осуществляется» - Пассивный залог EN: «was created», «is used», «has been» - Номинализации RU: слова на -ание/-ение/-ция/-изация/-ость (вместо глаголов) - Клише: «в рамках», «с целью», «в ходе», «посредством», «в связи с»

**Флаги:** `--section`, `--top`, `--verbose`


### `improve_pre_commit.py` _(группа: cicd)_

**генерирует .pre-commit-config.yaml для проекта.**

Хуки включают: - trailing whitespace, end-of-file fixes - проверка YAML/JSON синтаксиса - проверка орфографии (improve_spellcheck.py) - проверка сломанных ссылок (improve_broken_links.py)

**Флаги:** `--dry-run`, `--install`


### `improve_priorities.py` _(группа: analysis)_

**ранжирует файлы по важности через TF-IDF.**

Ключевые термины = названия проектов + архитектурные понятия. Создаёт docs/PRIORITIES.md.


### `improve_progress.py` _(группа: reports)_

**трекер прогресса MVP-проекта.**

Извлекает чеклисты [ ] и [x] из docs/, группирует по теме, считает % выполнения. Создаёт docs/PROGRESS.md.


### `improve_progress_sync.py` _(группа: reports)_

**синхронизирует PROGRESS.md с реальным состоянием файлов.**

Stage 2: оркестратор, читает файловую систему, обновляет прогресс детерминированно. Что проверяет: Контакты:  сколько файлов в docs/contacts/, сколько с [x] отметками Обогащение: сколько файлов в docs/enriched/ Архитектура: наличие ключевых документов

**Флаги:** `--dry-run`


### `improve_qa.py` _(группа: reports)_

**генерирует Q&A листы для каждого раздела docs/.**

Вопросы строятся детерминированно из заголовков и ключевых слов. Создаёт docs/QA.md и QA-файл в каждой подпапке.


### `improve_question_extractor.py` _(группа: nlpplus)_

**извлечение вопросов, гипотез и TODO.**

Ищет в текстах: - Вопросы: предложения с «?» или «как», «почему», «зачем», «что если» - Гипотезы: «возможно», «предположим», «скорее всего», «вероятно» - TODO/Ideas: «нужно», «стоит», «следует», «можно было бы», «планируется» - Открытые вопросы: «неясно», «непонятно», «требует изучения»

**Флаги:** `--min-words`, `--section`, `--type`


### `improve_questions.py` _(группа: extract)_

**извлекает открытые вопросы из docs/.**

Ищет вопросительные предложения и паттерны "открытый вопрос". Создаёт docs/QUESTIONS.md.


### `improve_readability_v2.py` _(группа: quality)_

**индекс читаемости текстов.**

Адаптированная метрика Флеша–Кинкейда для русского языка. Формула: 206.835 - 1.015*(слов/предл.) - 84.6*(слогов/слово) Дополнительно: средняя длина предложения, средняя длина слова. Создаёт docs/READABILITY.md.

**Флаги:** `--section`


### `improve_reading_list.py` _(группа: nlpplus)_

**персонализированный список чтения по теме.**

Генерирует упорядоченный список документов для изучения темы: 1. BM25-поиск по запросу → релевантные файлы 2. Ранжирование: score × (1 + важность файла) × (1 + связность) 3. Оценивает время чтения (200 сл/мин RU, 250 EN) 4. Группирует по секциям для логического порядка

**Флаги:** `--format`, `--query`, `--section`, `--top`


### `improve_reading_order.py` _(группа: reports)_

**строит рекомендуемый порядок чтения документов**

от базовых концепций к сложным. Создаёт docs/READING_ORDER.md.


### `improve_reading_time.py` _(группа: analytics)_

**оценивает время чтения каждого документа.**

Формула: - Средняя скорость чтения: 200 слов/мин (русский) / 250 слов/мин (английский) - Время на код: 50 слов/мин (или 30 сек/блок) - Минимум: 1 мин Создаёт docs/READING_TIME.md.

**Флаги:** `--section`, `--wpm`


### `improve_readmes.py` _(группа: structure)_

**создаёт README.md для каждой подпапки docs/.**

README содержит: список файлов, первые строки каждого файла как описание.


### `improve_reclassify.py` _(группа: textwork)_

**раскладывает файлы по подпапкам на основе TF-IDF тематики.**

Алгоритм: 1. TF-IDF по всем файлам секции 2. k-means кластеризация (без numpy: по ключевым словам) 3. Именование кластеров по топ-словам 4. Предложение подпапок + перемещение файлов (с --apply)

**Флаги:** `--apply`, `--dry-run`, `--section`, `--topics`


### `improve_report.py` _(группа: reports)_

**итоговый executive report о состоянии репозитория.**

Агрегирует данные из HEALTH, STATS, KPI, DECISIONS, VALIDATION, NETWORK. Создаёт docs/REPORT.md — главный отчёт для быстрого обзора.


### `improve_risk_register.py` _(группа: без группы)_

**реестр рисков проекта Svyazi 2.0.**

Извлекает риски из документов (слова: риск, проблема, блокер, угроза), дополняет курированным списком, строит матрицу вероятность × влияние. Создаёт docs/RISK_REGISTER.md.


### `improve_rss.py` _(группа: export)_

**генерирует RSS/Atom фид из истории git-коммитов.**

Каждый коммит, затрагивающий docs/, становится элементом фида. Фид описывает изменения в Knowledge Base Lorenzo/Svyazi 2.0. Создаёт: docs/feed.rss  — RSS 2.0 docs/feed.atom — Atom 1.0

**Флаги:** `--base-url`, `--max-items`


### `improve_run_all.py` _(группа: без группы)_

**мастер-скрипт для запуска всех improve_*.py.**

**Флаги:** `--changed`, `--dry-run`, `--fast`, `--group`, `--only`, `--parallel`, `--report`, `--smart`, `--stat`


### `improve_schedule.py` _(группа: reports)_

**строит расписание проекта из ACTION_ITEMS и временных маркеров.**

Группирует задачи по кварталам/месяцам, строит Gantt-подобную таблицу. Создаёт docs/SCHEDULE.md.


### `improve_scoring.py` _(группа: reports)_

**система оценки готовности проекта к запуску (Go/No-Go).**

Проверяет 20+ критериев по 5 категориям: документация, архитектура, команда, риски, MVP-готовность. Создаёт docs/SCORING.md.


### `improve_search_index.py` _(группа: index)_

**строит полнотекстовый JSON-индекс всех docs/.**

Создаёт docs/search_index.json для быстрого поиска по проекту.


### `improve_see_also.py` _(группа: generate)_

**добавляет блок "See Also / Смотрите также"**

в ключевые документы на основе тематического сходства. Создаёт docs/SEE_ALSO.md (индекс) и вставляет блоки в файлы.


### `improve_sentiment.py` _(группа: analysis)_

**тональный анализ документов.**

Оценивает: оптимизм, скептицизм, срочность, неопределённость. Создаёт docs/SENTIMENT.md.


### `improve_similar.py` _(группа: analysis)_

**для каждого документа находит топ-3 похожих.**

Использует Jaccard по множеству слов (без ML-зависимостей). Добавляет блок "Похожие документы" в конец каждого файла и создаёт сводный docs/SIMILAR.md.


### `improve_similar_passages.py` _(группа: nlpplus)_

**поиск похожих абзацев между файлами (TF-IDF cosine).**

Полезно для: - Нахождения дублирующегося контента в разных секциях - Кандидатов для слияния документов - Обнаружения «скопированных» блоков Алгоритм:

**Флаги:** `--min-sim`, `--min-words`, `--section`, `--top`


### `improve_sitemap.py` _(группа: reports)_

**генерирует навигационную карту репозитория.**

Создаёт: docs/SITEMAP.md (текстовый) + docs/sitemap.xml (XML для поиска).


### `improve_source_map.py` _(группа: textwork)_

**строит карту происхождения текстов.**

Для каждого файла определяет: - Дата первого появления (git log) - Автор коммита (git log --format=%an) - Источники в frontmatter (поле source:, url:, origin:) - Внешние URL, указанные в тексте

**Флаги:** `--authors`, `--format`, `--section`, `--show-imported`


### `improve_spellcheck.py` _(группа: quality)_

**проверка орфографии в docs/.**

Без внешних зависимостей: использует встроенный словарь частых опечаток и опциональный pyspellchecker если установлен. Создаёт docs/SPELLCHECK.md — список подозрительных слов по файлам.

**Флаги:** `--fix`, `--section`


### `improve_staleness.py` _(группа: reports)_

**находит документы которые давно не обновлялись или неполные.**

Проверяет: - Файлы без изменений в git > N дней (по умолчанию 30) - Файлы без summary-комментария - Файлы без тегов - Файлы короче 100 слов (заготовки)

**Флаги:** `--days`, `--no-git`


### `improve_stats.py` _(группа: reports)_

**детальная статистика по каждому разделу docs/.**

Считает: файлы, слова, заголовки H1-H4, таблицы, code-блоки, ссылки, изображения. Создаёт docs/STATS.md.


### `improve_subtopic_fill.py` _(группа: textwork)_

**дополняет файлы-заглушки контентом из базы знаний.**

Для каждого файла с малым количеством слов (<MIN_WORDS): 1. Определяет тему по заголовку и имеющимся словам 2. Находит релевантные фрагменты из других файлов базы (по ключевым словам) 3. Вставляет раздел "## Связанные материалы" с найденными цитатами 4. Добавляет перекрёстные ссылки

**Флаги:** `--apply`, `--dry-run`, `--min-words`, `--section`


### `improve_summaries.py` _(группа: structure)_

**добавляет краткую аннотацию в начало каждого файла.**

Аннотация = первые 3 значимые строки + список найденных проектов в файле. НЕ использует LLM — работает детерминированно.


### `improve_tags.py` _(группа: structure)_

**тегирует каждый файл по темам, создаёт docs/TAGS.md**

и добавляет строку тегов в начало каждого файла.


### `improve_task_codegen.py` _(группа: без группы)_

**генератор слоёв (скилл / MCP-tool / index) из манифестов tasks/*.task.yaml.**

Манифест — единый источник истины. По нему собираются: 1. .claude/skills/<id>.md (если ещё нет — создаётся скелет; если есть — обновляется метаданными) 2. docs/TASKS_INDEX.md — общий индекс задач 3. tasks/_generated/<id>.json — машиночитаемая копия для MCP-инструментов 4. (опционально) tasks/_validation.md — отчёт о невалидных манифестах

**Флаги:** `--dry-run`, `--list`, `--task`, `--validate`


### `improve_tech_radar.py` _(группа: без группы)_

**tech radar для технологий проекта Svyazi 2.0.**

Классифицирует компоненты по 4 квадрантам: ADOPT / TRIAL / ASSESS / HOLD. Создаёт docs/TECH_RADAR.md.


### `improve_template_init.py` _(группа: без группы)_

**инициализация нового документа из шаблона.**

Создаёт файл по слаг-пути, подставляет переменные frontmatter и плейсхолдеры в теле, делает базовую валидацию через improve_validate_templates. Использование:

**Флаги:** `--list`, `--show`, `--slug`, `--type`, `--vars`


### `improve_template_migrate.py` _(группа: без группы)_

**миграции frontmatter при изменении схемы шаблона.**

Сравнивает frontmatter существующих документов со схемой и предлагает миграции: - добавить отсутствующие обязательные поля (с дефолтами) - удалить несуществующие в схеме поля - привести значения к допустимым enum Использование:

**Флаги:** `--all`, `--apply`, `--dry-run`, `--template`


### `improve_templates.py` _(группа: generate)_

**генерирует шаблоны документов для каждого раздела.**

Создаёт папку docs/templates/ с готовыми заготовками.


### `improve_text_segmenter.py` _(группа: deeptext)_

**разбивает большие файлы на логические части.**

Для файлов > MAX_WORDS слов: 1. Определяет смысловые границы (заголовки H2/H3, пустые строки, тематические сдвиги) 2. Разбивает на части с сохранением контекста (breadcrumb) 3. Создаёт индекс-файл и отдельные части в подпапке Режимы:

**Флаги:** `--apply`, `--dry-run`, `--max-words`, `--part-size`, `--section`


### `improve_textrank.py` _(группа: nlpplus)_

**извлекательное резюме через TextRank (без LLM).**

Алгоритм TextRank: 1. Разбивает текст на предложения 2. Строит граф сходства (Jaccard на токенах) 3. Запускает PageRank на графе 4. Топ-N предложений = резюме

**Флаги:** `--apply`, `--query`, `--section`, `--sentences`


### `improve_timeline.py` _(группа: index)_

**извлекает даты и временные маркеры из всех docs/,**

создаёт docs/TIMELINE.md с хронологией событий.


### `improve_timeline_events.py` _(группа: deeptext)_

**извлекает даты и события из базы знаний.**

Строит хронологическую ленту: - Конкретные даты: 2024-03-15, март 2024, Q2 2024 - Относительные: «через 3 месяца», «в следующем квартале» - Контекст события (предложение с датой) - Источник (файл + заголовок секции)

**Флаги:** `--format`, `--from`, `--section`, `--to`


### `improve_toc.py` _(группа: structure)_

**добавляет Table of Contents в начало файлов длиннее 500 слов.**

Генерирует TOC из H2/H3 заголовков с якорными ссылками.


### `improve_topic_model.py` _(группа: analytics)_

**тематическое моделирование без ML-зависимостей.**

Реализует упрощённый TF-IDF + кластеризацию по ключевым словам. Без sklearn/gensim: только стандартная библиотека Python. Алгоритм: 1. TF-IDF для всех слов во всех файлах 2. Топ-N ключевых слов по TF-IDF для каждого файла

**Флаги:** `--section`, `--top-words`, `--topics`


### `improve_validate.py` _(группа: quality)_

**валидация структуры репозитория.**

Проверяет: наличие README в разделах, правильность именования, непустые файлы, корректность ссылок, обязательные мета-поля. Создаёт docs/VALIDATION.md.


### `improve_validate_templates.py` _(группа: без группы)_

**валидация документов по схемам шаблонов.**

Сканирует docs/, читает YAML-frontmatter каждого .md файла, ищет соответствующую схему в docs/templates/_schemas/<template>.json и проверяет: 1. Frontmatter присутствует и валиден по полям/типам схемы. 2. Required-поля присутствуют. 3. Enum-значения соответствуют допустимым.

**Флаги:** `--file`, `--report`, `--section`, `--strict`


### `improve_version_diff.py` _(группа: analytics)_

**показывает содержательные изменения docs/ между коммитами.**

В отличие от git diff показывает: - какие темы добавлены/удалены (по заголовкам ##) - сколько слов добавлено/удалено - какие файлы сильнее всего изменились Создаёт docs/VERSION_DIFF.md.

**Флаги:** `--from`, `--last`, `--to`


### `improve_vocabulary_richness.py` _(группа: deeptext)_

**метрики богатства словаря документов.**

Вычисляет: - TTR (Type-Token Ratio): уникальных слов / всего слов - STTR (Standardised TTR): средний TTR по окнам 100 слов - Unique per 1000: число уникальных слов на 1000 токенов - Hapax legomena: слова, встречающиеся ровно 1 раз

**Флаги:** `--section`, `--top`, `--window`


### `improve_watch.py` _(группа: без группы)_

**следит за изменениями в docs/ и перезапускает нужные скрипты.**

Использует polling (без внешних зависимостей).

**Флаги:** `--changed`, `--fast`, `--group`, `--interval`


### `improve_watcher.py` _(группа: без группы)_

**автономный агент-наблюдатель (Ступень 6).**

Следит за изменениями в docs/ и автоматически запускает нужные скрипты.

**Флаги:** `--once`


### `improve_word_cloud.py` _(группа: generate)_

**генерирует SVG word cloud из топ-слов репозитория.**

Без внешних зависимостей: чистый SVG с псевдо-случайным размещением. Создаёт docs/WORD_CLOUD.svg и docs/WORD_CLOUD.md.


### `improve_word_freq.py` _(группа: analysis)_

**частотный анализ слов по разделам.**

Топ-30 слов в каждом разделе и общий топ-50. Создаёт docs/WORD_FREQ.md.

