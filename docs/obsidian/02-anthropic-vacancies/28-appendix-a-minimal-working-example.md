---
title: "Appendix A: Minimal Working Example"
tags:
  - ingestion
  - rag
  - anthropic-vacancies
date: 2026-05-14
---

# Appendix A: Minimal Working Example

<!-- toc-auto -->
## Contents

- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - [A.1. Minimal nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter](#a2-minimal-adapter)
  - [A.3. Minimal Passport](#a3-minimal-passport)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

  - [A.1. Minimal nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter](#a2-minimal-adapter)
  - [A.3. Minimal Passport](#a3-minimal-passport)
  - A.1. Minimal [nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter](#a2-minimal-adapter)
  - [A.3. Minimal Passport](#a3-minimal-passport)
  - A.1. Minimal [nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter](#a2-minimal-adapter)
  - [A.3. Minimal Passport](#a3-minimal-passport)
  - A.1. Minimal [nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter](#a2-minimal-adapter)
  - [A.3. Minimal Passport](#a3-minimal-passport)
<!-- summary -->
> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. "adapter": "adapters/my_notes.py", _Документ индексирован в базе знаний репозитория Lorenzo._ _Для поиска доступен._
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> "adapter": "adapters/my_notes.py",

---
<!-- tags: ingestion, rag -->


## Appendix A: Minimal Working Example

### A.1. Minimal `nautilus.json`

```json
{
  "protocol_version": "1.0",
  "ecosystem_name": "example",
  "repositories": [
    {
      "name": "my_notes",
      "format": ".md",
      "adapter": "adapters/my_notes.py",
      "compatibility_level": 2
    }
  ]
}
```

### A.2. Minimal Adapter

```python
from pathlib import Path
from base import BaseAdapter, PortalEntry


class MyNotesAdapter(BaseAdapter):
    name = "my_notes"
    
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
    
    def describe(self):
        md_files = list(self.repo_path.glob("**/*.md"))
        return {
            "name": self.name,
            "format": ".md",
            "total_entries": len(md_files),
            "topics": []
        }
    
    def fetch(self, query):
        results = []
        for path in self.repo_path.glob("**/*.md"):
            text = path.read_text()
            if query.lower() in text.lower():
                results.append(PortalEntry(
                    repo_name=self.name,
                    native_id=str(path.relative_to(self.repo_path)),
                    title=path.stem,
                    summary=text[:280],
                    content=text,
                    tags=[],
                    confidence=1.0,
                    native_metadata={"path": str(path)},
                    url=None
                ))
        return results
```

### A.3. Minimal Passport

```markdown
# my_notes

<!-- similar-docs -->

---

## Похожие документы
- [[98-appendix-a-minimal-working-example]] (сходство 0.44)
- [[03-portal-protocol-md]] (сходство 0.18)
- [[123-portal-mcp-py]] (сходство 0.17)


<!-- see-also -->

---

## Смотрите также
- [[98-appendix-a-minimal-working-example]]
- [[123-portal-mcp-py]]
- [[03-portal-protocol-md]]
- [[105-review-methodology-md]]


<!-- backlinks -->

---

## Кто ссылается на этот документ (31)
- [[03-portal-protocol-md]]
- [[04-abstract]]
- [[09-4-passport-passport-md]]
- [[103-appendix-b-change-log]]
- [[104-appendix-c-references]]
- [[105-review-methodology-md]]
- [[122-глоссарий]]
- [[123-portal-mcp-py]]
- _...ещё 23_

_Документ индексирован в базе знаний репозитория Lorenzo._ _Для поиска доступен._
