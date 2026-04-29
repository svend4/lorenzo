# Комбинация 28: Pydantic-Enforced Legal Workflows

> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Pydantic validation (structured LLM outputs)

Sequential Protocol (specialist chain)

Adversarial review (writer + reviewers)

LLM parsing (text → structured data)

Дети:

Type-safe legal document pipeline

python

class BescheidAnalysis(BaseModel):
aktenzeichen: str
court: str
decision_date: date
paragraphs: List[str]
deadline: date
violations: List[LegalViolation]

@validator('deadline')
def check_deadline_not_passed(cls, v):
if v < date.today():
raise ValueError(f"Deadline {v} already passed!")
return v

# Sequential pipeline with Pydantic validation at each stage
bescheid_pdf → LLM extraction → BescheidAnalysis (validated)
↓
WiderspruchArguments (validated) ← LLM generation
↓
Widerspruch.docx ← Template rendering

Adversarial pipeline with schema enforcement

Writer Agent generates Widerspruch

Output: WiderspruchDraft(Pydantic)

Reviewer 1: validates legal citations → CitationReview(Pydantic)

Reviewer 2: validates deadlines → DeadlineReview(Pydantic)

Reviewer 3: validates formatting → FormatReview(Pydantic)

If validation fails: ModelRetry with specific error context

ROI: Type-safe legal automation, catches errors before human review

Уникальность: First legal workflow with Pydantic enforcement at every stage. LLM outputs are validated against legal schemas. Errors detected in seconds, not days.
