"""Авто-тюнинг: применяет feedback для замены retriever/answerer/prompt с лучшим winrate.

Читает FeedbackStore, вычисляет Wilson confidence interval по retriever/answerer,
и предлагает (или автоматически применяет) переключение на вариант с лучшим winrate.

Использование:
    from docstoolkit.feedback.autotuner import AutoTuner
    from docstoolkit.feedback import FeedbackStore

    store = FeedbackStore()
    tuner = AutoTuner(store, min_samples=20, improve_threshold=0.15)

    # Подсказки для ручного применения
    for suggestion in tuner.suggest_improvements():
        print(suggestion)

    # Авто-обновление конфига
    changed = tuner.apply_to_config(Path("docstoolkit.toml"))
"""
import math
import tomllib
from dataclasses import dataclass
from pathlib import Path

from docstoolkit.feedback.store import Feedback, FeedbackStore


@dataclass
class WinRateStats:
    """Статистика побед для одного варианта (retriever или answerer)."""
    name: str
    thumbs_up: int
    thumbs_down: int
    total: int           # total с thumbs up/down (не нейтральные)
    winrate: float       # thumbs_up / total  (0 если total==0)
    wilson_lower: float  # Wilson lower bound (95%)


def wilson_lower(ups: int, n: int, z: float = 1.96) -> float:
    """Wilson confidence interval lower bound.

    Формула:
        (p̂ + z²/2n − z·√(p̂(1−p̂)/n + z²/4n²)) / (1 + z²/n)

    Возвращает 0 если n == 0.
    """
    if n == 0:
        return 0.0
    p = ups / n
    z2 = z * z
    center = (p + z2 / (2 * n)) / (1 + z2 / n)
    margin = (z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) / (1 + z2 / n)
    return max(0.0, center - margin)


def compute_winrates(feedback_list: list[Feedback]) -> dict[str, WinRateStats]:
    """Сгруппировать отзывы по полю `retriever` и вычислить статистику.

    Считаются только записи с thumbs in {'up', 'down'}.
    Записи с пустым retriever игнорируются.
    """
    buckets: dict[str, dict] = {}

    for fb in feedback_list:
        name = fb.retriever
        if not name:
            continue
        if fb.thumbs not in ("up", "down"):
            continue
        if name not in buckets:
            buckets[name] = {"up": 0, "down": 0}
        if fb.thumbs == "up":
            buckets[name]["up"] += 1
        else:
            buckets[name]["down"] += 1

    result: dict[str, WinRateStats] = {}
    for name, counts in buckets.items():
        up = counts["up"]
        down = counts["down"]
        total = up + down
        wr = up / total if total else 0.0
        wl = wilson_lower(up, total)
        result[name] = WinRateStats(
            name=name,
            thumbs_up=up,
            thumbs_down=down,
            total=total,
            winrate=wr,
            wilson_lower=wl,
        )
    return result


def _compute_winrates_by_field(
    feedback_list: list[Feedback], field: str
) -> dict[str, WinRateStats]:
    """Обобщённая версия compute_winrates для произвольного поля."""
    buckets: dict[str, dict] = {}

    for fb in feedback_list:
        name = getattr(fb, field, "") or ""
        if not name:
            continue
        if fb.thumbs not in ("up", "down"):
            continue
        if name not in buckets:
            buckets[name] = {"up": 0, "down": 0}
        if fb.thumbs == "up":
            buckets[name]["up"] += 1
        else:
            buckets[name]["down"] += 1

    result: dict[str, WinRateStats] = {}
    for name, counts in buckets.items():
        up = counts["up"]
        down = counts["down"]
        total = up + down
        wr = up / total if total else 0.0
        wl = wilson_lower(up, total)
        result[name] = WinRateStats(
            name=name,
            thumbs_up=up,
            thumbs_down=down,
            total=total,
            winrate=wr,
            wilson_lower=wl,
        )
    return result


class AutoTuner:
    """Анализирует feedback и предлагает лучший retriever/answerer.

    Критерий переключения:
      - лучший вариант имеет >= min_samples записей с thumbs up/down
      - его wilson_lower превышает wilson_lower текущего дефолта
        минимум на improve_threshold (0.15 = 15 п.п.)
    """

    def __init__(
        self,
        store: FeedbackStore,
        min_samples: int = 20,
        improve_threshold: float = 0.15,
    ):
        self.store = store
        self.min_samples = min_samples
        self.improve_threshold = improve_threshold

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _all_feedback(self) -> list[Feedback]:
        """Читаем весь feedback без лимита."""
        return self.store.list_recent(limit=100_000)

    def _best_variant(
        self, field: str, current_default: str | None = None
    ) -> str | None:
        """Найти вариант с максимальным wilson_lower среди тех, кто удовлетворяет min_samples.

        Возвращает имя варианта, только если он строго лучше current_default
        на improve_threshold. Если current_default не передан — берём вариант
        с наименьшим wilson_lower как «текущий».
        """
        stats = _compute_winrates_by_field(self._all_feedback(), field)
        qualified = {
            name: s for name, s in stats.items()
            if s.total >= self.min_samples
        }
        if not qualified:
            return None

        best_name = max(qualified, key=lambda n: qualified[n].wilson_lower)
        best = qualified[best_name]

        # Определяем текущий дефолт
        if current_default and current_default in stats:
            current_wl = stats[current_default].wilson_lower
        else:
            # Фоллбэк: минимальный wilson_lower среди квалифицированных
            current_wl = min(s.wilson_lower for s in qualified.values())

        if best.wilson_lower > current_wl + self.improve_threshold:
            return best_name
        return None

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def best_retriever(self) -> str | None:
        """Возвращает имя retriever с наивысшим wilson_lower, если он заметно лучше.

        Возвращает None если нет явного победителя или недостаточно данных.
        """
        return self._best_variant("retriever")

    def best_answerer(self) -> str | None:
        """То же самое для поля answerer."""
        return self._best_variant("answerer")

    def suggest_improvements(self) -> list[str]:
        """Список человекочитаемых рекомендаций на основе feedback.

        Формат: "Переключить <field>: <old> → <new> (winrate X.XX vs Y.YY, n=NN)"
        """
        suggestions: list[str] = []
        feedback = self._all_feedback()

        for field in ("retriever", "answerer"):
            stats = _compute_winrates_by_field(feedback, field)
            qualified = {
                name: s for name, s in stats.items()
                if s.total >= self.min_samples
            }
            if len(qualified) < 2:
                continue

            sorted_variants = sorted(
                qualified.values(), key=lambda s: s.wilson_lower, reverse=True
            )
            best = sorted_variants[0]
            worst = sorted_variants[-1]

            if best.wilson_lower > worst.wilson_lower + self.improve_threshold:
                suggestions.append(
                    f"Переключить {field}: {worst.name} → {best.name} "
                    f"(winrate {best.winrate:.2f} vs {worst.winrate:.2f}, "
                    f"n={best.total})"
                )

        return suggestions

    def apply_to_config(self, cfg_path: Path) -> bool:
        """Обновить docstoolkit.toml: [rag] default_retriever / default_answerer.

        Читает текущий файл как текст, модифицирует нужные ключи, записывает обратно.
        Возвращает True если файл был изменён.
        """
        cfg_path = Path(cfg_path)
        if not cfg_path.exists():
            return False

        with cfg_path.open("rb") as f:
            cfg = tomllib.load(f)

        current_retriever = cfg.get("rag", {}).get("default_retriever", "")
        current_answerer = cfg.get("rag", {}).get("default_answerer", "")

        new_retriever = self._best_variant("retriever", current_retriever or None)
        new_answerer = self._best_variant("answerer", current_answerer or None)

        if not new_retriever and not new_answerer:
            return False

        # Читаем файл как текст для минимального diff (tomllib не умеет писать)
        text = cfg_path.read_text(encoding="utf-8")
        changed = False

        if new_retriever:
            text, changed_r = _update_toml_key(
                text, "rag", "default_retriever", new_retriever
            )
            changed = changed or changed_r

        if new_answerer:
            text, changed_a = _update_toml_key(
                text, "rag", "default_answerer", new_answerer
            )
            changed = changed or changed_a

        if changed:
            cfg_path.write_text(text, encoding="utf-8")

        return changed


# ------------------------------------------------------------------ #
# TOML writer helpers (stdlib-only, minimal implementation)           #
# ------------------------------------------------------------------ #

def _update_toml_key(
    text: str, section: str, key: str, value: str
) -> tuple[str, bool]:
    """Обновить или добавить ключ в TOML-секции.

    Возвращает (новый текст, изменён ли).
    Работает на уровне строк — не использует сторонних библиотек.
    """
    lines = text.splitlines(keepends=True)
    in_section = False
    key_found = False
    section_line = -1

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Вход в нашу секцию
        if stripped == f"[{section}]":
            in_section = True
            section_line = i
            continue
        # Выход из секции при следующем [...]
        if in_section and stripped.startswith("[") and not stripped.startswith("[#"):
            in_section = False

        if in_section and stripped.startswith(f"{key}"):
            # Проверяем что это именно этот ключ (= или пробел после имени)
            rest = stripped[len(key):]
            if rest and rest[0] in (" ", "\t", "="):
                new_line = f'{key} = "{value}"\n'
                if lines[i] == new_line:
                    return text, False
                lines[i] = new_line
                key_found = True
                break

    if not key_found:
        # Добавляем секцию или ключ
        if section_line == -1:
            # Секции нет — добавляем в конец
            if not text.endswith("\n"):
                lines.append("\n")
            lines.append(f"\n[{section}]\n")
            lines.append(f'{key} = "{value}"\n')
        else:
            # Секция есть, вставляем после заголовка секции
            lines.insert(section_line + 1, f'{key} = "{value}"\n')

    return "".join(lines), True
