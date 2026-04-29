# 15. Glossary of Examples

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: ingestion, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 15. Glossary of Examples

В качестве иллюстраций используется экосистема `svend4` с тремя 
Repos:

- **info1**: 74 документа с α-уровнями, методологический угол
- **pro2**: Q6-концепты, граф знаний, семантический угол
- **meta**: 256 CA-правил, гексаграммы, символьный угол

Эти Repos служат reference examples для тестирования NPP-совместимых 
implementations.

---

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
- [27-15-glossary-of-examples](docs/02-anthropic-vacancies/27-15-glossary-of-examples.md)
- [17-appendix-b-change-log](docs/nautilus/npp-v1-0/17-appendix-b-change-log.md)
- [13-reference-implementation](docs/nautilus/npp-v1-0/13-reference-implementation.md)
- [10-query-result](docs/nautilus/npp-v1-0/10-query-result.md)

