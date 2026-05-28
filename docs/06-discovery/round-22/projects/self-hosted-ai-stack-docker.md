---
date: 2026-05-28
tags: [memory, rag, orchestration, local-first, architecture]
state: normalized
---

# Self-hosted AI платформа — полный стек: n8n + Ollama + Open WebUI + Docker

<!-- toc-auto -->
<!-- tags: self-hosted-ai-stack-docker, docs -->


<!-- summary -->
> docker-compose.yml (упрощённый) n8n как оркестратор AI workflows Бенчмарки (декабрь 2025, RTX 4090)
 
docker-compose.yml (упрощённый)
 
n8n как оркестратор AI workflows
 
Бенчмарки (декабрь 2025, RTX 4090)
 
Coolify для управления деплоем
 
Полная стоимость vs Cloud AI
 
Применение к Lorenzo
Lorenzo сейчас: Claude API + Python скри


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр, декабрь 2025)  
**Хабр:** https://habr.com/ru/articles/973456/  
**GitHub:** https://github.com/coleam00/local-ai-packaged (MIT, community fork)  
**Слой:** orchestration / memory / ingestion  
**Дата:** декабрь 2025  
**Уникальность:** Первый полный русскоязычный production-гайд по self-hosted AI стеку: n8n (автоматизация, 400+ интеграций) + Ollama (локальные LLM) + Open WebUI (интерфейс) + PostgreSQL + Docker Compose. Бенчмарки моделей декабрь 2025. Работает без облака, данные не покидают сервер.

## Компоненты стека

```
┌──────────────────────────────────────────────────────┐
│              Self-hosted AI Stack                    │
├──────────────┬───────────────────────────────────────┤
│ Open WebUI   │ ChatGPT-подобный интерфейс            │
│              │ Built-in RAG, история, промпты        │
├──────────────┼───────────────────────────────────────┤
│ Ollama       │ Локальный LLM-сервер                  │
│              │ GGUF + GPU auto-detect + OpenAI API   │
├──────────────┼───────────────────────────────────────┤
│ n8n          │ Оркестратор автоматизации             │
│              │ 400+ интеграций, visual workflows     │
├──────────────┼───────────────────────────────────────┤
│ PostgreSQL   │ Хранилище для n8n + векторное (pgvec) │
├──────────────┼───────────────────────────────────────┤
│ FFmpeg       │ Аудио/видео обработка (встроен)       │
└──────────────┴───────────────────────────────────────┘
```

## docker-compose.yml (упрощённый)

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      OLLAMA_BASE_URL: http://ollama:11434
    volumes:
      - open_webui_data:/app/backend/data

  n8n:
    image: docker.n8n.io/n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
    volumes:
      - n8n_data:/home/node/.n8n

  postgres:
    image: pgvector/pgvector:pg16  # pgvector встроен
    environment:
      POSTGRES_DB: n8n
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: ${DB_PASSWORD}

volumes:
  ollama_data:
  open_webui_data:
  n8n_data:
```

## n8n как оркестратор AI workflows

```
Примеры workflows из статьи:

1. Email AI assistant:
   Gmail trigger → n8n → Ollama(qwen2.5:7b) → classify → reply draft

2. Document processing:
   Webhook → MarkItDown → chunk → Ollama embed → pgvector → search

3. Monitoring alert:
   Prometheus alert → n8n → Ollama(analyze) → Telegram notification

4. RAG pipeline:
   Новый файл → extract text → Ollama embed → pgvector store
   User query → Ollama embed → pgvector search → Ollama generate → answer
```

## Бенчмарки (декабрь 2025, RTX 4090)

```
Модель              | Tokens/s | VRAM  | Quality (субъективно)
─────────────────────────────────────────────────────────────
qwen2.5:7b (Q4_K_M) |   85/s  |  6GB  | ★★★★☆ (code, RU)
qwen2.5:14b (Q4_K_M)|   42/s  | 10GB  | ★★★★★ (best overall)
llama3.1:8b (Q4_K_M)|   78/s  |  6GB  | ★★★☆☆ (EN-first)
mistral:7b (Q4_K_M) |   82/s  |  5GB  | ★★★☆☆ (instruction)
gemma2:9b (Q4_K_M)  |   55/s  |  7GB  | ★★★★☆ (reasoning)

Рекомендация: qwen2.5:14b для качества, qwen2.5:7b для скорости/RU
```

## Coolify для управления деплоем

```
Coolify = self-hosted Heroku:
  → web UI для управления Docker-сервисами
  → auto SSL через Let's Encrypt
  → git webhooks: push → auto redeploy
  → мониторинг: CPU, RAM, disk по сервисам
  → backups: volume snapshots

Установка:
  curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
  # → открыть :8000 → добавить сервис → вставить docker-compose.yml
```

## Полная стоимость vs Cloud AI

```
Self-hosted (VDS 2× A100 80GB):
  Сервер: ~$1200/месяц (Hetzner / SelectelGPU)
  Модели: $0 (open weights)
  При 10K запросов/день: $1200/месяц

Cloud API (Claude Sonnet):
  10K запросов × 2000 токенов avg = 20M токенов
  $3/1M × 20M = $60/месяц

Вывод: Cloud дешевле при <100K токенов/день
  Self-hosted дешевле при >500K токенов/день
  + 100% контроль данных (ФЗ-152)
```

## Применение к Lorenzo

Lorenzo сейчас: Claude API + Python скрипты.  
Self-hosted стек = автономный Lorenzo без зависимости от API:

```bash
# Lorenzo на self-hosted:
docker-compose up -d  # поднять стек

# В .env:
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen2.5:14b

# improve_llm_qa.py, improve_llm_enrich.py → работают без ANTHROPIC_API_KEY
# n8n автоматизирует: cron → run_improve.py --group reports
```

n8n заменяет `improve_workflow_v2.py` для визуального построения пайплайнов.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Self-hosted + FRIDA (R18)** | FRIDA embeddings + pgvector = локальный нейронный поиск |
| **Self-hosted + llama.cpp (R19)** | llama.cpp сервер вместо Ollama = в 3× быстрее |
| **Self-hosted + GigaAM (R16)** | Voice → GigaAM → n8n → Ollama → ответ (100% локально) |
| **Self-hosted + Jay Guard (R21)** | Jay Guard перед Ollama: ПД никогда не покидают контур |
| **Self-hosted + Langfuse (R13)** | Langfuse self-hosted: трейсинг локального LLM-стека |

## Контакт

- Статья: https://habr.com/ru/articles/973456/ (декабрь 2025)
- GitHub (local-ai-packaged): https://github.com/coleam00/local-ai-packaged (MIT)
- Open WebUI: https://github.com/open-webui/open-webui (MIT)
- n8n: https://github.com/n8n-io/n8n (Sustainable Use License)
- Ollama: https://github.com/ollama/ollama (MIT)
- Coolify: https://github.com/coollabsio/coolify (Apache 2.0)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
