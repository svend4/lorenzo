---
title: "Домен: немецкое социальное право"
tags:
  - rag
  - knowledge
  - ingestion
  - architecture
  - technology-combinations
date: 2026-05-11
---

# Домен: немецкое социальное право

<!-- toc-auto -->
## Contents

- [Похожие документы](#похожие-документы)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) LLM+Pydantic parses legal entities: class Bescheid(BaseModel): aktenzeichen: str; p
**Проекты:** Svyazi, [[01-executive-summary|CardIndex]]

---
<!-- tags: rag, knowledge, ingestion, architecture -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





**1. Sozialrecht corpus auto-builder**

Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations). LLM+Pydantic parses legal entities:

```python
class Bescheid(BaseModel):
    aktenzeichen: str
    paragraphs: List[SGB_Reference]
    deadline: date
```

[[01-executive-summary|CardIndex]] deduplicates decisions by SHA256. Итог: self-updating knowledge base of 50k+ decisions, structured queries.

**2. Precedent search with semantic + structural filters**

Docling knows document structure (§, headings, footnotes). Pydantic enforces schema:

```python
query = {"type": "Widerspruch", "sgb": "IX", "paragraph": "78 Abs. 6"}
```

Graph-RAG links precedents through citations. ROI: 10 sec queries vs 2 hour manual search.

Уникальность: Docling maintains structure, Pydantic validates legal schema, Svyazi deduplicates. Ни один SaaS не делает это для немецкого социального права.

<!-- similar-docs -->

---

## Похожие документы
- [[README]] (сходство 0.15)


<!-- see-also -->

---

## Смотрите также
- [[GLOSSARY]]
- [[MINDMAP]]
- [[360-что-ты-всегда-делаешь]]
- [[306-with-anthropic-s-cowork-platform|321-appendix-a-decision-tree-for-[ingit]]-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [[321-appendix-a-decision-tree-for-ingit-adopters]]
- [[01-agent-routing]]
- [[README]]

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документ индексирован в базе знаний репозитория.
