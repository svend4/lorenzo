# Native Format

<!-- summary -->
> **Структура концепта (предположительно):** [? уточнить точный формат]

---
<!-- tags: anthropic -->




## Native Format

**Расширение:** `.pro2`

**Структура концепта (предположительно):** [? уточнить точный формат]
```
{
"id": "unique-concept-id",
"title": "Human-readable name",
"q6_vertex": "binary string, 6 bits (e.g. '101100')",
"definition": "Formal or informal definition",
"related": ["id1", "id2", ...],  // hamming-distance 1 neighbors
"hexagram_mapping": "hexagram number 1–64 from I Ching",
"tags": ["tag1", "tag2"],
"metadata": { ... }
}
```
**Q6-вершина** определяет 6 бинарных атрибутов концепта. Соседи по 
графу (с hamming distance 1) — концепты, отличающиеся ровно в одном 
атрибуте.

**Особенность:** Q6-граф имеет строго 64 вершины и 192 ребра. Каждая 
вершина имеет ровно 6 соседей (один на каждое измерение).

---

<!-- similar-docs -->

---

**Похожие документы:**
- [57-native-format](57-native-format.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [57-native-format](57-native-format.md)
- [50-bridges](50-bridges.md)
- [49-angle-perspective](49-angle-perspective.md)
- [42-author-contact](42-author-contact.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Native Format](57-native-format.md) _29%_
- [Angle / Perspective](49-angle-perspective.md) _25%_
- [Bridges](50-bridges.md) _25%_
- [Native Format](37-native-format.md) _21%_
- [History](43-history.md) _21%_
- [Content Overview](48-content-overview.md) _21%_
- [Compatibility Level](51-compatibility-level.md) _21%_
- [Abstract](04-abstract.md) _17%_
