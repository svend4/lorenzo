# Healenium + локальная LLM — самовосстанавливающиеся тесты

**Автор:** команда Healenium (EPAM + OSS) + авторы статьи  
**Хабр:** https://habr.com/ru/articles/887226/  
**GitHub:** https://github.com/healenium/healenium-web (Apache 2.0)  
**Слой:** quality / testing / automation  
**Дата:** 2025  
**Уникальность:** Два подхода в одном паттерне: **Healenium** (библиотека: дерево DOM → алгоритм поиска альтернативных элементов) + **локальная LLM** (читает page_source, 10k токенов, возвращает новый селектор). Тест падает → агент чинит сам → тест продолжает. Без облака, без JIRA-тикета.

## Два подхода к self-healing

### Healenium (алгоритмический)

```
Selenium: элемент не найден (сломан селектор)
        ↓
Healenium: читает DOM-дерево
        ↓
Алгоритм поиска похожих элементов (дерево сходства)
        ↓
Исправленный XPath / CSS-селектор → продолжение теста
        ↓
Новый селектор сохраняется в PostgreSQL
```

### Локальная LLM (семантический)

```
Selenium: page_source (очищен от style/script, ~10k токенов)
        ↓
Локальная LLM (Ollama: llama3, Qwen и др.)
        ↓
Промпт: "найди элемент с функцией X, верни новый XPath"
        ↓
Исправленный селектор
```

## Технический стек Healenium

| Компонент | Технология |
|-----------|-----------|
| Core | Java / Selenium WebDriver |
| Storage | PostgreSQL (история исправлений) |
| Дерево сходства | кастомный алгоритм (EPAM Research) |
| LLM-расширение | через кастомный хук |
| Лицензия | Apache 2.0 |

## Healenium для Python-проектов

Healenium-web — Java. Для Python + Selenium:  
паттерн из статьи (887226) — ручная реализация через Ollama + очистка DOM.  
`scripts/utils_chunker.py` (Lorenzo) уже есть для чанкинга — применим к page_source.

## Почему важно для Lorenzo

Lorenzo имеет 159 скриптов (`improve_*.py`) и тест-смоук (`improve_mcp_test.py`).  
При изменении MCP-интерфейса тесты ломаются.  
Паттерн Healenium: **test_runner → ошибка → LLM → исправление → повтор**.  
Это аналог ADD feedback loop применённый к тестированию.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Healenium + improve_mcp_test** | Self-healing smoke-тесты MCP-серверов Lorenzo |
| **Healenium + ADD (R13)** | ADD-цикл с feedback от тестов: агент чинит то, что сломали |
| **Healenium + Observability (R13)** | Langfuse трейсит self-healing события → видно сколько раз тест чинился |
| **Healenium + openLight (R07)** | openLight проверяет что healing не меняет бизнес-логику |

## Контакт

- GitHub (core): https://github.com/healenium/healenium-web
- GitHub (Python-паттерн): статья 887226 на Хабре
- Статья: https://habr.com/ru/articles/887226/
- Лицензия: Apache 2.0
