# Комбинация 29: Meta-Programmatic Legal Template Generator

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

DSL metaprogramming (domain-specific legal language)

Python AST (code generation)

Pydantic schemas (legal object validation)

German legal templates (Widerspruch, Klage, Antrag)

Дети:

DSL → Template compiler

python

# Legal DSL (declarative)
template WiderspruchKSV {
against: Bescheid
grounds: [
violation("SGB IX § 78 Abs. 6", "insufficient support hours"),
violation("BSG B 8 SO 9/19 R", "retroactive personal budget")
]
demands: [
approve_personal_budget(hours=24/7),
retroactive_payment(from=against.application_date)
]
}

# Compiler generates Python code
class WiderspruchKSV:
def __init__(self, bescheid: Bescheid):
self.gegen = bescheid
self.violations = [...] # auto-generated

def render(self) -> Document:
# auto-generated rendering logic

Multi-format output generator

Single DSL source → multiple output formats

PDF (formal submission), DOCX (editing), HTML (preview), JSON (API)

Python AST generates format-specific renderers

ROI: Write once, deploy everywhere

Уникальность: Legal templates as compiled DSL. Changes to legal requirements → recompile DSL → all templates updated. First application of metaprogramming to German Sozialrecht.

<!-- see-also -->

---

**Смотрите также:**
- [25-legal-dsl-code-transpiler](docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md)
- [28-pydantic-enforced-legal-workflows](docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md)
- [25-30-extended](docs/technology-combinations/synthesis-tables/25-30-extended.md)
- [10-legal-document-intelligence-pipeline](docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)

