# Appendix A: Minimal Working Example

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Appendix A: Minimal Working Example Contents - Appendix A: Minimal Working Example(appendix-a-minimal-working-example) - A.1.
> 🔧 **Подход:** --- Похожие документы: - 28-appendix-a-minimal-working-example(docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) (сходство 0.44) - 03-portal-protocol-md(docs/02
> 🏷️ **Ключевые слова:** `minimal`, `appendix`, `working`, `example`, `anthropic`, `vacancies`, `portal`, `notes`
>


<!-- toc-auto -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Contents

- [Contents](#contents)
- [Contents](#contents-1)
- [Contents](#contents-2)
- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - A.1. Minimal [nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter (Level 1)](#a2-minimal-adapter-level-1)
  - [A.3. Minimal Passport](#a3-minimal-passport)
## Contents

- [Contents](#contents)
- [Contents](#contents-1)
- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - A.1. Minimal [nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter (Level 1)](#a2-minimal-adapter-level-1)
  - [A.3. Minimal Passport](#a3-minimal-passport)
## Contents

- [Contents](#contents)
- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - A.1. Minimal [nautilus.json](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter (Level 1)](#a2-minimal-adapter-level-1)
  - [A.3. Minimal Passport](#a3-minimal-passport)
## Contents

- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - [A.1. Minimal [nautilus](../05-habr-projects/memory/memnet.md).json](#a1-minimal-nautilusjson)
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


<!-- backlinks -->

---

**Кто ссылается на этот документ (17):**
- [03-portal-protocol-md](03-portal-protocol-md.md)
- [04-abstract](04-abstract.md)
- [09-4-passport-passport-md](09-4-passport-passport-md.md)
- [105-review-methodology-md](105-review-methodology-md.md)
- [123-portal-mcp-py](123-portal-mcp-py.md)
- [125-readme-mcp-md-инструкция-по-установке](125-readme-mcp-md-инструкция-по-установке.md)
- [132-planned-v0-2-0](132-planned-v0-2-0.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)
- _...ещё 9_

