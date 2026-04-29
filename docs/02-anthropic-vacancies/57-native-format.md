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
- [37-native-format](37-native-format.md) (сходство 0.12)
- [60-bridges](60-bridges.md) (сходство 0.12)
- [47-native-format](47-native-format.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [60-bridges](60-bridges.md)
- [51-compatibility-level](51-compatibility-level.md)
- [61-compatibility-level](61-compatibility-level.md)
- [47-native-format](47-native-format.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Native Format](37-native-format.md) _33%_
- [Bridges](50-bridges.md) _33%_
- [Compatibility Level](51-compatibility-level.md) _33%_
- [Native Format](47-native-format.md) _29%_
- [Bridges](60-bridges.md) _29%_
- [Bridges](40-bridges.md) _25%_
- [Angle / Perspective](49-angle-perspective.md) _25%_
- [Compatibility Level](61-compatibility-level.md) _25%_
