---
date: 2026-05-29
tags: [orchestration, security, architecture, anthropic, self-improve]
state: normalized
---

# AI Review — локальное LLM-ревью кода в CI/CD

<!-- toc-auto -->
<!-- tags: ai-review-local-llm, docs -->


<!-- summary -->
> AI Review — локальное LLM-ревью кода в CI/CD — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Nikita Filonov (GitHub подтверждён)  
**Хабр:** https://habr.com/ru/articles/951434/ + https://habr.com/ru/articles/953598/  
**GitHub:** https://github.com/Nikita-Filonov/ai-review  
**Слой:** quality / cicd / orchestration  
**Дата:** декабрь 2025  
**Уникальность:** Клиентский open-source инструмент для автоматического ревью кода через LLM: интеграция с GitHub Actions и GitLab CI, поддержка любого LLM-провайдера (Ollama, OpenAI, Anthropic). Большинство аналогов — cloud SaaS. AI Review запускается локально — никакой код не покидает инфраструктуру.

## Архитектура

```
PR/MR открыт → GitHub Actions / GitLab CI
                        ↓
              AI Review (ai-review v0.20.0+)
                        ↓
              LLM: Ollama (локально) / OpenAI / Anthropic
                        ↓
              Diff анализ + custom prompts (Markdown)
                        ↓
              Комментарии прямо в PR/MR
```

## Ключевые возможности

| Возможность | Описание |
|-------------|----------|
| Провайдеры | Ollama, OpenAI, Anthropic, любой OpenAI-совместимый |
| CI/CD | GitHub Actions, GitLab CI (YAML-конфигурация) |
| Промпты | Кастомизируемые .md-файлы с правилами проекта |
| Приватность | Локальный Ollama — код не уходит в облако |
| Установка | pip install ai-review + несколько строк в YAML |

## Пример конфигурации (GitHub Actions)

```yaml
- uses: Nikita-Filonov/ai-review@v0.20.0
  with:
    model: llama3.1
    provider: ollama
    ollama_url: http://localhost:11434
    temperature: 0.3
    custom_prompts_path: .ai-review/prompts/
```

## Почему важно для Lorenzo

Lorenzo уже имеет:
- `improve_pre_commit.py` — pre-commit хуки
- `improve_ci_config.py` — `.github/workflows/docs.yml`
- `improve_validate.py` — валидация структуры

AI Review добавляет **LLM-ревью самих скриптов** (`scripts/improve_*.py`) при каждом PR:  
не просто синтаксис — проверка промптов, логики, соответствия openLight принципу.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AI Review + openLight (R07)** | AI Review проверяет, что скрипты используют whitelist-инструменты |
| **AI Review + Security Audit (R14)** | CI проверяет безопасность агентов при каждом коммите |
| **AI Review + Healenium (R13)** | Self-healing тесты + AI-ревью = полный automated QA цикл |
| **AI Review + DevClaw (R06)** | DevClaw создаёт PR → AI Review автоматически ревьюирует |

## Контакт

- GitHub: https://github.com/Nikita-Filonov/ai-review
- Статья (инструмент): https://habr.com/ru/articles/951434/
- Статья (гайд за 30 мин): https://habr.com/ru/articles/953598/
- Гайд с Ollama: https://vc.ru/ai/2888775

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
