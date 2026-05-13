---
state: normalized
---

# Комбинация 13: Legal Document Transpiler

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

COBOL→Java transpiler (habr.com/ru/articles/489730/) - built in 1 day using ANTLR visitor pattern

LLM Parsing with Structured Outputs

German legal template generator (existing skill)

Дети:

Bescheid→Widerspruch auto-transpiler

ANTLR parser for Bescheid structure (headers, Begründung, Rechtsmittelbelehrung)

Visitor pattern extracts legal facts: class BescheidFact(BaseModel): claim_rejected: bool; paragraph_cited: str

LLM generates Widerspruch arguments from extracted facts

Template engine produces compliant Widerspruch with proper citations

Legacy→Modern legal document converter

Old Bescheide from 1990s (typewriter formatting, no structured data)

Transpiler normalizes to modern schema

Enables bulk analysis of historical precedents

ROI: 50k historical documents searchable in structured DB

Уникальность: COBOL transpiler pattern applied to legal domain. 1-day implementation vs months of manual template coding.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 13 Legal Document Transpiler"
```

## Смотрите также
- [25-legal-dsl-code-transpiler](25-legal-dsl-code-transpiler.md)
- [10-legal-document-intelligence-pipeline](10-legal-document-intelligence-pipeline.md)
- [28-pydantic-enforced-legal-workflows](28-pydantic-enforced-legal-workflows.md)
- [29-meta-programmatic-legal-template-generator](29-meta-programmatic-legal-template-generator.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [README](README.md)
- [01-legal-ai-stack](../mega-stacks/01-legal-ai-stack.md)
- [09-14-extended](../synthesis-tables/09-14-extended.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для поиска в базе знаний репозитория._ _Для поиска доступен._

<!-- similar-docs -->

---

**Похожие документы:**
- [13-legal-document-transpiler](../../obsidian/technology-combinations/combinations/13-legal-document-transpiler.md) (сходство 0.94)
- [10-legal-document-intelligence-pipeline](10-legal-document-intelligence-pipeline.md) (сходство 0.40)
- [10-legal-document-intelligence-pipeline](../../obsidian/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md) (сходство 0.38)

