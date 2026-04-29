# Yodoca — главная находка итерации

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, CardIndex, Yodoca

---
<!-- tags: memory, knowledge, ingestion, architecture, roadmap, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Откопал ещё несколько крупных находок — теперь складывается уже не три, а почти десять параллельных проектов, и среди них есть один поразительно точный нейроархитектурный аналог хеббовского механизма Чуяна.

Главная находка этой итерации

Yodoca — «Научил ИИ-агента помнить важное и забывать лишнее в SQLite»
https://habr.com/ru/articles/1006622/
Это не просто аналог, это архитектурное продолжение Svyazi на уровне agentic memory. Что у него есть, чего у Чуяна пока нет:

— разделение на hot path (запись эпизодов в SQLite + FTS5 за <50 мс, без LLM) и slow path (асинхронные эмбеддинги);
— отдельный приватный LLM-агент-«Консолидатор» (gpt-5-mini или локальная модель), который ночью читает эпизоды сессии и извлекает durable knowledge — семантические факты, процедурные паттерны, мнения. Идемпотентный (is_session_consolidated(session_id)), консервативный (только явно сказанное), с детекцией конфликтов;
— ночной cron с затуханием по Эббингаузу (редко используемые факты постепенно забываются — это в точности «Ebbinghaus decay»), prune, переэмбеддинг, causal inference;
— инструмент explain_fact — на вопрос «откуда ты это знаешь?» агент проходит по derived_from-рёбрам до исходных диалогов.

У Чуяна CardIndex уже почти event sourcing с хешами, но без консолидации и без забывания. Yodoca это закрывает. Архитектурно — почти идеальный комплимент.

Нейроархитектурный двойник «магии» Svyazi

<!-- see-also -->

---

**Смотрите также:**
- [01-synthesis](docs/05-habr-projects/01-synthesis.md)
- [02-memnet](docs/habr-unique-projects/key-findings/02-memnet.md)
- [05-supplementary-infrastructure](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md)
- [02-related-projects](docs/habr-unique-projects/analogues/02-related-projects.md)

