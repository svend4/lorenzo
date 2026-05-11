# Обработка больших массивов — Часть 8: Экспорт и интеграции

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Куда отправить обработанную базу знаний: форматы, платформы, пайплайны.
**Проекты:** Svyazi, Yodoca

---

<!-- toc -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Содержание

- [Зачем экспортировать?](#зачем-экспортировать)
- [Obsidian Vault — improve_obsidian.py](#obsidian-vault-improve_obsidianpy)
- [Confluence — improve_confluence.py](#confluence-improve_confluencepy)
- [EPUB — improve_epub.py](#epub-improve_epubpy)
- [RSS/Atom — improve_rss.py](#rssatom-improve_rsspy)
- [JSON/CSV — improve_export_json.py, improve_export_csv.py](#jsoncsv-improve_export_jsonpy-improve_export_csvpy)
- [JSONL для RAG — improve_chunk_semantic.py](#jsonl-для-rag-improve_chunk_semanticpy)
- [HTML — improve_export_html.py](#html-improve_export_htmlpy)
- [Карта сайта — improve_sitemap.py](#карта-сайта-improve_sitemappy)
- [MCP-сервер — mcp_server.py](#mcp-сервер-mcp_serverpy)
- [Сводная таблица экспортных форматов](#сводная-таблица-экспортных-форматов)
- [Следующий шаг](#следующий-шаг)

---

<!-- tags: memory, rag, orchestration, knowledge, ingestion, architecture, collaboration -->




> Куда отправить обработанную базу знаний: форматы, платформы, пайплайны.

---

## Зачем экспортировать?

Markdown-база — это хорошо, но разные инструменты требуют разных форматов:
- **Obsidian** — vault с wikilinks и YAML frontmatter
- **Confluence** — корпоративная wiki (`.wiki` разметка)
- **EPUB** — книга для чтения офлайн
- **RSS/Atom** — фид изменений для подписчиков
- **JSONL** — для RAG-пайплайна (LlamaIndex, LangChain)
- **CSV** — для таблиц, Excel, Google Sheets
- **HTML** — для публикации на сайте

---

## Obsidian Vault — improve_obsidian.py

**Что делает:**
- Добавляет YAML frontmatter (теги, дата, тип документа)
- Конвертирует `[text](path/file.md)` → `[[wikilinks]]`
- Копирует в `docs/obsidian/` с сохранением структуры

```bash
python scripts/improve_obsidian.py
# → docs/obsidian/ (1053 файла готовы к открытию в Obsidian)
```

**Результат:** Открыть `docs/obsidian/` как vault в Obsidian → граф связей, поиск, теги.

---

## Confluence — improve_confluence.py

**Что делает:** Конвертирует Markdown → Confluence Wiki Markup (`.wiki`).

```bash
python scripts/improve_confluence.py
# → docs/confluence/**/*.wiki
```

Поддерживает: таблицы, заголовки, блоки кода, ссылки, callout-блоки → `{note}`, `{tip}`.

---

## EPUB — improve_epub.py

**Что делает:** Через `pandoc` собирает всю секцию в книгу.

```bash
python scripts/improve_epub.py --check           # проверить наличие pandoc
python scripts/improve_epub.py --section 01-svyazi
python scripts/improve_epub.py --section 05-habr-projects
```

**Требования:** `apt install pandoc`

---

## RSS/Atom — improve_rss.py

**Что делает:** Читает `git log` → генерирует RSS/Atom фид изменений.

```bash
python scripts/improve_rss.py
# → docs/feed.rss
# → docs/feed.atom
```

**Применение:** Подписчики могут следить за изменениями базы знаний через RSS-ридер.

---

## JSON/CSV — improve_export_json.py, improve_export_csv.py

```bash
python scripts/improve_export_json.py
# → docs/export_full.json  (528 документов, метаданные + текст)

python scripts/improve_export_csv.py
# → docs/export_full.csv  (для Excel, Google Sheets, pandas)
```

**Формат JSON:**
```json
[
  {
    "file": "docs/05-habr-projects/memory/yodoca.md",
    "title": "Yodoca: консолидация и забывание",
    "tags": ["memory", "sqlite"],
    "words": 847,
    "section": "05-habr-projects",
    "content": "Yodoca — Научил ИИ-агента..."
  }
]
```

---

## JSONL для RAG — improve_chunk_semantic.py

**Для LlamaIndex / LangChain / любого RAG-пайплайна:**

```bash
python scripts/improve_chunk_semantic.py
# → docs/all_chunks.jsonl  (семантические чанки, каждый 200-500 слов)
```

**Подключение к LlamaIndex:**
```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser

# Или напрямую из our chunks
import json
chunks = [json.loads(l) for l in open('docs/all_chunks.jsonl')]
```

---

## HTML — improve_export_html.py

```bash
python scripts/improve_export_html.py
# → docs/export_full.html  (статический сайт, можно открыть в браузере)
```

---

## Карта сайта — improve_sitemap.py

```bash
python scripts/improve_sitemap.py
# → docs/SITEMAP.md    (навигационная карта для людей)
# → docs/sitemap.xml   (для поисковых роботов)
```

---

## MCP-сервер — mcp_server.py

**Самая мощная интеграция:** Подключить базу знаний как MCP-инструменты к Claude Desktop.

```bash
python scripts/mcp_server.py  # stdio режим
```

**7 инструментов Claude получает:**

| Инструмент | Что делает |
|-----------|-----------|
| `search_docs` | BM25-поиск по базе |
| `get_doc` | Прочитать конкретный файл |
| `get_decisions` | Архитектурные решения |
| `get_contacts` | Авторы и статус связи |
| `get_project_status` | Статус конкретного проекта |
| `run_improve` | Запустить любой скрипт |
| `update_contact_status` | Обновить статус контакта |

**Конфигурация в Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "lorenzo": {
      "command": "python",
      "args": ["/home/user/lorenzo/scripts/mcp_server.py"]
    }
  }
}
```

---

## Сводная таблица экспортных форматов

| Формат | Инструмент | Назначение |
|--------|-----------|-----------|
| Obsidian vault | `improve_obsidian.py` | Личная база знаний |
| Confluence wiki | `improve_confluence.py` | Корпоративная wiki |
| EPUB | `improve_epub.py` | Офлайн-чтение |
| RSS/Atom | `improve_rss.py` | Подписка на изменения |
| JSON | `improve_export_json.py` | API, анализ данных |
| CSV | `improve_export_csv.py` | Excel, Google Sheets |
| HTML | `improve_export_html.py` | Статический сайт |
| JSONL (чанки) | `improve_chunk_semantic.py` | RAG-пайплайн |
| XML sitemap | `improve_sitemap.py` | SEO, навигация |
| MCP-сервер | `mcp_server.py` | Claude Desktop |

---

## Следующий шаг

После экспорта → **Часть 9: Автоматизация (оркестратор, watcher, CI/CD)**

<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [01-overview](01-overview.md)
- [PROCESSING_GUIDE](PROCESSING_GUIDE.md)
- [README](README.md)


<!-- see-also -->

---

## Смотрите также
- [PROCESSING_GUIDE](PROCESSING_GUIDE.md)
- [09-automation](09-automation.md)
- [01-overview](01-overview.md)
- [10-future](10-future.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [08-export](../obsidian/processing-guide/08-export.md) (сходство 0.99)
- [01-overview](01-overview.md) (сходство 0.17)
- [01-overview](../obsidian/processing-guide/01-overview.md) (сходство 0.17)

