# Native Format

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
