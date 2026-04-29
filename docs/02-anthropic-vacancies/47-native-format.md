# Native Format

<!-- summary -->
> **Структура концепта (предположительно):** [? уточнить точный формат]

---



## Native Format

**Расширение:** `.[pro2](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`

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
- [57-native-format](docs/02-anthropic-vacancies/57-native-format.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [57-native-format](docs/02-anthropic-vacancies/57-native-format.md)
- [50-bridges](docs/02-anthropic-vacancies/50-bridges.md)
- [49-angle-perspective](docs/02-anthropic-vacancies/49-angle-perspective.md)
- [42-author-contact](docs/02-anthropic-vacancies/42-author-contact.md)

