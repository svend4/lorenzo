# 8. Q6 Space (Normative)

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 8. Q6 Space (Normative)

### 8.1. Definition

Q6 — 6-мерное бинарное пространство {0,1}⁶. Содержит 64 вершины.

Каждая вершина представлена 6-битной строкой, например `"010100"`.

### 8.2. Mandatory for Level 2+

Адаптеры Level 2 и выше MUST обеспечивать Q6-координату в каждом 
PortalEntry через `metadata["q6"]`.

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
assert len(bits) = 6
assert all(c in "01" for c in bits)

visited = {bits: 0}
queue = [bits]

while queue:
current = queue.pop(0)
current_dist = visited[current]
if current_dist >= max_distance:
continue

for i in range(6):
neighbor = current[:i] + ("1" if current[i] = "0" else "0") + current[i+1:]
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

<!-- see-also -->

---

**Смотрите также:**
- [83-8-q6-space-normative](docs/02-anthropic-vacancies/83-8-q6-space-normative.md)
- [07-portal-entry](docs/nautilus/npp-v1-1/07-portal-entry.md)
- [20-adr-002-q6-first-class](docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md)
- [13-rest-api](docs/nautilus/npp-v1-1/13-rest-api.md)

