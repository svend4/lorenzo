"""Tests for docstoolkit.prompts_ga — genetic algorithm prompt evolution."""
import random
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.prompts_ga import (
    mutate, crossover, MutationOp,
    FitnessCache, evaluate_population,
    GAConfig, GenerationStats, PromptGA,
)
from docstoolkit.prompts_ga.operators import _split_sentences, _join_sentences


# ---------------------------------------------------------------------------
# MutationOp enum
# ---------------------------------------------------------------------------

def test_mutation_op_all_values():
    values = {op.value for op in MutationOp}
    assert values == {"rephrase", "inject", "remove", "reorder"}


def test_mutation_op_four_members():
    assert len(MutationOp) == 4


# ---------------------------------------------------------------------------
# _split_sentences / _join_sentences
# ---------------------------------------------------------------------------

def test_split_sentences_single():
    result = _split_sentences("Hello world.")
    assert result == ["Hello world."]


def test_split_sentences_multi():
    text = "First sentence. Second sentence. Third sentence."
    parts = _split_sentences(text)
    assert len(parts) == 3


def test_split_sentences_with_exclamation():
    parts = _split_sentences("Hello! World.")
    assert len(parts) == 2


def test_split_sentences_question():
    parts = _split_sentences("What is this? It is a test.")
    assert len(parts) == 2


def test_join_sentences_single():
    result = _join_sentences(["Hello world."])
    assert result == "Hello world."


def test_join_sentences_multi():
    result = _join_sentences(["First.", "Second.", "Third."])
    # Should be joined
    assert "First" in result
    assert "Second" in result
    assert "Third" in result


def test_round_trip_split_join():
    text = "First sentence. Second sentence. Third sentence."
    parts = _split_sentences(text)
    rejoined = _join_sentences(parts)
    # All original words should be present
    for word in ["First", "Second", "Third"]:
        assert word in rejoined


def test_join_strips_trailing_whitespace():
    result = _join_sentences(["Hello", "World"])
    assert result == result.strip()


# ---------------------------------------------------------------------------
# mutate
# ---------------------------------------------------------------------------

def test_mutate_returns_nonempty_string():
    result = mutate("This is a test sentence.")
    assert isinstance(result, str)
    assert len(result) > 0


def test_mutate_inject_longer_than_input():
    rng = random.Random(42)
    template = "Be helpful."
    result = mutate(template, op=MutationOp.INJECT, rng=rng)
    assert len(result) > len(template)


def test_mutate_remove_multi_sentence():
    rng = random.Random(42)
    template = "First sentence. Second sentence. Third sentence."
    result = mutate(template, op=MutationOp.REMOVE, rng=rng)
    original_parts = _split_sentences(template)
    result_parts = _split_sentences(result)
    assert len(result_parts) < len(original_parts)


def test_mutate_reorder_same_sentences_different_order():
    rng = random.Random(1)
    template = "Alpha sentence. Beta sentence. Gamma sentence."
    original_parts = set(_split_sentences(template))
    result = mutate(template, op=MutationOp.REORDER, rng=rng)
    result_parts = set(_split_sentences(result))
    # Same sentences, possibly different order
    assert original_parts == result_parts


def test_mutate_rephrase_returns_string():
    rng = random.Random(42)
    result = mutate("Use this information. Return the answer.", op=MutationOp.REPHRASE, rng=rng)
    assert isinstance(result, str)
    assert len(result) > 0


def test_mutate_single_sentence_remove_fallback():
    rng = random.Random(42)
    template = "Only one sentence."
    # Should not crash, returns non-empty
    result = mutate(template, op=MutationOp.REMOVE, rng=rng)
    assert isinstance(result, str)
    assert len(result) > 0


def test_mutate_single_sentence_reorder_fallback():
    rng = random.Random(42)
    template = "Only one sentence."
    result = mutate(template, op=MutationOp.REORDER, rng=rng)
    assert isinstance(result, str)
    assert len(result) > 0


def test_mutate_random_op_no_crash():
    rng = random.Random(99)
    template = "This is a test. With two sentences."
    result = mutate(template, op=None, rng=rng)
    assert isinstance(result, str)
    assert len(result) > 0


def test_mutate_deterministic_with_seed():
    template = "First sentence. Second sentence. Third sentence."
    result1 = mutate(template, rng=random.Random(7))
    result2 = mutate(template, rng=random.Random(7))
    assert result1 == result2


def test_mutate_inject_adds_known_phrase():
    from docstoolkit.prompts_ga.operators import _INJECT_PHRASES
    rng = random.Random(42)
    template = "Be helpful."
    result = mutate(template, op=MutationOp.INJECT, rng=rng)
    # Result should contain one of the inject phrases
    assert any(phrase in result for phrase in _INJECT_PHRASES)


# ---------------------------------------------------------------------------
# crossover
# ---------------------------------------------------------------------------

def test_crossover_returns_tuple_of_two():
    result = crossover("A. B. C.", "D. E. F.")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_crossover_both_nonempty():
    c1, c2 = crossover("A sentence. B sentence.", "C sentence. D sentence.")
    assert len(c1) > 0
    assert len(c2) > 0


def test_crossover_single_sentence_parents_unchanged():
    a = "Only one sentence."
    b = "Another single sentence."
    c1, c2 = crossover(a, b)
    assert c1 == a
    assert c2 == b


def test_crossover_multi_sentence_children_differ_from_parents():
    rng = random.Random(42)
    a = "Alpha. Beta. Gamma."
    b = "Delta. Epsilon. Zeta."
    c1, c2 = crossover(a, b, rng=rng)
    # At least one child should differ from both parents
    assert c1 != a or c2 != b


def test_crossover_sentences_from_parents_in_children():
    rng = random.Random(42)
    a = "Alpha sentence. Beta sentence. Gamma sentence."
    b = "Delta sentence. Epsilon sentence. Zeta sentence."
    c1, c2 = crossover(a, b, rng=rng)
    # Children should contain sentences from parents
    all_sentences = set(_split_sentences(a)) | set(_split_sentences(b))
    child1_sentences = set(_split_sentences(c1))
    child2_sentences = set(_split_sentences(c2))
    assert child1_sentences.issubset(all_sentences)
    assert child2_sentences.issubset(all_sentences)


def test_crossover_deterministic_with_seed():
    a = "Alpha. Beta. Gamma."
    b = "Delta. Epsilon. Zeta."
    r1 = crossover(a, b, rng=random.Random(10))
    r2 = crossover(a, b, rng=random.Random(10))
    assert r1 == r2


# ---------------------------------------------------------------------------
# FitnessCache
# ---------------------------------------------------------------------------

def test_fitness_cache_get_unknown_returns_none():
    cache = FitnessCache()
    assert cache.get("unknown template") is None


def test_fitness_cache_set_get_roundtrip():
    cache = FitnessCache()
    cache.set("my template", 0.75)
    assert cache.get("my template") == 0.75


def test_fitness_cache_size_property():
    cache = FitnessCache()
    assert cache.size == 0
    cache.set("t1", 0.5)
    assert cache.size == 1
    cache.set("t2", 0.8)
    assert cache.size == 2


def test_fitness_cache_same_template_same_hash():
    cache = FitnessCache()
    h1 = cache._hash("hello world")
    h2 = cache._hash("hello world")
    assert h1 == h2


def test_fitness_cache_different_templates_different_hash():
    cache = FitnessCache()
    h1 = cache._hash("template one")
    h2 = cache._hash("template two")
    assert h1 != h2


def test_fitness_cache_overwrite():
    cache = FitnessCache()
    cache.set("t", 0.3)
    cache.set("t", 0.9)
    assert cache.get("t") == 0.9


# ---------------------------------------------------------------------------
# evaluate_population
# ---------------------------------------------------------------------------

def test_evaluate_population_same_length():
    templates = ["a", "b", "c"]
    scores = evaluate_population(templates, fitness_fn=lambda t: 0.5)
    assert len(scores) == len(templates)


def test_evaluate_population_values_from_fitness_fn():
    templates = ["short", "longer template", "a"]
    scores = evaluate_population(templates, fitness_fn=lambda t: len(t) / 100.0)
    assert scores[0] == pytest.approx(len("short") / 100.0)
    assert scores[1] == pytest.approx(len("longer template") / 100.0)


def test_evaluate_population_cache_hit_avoids_fn_call():
    cache = FitnessCache()
    mock_fn = MagicMock(return_value=0.7)
    templates = ["template one", "template two"]

    # First call populates cache
    evaluate_population(templates, fitness_fn=mock_fn, cache=cache)
    assert mock_fn.call_count == 2

    # Second call with same templates should use cache
    mock_fn.reset_mock()
    evaluate_population(templates, fitness_fn=mock_fn, cache=cache)
    assert mock_fn.call_count == 0  # All hits from cache


def test_evaluate_population_without_cache_always_calls_fn():
    mock_fn = MagicMock(return_value=0.5)
    templates = ["a", "b"]
    evaluate_population(templates, fitness_fn=mock_fn)
    evaluate_population(templates, fitness_fn=mock_fn)
    assert mock_fn.call_count == 4  # called each time, no cache


def test_evaluate_population_empty():
    scores = evaluate_population([], fitness_fn=lambda t: 1.0)
    assert scores == []


# ---------------------------------------------------------------------------
# PromptGA
# ---------------------------------------------------------------------------

def test_prompts_ga_init_pads_population_when_fewer_seeds():
    seeds = ["Short prompt. Be helpful."]
    cfg = GAConfig(population_size=5, seed=42)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    assert len(ga._population) == 5


def test_prompts_ga_init_truncates_when_more_seeds():
    seeds = [f"Prompt number {i}. Be detailed." for i in range(20)]
    cfg = GAConfig(population_size=5, seed=42)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    assert len(ga._population) == 5


def test_prompts_ga_best_returns_string():
    seeds = ["Be concise. Answer clearly."]
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=GAConfig(seed=0))
    result = ga.best()
    assert isinstance(result, str)
    assert len(result) > 0


def test_prompts_ga_history_initially_empty():
    seeds = ["First sentence. Second sentence."]
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=GAConfig(seed=0))
    assert ga.history() == []


def test_prompts_ga_history_grows_after_evolve():
    seeds = ["First sentence. Second sentence."]
    cfg = GAConfig(population_size=4, generations=3, seed=0)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    ga.evolve()
    assert len(ga.history()) == 3


def test_prompts_ga_step_returns_generation_stats():
    seeds = ["Alpha sentence. Beta sentence."]
    cfg = GAConfig(population_size=4, seed=1)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    stats = ga.step()
    assert isinstance(stats, GenerationStats)
    assert stats.generation == 1
    assert isinstance(stats.best_fitness, float)
    assert isinstance(stats.mean_fitness, float)
    assert isinstance(stats.worst_fitness, float)
    assert isinstance(stats.best_template, str)


def test_generation_stats_ordering():
    seeds = ["Alpha. Beta. Gamma.", "Short.", "Longer template sentence here."]
    cfg = GAConfig(population_size=6, seed=2)

    def fitness_fn(t: str) -> float:
        return len(t) / 1000.0

    ga = PromptGA(seeds, fitness_fn=fitness_fn, config=cfg)
    stats = ga.step()
    assert stats.best_fitness >= stats.mean_fitness - 1e-9
    assert stats.mean_fitness >= stats.worst_fitness - 1e-9


def test_prompts_ga_evolve_returns_sorted_tuples():
    seeds = ["Alpha. Beta.", "Gamma. Delta. Epsilon."]
    cfg = GAConfig(population_size=4, generations=2, seed=3)

    def fitness_fn(t: str) -> float:
        return len(t) / 1000.0

    ga = PromptGA(seeds, fitness_fn=fitness_fn, config=cfg)
    result = ga.evolve()
    assert isinstance(result, list)
    assert all(isinstance(r, tuple) and len(r) == 2 for r in result)
    # Sorted descending
    scores = [s for _, s in result]
    assert scores == sorted(scores, reverse=True)


def test_prompts_ga_evolve_length_equals_population_size():
    seeds = ["Alpha. Beta."]
    cfg = GAConfig(population_size=6, generations=2, seed=4)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    result = ga.evolve()
    assert len(result) == 6


def test_prompts_ga_elitism_best_fitness_nondecreasing():
    seeds = ["Alpha. Beta. Gamma.", "Short.", "Medium length template.", "Another one."]
    cfg = GAConfig(population_size=6, generations=5, elite_count=2, seed=5)

    call_count = [0]

    def fitness_fn(t: str) -> float:
        call_count[0] += 1
        return len(t) / 200.0

    ga = PromptGA(seeds, fitness_fn=fitness_fn, config=cfg)
    ga.evolve()
    hist = ga.history()

    best_scores = [s.best_fitness for s in hist]
    for i in range(1, len(best_scores)):
        assert best_scores[i] >= best_scores[i - 1] - 1e-9, (
            f"Best fitness decreased at generation {i+1}: "
            f"{best_scores[i-1]} -> {best_scores[i]}"
        )


def test_prompts_ga_longer_templates_preferred():
    """With fitness = len(template), evolved templates should grow."""
    seeds = ["Short text. Simple.", "Another short one."]
    cfg = GAConfig(population_size=6, generations=5, mutation_rate=0.8, seed=42)

    def fitness_fn(t: str) -> float:
        return len(t) / 500.0

    ga = PromptGA(seeds, fitness_fn=fitness_fn, config=cfg)
    initial_best_len = max(len(s) for s in seeds)
    result = ga.evolve()
    final_best_len = len(result[0][0])
    # With INJECT mutations the best should get longer
    assert final_best_len >= initial_best_len


def test_prompts_ga_fitness_cache_used():
    seeds = ["Alpha sentence. Beta sentence.", "Gamma sentence. Delta sentence."]
    cfg = GAConfig(population_size=4, generations=3, seed=7)
    mock_fn = MagicMock(side_effect=lambda t: len(t) / 200.0)
    ga = PromptGA(seeds, fitness_fn=mock_fn, config=cfg)
    ga.evolve()
    first_run_calls = mock_fn.call_count

    # Run again — some templates cached from first run
    mock_fn.reset_mock()
    ga2 = PromptGA(seeds, fitness_fn=mock_fn, config=cfg)
    # Cache is per-instance, but the same seeds won't be re-evaluated
    # in the same GA run (confirmed by cache hits within evolve)
    ga2.evolve()
    # Both runs should have evaluated all their unique templates
    assert ga2._cache.size > 0  # Cache was populated


def test_gaconfig_defaults():
    cfg = GAConfig()
    assert cfg.population_size == 20
    assert cfg.generations == 15
    assert cfg.mutation_rate == pytest.approx(0.3)
    assert cfg.crossover_rate == pytest.approx(0.5)
    assert cfg.elite_count == 4
    assert cfg.tournament_size == 3
    assert cfg.seed is None


def test_prompts_ga_step_increments_generation_number():
    seeds = ["Step test. More content."]
    cfg = GAConfig(population_size=4, seed=9)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    s1 = ga.step()
    s2 = ga.step()
    assert s1.generation == 1
    assert s2.generation == 2


def test_prompts_ga_population_stays_at_size_after_steps():
    seeds = ["Alpha. Beta.", "Gamma. Delta."]
    cfg = GAConfig(population_size=5, seed=11)
    ga = PromptGA(seeds, fitness_fn=lambda t: 0.5, config=cfg)
    for _ in range(3):
        ga.step()
    assert len(ga._population) == 5
