"""
Тесты для scripts/gateway.py — Lorenzo Gateway (FastAPI).

Покрытие:
  - GET /api/health — статус и поля ответа
  - GET /api/status — статистика корпуса
  - GET /v1/models — список моделей
  - POST /api/ask   — RAG-запрос, режим hybrid
  - POST /api/cards — добавление карточки, cleanup
  - POST /v1/chat/completions — OpenAI-формат, finish_reason, _meta

Запуск:
    pytest tests/test_gateway.py -v
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# ── Импорт приложения ────────────────────────────────────────────────────────

from gateway import app  # noqa: E402  (после sys.path)
from fastapi.testclient import TestClient

client = TestClient(app)

# ── /api/health ──────────────────────────────────────────────────────────────

def test_health_status_ok():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"


def test_health_has_cards_count():
    r = client.get("/api/health")
    data = r.json()
    assert "cards" in data
    assert isinstance(data["cards"], int)
    assert data["cards"] > 0


def test_health_has_passages_count():
    r = client.get("/api/health")
    data = r.json()
    assert "passages" in data
    assert data["passages"] > 0


def test_health_has_version():
    r = client.get("/api/health")
    assert r.json()["version"] == "1.0.0"


def test_health_has_llm_flag():
    r = client.get("/api/health")
    assert "llm" in r.json()

# ── /api/status ──────────────────────────────────────────────────────────────

def test_status_total_cards():
    r = client.get("/api/status")
    assert r.status_code == 200
    data = r.json()
    assert data["total_cards"] > 0


def test_status_sections_nonempty():
    r = client.get("/api/status")
    sections = r.json()["sections"]
    assert isinstance(sections, dict)
    assert len(sections) > 0


def test_status_tools_list():
    r = client.get("/api/status")
    tools = r.json()["tools"]
    assert "search" in tools
    assert "add_card" in tools
    assert "find_collabs" in tools
    assert "get_contacts" in tools


def test_status_core_cards_present():
    r = client.get("/api/status")
    data = r.json()
    assert "core_cards" in data
    assert data["core_cards"] > 0


def test_status_core_le_total():
    r = client.get("/api/status")
    data = r.json()
    assert data["core_cards"] <= data["total_cards"]

# ── /api/search ──────────────────────────────────────────────────────────────

def test_search_returns_results():
    r = client.post("/api/search", json={"query": "агент память", "top_k": 3})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_search_has_count_field():
    r = client.post("/api/search", json={"query": "Yodoca", "top_k": 5})
    data = r.json()
    assert "count" in data
    assert data["count"] == len(data["results"])


def test_search_has_latency():
    r = client.post("/api/search", json={"query": "граф знаний", "top_k": 3})
    data = r.json()
    assert "latency_s" in data
    assert data["latency_s"] < 10.0


def test_search_no_answer_field():
    r = client.post("/api/search", json={"query": "RAG retrieval", "top_k": 3})
    data = r.json()
    assert "answer" not in data   # лёгкий эндпоинт — без LLM-синтеза

# ── /v1/models ───────────────────────────────────────────────────────────────

def test_models_list():
    r = client.get("/v1/models")
    assert r.status_code == 200
    data = r.json()
    assert data["object"] == "list"
    assert len(data["data"]) >= 1
    assert data["data"][0]["id"] == "lorenzo-gateway"

# ── /api/ask ─────────────────────────────────────────────────────────────────

def test_ask_returns_results():
    r = client.post("/api/ask", json={"query": "агент память", "top_k": 3})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_ask_results_have_path():
    r = client.post("/api/ask", json={"query": "граф знаний", "top_k": 3})
    results = r.json()["results"]
    if results:
        assert "path" in results[0]


def test_ask_latency_field():
    r = client.post("/api/ask", json={"query": "RAG retrieval", "top_k": 3})
    data = r.json()
    assert "latency_s" in data
    assert data["latency_s"] < 30.0       # разумный таймаут


def test_ask_has_answer():
    r = client.post("/api/ask", json={"query": "Yodoca консолидация", "top_k": 3})
    data = r.json()
    assert "answer" in data
    assert len(data["answer"]) > 0


def test_ask_empty_query_returns_empty():
    r = client.post("/api/ask", json={"query": "", "top_k": 5})
    assert r.status_code == 200   # не должен падать


def test_ask_search_mode_field():
    r = client.post("/api/ask", json={"query": "граф", "top_k": 3})
    data = r.json()
    assert "search_mode" in data
    assert data["search_mode"] in {"hybrid", "ann"}

# ── /api/cards ───────────────────────────────────────────────────────────────

CARD_SLUG = "test-gateway-card-pytest"
CARD_PATH = ROOT / "docs" / "04-ai-collaborations" / f"{CARD_SLUG}.md"


@pytest.fixture(autouse=False)
def cleanup_test_card():
    """Удалить тестовую карточку после теста."""
    yield
    if CARD_PATH.exists():
        CARD_PATH.unlink()


def test_add_card_creates_file(cleanup_test_card):
    r = client.post("/api/cards", json={
        "title": "Test Gateway Card Pytest",
        "content": "Тестовая карточка создана через pytest.",
        "section": "04-ai-collaborations",
        "tags": ["test", "pytest"],
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "created"
    # Файл должен появиться на диске
    created = list((ROOT / "docs" / "04-ai-collaborations").glob("test-gateway-card-pytest*.md"))
    assert len(created) >= 1
    created[0].unlink()   # cleanup


def test_add_card_response_has_message(cleanup_test_card):
    r = client.post("/api/cards", json={
        "title": "Test Card Message",
        "content": "Проверка поля message в ответе.",
        "section": "04-ai-collaborations",
        "tags": [],
    })
    assert "message" in r.json()
    # cleanup
    for f in (ROOT / "docs" / "04-ai-collaborations").glob("test-card-message*.md"):
        f.unlink()


def test_add_card_minimal_fields():
    r = client.post("/api/cards", json={
        "title": "Minimal Test Card",
        "content": "Минимальные поля.",
    })
    assert r.status_code == 200
    for f in (ROOT / "docs" / "04-ai-collaborations").glob("minimal-test-card*.md"):
        f.unlink()

# ── /v1/chat/completions ─────────────────────────────────────────────────────

def test_chat_completions_basic():
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "Что такое Yodoca?"}],
    })
    assert r.status_code == 200


def test_chat_completions_openai_format():
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "граф знаний AgentFS"}],
    })
    data = r.json()
    assert "choices" in data
    assert "id" in data
    assert "object" in data
    assert data["object"] == "chat.completion"


def test_chat_completions_finish_reason_stop():
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "агент с памятью"}],
    })
    choice = r.json()["choices"][0]
    assert choice["finish_reason"] in {"stop", "tool_calls"}


def test_chat_completions_has_message_content():
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "поиск знаний"}],
    })
    msg = r.json()["choices"][0]["message"]
    assert msg["role"] == "assistant"
    # content либо строка (stop), либо None (tool_calls)
    assert msg["content"] is None or isinstance(msg["content"], str)


def test_chat_completions_latency_meta():
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "тест"}],
    })
    data = r.json()
    if "_meta" in data:
        assert data["_meta"]["latency_s"] < 30.0


def test_chat_collab_intent():
    """Запрос с 'коллаб' должен вернуть результат без ошибки."""
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "найди коллаборации для памяти агента"}],
    })
    assert r.status_code == 200


def test_chat_with_tool_calls_returns_tool_calls():
    """Когда клиент передаёт tools, gateway возвращает tool_calls."""
    r = client.post("/v1/chat/completions", json={
        "model": "lorenzo-gateway",
        "messages": [{"role": "user", "content": "найди проекты про граф"}],
        "tools": [{
            "type": "function",
            "function": {
                "name": "search",
                "description": "Search",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        }],
    })
    assert r.status_code == 200
    choice = r.json()["choices"][0]
    assert choice["finish_reason"] == "tool_calls"
    assert choice["message"]["tool_calls"] is not None


def test_benchmark_status_ok():
    r = client.get("/api/benchmark")
    assert r.status_code == 200


def test_benchmark_has_required_criteria():
    r = client.get("/api/benchmark")
    body = r.json()
    assert "criteria" in body
    assert "all_pass" in body
    for key in ("latency_s", "cards", "orphan_rate", "hit_rate_10"):
        assert key in body["criteria"], f"Missing criterion: {key}"


def test_benchmark_all_pass():
    r = client.get("/api/benchmark")
    body = r.json()
    assert body["all_pass"] is True, (
        f"PROTOTYPE_SPEC §8 criteria not all passing: {body['criteria']}"
    )
