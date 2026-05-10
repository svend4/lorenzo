# Appendix A: Minimal Working Example

<!-- toc-auto -->
## Contents

- [Contents](#contents)
- [Contents](#contents-1)
- [Essence](#essence)
- [Native Format](#native-format)
- [Content Overview](#content-overview)
- [Angle / Perspective](#angle-perspective)
- [Author](#author)
## Contents

- [Contents](#contents)
- [Essence](#essence)
- [Native Format](#native-format)
- [Content Overview](#content-overview)
- [Angle / Perspective](#angle-perspective)
- [Author](#author)
## Contents

- [Essence](#essence)
- [Native Format](#native-format)
- [Content Overview](#content-overview)
- [Angle / Perspective](#angle-perspective)
- [Author](#author)


<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

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
- [17-appendix-b-change-log](17-appendix-b-change-log.md)
- [15-glossary](15-glossary.md)
- [13-reference-implementation](13-reference-implementation.md)
- [10-query-result](10-query-result.md)

