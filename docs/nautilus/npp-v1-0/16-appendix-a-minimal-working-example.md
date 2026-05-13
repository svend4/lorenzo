---
state: normalized
---

# Appendix A: Minimal Working Example

<!-- toc-auto -->
## Contents

- [Essence](#essence)
- [Native Format](#native-format)
- [Content Overview](#content-overview)
- [Angle / Perspective](#angle-perspective)
- [Author](#author)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

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

## Смотрите также
- [17-appendix-b-change-log](17-appendix-b-change-log.md)
- [15-glossary](15-glossary.md)
- [13-reference-implementation](13-reference-implementation.md)
- [10-query-result](10-query-result.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документ индексирован в базе знаний репозитория.

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [16-appendix-a-minimal-working-example](../../obsidian/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md) (сходство 0.99)
- [17-appendix-b-change-log](../../obsidian/nautilus/npp-v1-0/17-appendix-b-change-log.md) (сходство 0.50)
- [13-reference-implementation](../../obsidian/nautilus/npp-v1-0/13-reference-implementation.md) (сходство 0.47)

