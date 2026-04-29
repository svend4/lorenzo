# Appendix A: Minimal Working Example

<!-- toc-auto -->
## Contents

- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - [A.1. Minimal nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter (Level 1)](#a2-minimal-adapter-level-1)
  - [A.3. Minimal Passport](#a3-minimal-passport)


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

<!-- similar-docs -->

---

**Похожие документы:**
- [28-appendix-a-minimal-working-example](28-appendix-a-minimal-working-example.md) (сходство 0.44)
- [03-portal-protocol-md](03-portal-protocol-md.md) (сходство 0.11)
- [35-passports-info1-md](35-passports-info1-md.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [28-appendix-a-minimal-working-example](28-appendix-a-minimal-working-example.md)
- [123-portal-mcp-py](123-portal-mcp-py.md)
- [03-portal-protocol-md](03-portal-protocol-md.md)
- [105-review-methodology-md](105-review-methodology-md.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _60%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _37%_
- [Abstract](04-abstract.md) _33%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _33%_
- [REVIEW_METHODOLOGY.md](105-review-methodology-md.md) _33%_
- [portal-mcp.py](123-portal-mcp-py.md) _33%_
- [Compatibility Level](41-compatibility-level.md) _33%_
- [Native Format](37-native-format.md) _29%_
