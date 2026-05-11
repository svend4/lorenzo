# Комбинация 29: Meta-Programmatic Legal Template Generator

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 29 Meta Programmatic Legal"
```

## Смотрите также
- [25-legal-dsl-code-transpiler](25-legal-dsl-code-transpiler.md)
- [28-pydantic-enforced-legal-workflows](28-pydantic-enforced-legal-workflows.md)
- [25-30-extended](../synthesis-tables/25-30-extended.md)
- [10-legal-document-intelligence-pipeline](10-legal-document-intelligence-pipeline.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации по графу._ _Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (11):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [13-legal-document-transpiler](13-legal-document-transpiler.md)
- [25-legal-dsl-code-transpiler](25-legal-dsl-code-transpiler.md)
- [26-ast-based-code-analysis-for-legal-automation](26-ast-based-code-analysis-for-legal-automation.md)
- _...ещё 3_

