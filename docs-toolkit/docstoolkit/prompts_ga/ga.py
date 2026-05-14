"""Genetic algorithm for evolving prompt templates."""
import random
from dataclasses import dataclass, field
from typing import Callable

from docstoolkit.prompts_ga.operators import mutate, crossover
from docstoolkit.prompts_ga.fitness import FitnessCache, evaluate_population


@dataclass
class GAConfig:
    population_size: int = 20
    generations: int = 15
    mutation_rate: float = 0.3
    crossover_rate: float = 0.5
    elite_count: int = 4
    tournament_size: int = 3
    seed: int | None = None


@dataclass
class GenerationStats:
    generation: int
    best_fitness: float
    mean_fitness: float
    worst_fitness: float
    best_template: str


class PromptGA:
    """Genetic algorithm for evolving prompt templates.

    fitness_fn: callable that takes a template string and returns float in [0,1].
    Can be anything — mock for tests, real eval for production.
    """

    def __init__(
        self,
        seed_templates: list[str],       # initial population seeds
        fitness_fn: Callable[[str], float],
        config: GAConfig | None = None,
    ):
        self._cfg = config or GAConfig()
        self._fitness_fn = fitness_fn
        self._cache = FitnessCache()
        self._rng = random.Random(self._cfg.seed)
        self._history: list[GenerationStats] = []

        # Initialize population: use seeds, pad/trim to population_size
        self._population = self._init_population(seed_templates)

    def _init_population(self, seeds: list[str]) -> list[str]:
        """Build initial population from seeds.

        If fewer seeds than population_size: add mutations of seeds.
        If more: truncate.
        """
        pop = list(seeds[:self._cfg.population_size])
        while len(pop) < self._cfg.population_size:
            # Add mutations of seeds to fill population
            seed = self._rng.choice(seeds) if seeds else "Provide a helpful response."
            pop.append(mutate(seed, rng=self._rng))
        return pop

    def _tournament_select(self, population: list[str], fitnesses: list[float]) -> str:
        """Tournament selection: pick tournament_size random candidates, return best."""
        size = min(self._cfg.tournament_size, len(population))
        indices = self._rng.sample(range(len(population)), size)
        best_idx = max(indices, key=lambda i: fitnesses[i])
        return population[best_idx]

    def step(self) -> GenerationStats:
        """Run one generation. Returns stats for this generation."""
        # 1. Evaluate fitness for all
        fitnesses = evaluate_population(self._population, self._fitness_fn, self._cache)

        # 2. Sort by fitness descending
        paired = sorted(zip(fitnesses, self._population), key=lambda x: x[0], reverse=True)
        sorted_fitnesses = [f for f, _ in paired]
        sorted_pop = [t for _, t in paired]

        # 3. Keep elite_count elites
        elite_count = min(self._cfg.elite_count, len(sorted_pop))
        new_pop = list(sorted_pop[:elite_count])

        # 4. Fill rest with crossover + mutation offspring
        while len(new_pop) < self._cfg.population_size:
            if self._rng.random() < self._cfg.crossover_rate and len(sorted_pop) >= 2:
                parent_a = self._tournament_select(sorted_pop, sorted_fitnesses)
                parent_b = self._tournament_select(sorted_pop, sorted_fitnesses)
                child_a, child_b = crossover(parent_a, parent_b, rng=self._rng)
                # Pick one child to add
                child = self._rng.choice([child_a, child_b])
            else:
                child = self._tournament_select(sorted_pop, sorted_fitnesses)

            if self._rng.random() < self._cfg.mutation_rate:
                child = mutate(child, rng=self._rng)

            new_pop.append(child)

        # 5. Update population
        self._population = new_pop[:self._cfg.population_size]

        # Compute stats
        best_fitness = sorted_fitnesses[0]
        worst_fitness = sorted_fitnesses[-1]
        mean_fitness = sum(sorted_fitnesses) / len(sorted_fitnesses) if sorted_fitnesses else 0.0
        best_template = sorted_pop[0]

        gen_num = len(self._history) + 1
        stats = GenerationStats(
            generation=gen_num,
            best_fitness=best_fitness,
            mean_fitness=mean_fitness,
            worst_fitness=worst_fitness,
            best_template=best_template,
        )
        self._history.append(stats)
        return stats

    def evolve(self) -> list[tuple[str, float]]:
        """Run all generations. Returns [(template, fitness)] sorted best→worst."""
        for _ in range(self._cfg.generations):
            self.step()

        # Final evaluation of current population
        fitnesses = evaluate_population(self._population, self._fitness_fn, self._cache)
        result = sorted(zip(self._population, fitnesses), key=lambda x: x[1], reverse=True)
        return list(result)

    def best(self) -> str:
        """Return best template found so far."""
        if self._history:
            return self._history[-1].best_template
        # No generations run yet — evaluate initial population
        fitnesses = evaluate_population(self._population, self._fitness_fn, self._cache)
        best_idx = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
        return self._population[best_idx]

    def history(self) -> list[GenerationStats]:
        """Return per-generation stats."""
        return list(self._history)
