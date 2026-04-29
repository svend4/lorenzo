"""Часть 8: AI коллаборации и Хабр-проекты."""
from part1_utils import ROOT, DOCS
from part5_mhtml_engine import extract_and_split

# --- docs/04-ai-collaborations/ ---
COLLAB_MHTML = ROOT / "Поиск коллабораций AI проектов"

COLLAB_KEYWORDS = {
    "ансамбл": ("01-overview.md", "Обзор ансамблей AI-проектов"),
    "knowledge": ("ensembles/01-knowledge-os.md", "Ансамбль: Knowledge OS"),
    "Svyazi": ("ensembles/01-knowledge-os.md", "Ансамбль: Knowledge OS"),
    "AgentFS": ("ensembles/01-knowledge-os.md", "Ансамбль: Knowledge OS"),
    "forensic": ("ensembles/02-forensic-rag.md", "Ансамбль: Forensic RAG"),
    "LiteParse": ("ensembles/02-forensic-rag.md", "Ансамбль: Forensic RAG"),
    "Rufler": ("ensembles/03-agent-teams.md", "Ансамбль: Agent Teams"),
    "AI Factory": ("ensembles/03-agent-teams.md", "Ансамбль: Agent Teams"),
    "SENTINEL": ("ensembles/04-security-runtime.md", "Ансамбль: Security Runtime"),
    "Firecrawl": ("ensembles/05-web-intelligence.md", "Ансамбль: Web Intelligence"),
    "CRDT": ("02-architecture-patterns.md", "Архитектурные паттерны"),
    "MVP": ("03-roadmap.md", "Дорожная карта MVP"),
}

# --- docs/05-habr-projects/ ---
HABR_MHTML = ROOT / "Поиск уникальных проектов на Хабре для совместной разработки - Claude"

HABR_KEYWORDS = {
    "методолог": ("README.md", "Методология поиска проектов на Хабре"),
    "Yodoca": ("memory/yodoca.md", "Yodoca: консолидация и забывание"),
    "консолид": ("memory/yodoca.md", "Yodoca: консолидация и забывание"),
    "NGT": ("memory/ngt-memory.md", "NGT Memory: ассоциативный граф"),
    "ассоциат": ("memory/ngt-memory.md", "NGT Memory: ассоциативный граф"),
    "MemNet": ("memory/memnet.md", "MemNet: исследовательская память"),
    "agent-memory-mcp": ("memory/agent-memory-mcp.md", "agent-memory-mcp"),
    "knowledge-space": ("knowledge/knowledge-space.md", "knowledge-space: 785+ карточек"),
    "агентных карт": ("knowledge/knowledge-space.md", "knowledge-space: 785+ карточек"),
    "AgentFS": ("knowledge/agentfs.md", "AgentFS: Obsidian vault для агентов"),
    ".agentos": ("knowledge/agentfs.md", "AgentFS: Obsidian vault для агентов"),
    "Wikontic": ("knowledge/wikontic.md", "Wikontic: семантический граф"),
    "синтез": ("01-synthesis.md", "Синтез: как проекты собираются вместе"),
    "коллаборац": ("02-collaboration-partners.md", "Авторы и контакты"),
    "автор": ("02-collaboration-partners.md", "Авторы и контакты"),
}


def run():
    print("\n--- AI Collaborations ---")
    extract_and_split(COLLAB_MHTML, COLLAB_KEYWORDS, DOCS / "04-ai-collaborations")

    print("\n--- Habr Projects ---")
    extract_and_split(HABR_MHTML, HABR_KEYWORDS, DOCS / "05-habr-projects")


if __name__ == '__main__':
    run()
