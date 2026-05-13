---
state: normalized
---

# 10. Open Questions

<!-- toc-auto -->
## Contents

- [10. Open Questions](#10-open-questions)
  - [10.1. Scope of "Profession"](#101-scope-of-profession)
  - [10.2. Multi-Profession Practitioners](#102-multi-profession-practitioners)
  - [10.3. International Variation](#103-international-variation)
  - [10.4. Update Cadence](#104-update-cadence)
  - [10.5. Quality Assessment](#105-quality-assessment)
  - [10.6. Transition Costs](#106-transition-costs)
  - [10.7. Profession-Wide Effects](#107-profession-wide-effects)
  - [10.8. Appropriate Resistance](#108-appropriate-resistance)
- [Использование](#использование)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Professional Colleague Agents (EN)», написанный совместно с Claude.

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Professional Colleague Agents (EN)», написанный совместно с Claude.

## 10. Open Questions

Several questions remain unresolved.

### 10.1. Scope of "Profession"

**What constitutes a profession** for the purposes of agent
specialization? Can sub-specialties have their own agents
(family law vs. criminal law vs. social law)? What's the
right granularity?

Answer likely emerges from market: where practitioners cluster
and where shared knowledge bases provide enough overlap to
justify development cost.

### 10.2. Multi-Profession Practitioners

How do agents handle practitioners who span multiple
professional contexts (researcher who also teaches; lawyer
who is also academic; engineer who is also entrepreneur)?

Possibilities: separate agents, combined agent with profile
toggling, hybrid that automatically applies relevant
context.

### 10.3. International Variation

A Professional Colleague Agent for German social law cannot
serve American social law practitioners. How do we structure
international variation? Per-country agents? Modular knowledge
bases with country-specific layers?

### 10.4. Update Cadence

How quickly should knowledge bases update as authoritative
sources change? Real-time? Daily? Quarterly? With release
cadences? Different for different types of changes
(emergency vs. ordinary)?

### 10.5. Quality Assessment

How do we measure quality of a Professional Colleague Agent?
Practitioner satisfaction? Time savings? Output accuracy
(measured how)? Long-term professional development? Different
metrics serve different stakeholders.

### 10.6. Transition Costs

When practitioners move between Professional Colleague Agents
(switching providers), what's the friction? Personal preferences
and history transfer? Trained habits? Modified knowledge bases
that practitioner has customized?

### 10.7. Profession-Wide Effects

Beyond individual practitioner effects, what happens to a
profession as a whole when most practitioners use the same
Professional Colleague Agent? Does practice homogenize? Does
quality improve? Does innovation slow? Empirical question
requiring measurement.

### 10.8. Appropriate Resistance

Should some professions resist Professional Colleague Agents?
Are there professional values that AI augmentation undermines?
What might we lose? These are not technical questions but
they shape technical decisions.

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "10 Open Questions"
```

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
- [10-open-questions](../../obsidian/nautilus/professional-colleague-agents-en/10-open-questions.md) (сходство 0.98)
- [221-10-open-questions](../../02-anthropic-vacancies/221-10-open-questions.md) (сходство 0.81)
- [221-10-open-questions](../../obsidian/02-anthropic-vacancies/221-10-open-questions.md) (сходство 0.80)

