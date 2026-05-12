# Обучил свой DevOps-агент: fine-tuning + дистилляция qwen3 для серверного мониторинга

**Автор:** независимый разработчик (Хабр, май 2026)  
**Хабр:** https://habr.com/ru/articles/1033128/ (Часть 1)  
**Смежные:** https://habr.com/ru/articles/1033426/ (Часть 2: Обучение), https://habr.com/ru/articles/1033434/ (Часть 3: Дистилляция)  
**GitHub:** не опубликован (код частично в статьях)  
**Слой:** orchestration / automation / knowledge  
**Дата:** май 2026  
**Уникальность:** Серия из 3 частей: разработчик хотел пойти в отпуск — ни одна из существующих локальных LLM не справилась с реальными DevOps-задачами. Потратил 2 недели и RTX 3090, чтобы дообучить qwen3:14b через дистилляцию — результат 10/10 на реальных тестах против 7/10 у исходной модели. Zero галлюцинаций «отчитался, но не выполнил».

## Проблема: локальные LLM ломаются на DevOps

```
Задача: агент, который может подключиться по SSH и проверить логи контейнеров

Протестированы (все провалились):
  qwen3:14b (базовая):    inconsistent tool calling, галлюцинации в ответах
  llama3.1:8b:           truncated output, путается с аргументами функций
  mistral:7b:            не понимает многошаговые серверные задачи
  gemma2:9b:             отчитывается об успехе не выполнив команду

Реальные случаи (50% не обрабатываются):
  "nginx не стартует, найди причину" → модель выдумывает причину
  "посмотри логи за последний час" → усекает вывод, теряет ошибки
  "проверь дисковое пространство на всех нодах" → путает инструменты
```

## Подход: дистилляция от сильной модели

```python
# Идея: GPT-4o/Claude правильно решает DevOps-задачи
# → сгенерировать dataset правильных traces
# → дообучить qwen3:14b на этих traces

PIPELINE:
  1. Собрать реальные DevOps-задачи (SSH, nginx, docker, postgres, systemd...)
  2. Запустить GPT-4o/Claude → получить правильные tool call + reasoning traces
  3. Отфильтровать: принять только корректные (acceptance rate ~76%)
  4. Fine-tune qwen3:14b на отфильтрованных traces (2107 примеров, 2 эпохи)
  5. Тестировать на реальных задачах (не синтетических!)
```

## Датасет: домены DevOps-задач

```
Покрытые домены (2107 traces):
  ssh              — подключение, передача файлов, туннели
  nginx            — статус, конфиги, логи, restart, upstream
  docker           — контейнеры, логи, stats, exec, compose
  systemd          — статус сервисов, journalctl, enable/disable
  postgres         — запросы, логи медленных запросов, размер БД
  monitoring       — CPU, RAM, disk, сетевые интерфейсы
  dns              — dig, nslookup, резолвинг
  ssl              — certbot, дата истечения, цепочка сертификатов
  storage          — df, lsblk, du, mount
  proxies          — nginx upstream, балансировщики
  backups          — rsync, tar, проверка целостности
  vpn              — wireguard, openvpn статус
  firewall         — iptables, ufw, nftables

Формат traces:
  system_prompt → user_task → [tool_call → tool_result]* → final_answer
```

## Catastrophic Forgetting: главная проблема fine-tuning

```python
# Проблема: после fine-tuning модель "забывает" общие знания
# (catastrophic forgetting = классическая проблема transfer learning)

# Решение из статьи: смешивание датасетов

TRAINING_MIX = {
    "devops_traces": 0.70,      # специализированные (70%)
    "general_instructions": 0.30, # общий instruction-following (30%)
}
# → модель сохраняет общую связность речи
# → добавляет специализированное поведение tool call

# Параметры LoRA (RTX 3090, 24GB VRAM):
lora_config = {
    "r": 16,
    "lora_alpha": 32,
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
    "lora_dropout": 0.1,
    "bias": "none"
}
```

## Результаты: 10/10 vs 7/10

```
Тест: 10 реальных серверных задач (не синтетических)

qwen3:14b (базовая):
  Оценка: 7/10
  Проблемы: галлюцинации в tool results, truncation, неверные аргументы

qwen3:14b (fine-tuned):
  Оценка: 10/10
  Zero галлюцинаций "выполнено" когда не выполнено
  Честный отказ: "Не знаю как выполнить эту задачу"
  Правильный tool calling: инструменты + аргументы без ошибок
  Полный вывод: не усекает длинные логи
  
Размер: те же 14B параметров, тот же hardware
Прирост: от "иногда работает" до "надёжно работает"
```

## Инфраструктура: RTX 3090 за 2 недели

```
Hardware: Nvidia RTX 3090 24GB
Framework: Unsloth (быстрее transformers на 2×, меньше VRAM)
Base model: qwen3:14b-Q4_K_M (через Ollama)
Fine-tune: LoRA (не full fine-tuning — не помещается)
Data: 2107 traces от Claude/GPT-4o (acceptance rate 76%)
Эпохи: 2
Время обучения: ~18 часов (2 недели потрачены на эксперименты + датасет)
Деплой: Ollama → тот же API что и базовая модель
```

## Применение к Lorenzo

Lorenzo запускает `improve_run_all.py` и Python-скрипты.  
DevOps LLM паттерн = **Custom Tool-Calling Model** для Lorenzo-специфичных задач:

```python
# Проблема Lorenzo: Claude хорошо отвечает на вопросы, но иногда
# галлюцинирует при вызове инструментов с нестандартными параметрами

# Паттерн distillation для Lorenzo:
# 1. Записывать успешные Claude tool calls (audit.db уже есть!)
# 2. Экспортировать traces: query → tool_call → result → final
# 3. Fine-tune Qwen2.5:7b на Lorenzo-специфичных tool calls
# 4. Использовать локальную модель для быстрых/дешёвых операций

# Конкретно: improve_llm_qa.py traces → fine-tune → local Q&A model
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DevOps LLM + LLM Router (R20)** | Маршрутизация: простые DevOps-задачи → fine-tuned local, сложные → Claude |
| **DevOps LLM + Sberbank AIOps (R24)** | Кастомный DevOps-агент + ML-мониторинг: от предсказания до исправления |
| **DevOps LLM + Self-hosted (R22)** | Ollama + fine-tuned qwen = полностью локальный DevOps-агент |
| **DevOps LLM + LLM Tests (R20)** | Mutation testing для DevOps-агента: проверка edge cases инструментов |
| **DevOps LLM + Langfuse (R13)** | Трейсинг кастомного агента: сравнение base vs fine-tuned на реальных задачах |

## Контакт

- Часть 1 (проблема + подход): https://habr.com/ru/articles/1033128/ (май 2026)
- Часть 2 (обучение): https://habr.com/ru/articles/1033426/
- Часть 3 (дистилляция): https://habr.com/ru/articles/1033434/
- Unsloth (fast fine-tuning): github.com/unslothai/unsloth (Apache 2.0)
- Смежная (LLM дообучение 2026): https://habr.com/ru/companies/otus/articles/1026700/
