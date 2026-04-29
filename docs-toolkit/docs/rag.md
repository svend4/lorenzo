# RAG: вопрос-ответ

End-to-end Retrieval-Augmented Generation: retrieve → assemble → answer.

## Quickstart

```bash
docstoolkit rag ask "Что такое X?" --top 5 --method hybrid --answerer echo
```

## Provider'ы (LLM)

| Provider | Установка | Cost | Использование |
|---|---|---|---|
| `echo` | встроен | free | mock для тестов |
| `anthropic` | `pip install anthropic` | paid | Claude Haiku/Sonnet/Opus |
| `openai` | `pip install openai` | paid | GPT-4o-mini / GPT-4o |
| `gemini` | `pip install google-generativeai` | free tier | Gemini 2.0 Flash / 1.5 Pro |
| `ollama` | локальный daemon | free | Llama 3.2 / любая локальная модель |

```bash
# Список доступных
docstoolkit rag ask "?" --answerer echo --json | python -c "import json,sys; print(json.load(sys.stdin)['answerer'])"
```

## API

### Простой ask()

```python
from docstoolkit.rag import ask

result = ask(
    "Что такое Yodoca?",
    top_k=5,
    method="hybrid",        # keyword | semantic | hybrid
    answerer="anthropic",
    model="claude-haiku-4-5-20251001",
)

print(result.answer)
print(f"Tokens: {result.tokens_used}, cost: ${result.cost_estimate}")
for c in result.citations:
    print(f"  [{c['n']}] {c['title']}")
```

### Конфигурируемый pipeline

```python
from docstoolkit.rag import RAGPipeline, RAGQuery

query = RAGQuery(
    question="Что такое X?",
    top_k=10,
    method="semantic",
    answerer="openai",
    model="gpt-4o-mini",
    max_context_tokens=12000,
    include_citations=True,
    locale="ru",
)
result = RAGPipeline(query).run()
```

### Custom Answerer

```python
from docstoolkit.rag.answerer import Answerer, register_answerer

class MyAnswerer(Answerer):
    name = "my-llm"

    def answer(self, system, user, model=""):
        # ... ваша логика ...
        return ("Ответ", tokens_used, cost_usd)

register_answerer("my-llm", MyAnswerer)
```

## Конфигурация через docstoolkit.toml

```toml
[rag]
default_answerer = "anthropic"
default_method = "hybrid"
default_top_k = 5
max_context_tokens = 8000

[rag.anthropic]
model = "claude-haiku-4-5-20251001"
# api_key через ANTHROPIC_API_KEY env
```

## Архитектура

```
┌─────────┐     ┌──────────┐     ┌─────────┐
│Question │ →   │Retriever │ →   │Passages │
└─────────┘     └──────────┘     └────┬────┘
                                      ↓
                                 ┌──────────┐
                                 │Assembler │ → system_prompt + user_message
                                 └────┬─────┘
                                      ↓
                                 ┌──────────┐
                                 │ Answerer │ → text + tokens + cost
                                 └────┬─────┘
                                      ↓
                                 ┌─────────────┐
                                 │AnswerResult │
                                 └─────────────┘
```

- **Retriever**: оборачивает `embeddings.search()` (keyword / semantic / hybrid)
- **Assembler**: формирует промпт с пронумерованными цитатами `[1]`, `[2]`...
- **Answerer**: LLM-вызов с pricing tracking
