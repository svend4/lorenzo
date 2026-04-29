"""Часть 6: обработка 'Вакансии в Anthropic по кластерам - Claude' в docs/02-anthropic-vacancies/."""
from part1_utils import ROOT, DOCS
from part5_mhtml_engine import extract_and_split

MHTML = ROOT / "Вакансии в Anthropic по кластерам - Claude"

KEYWORDS = {
    "Research & ML": ("clusters/01-research-ml.md", "Research & ML Engineering"),
    "Go-To-Market": ("clusters/02-gtm-sales.md", "GTM и Sales"),
    "Finance": ("clusters/03-finance-operations.md", "Finance & Operations"),
    "Security": ("clusters/04-security-compliance.md", "Security & Compliance"),
    "Product Marketing": ("clusters/05-product-marketing.md", "Product Marketing"),
    "Product Engineering": ("clusters/06-product-engineering.md", "Product Engineering"),
    "Inference": ("clusters/07-inference-infrastructure.md", "Inference & Infrastructure"),
    "Trust & Safety": ("clusters/08-trust-safety.md", "Trust & Safety"),
    "Product Management": ("clusters/09-product-management.md", "Product Management"),
    "Data Center": ("clusters/10-datacenter-hardware.md", "Data Center & Hardware"),
    "Legal": ("clusters/11-legal.md", "Legal & Compliance"),
    "Human Resources": ("clusters/12-hr.md", "Human Resources"),
    "карьер": ("13-career-mapping.md", "Карьерный маппинг для svend4"),
    "стратег": ("01-market-overview.md", "Обзор рынка и стратегические сигналы"),
}


def run():
    out = DOCS / "02-anthropic-vacancies"
    print(f"\n--- Anthropic Vacancies ---")
    extract_and_split(MHTML, KEYWORDS, out)


if __name__ == '__main__':
    run()
