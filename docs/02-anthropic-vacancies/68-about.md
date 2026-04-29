# 🇬🇧 About

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Documentation - PORTAL-PROTOCOL.md(./PORTAL-PROTOCOL.md) — formal v1.0 specification (15 pages) - passports/(./passports/) — human-readable repo descriptions - info1(./passports/in
> 🔧 **Подход:** - 0: Discoverable — declared in registry only - 1: Readable — has passport + describe() method - 2: Queryable — implements fetch(query) — search works - 3: Interactive — translatet
> ✅ **Результат:** Reports always show attribution — which repo each result came from.
> 🏷️ **Ключевые слова:** `nautilus`, `portal`, `protocol`, `reference`, `https`, `anthropic`, `svend`, `passports`
>


<!-- summary -->
> Nautilus is a **federation protocol** and reference implementation

---

<!-- toc -->
## Содержание

- [🇬🇧 About](#about)
  - [Philosophy](#philosophy)
  - [Reference Ecosystem: svend4](#reference-ecosystem-svend4)
  - [Quick Start](#quick-start)
  - [Connect Your Repository](#connect-your-repository)
  - [How It Works](#how-it-works)
  - [Compatibility Levels](#compatibility-levels)
  - [Documentation](#documentation)
  - [Project Status](#project-status)
  - [Why "Nautilus"?](#why-nautilus)
  - [Related Work](#related-work)
  - [Licenses](#licenses)
  - [Contact](#contact)

---

<!-- tags: rag, architecture, anthropic, collaboration -->




## 🇬🇧 About

Nautilus is a **federation protocol** and reference implementation 
for independent git repositories containing knowledge in different 
native formats, without forcing them into a unified schema.

Just as an Office Suite reads `.docx`, `.pdf`, and `.xlsx` without 
merging them into one format — Nautilus reads repositories in an 
ecosystem, finds bridges between them, and builds a common search 
layer on top.

### Philosophy

Most modern knowledge systems (Notion, Obsidian, Roam, Coda) 
require migrating data into their unified format. This creates 
vendor lock-in, erases authorial models, and homogenizes different 
types of knowledge.

**Nautilus takes the opposite path:**

- Each repository keeps its native format
- Translation between formats happens through adapters, on demand
- Consensus is computed as intersection of results across repos
- Adding a new repository takes 5 minutes and requires no 
  refactoring

### Reference Ecosystem: svend4

Reference implementation demonstrates on three repositories:

| Repo | Format | Content | Perspective |
| --- | --- | --- | --- |
| [info1](https://github.com/svend4/info1) | `.info1` | 74 documents with α-levels | Methodological |
| [pro2](https://github.com/svend4/pro2) | `.pro2` | Q6-graph, 64 vertices | Semantic |
| [meta](https://github.com/svend4/meta) | `.meta` | 256 CA rules + 64 hexagrams | Symbolic |

The three-perspective structure is not accidental — it reflects 
Peirce's semiotic triad (pragmatic × semantic × syntactic), 
realized as a federated knowledge ecosystem.

### Quick Start

```bash
git clone https://github.com/svend4/nautilus
cd nautilus
pip install -r requirements.txt

# CLI
python portal.py --query "crystal"

# Web interface
python portal.py --serve
# open http://localhost:8000

# MCP for Claude Desktop (in development)
# see MCP-EXTENSION.md
```

### Connect Your Repository

**Minimal (Level 0–1, 5 minutes):**

1. Place `nautilus.json` in your repo's root:

```json
{
  "name": "my-repo",
  "format": ".my-format",
  "native_unit": "what is stored",
  "bridges": {
    "info1": "how concepts correspond",
    "pro2": "...",
    "meta": "..."
  }
}
```

2. Write `passport.md` — a one-page description (see templates in 
   [`passports/`](./passports/))

**Full (Level 2–3, a few hours):**

3. Add an adapter in `adapters/my_repo.py` implementing the 
   `BaseAdapter` interface (see 
   [PORTAL-PROTOCOL.md §6](./PORTAL-PROTOCOL.md#6-adapter-interface))

4. Register the repo in the portal's root `nautilus.json`

### How It Works

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  info1   │  │   pro2   │  │   meta   │
│ α-levels │  │Q6-graph  │  │ CA-rules │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
           ⬡ Nautilus Portal
         (adapters + consensus)
                   │
         ┌─────────┼─────────┐
         │         │         │
       CLI       Web       MCP
                        (for Claude)
```

**Consensus** is computed as intersection: a concept has "full 
consensus" if found in all queried repos; "partial" if found in 
some; "singular" if only in one. Reports always show attribution — 
which repo each result came from.

### Compatibility Levels

Repos are connected gradually — not necessarily at max level from 
day one.

- **0: Discoverable** — declared in registry only
- **1: Readable** — has passport + `describe()` method
- **2: Queryable** — implements `fetch(query)` — search works
- **3: Interactive** — `translate_to()` — cross-repo translations 
  via bridges

Details in [PORTAL-PROTOCOL.md §5](./PORTAL-PROTOCOL.md#5-compatibility-levels).

### Documentation

- **[PORTAL-PROTOCOL.md](./PORTAL-PROTOCOL.md)** — formal v1.0 
  specification (15 pages)
- **[passports/](./passports/)** — human-readable repo descriptions
  - [info1](./passports/info1.md)
  - [pro2](./passports/pro2.md)
  - [meta](./passports/meta.md)
- **Issues** — questions, proposals, bug reports

### Project Status

Nautilus is under **active development**:

- ✅ Protocol v1.0 (draft) — specification written
- ✅ Reference implementation — portal working with three repos
- 🔄 MCP wrapper — in progress
- 🔄 PyPI packaging — planned
- 🔄 Arxiv preprint — planned
- ⏳ [MCP Registry](https://github.com/mcp) submission — after MCP 
  wrapper completion

**Current version**: v1.0.0-draft. Breaking changes possible until 
v1.0.0-stable.

### Why "Nautilus"?

A nautilus shell is a **spiral of nested chambers**, each larger 
than the last but built on the same geometry. This is *fractal 
scaling with preserved proportion*. Nautilus Protocol embodies the 
same pattern: repos nested inside an ecosystem, each self-contained 
yet connected by the same protocol, the same geometry of bridges.

### Related Work

Nautilus sits in the space of knowledge federation protocols, 
alongside:

- **[ActivityPub](https://activitypub.rocks/)** (W3C) — federation 
  for social activities
- **[Solid](https://solidproject.org/)** (Tim Berners-Lee) — 
  personal data pods
- **[Linked Data](https://www.w3.org/standards/semanticweb/data)** 
  (W3C) — semantic web
- **[Model Context Protocol](https://github.com/anthropics/mcp)** 
  (Anthropic) — LLM↔tools integration

Nautilus is unique in combining: (1) git-based storage, (2) 
native-format federation without unified schema, (3) 
consensus-based validation across repos.

### Licenses

- **Documentation** (README, PORTAL-PROTOCOL, passports): 
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code** (portal, adapters, glyph_adapter): 
  [MIT](./LICENSE)

### Contact

- **Author**: svend4
- **Get in touch**: via [Issues](https://github.com/svend4/nautilus/issues)

---

<!-- similar-docs -->

---

**Похожие документы:**
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md) (сходство 0.17)
- [141-4-nautilus-portal-as-reference-substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) (сходство 0.16)
- [158-4-proposed-infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md)
- [141-4-nautilus-portal-as-reference-substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md)
- [158-4-proposed-infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md)
- [164-10-appendices](docs/02-anthropic-vacancies/164-10-appendices.md)

