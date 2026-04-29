# Сводная таблица 25–30 (Complete 1–30)

> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude`, секция «EXTENDED SYNTHESIS TABLE (Complete 1‑30)».

| # | Components | Result | Impact |
|---|---|---|---|
| [25](../combinations/25-legal-dsl-code-transpiler.md) | Python AST + DSL + Pydantic | Legal document transpiler | 50k docs in 1 day |
| [26](../combinations/26-ast-based-code-analysis-for-legal-automation.md) | AST + ASTChunk + LLM | Code analysis for legal automation | Self‑documenting code |
| [27](../combinations/27-hybrid-rag-with-ast-chunked-code.md) | ASTChunk + Graph‑RAG + ClickHouse | Code + precedents unified KB | Developer↔lawyer bridge |
| [28](../combinations/28-pydantic-enforced-legal-workflows.md) | Pydantic + Sequential + Adversarial | Type‑safe legal workflows | Errors caught in seconds |
| [29](../combinations/29-meta-programmatic-legal-template-generator.md) | DSL + AST + Templates | Meta‑programmatic templates | Write once, deploy everywhere |
| [30](../combinations/30-mega-stack-3-0-with-dsl-ast.md) | ALL ABOVE | Complete legal‑AI + DSL stack | Production system with DSL |

## Рекомендация

**Комбинация 28** (Pydantic‑enforced workflows) — начать с validation Bescheid parsing:

```python
class Bescheid(BaseModel):
    aktenzeichen: str = Field(regex=r"[A-Z]\s\d+\sSO\s\d+/\d+")
    deadline: date

    @validator('deadline')
    def not_in_past(cls, v):
        if v < date.today():
            raise ValueError(f"Deadline passed: {v}")
        return v
```

Альтернатива: **Комбинация 25** (Legal DSL transpiler) — если хочешь declarative legal automation.
