# Appendix A: Minimal Working Example

<!-- toc-auto -->
## Contents

- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - [A.1. Minimal nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter](#a2-minimal-adapter)
  - [A.3. Minimal Passport](#a3-minimal-passport)


<!-- summary -->
> "adapter": "adapters/my_notes.py",

---
<!-- tags: ingestion -->




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

**Похожие документы:**
- [98-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) (сходство 0.44)
- [03-portal-protocol-md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) (сходство 0.18)
- [123-portal-mcp-py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [98-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)
- [123-portal-mcp-py](docs/02-anthropic-vacancies/123-portal-mcp-py.md)
- [03-portal-protocol-md](docs/02-anthropic-vacancies/03-portal-protocol-md.md)
- [105-review-methodology-md](docs/02-anthropic-vacancies/105-review-methodology-md.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) _60%_
- [REVIEW_METHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md) _37%_
- [Abstract](docs/02-anthropic-vacancies/04-abstract.md) _33%_
- [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) _33%_
- [Содержание](docs/02-anthropic-vacancies/190-содержание.md) _33%_
- [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) _33%_
- [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) _29%_
- [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) _29%_
