---
title: "6. Coordination and Disagreement Resolution"
tags:
  - rag
  - ingestion
  - anthropic-vacancies
date: 2026-04-29
---

# 6. Coordination and Disagreement Resolution

<!-- summary -->
> The composite agent's most subtle function is coordinating

---

<!-- toc -->
## Содержание

- [6. Coordination and Disagreement Resolution](#6-coordination-and-disagreement-resolution)
  - [6.1. Why Sub-Agents Disagree](#61-why-sub-agents-disagree)
  - [6.2. Surfacing Versus Resolving](#62-surfacing-versus-resolving)
  - [6.3. Presentation of Disagreement](#63-presentation-of-disagreement)
  - [6.4. When the Principal Cannot Decide](#64-when-the-principal-cannot-decide)
  - [6.5. Learning from Resolution](#65-learning-from-resolution)

---

<!-- tags: rag, ingestion -->




## 6. Coordination and Disagreement Resolution

The composite agent's most subtle function is coordinating 
multiple sub-agents that may disagree.

### 6.1. Why Sub-Agents Disagree

Disagreement is normal and informative in composite configurations. 
Several common causes:

**Different specialization frames.** A sub-agent on legal 
strategy may recommend X; a sub-agent on case management may 
recommend Y. Each is correct within its frame.

**Different evidence weights.** A sub-agent may weight recent 
case law heavily; another may weight long-established 
methodology more. Both are reasonable choices that produce 
different recommendations.

**Different optimization targets.** A sub-agent may optimize 
for client outcomes; another for procedural correctness. These 
goals can conflict.

**Different boundary handling.** Some questions fall on the 
boundary between specializations. Each sub-agent may interpret 
the boundary differently.

These disagreements often contain the most important information 
the principal needs. A composite agent that resolved them 
silently would hide what the principal most needs to see.

### 6.2. Surfacing Versus Resolving

A central architectural commitment: the composite agent 
**surfaces** disagreements; it does not **resolve** them.

Surfacing means: presenting each sub-agent's recommendation 
clearly, with reasoning, so the principal can see what each 
specialization contributes.

Not resolving means: the composite agent does not vote, average, 
or arbitrate between sub-agents. The principal makes the call.

This is critical because:
- Algorithmic resolution would impose hidden judgment on the 
  principal
- Resolution loses information that the disagreement contains
- The principal's authority over their work depends on access 
  to underlying disagreement
- Profession-level differences in approach should remain visible, 
  not be smoothed away

### 6.3. Presentation of Disagreement

How disagreement is presented matters. Some patterns work well:

**Pattern 1 — Side-by-side recommendation.** "Sub-agent A 
recommends X with reasoning [...]; sub-agent B recommends Y 
with reasoning [...]." Principal sees both directly.

**Pattern 2 — Common ground first.** "Both sub-agents agree 
that [base position]. They differ on [specific issue]: A says 
X; B says Y." Helps principal see what is settled and what is 
contested.

**Pattern 3 — Compatibility analysis.** "A's recommendation 
may produce result X. B's recommendation may produce result Y. 
The choice depends on whether you prioritize Z." Helps principal 
see what the disagreement actually means for outcomes.

**Pattern 4 — Resolution suggestion (without execution).** "If 
you favor X, here's how A's recommendation can be implemented. 
If you favor Y, here's how B's." Principal still chooses; the 
agent helps with implementation of the chosen direction.

What does **not** work: averaging, voting, "balanced" outputs 
that mask the underlying disagreement. These appear neutral 
but actually impose hidden judgment.

### 6.4. When the Principal Cannot Decide

Sometimes the principal genuinely doesn't know which 
recommendation to follow. The composite agent has options:

**Escalation to mentor.** If the principal has access to a human 
mentor, the composite agent can structure the disagreement for 
mentor review.

**Deferred decision.** Some decisions can be deferred — the 
agent helps the principal collect more information before 
committing.

**Risk-weighted default.** If one recommendation is more 
conservative (smaller commitment, easier reversal), the composite 
agent can suggest defaulting to that while gathering more 
information.

**Acknowledged uncertainty.** Sometimes the right output is: 
"You face a genuine professional judgment call here. Here's 
what each sub-agent recommends; here's what's at stake; this 
is a moment where your accumulated experience matters."

The composite agent acknowledging the limits of agent guidance 
is itself valuable.

### 6.5. Learning from Resolution

How the principal resolves disagreements — over time — is 
informative. The composite agent can track:

- Which sub-agents the principal tends to follow when there's 
  disagreement
- Which contexts predict which choice
- Whether the principal's choices show evolving patterns

This information should be available to the principal (their 
own pattern of decisions over time) but not used to hide future 
disagreements. The point is not to predict and pre-resolve; 
the point is to give the principal insight into their own 
practice.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[256-3-what-makes-a-composite-skills-agent]] (сходство 0.18)
- [[258-5-configuration-how-principals-build-their-ensembl]] (сходство 0.14)
- [[263-10-risks-specific-to-composite-architectures]] (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [[256-3-what-makes-a-composite-skills-agent]]
- [[258-5-configuration-how-principals-build-their-ensembl]]
- [[263-10-risks-specific-to-composite-architectures]]
- [[264-11-open-questions]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]] _33%_
- [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]] _33%_
- [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their Ensembles]] _29%_
- [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]] _29%_
- [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] _25%_
- [[174-5-architectural-specification|5. Architectural Specification]] _25%_
- [[211-table-of-contents|Table of Contents]] _25%_
- [[253-table-of-contents|Table of Contents]] _25%_
