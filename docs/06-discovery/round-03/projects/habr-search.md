# HabrSearch (Semantic Habr)

**Автор:** igor_suhorukov (Habr-профиль)  
**Хабр:** https://habr.com/ru/articles/915348/  
**GitHub:** не найден явно (проект на Java/Spring Boot, возможно в профиле автора)  
**Слой:** search / ingestion / knowledge-index  
**Дата:** июнь 2025  
**Уникальность:** Семантический поиск по всем статьям Хабра через PostgreSQL + pgvector + локальный Ollama. Чистый pipeline без внешних API: Habr API → LLM извлекает темы/ключевые слова → embedding → pgvector поиск. Работает на своём железе, бесплатно.

## Что делает

- Загружает статьи через Habr API, сохраняет в PostgreSQL
- LLM (через Ollama, локально) извлекает темы, ключевые слова, краткое содержание
- Embedding-модель (через Ollama) создаёт векторные представления
- pgvector — хранение и поиск по embeddings
- Результат: полнотекстовый + семантический поиск по всему корпусу Хабра локально

## Почему интересно для Svyazi

Svyazi уже хранит 2483 документа в search_index.json и использует BM25+TF-IDF. HabrSearch показывает как добавить **настоящий семантический поиск** (embeddings) поверх корпуса через Postgres+pgvector — без ChromaDB, без Pinecone, без внешних сервисов.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **HabrSearch pipeline + Lorenzo corpus** | Заменить BM25 на pgvector-поиск: семантические запросы к 2483 документам |
| **HabrSearch + knowledge-space** | Семантически проиндексированная knowledge-space с Postgres backend |
| **HabrSearch + improve_embedding_index** | Гибридный поиск: TF-IDF (текущий) + pgvector (новый) + BM25 = три метода в одном |
| **HabrSearch + LiteParse (nlaik)** | Habr-статьи → LiteParse извлекает evidence → pgvector индекс → поиск по доказательствам |

## Контакт

- Habr: https://habr.com/ru/users/igor_suhorukov/
