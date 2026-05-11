# Ансамбль 4 — Web-to-Knowledge Pipeline

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, knowledge-space, Firecrawl

---
<!-- tags: knowledge, ingestion, architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

4. Web-to-Knowledge Pipeline: «браузер не как экран, а как датчик данных»

Родители: Firecrawl Browser Sandbox + Playwright ARIA snapshots + агент конкурентного анализа + knowledge-space/Svyazi.

Firecrawl Browser Sandbox превращает браузинг в команды уровня намерений: open → click → fill → snapshot → scrape; агент получает готовые артефакты, а не сырой DOM и логи драйвера, что экономит токены и снимает боль с browser automation. Habr

Статья про то, как агенты видят веб-страницы, хорошо объясняет второй кубик: Playwright формирует ARIA snapshot — YAML-дерево, оптимизированное для LLM, где видны роли элементов, интерактивность, ссылки, текстовые поля и кнопки, без CSS и лишнего DOM-мусора. Habr

В статье про агента конкурентного анализа Firecrawl используется как crawler/parser с MCP-сервером: он обходит сайты, собирает страницы и возвращает данные в удобном для LLM виде; шаблон конкурентного анализа заставляет агента не писать «простыню», а заполнять фиксированные поля. Habr

Что рождается при склейке:

Получается web-to-knowledge конвейер: веб-страница перестаёт быть HTML-хаосом и превращается в структурированную карточку.

Схема:

Firecrawl/Playwright → ARIA snapshot → fixed extraction schema → Svyazi-like normalization → knowledge-space cards → Graph/Memory OS

Дети этой связки:

Habr Scout — агент ежедневно обходит новые статьи Хабра, вытаскивает проекты, авторов, стек, открытые вопросы, потенциальные связки и складывает в карточки.

Market Intelligence Bot — регулярный конкурентный анализ: сайты, changelog, GitHub, документация, цены, вакансии, новые API.

Court/Regulation Watcher — отслеживание судебных сайтов, ведомственных страниц, изменений регламентов; всё не просто в RSS, а в карточки с нормализованными сущностями.

Главное новое свойство: браузер становится сенсорным слоем для базы знаний. Агент не «гуляет по интернету», а извлекает структурированные сигналы и обновляет память.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Ансамбль 4 Web to Knowledge Pipeline"
```

## Смотрите также
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [9-ambient-team-agent](9-ambient-team-agent.md)
- [7-domain-agent-app-factory](7-domain-agent-app-factory.md)
- [8-budget-aware-intelligence-stack](8-budget-aware-intelligence-stack.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [9-ambient-team-agent](9-ambient-team-agent.md)
- [README](README.md)

