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
- [98-appendix-a-minimal-working-example](98-appendix-a-minimal-working-example.md) (сходство 0.44)
- [03-portal-protocol-md](03-portal-protocol-md.md) (сходство 0.18)
- [123-portal-mcp-py](123-portal-mcp-py.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [98-appendix-a-minimal-working-example](98-appendix-a-minimal-working-example.md)
- [123-portal-mcp-py](123-portal-mcp-py.md)
- [03-portal-protocol-md](03-portal-protocol-md.md)
- [105-review-methodology-md](105-review-methodology-md.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. QueryResult Structure](22-10-queryresult-structure.md)
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md)
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md)
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md)
- [9. Query Flow](21-9-query-flow.md)
- [Abstract](04-abstract.md)
- [Appendix A: Decision Tree for InGit Adopters](321-appendix-a-decision-tree-for-ingit-adopters.md)
- [Appendix A: Minimal Working Example](98-appendix-a-minimal-working-example.md)
- [Appendix B: Change Log](103-appendix-b-change-log.md)
- [Appendix B: Sub-Agent Registry Schema (Sketch)](270-appendix-b-sub-agent-registry-schema-sketch.md)
- [Appendix C: References](104-appendix-c-references.md)
- [Bridges](60-bridges.md)
- [Compatibility Level](41-compatibility-level.md)
- [For the Curious: Philosophy](44-for-the-curious-philosophy.md)
- [For the Curious: Philosophy](54-for-the-curious-philosophy.md)
- [For the Curious: Philosophy](64-for-the-curious-philosophy.md)
- [History](63-history.md)
- [Planned (v0.2.0)](132-planned-v0-2-0.md)
- [README-MCP.md— инструкция по установке](125-readme-mcp-md-инструкция-по-установке.md)
- [README.md](65-readme-md.md)
- [REVIEW_METHODOLOGY.md](105-review-methodology-md.md)
- [Table of Contents](154-table-of-contents.md)
- [portal-mcp.py](123-portal-mcp-py.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Глоссарий](122-глоссарий.md)
- [Зачем две версии параллельно](70-зачем-две-версии-параллельно.md)
- [Инвертированный индекс ключевых слов](../KEYWORD_INDEX.md)
- [Критерии выбора для фазы 3](71-критерии-выбора-для-фазы-3.md)
- [Ограничения текущей версии (0.1.0-draft)](131-ограничения-текущей-версии-0-1-0-draft.md)
- [Отладка](130-отладка.md)
- [Подключение к Claude Desktop](127-подключение-к-claude-desktop.md)
- [Содержание](190-содержание.md)
- [Содержание](326-содержание.md)
- [Установка](126-установка.md)
- [Что ты ВСЕГДА делаешь](360-что-ты-всегда-делаешь.md)
- [⬡](69-section.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Appendix A: Minimal Working Example](98-appendix-a-minimal-working-example.md) _60%_
- [REVIEW_METHODOLOGY.md](105-review-methodology-md.md) _42%_
- [portal-mcp.py](123-portal-mcp-py.md) _37%_
- [Abstract](04-abstract.md) _33%_
- [Содержание](190-содержание.md) _33%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _33%_
- [For the Curious: Philosophy](44-for-the-curious-philosophy.md) _33%_
- [README.md](65-readme-md.md) _33%_
## Связанные документы

- [Appendix A: Minimal Working Example](98-appendix-a-minimal-working-example.md) _60%_
- [REVIEW_METHODOLOGY.md](105-review-methodology-md.md) _37%_
- [Abstract](04-abstract.md) _33%_
- [portal-mcp.py](123-portal-mcp-py.md) _33%_
- [Содержание](190-содержание.md) _33%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _33%_
- [Глоссарий](122-глоссарий.md) _29%_
- [README-MCP.md— инструкция по установке](125-readme-mcp-md-инструкция-по-установке.md) _29%_
