---
title: "Appendix A: Minimal Working Example"
tags:
  - ingestion
  - anthropic
  - nautilus
date: 2026-04-29
---

# Appendix A: Minimal Working Example

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: ingestion, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

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

## Essence
Персональная коллекция Markdown-заметок.

## Native Format
`.md` файлы в произвольной иерархии.

## Content Overview
~200 заметок, темы: software engineering, philosophy, music.

## Angle / Perspective
Methodological: how-to и reflection.

## Author
example_user, example@email.com
```

---

<!-- see-also -->

---

**Смотрите также:**
- [[17-appendix-b-change-log]]
- [[15-glossary]]
- [[13-reference-implementation]]
- [[10-query-result]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[17-appendix-b-change-log]] (сходство 0.30)
- [[15-glossary]] (сходство 0.28)
- [[13-reference-implementation]] (сходство 0.27)

