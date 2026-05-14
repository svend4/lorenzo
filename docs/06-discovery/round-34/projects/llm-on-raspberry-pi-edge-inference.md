# Как запустить LLM на Raspberry Pi 5: GGUF квантизация и Edge inference

**Автор:** Denbackyard (Cloud.ru)  
**Хабр:** https://habr.com/ru/companies/cloud_ru/articles/964136/  
**GitHub:** https://github.com/open-webui/open-webui (веб-интерфейс)  
**Слой:** orchestration / edge  
**Дата:** ноябрь 2025  
**Уникальность:** Единственный практический русскоязычный бенчмарк LLM на Raspberry Pi 5 с реальными замерами TTFT и TPS: TinyLlama, Phi-3 Mini, Mistral 7B, Gemma2-2B, LLaVA 7B через Ollama/llama.cpp с GGUF квантизацией q4_K_M/q5_K_S/q8. Автор предлагает гибридную edge архитектуру — Pi обрабатывает локально, тяжёлый inference уходит в облако.

## Зачем LLM на Raspberry Pi

```
Сценарии использования (из статьи):
  1. Локальный AI-ассистент без доступа в интернет
     (закрытые производства, больницы, военные объекты)
  2. Умный дом: голосовые команды → локальный LLM → действия
  3. IoT edge: предобработка данных сенсоров до отправки в облако
  4. Обучение / прототипирование без облачных расходов

Raspberry Pi 5:
  CPU: Cortex-A76 quad-core @ 2.4 GHz
  RAM: 8 GB / 16 GB LPDDR4X
  Storage: NVMe SSD (через PCIe)
  Цена: ~$80 (8GB) / ~$120 (16GB)
  vs H100: ~$30K → разница x375 по цене
```

## GGUF квантизация: как влезть в 8 GB RAM

```python
# llama.cpp GGUF квантизация: разные уровни сжатия

GGUF_QUANTIZATION_TYPES = {
    "q4_K_M": {
        "описание": "4-bit квантизация, Medium размер",
        "сжатие": "~4x от BF16",
        "качество": "★★★★ — рекомендовано для Pi",
        "Mistral_7B_размер": "4.1 GB → влезает в 8 GB Pi",
        "Mistral_7B_TPS": "2-3 tok/sec на Pi 5",
        "потеря_качества": "~1-3% на бенчмарках"
    },
    "q5_K_M": {
        "описание": "5-bit квантизация, Medium размер",
        "сжатие": "~3.2x от BF16",
        "качество": "★★★★★ — лучший баланс",
        "Mistral_7B_размер": "4.8 GB",
        "Mistral_7B_TPS": "1.5-2 tok/sec на Pi 5",
        "потеря_качества": "~0.5%"
    },
    "q8_0": {
        "описание": "8-bit квантизация",
        "сжатие": "~2x от BF16",
        "качество": "★★★★★ — почти без потерь",
        "Mistral_7B_размер": "7.2 GB → едва влезает",
        "Mistral_7B_TPS": "0.8-1 tok/sec на Pi 5",
        "потеря_качества": "< 0.1%"
    },
    "q2_K": {
        "описание": "2-bit квантизация (агрессивная)",
        "сжатие": "~8x от BF16",
        "качество": "★★ — заметная деградация",
        "Mistral_7B_размер": "2.7 GB",
        "Mistral_7B_TPS": "4-5 tok/sec на Pi 5",
        "потеря_качества": "~10-15%"
    }
}

# Вывод из статьи:
# q4_K_M = оптимальная точка для Pi 5 (RAM vs качество vs скорость)
```

## Установка Ollama на Raspberry Pi

```bash
# Установка Ollama на Raspberry Pi OS (Debian-based)
# Поддерживает: Pi 4 (4-8GB), Pi 5 (8-16GB)

# 1. Установить Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Запустить сервер
ollama serve &

# 3. Скачать модели (выбор по RAM)
# 8 GB Pi → рекомендуемые модели:
ollama pull tinyllama:1b          # 637 MB — мгновенный ответ
ollama pull phi3:mini             # 2.3 GB — хорошее качество
ollama pull gemma2:2b             # 1.6 GB — Google модель
ollama pull mistral:7b-q4_K_M    # 4.1 GB — максимум для 8GB Pi

# 16 GB Pi → можно добавить:
ollama pull mistral:7b-q5_K_M    # 4.8 GB — лучше качество
ollama pull llava:7b-q4_K_M      # 4.7 GB — мультимодальная (изображения)

# 4. Тест
ollama run mistral:7b-q4_K_M "Привет! Расскажи о себе."
```

## Реальные замеры TTFT и TPS

```python
import requests
import time

def benchmark_model(model: str, prompt: str) -> dict:
    """Замер TTFT (time to first token) и TPS (tokens per second)"""
    start = time.time()
    first_token_time = None
    total_tokens = 0

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": True},
        stream=True
    )

    for line in response.iter_lines():
        data = json.loads(line)
        if first_token_time is None:
            first_token_time = time.time() - start
        total_tokens += 1
        if data.get("done"):
            break

    total_time = time.time() - start
    return {
        "ttft_sec": first_token_time,
        "tps": total_tokens / total_time,
        "total_tokens": total_tokens
    }

# Результаты из статьи (Raspberry Pi 5, 8 GB RAM):
PI5_BENCHMARKS = {
    "tinyllama:1b-q4_K_M": {
        "TTFT": "0.3 сек",  "TPS": "8-12",  "качество": "★★"
    },
    "phi3:mini-q4_K_M": {
        "TTFT": "0.8 сек",  "TPS": "4-6",   "качество": "★★★★"
    },
    "gemma2:2b-q4_K_M": {
        "TTFT": "0.6 сек",  "TPS": "5-8",   "качество": "★★★"
    },
    "mistral:7b-q4_K_M": {
        "TTFT": "1.5-3 сек", "TPS": "2-3",  "качество": "★★★★★"
    },
    "llava:7b-q4_K_M": {
        "TTFT": "2-4 сек",  "TPS": "1.5-2", "качество": "★★★★ (мультимодальная)"
    }
}

# Практический вывод:
# phi3:mini → лучший для realtime задач (вопрос-ответ)
# mistral:7b → лучший для качества (генерация текста, анализ)
# tinyllama → для встроенных систем с жёстким ограничением по RAM
```

## Гибридная архитектура: Pi + Cloud

```python
# Ключевая идея статьи: Pi для локальной обработки,
# облако для тяжёлых задач

class HybridEdgeCloudPipeline:
    """
    Pi обрабатывает:
      → Простые вопросы (phi3:mini TTFT ~0.8с)
      → Локальное индексирование данных
      → PII фильтрация перед облаком

    Cloud.ru обрабатывает:
      → Сложные reasoning задачи (70B+ модели)
      → Batch processing (низкий приоритет)
      → Fine-tuning
    """

    def __init__(self):
        self.local_llm = OllamaClient(url="http://localhost:11434")
        self.cloud_llm = CloudRuClient(api_key=os.environ["CLOUD_API_KEY"])

    def route_request(self, query: str, context: str) -> str:
        # Оценить сложность запроса локально (быстро)
        complexity = self._estimate_complexity(query)

        if complexity < 0.4:
            # Простой вопрос → phi3:mini на Pi (бесплатно, ~1 сек)
            return self.local_llm.generate(
                model="phi3:mini",
                prompt=f"{context}\n\n{query}"
            )
        else:
            # Сложный → PII маскировка → облако
            safe_context = self.pii_masker.mask(context)
            return self.cloud_llm.generate(
                model="mistral-7b-instruct",  # Cloud.ru endpoint
                prompt=f"{safe_context}\n\n{query}"
            )

    def _estimate_complexity(self, query: str) -> float:
        """Быстрая эвристика сложности запроса."""
        COMPLEX_WORDS = ["сравни", "проанализируй", "объясни", "докажи", "синтезируй"]
        score = sum(1 for w in COMPLEX_WORDS if w in query.lower()) / len(COMPLEX_WORDS)
        return min(1.0, score + len(query) / 500)
```

## Open WebUI: браузерный интерфейс к Ollama

```bash
# Open WebUI — ChatGPT-подобный интерфейс к Ollama на Pi
# GitHub: github.com/open-webui/open-webui

# Запуск через Docker (Pi 5 + Docker ARM64):
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main

# Доступ: http://raspberry-pi-ip:3000
# Функции: история чатов, выбор модели, загрузка файлов, RAG
```

## Применение к Lorenzo

```python
# Lorenzo на edge устройстве (без интернета):

LORENZO_EDGE_CONFIG = {
    "устройство": "Raspberry Pi 5 (16 GB)",
    "модель": "mistral:7b-q4_K_M",
    "endpoint": "http://localhost:11434/v1",
    "совместимость": "OpenAI API (improve_llm_*.py работают без изменений)",
    "use_cases": [
        "improve_llm_qa.py --question '...' — Q&A по базе знаний офлайн",
        "improve_llm_enrich.py — обогащение документов без облака",
        "Закрытые корпоративные сети (152-ФЗ compliance)"
    ],
    "ограничения": [
        "TPS ~2-3 vs ~50+ в облаке",
        "Контекстное окно 32K (vs 200K у Claude)",
        "Нет fine-tuning (только inference)"
    ]
}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Pi Edge + YADRO Sovereign (R33)** | Продолжение суверенного AI: YADRO кластер → edge Pi устройства |
| **Pi Edge + Cognitive Memory (R31)** | SQLite память агента на Pi — полностью локальный intelligent agent |
| **Pi Edge + ai-review (R34)** | Ollama на Pi как backend для ai-review в offline CI/CD |
| **Pi Edge + Federated Edge (R28)** | Pi 5 как federal edge node в federated learning кластере |
| **Pi Edge + MT-Bench RU (R34)** | Бенчмарк RU моделей на Pi: сравнить качество vs latency tradeoff |

## Контакт

- Статья: https://habr.com/ru/companies/cloud_ru/articles/964136/ (ноябрь 2025)
- Cloud.ru: cloud.ru (российский облачный провайдер)
- Ollama: ollama.com
- Open WebUI: github.com/open-webui/open-webui
- llama.cpp (GGUF runtime): github.com/ggerganov/llama.cpp
- Смежная (Ollama vs vLLM vs llama.cpp): https://habr.com/ru/articles/948934/
- Смежная (EdgeAI 2024/2025 how-to): https://habr.com/ru/companies/recognitor/articles/846936/
