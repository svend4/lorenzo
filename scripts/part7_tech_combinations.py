"""Часть 7: обработка 'Комбинирование технологий для новых свойств - Claude' в docs/03-technology-combinations/."""
from part1_utils import ROOT, DOCS
from part5_mhtml_engine import extract_and_split

MHTML = ROOT / "Комбинирование технологий для новых свойств - Claude"

KEYWORDS = {
    "методолог": ("README.md", "Методология комбинирования технологий"),
    "роутинг": ("01-agent-routing.md", "Агентные системы и роутинг"),
    "самоулучш": ("01-agent-routing.md", "Агентные системы и роутинг"),
    "граф знан": ("02-knowledge-graphs.md", "Графы знаний и Legal AI"),
    "правов": ("02-knowledge-graphs.md", "Графы знаний и Legal AI"),
    "локальн": ("03-local-first.md", "Local-first и P2P стек"),
    "Sozialrecht": ("04-sozialrecht-domain.md", "Домен: немецкое социальное право"),
    "немецк": ("04-sozialrecht-domain.md", "Домен: немецкое социальное право"),
    "бенчмарк": ("05-benchmarks.md", "Бенчмарки и производительность"),
    "производительн": ("05-benchmarks.md", "Бенчмарки и производительность"),
}


def run():
    out = DOCS / "03-technology-combinations"
    print(f"\n--- Technology Combinations ---")
    extract_and_split(MHTML, KEYWORDS, out)


if __name__ == '__main__':
    run()
