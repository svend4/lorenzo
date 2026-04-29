# Native Format

<!-- summary -->
> **Структура записи:** [? уточнить]

---



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
