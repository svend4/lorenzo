# Round 03 — Лог поисковой сессии

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** код, мониторинг, семантический поиск, domain-specific LLM, Telegram-агенты

## Ниши Round 03 (новые, не в R01/R02)

- Code review / developer tools
- Domain-specific fine-tuned LLM (не generic, а под задачу)
- Семантический поиск с vector DB (без внешних сервисов)
- Telegram как среда для агентов
- Second brain / PKM с AI

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| AI Review | @Nikita-Filonov / @sound_right | Code review CI/CD | `projects/ai-review.md` |
| DevOps LLM Monitor | @oni_devops_lab | Domain-specific fine-tuned LLM | `projects/devops-llm-monitor.md` |
| HabrSearch | @igor_suhorukov | Semantic search / pgvector | `projects/habr-search.md` |

## Лучшие комбинации

| Новый проект | + Из Round 01/02 | Новое свойство | Сила |
|-------------|------------------|----------------|------|
| AI Review | PocketCoder (R02) | Замкнутый цикл: write→review→fix | ⭐⭐⭐ |
| DevOps LLM паттерн | Lorenzo corpus | Дистиллированный offline Knowledge OS | ⭐⭐⭐⭐ |
| HabrSearch pipeline | improve_embedding_index | Реальный векторный поиск по базе Svyazi | ⭐⭐⭐⭐ |
| AI Review | improve_contradiction_check | Doc-review при каждом коммите | ⭐⭐⭐ |

## Главная находка раунда

**DevOps LLM Monitor** даёт паттерн следующего шага для Svyazi:  
не RAG (поиск в документах), а **дистилляция** (знания Svyazi → маленькая локальная модель).  
Это переход от «базы знаний» к «модели со знаниями».

## Что не нашли (осталось на R04)

- Готовый PKM/second brain инструмент с открытым кодом от русского автора
- AI для Telegram с постоянной памятью (не просто бот, а агент)
- Проекты из медицины/науки с реальным open-source кодом
