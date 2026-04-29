---
title: "Native Format"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# Native Format

<!-- summary -->
> **Структура записи:** [? уточнить]

---
<!-- tags: anthropic -->




## Native Format

**Расширение:** `.meta`

**Структура записи:** [? уточнить]

**Варианты интерпретации (выберите/дополните):**

*Вариант A — CA-rule first:*
```
{
"rule_number": 110,  // 0–255
"wolfram_class": "IV",  // I, II, III, IV
"associated_hexagrams": [49, 64, ...],  // связанные гексаграммы
"dynamics_description": "...",
"attractors": [...],
"stable_patterns": [...]
}
```
*Вариант B — hexagram first:*
```
{
"hexagram_number": 1,  // 1–64 (King Wen order) или 0–63 (binary)
"classical_name": "Qián / Creative",
"lines": [1,1,1,1,1,1],
"ca_rule_family": [30, 86, 135, 149],  // правила с эквивалентной
динамикой
"wolfram_class": "III",
"symbolic_meaning": "..."
}
```
*Вариант C — symmetric mapping*: обе структуры хранятся параллельно 
с cross-references.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[37-native-format]] (сходство 0.12)
- [[60-bridges]] (сходство 0.12)
- [[47-native-format]] (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [[60-bridges]]
- [[51-compatibility-level]]
- [[61-compatibility-level]]
- [[47-native-format]]

<!-- backlinks-auto -->
## Упоминается в

- [[49-angle-perspective|Angle / Perspective]]
- [[40-bridges|Bridges]]
- [[50-bridges|Bridges]]
- [[60-bridges|Bridges]]
- [[51-compatibility-level|Compatibility Level]]
- [[61-compatibility-level|Compatibility Level]]
- [[37-native-format|Native Format]]
- [[47-native-format|Native Format]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[51-compatibility-level|Compatibility Level]] _42%_
- [[49-angle-perspective|Angle / Perspective]] _37%_
- [[60-bridges|Bridges]] _37%_
- [[47-native-format|Native Format]] _33%_
- [[50-bridges|Bridges]] _33%_
- [[61-compatibility-level|Compatibility Level]] _33%_
- [[39-angle-perspective|Angle / Perspective]] _29%_
- [[40-bridges|Bridges]] _29%_
## Связанные документы

- [[37-native-format|Native Format]] _33%_
- [[50-bridges|Bridges]] _33%_
- [[51-compatibility-level|Compatibility Level]] _33%_
- [[47-native-format|Native Format]] _29%_
- [[60-bridges|Bridges]] _29%_
- [[40-bridges|Bridges]] _25%_
- [[49-angle-perspective|Angle / Perspective]] _25%_
- [[61-compatibility-level|Compatibility Level]] _25%_
