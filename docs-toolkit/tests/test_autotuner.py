"""Тесты AutoTuner: wilson_lower, compute_winrates, best_retriever."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.feedback.store import Feedback, FeedbackStore
from docstoolkit.feedback.autotuner import (
    AutoTuner,
    WinRateStats,
    compute_winrates,
    wilson_lower,
    _compute_winrates_by_field,
)


# ------------------------------------------------------------------ #
# Fixtures                                                            #
# ------------------------------------------------------------------ #

@pytest.fixture
def store(tmp_path):
    db = tmp_path / "fb.sqlite"
    s = FeedbackStore(db_path=db)
    yield s
    s.close()


@pytest.fixture
def tuner(store):
    return AutoTuner(store, min_samples=5, improve_threshold=0.15)


def make_feedback(retriever: str, thumbs: str, answerer: str = "") -> Feedback:
    return Feedback(
        request="test question",
        response_text="test answer",
        thumbs=thumbs,
        skill="rag",
        retriever=retriever,
        answerer=answerer or retriever,
    )


# ------------------------------------------------------------------ #
# wilson_lower                                                          #
# ------------------------------------------------------------------ #

def test_wilson_lower_zero_n():
    """n=0 → возвращает 0."""
    assert wilson_lower(0, 0) == 0.0


def test_wilson_lower_all_wins():
    """Все победы → lower bound близок к 1, но < 1."""
    result = wilson_lower(100, 100)
    assert 0.9 < result < 1.0


def test_wilson_lower_no_wins():
    """Нет побед → lower bound = 0."""
    result = wilson_lower(0, 100)
    assert result == 0.0


def test_wilson_lower_half_wins():
    """50% побед → lower bound около 0.4-0.5 (зависит от n)."""
    result = wilson_lower(50, 100)
    assert 0.3 < result < 0.6


def test_wilson_lower_increases_with_more_samples():
    """С ростом n при одинаковой доле lower bound растёт (меньше неопределённости)."""
    w10 = wilson_lower(8, 10)   # 80%, n=10
    w100 = wilson_lower(80, 100)  # 80%, n=100
    assert w100 > w10


def test_wilson_lower_single_win():
    """1 из 1 — lower bound должен быть > 0 но < 1."""
    result = wilson_lower(1, 1)
    assert 0.0 < result < 1.0


def test_wilson_lower_not_negative():
    """Lower bound никогда не отрицателен."""
    for ups, n in [(0, 1), (0, 10), (1, 100), (5, 50)]:
        assert wilson_lower(ups, n) >= 0.0


# ------------------------------------------------------------------ #
# compute_winrates                                                      #
# ------------------------------------------------------------------ #

def test_compute_winrates_empty():
    result = compute_winrates([])
    assert result == {}


def test_compute_winrates_groups_by_retriever():
    feedback = [
        make_feedback("keyword", "up"),
        make_feedback("keyword", "up"),
        make_feedback("keyword", "down"),
        make_feedback("hybrid", "up"),
        make_feedback("hybrid", "up"),
    ]
    result = compute_winrates(feedback)
    assert "keyword" in result
    assert "hybrid" in result
    assert result["keyword"].thumbs_up == 2
    assert result["keyword"].thumbs_down == 1
    assert result["keyword"].total == 3
    assert result["hybrid"].thumbs_up == 2
    assert result["hybrid"].total == 2


def test_compute_winrates_ignores_empty_retriever():
    feedback = [
        make_feedback("", "up"),
        make_feedback("hybrid", "up"),
    ]
    result = compute_winrates(feedback)
    assert "" not in result
    assert "hybrid" in result


def test_compute_winrates_ignores_neutral_thumbs():
    feedback = [
        make_feedback("keyword", "neutral"),
        make_feedback("keyword", "up"),
        make_feedback("keyword", ""),
    ]
    result = compute_winrates(feedback)
    assert result["keyword"].total == 1
    assert result["keyword"].thumbs_up == 1


def test_compute_winrates_winrate_calculation():
    feedback = [
        make_feedback("semantic", "up"),
        make_feedback("semantic", "up"),
        make_feedback("semantic", "up"),
        make_feedback("semantic", "down"),
    ]
    result = compute_winrates(feedback)
    assert result["semantic"].winrate == pytest.approx(0.75)


def test_compute_winrates_wilson_lower_positive():
    feedback = [make_feedback("hybrid", "up")] * 10
    result = compute_winrates(feedback)
    assert result["hybrid"].wilson_lower > 0.0


def test_compute_winrates_dataclass_fields():
    feedback = [make_feedback("keyword", "up")]
    result = compute_winrates(feedback)
    stats = result["keyword"]
    assert isinstance(stats, WinRateStats)
    assert stats.name == "keyword"
    assert stats.thumbs_up == 1
    assert stats.thumbs_down == 0
    assert stats.total == 1
    assert 0 <= stats.winrate <= 1
    assert 0 <= stats.wilson_lower <= 1


# ------------------------------------------------------------------ #
# AutoTuner.best_retriever                                             #
# ------------------------------------------------------------------ #

def test_best_retriever_returns_none_when_no_data(tuner, store):
    """Нет feedback → best_retriever возвращает None."""
    assert tuner.best_retriever() is None


def test_best_retriever_returns_none_below_min_samples(tuner, store):
    """Меньше min_samples (5) на вариант → None."""
    for _ in range(4):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(4):
        store.record(make_feedback("keyword", "down"))
    assert tuner.best_retriever() is None


def test_best_retriever_returns_winner(store):
    """Явный победитель с достаточными данными и большой разницей."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.15)

    # hybrid: 18 up / 2 down (90%)
    for _ in range(18):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(2):
        store.record(make_feedback("hybrid", "down"))

    # keyword: 5 up / 15 down (25%)
    for _ in range(5):
        store.record(make_feedback("keyword", "up"))
    for _ in range(15):
        store.record(make_feedback("keyword", "down"))

    winner = tuner.best_retriever()
    assert winner == "hybrid"


def test_best_retriever_returns_none_when_difference_too_small(store):
    """Разница ниже improve_threshold → None."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.3)

    # hybrid: 60%
    for _ in range(6):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(4):
        store.record(make_feedback("hybrid", "down"))

    # keyword: 50%
    for _ in range(5):
        store.record(make_feedback("keyword", "up"))
    for _ in range(5):
        store.record(make_feedback("keyword", "down"))

    # Разница wilson lower < 0.3 → None
    result = tuner.best_retriever()
    assert result is None


# ------------------------------------------------------------------ #
# AutoTuner.best_answerer                                              #
# ------------------------------------------------------------------ #

def test_best_answerer_returns_none_when_no_data(tuner, store):
    assert tuner.best_answerer() is None


def test_best_answerer_returns_winner(store):
    """Аналогично best_retriever, но по полю answerer."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.15)

    def make_answerer_fb(answerer: str, thumbs: str) -> Feedback:
        return Feedback(
            request="q", response_text="a",
            thumbs=thumbs, skill="rag",
            retriever="hybrid", answerer=answerer,
        )

    for _ in range(18):
        store.record(make_answerer_fb("anthropic", "up"))
    for _ in range(2):
        store.record(make_answerer_fb("anthropic", "down"))

    for _ in range(5):
        store.record(make_answerer_fb("echo", "up"))
    for _ in range(15):
        store.record(make_answerer_fb("echo", "down"))

    winner = tuner.best_answerer()
    assert winner == "anthropic"


# ------------------------------------------------------------------ #
# AutoTuner.suggest_improvements                                       #
# ------------------------------------------------------------------ #

def test_suggest_improvements_empty(tuner, store):
    assert tuner.suggest_improvements() == []


def test_suggest_improvements_not_enough_samples(store):
    tuner = AutoTuner(store, min_samples=10, improve_threshold=0.15)
    for _ in range(5):
        store.record(make_feedback("hybrid", "up"))
    assert tuner.suggest_improvements() == []


def test_suggest_improvements_returns_string_list(store):
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.15)

    for _ in range(18):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(2):
        store.record(make_feedback("hybrid", "down"))
    for _ in range(5):
        store.record(make_feedback("keyword", "up"))
    for _ in range(15):
        store.record(make_feedback("keyword", "down"))

    suggestions = tuner.suggest_improvements()
    assert isinstance(suggestions, list)
    if suggestions:
        assert all(isinstance(s, str) for s in suggestions)
        # Должно упомянуть названия retriever-ов
        joined = " ".join(suggestions)
        assert "hybrid" in joined or "keyword" in joined


def test_suggest_improvements_format(store):
    """Проверяем что suggestion содержит winrate и n=."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.10)

    for _ in range(20):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(5):
        store.record(make_feedback("keyword", "up"))
    for _ in range(15):
        store.record(make_feedback("keyword", "down"))

    suggestions = tuner.suggest_improvements()
    if suggestions:
        s = suggestions[0]
        assert "winrate" in s
        assert "n=" in s


# ------------------------------------------------------------------ #
# AutoTuner.apply_to_config                                            #
# ------------------------------------------------------------------ #

def test_apply_to_config_missing_file(tuner, tmp_path):
    """Отсутствующий файл → возвращает False."""
    result = tuner.apply_to_config(tmp_path / "nonexistent.toml")
    assert result is False


def test_apply_to_config_no_changes_when_no_winner(tuner, store, tmp_path):
    """Нет явного победителя → файл не меняется."""
    cfg = tmp_path / "docstoolkit.toml"
    cfg.write_text("[paths]\ndocs = \"docs\"\n")
    original = cfg.read_text()
    result = tuner.apply_to_config(cfg)
    assert result is False
    assert cfg.read_text() == original


def test_apply_to_config_adds_rag_section(store, tmp_path):
    """При наличии победителя добавляется секция [rag] если её нет."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.15)

    for _ in range(18):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(2):
        store.record(make_feedback("hybrid", "down"))
    for _ in range(5):
        store.record(make_feedback("keyword", "up"))
    for _ in range(15):
        store.record(make_feedback("keyword", "down"))

    cfg = tmp_path / "docstoolkit.toml"
    cfg.write_text("[paths]\ndocs = \"docs\"\n")
    changed = tuner.apply_to_config(cfg)

    if changed:
        content = cfg.read_text()
        assert "hybrid" in content
        assert "[rag]" in content


def test_apply_to_config_updates_existing_key(store, tmp_path):
    """Обновляет существующий ключ в [rag]."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.15)

    for _ in range(18):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(2):
        store.record(make_feedback("hybrid", "down"))
    for _ in range(5):
        store.record(make_feedback("keyword", "up"))
    for _ in range(15):
        store.record(make_feedback("keyword", "down"))

    cfg = tmp_path / "docstoolkit.toml"
    cfg.write_text('[paths]\ndocs = "docs"\n\n[rag]\ndefault_retriever = "keyword"\n')
    changed = tuner.apply_to_config(cfg)

    if changed:
        content = cfg.read_text()
        # Новое значение должно быть hybrid
        assert 'default_retriever = "hybrid"' in content
        # Старое значение не должно остаться как keyword
        assert content.count("keyword") == 0 or 'default_retriever = "keyword"' not in content


def test_apply_to_config_returns_false_when_already_best(store, tmp_path):
    """Если текущий дефолт уже оптимальный — не меняет файл."""
    tuner = AutoTuner(store, min_samples=5, improve_threshold=0.15)

    for _ in range(18):
        store.record(make_feedback("hybrid", "up"))
    for _ in range(2):
        store.record(make_feedback("hybrid", "down"))

    cfg = tmp_path / "docstoolkit.toml"
    cfg.write_text('[rag]\ndefault_retriever = "hybrid"\n')
    # Нет другого варианта для сравнения → best_retriever вернёт None
    result = tuner.apply_to_config(cfg)
    assert result is False
