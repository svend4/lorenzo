# Appendix A: Minimal Working Example

<!-- summary -->
> "passport": "passports/my_notes.md",

---
<!-- tags: ingestion -->




## Appendix A: Minimal Working Example

### A.1. Minimal `nautilus.json`

```json
{
  "protocol_version": "1.1",
  "ecosystem_name": "example",
  "registry": [
    {
      "name": "my_notes",
      "repo": "owner/my-notes",
      "format": "my_notes",
      "adapter": "my_notes",
      "passport": "passports/my_notes.md",
      "compatibility": 1,
      "q6_key": "не определено"
    }
  ]
}
```

### A.2. Minimal Adapter (Level 1)

```python
# adapters/my_notes.py
from .base import BaseAdapter, PortalEntry


class MyNotesAdapter(BaseAdapter):
    name = "my_notes"
    REPO = "owner/my-notes"
    
    def fetch(self, query: str) -> list[PortalEntry]:
        q = query.lower()
        results = [
            e for e in self._static_entries()
            if q in e.title.lower() or q in e.content.lower()
        ]
        return results or self._static_entries()[:2]  # fallback
    
    def _static_entries(self) -> list[PortalEntry]:
        return [
            PortalEntry(
                id="my_notes:intro",
                title="Introduction",
                source=self.REPO,
                format_type="document",
                content="Sample content about...",
                metadata={},
                links=[],
                is_fallback=True
            ),
            # ... больше entries
        ]
    
    def describe(self) -> dict:
        return {
            "repo": self.REPO,
            "format": "my_notes",
            "native_unit": "Markdown note",
            "total_items": "5",
            "compatibility": 1
        }
```

### A.3. Minimal Passport

```markdown
# Паспорт: owner/my-notes

| Поле | Значение |
|------|----------|
| Репозиторий | owner/my-notes |
| Формат | `.md` — Markdown notes |
| Единица | Markdown-документ |
| Адаптер | `adapters/my_notes.py` |
| Уровень совместимости | 1 — читаемый |

# Описание

## Описание

Персональная коллекция Markdown-заметок.
