# Комбинация 13: Legal Document Transpiler

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture, collaboration -->




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

**Смотрите также:**
- [25-legal-dsl-code-transpiler](docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md)
- [10-legal-document-intelligence-pipeline](docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)
- [28-pydantic-enforced-legal-workflows](docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md)
- [29-meta-programmatic-legal-template-generator](docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md)

