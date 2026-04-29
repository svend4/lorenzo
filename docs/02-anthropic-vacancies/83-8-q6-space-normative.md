# 8. Q6 Space (Normative)

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Это не обязательно, но RECOMMENDED для экосистем, интегрирующих symbolic и dynamical angles: - Class I (стационарные) — стабильные концепты (базовые алгоритмы, определения) - Class
> 🔧 **Подход:** CA-Class Mapping (Informative)(85-ca-class-mapping-informative) !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `class`, `mapping`, `level`, `portalentry`, `anthropic`, `vacancies`, `space`, `normative`
>


<!-- toc-auto -->
## Contents

- [8. Q6 Space (Normative)](#8-q6-space-normative)
  - [8.1. Definition](#81-definition)
  - [8.2. Mandatory for Level 2+](#82-mandatory-for-level-2)
  - [8.3. Q6 Mapping Rules](#83-q6-mapping-rules)
  - [8.4. Q6-Neighbors (Hamming Distance)](#84-q6-neighbors-hamming-distance)
  - [8.5. CA-Class Mapping (Informative)](#85-ca-class-mapping-informative)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Q6 — 6-мерное бинарное пространство {0,1}⁶. Содержит 64 вершины.

---



## 8. Q6 Space (Normative)

### 8.1. Definition

Q6 — 6-мерное бинарное пространство {0,1}⁶. Содержит 64 вершины.

Каждая вершина представлена 6-битной строкой, например `"010100"`.

### 8.2. Mandatory for Level 2+

Адаптеры Level 2 и выше MUST обеспечивать Q6-координату в каждом 
[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) через `metadata["q6"]`.

### 8.3. Q6 Mapping Rules

Каждый format определяет правило проекции своих native-сущностей в 
Q6. Правило MUST быть задокументировано в passport в разделе 
"Q6-отображение".

Примеры правил (из reference implementation):

| Format | Правило |
|--------|---------|
| `info1` | `alpha + 4` → 3 старших бита, остальные биты по категории |
| `pro2` | нативные Q6-координаты (Q6 — первичный концепт pro2) |
| `meta` | `hex_id - 1 → bin(6)` (гексаграмма 1 → `000000`, 64 → `111111`) |
| `data7` | `порядковый номер % 64 → bin(6)` |

Формат допускает явное указание `"не определено"`, если Q6-маппинг 
не применим (Level 1 репо MAY не иметь Q6).

### 8.4. Q6-Neighbors (Hamming Distance)

Два Q6-концепта считаются **соседями на расстоянии N**, если их 
Q6-координаты различаются ровно в N битах.

Portal MUST предоставлять функцию `q6_neighbors(bits, max_distance)` 
возвращающую все вершины в пределах Хэмминг-расстояния.

Pseudo-code:

```python
def q6_neighbors(bits: str, max_distance: int) -> list[str]:
    """BFS по 6-битному гиперкубу. Returns all vertices within max_distance."""
    assert len(bits) == 6
    assert all(c in "01" for c in bits)
    
    visited = {bits: 0}
    queue = [bits]
    
    while queue:
        current = queue.pop(0)
        current_dist = visited[current]
        if current_dist >= max_distance:
            continue
        
        for i in range(6):
            neighbor = current[:i] + ("1" if current[i] == "0" else "0") + current[i+1:]
            if neighbor not in visited:
                visited[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    return list(visited.keys())
```

### 8.5. CA-Class Mapping (Informative)

Вершины Q6 MAY маппиться на классы клеточных автоматов Вольфрама 
(Class I–IV). Это не обязательно, но RECOMMENDED для экосистем, 
интегрирующих symbolic и dynamical angles:

- **Class I** (стационарные) — стабильные концепты (базовые 
  алгоритмы, определения)
- **Class II** (периодические) — методология, архетипы
- **Class III** (хаотические) — конфликт, разрушение
- **Class IV** (сложные, edge of chaos) — синтез, emergent properties

---

<!-- similar-docs -->

---

**Похожие документы:**
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [82-7-portalentry-structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md)
- [08-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- [19-7-portalentry-structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)

