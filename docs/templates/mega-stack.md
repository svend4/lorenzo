---
template: mega-stack
version: "1.0"
stack_name: "[Название стека]"
domain: "[legal-AI | knowledge-OS | agent-platform]"
total_components: 0
maturity: design
target_scale: "[1k|1M|1B] documents"
created: 2026-04-29
tags: [mega-stack, архитектура]
---

# Mega-stack: [Название]


<!-- summary: Полный стек для класса задач X -->
<!-- tags: mega-stack, архитектура -->

## Назначение

**Класс задач:** [legal-AI / knowledge-OS / etc.]
**Целевой объём:** [1M документов]
**SLA:** latency p99 < 500ms, availability 99.9%

## Слои стека (сверху вниз)

### 1. UI / Client
| Компонент | Лицензия | Зрелость |
|-----------|----------|----------|
| | | |

### 2. Agent Layer
| Компонент | Тип агента | Откуда |
|-----------|------------|--------|
| | | |

### 3. Orchestration
| Компонент | Паттерн | … |
|-----------|---------|---|

### 4. RAG / Search
| Компонент | Тип | Узлы |
|-----------|-----|------|

### 5. Knowledge Graph
| Компонент | … | … |

### 6. Memory
| Компонент | Hot/Slow | … |

### 7. Storage (OLTP)
| Компонент | … | … |

### 8. Storage (OLAP)
| Компонент | … | … |

### 9. Ingestion
| Компонент | Форматы | … |

### 10. Infra
| Компонент | … | … |

## Cross-layer контракты

| Слой → слой | Формат | Протокол |
|-------------|--------|----------|
| Ingestion → Storage | JSON | HTTP REST |
| Storage → RAG | … | … |

## Roadmap по фазам

### Phase 1 — MVP (2-4 недели)
**Цель:** end-to-end вертикальный срез
**Включено:** [N компонентов]

### Phase 2 — Beta (1-2 месяца)
**Включено дополнительно:** [M]

### Phase 3 — RC (3 месяца)

### Phase 4 — GA (6+ месяцев)

## Стоимость

| Категория | $/месяц |
|-----------|---------|
| LLM API | |
| Хостинг | |
| Платные лицензии | |
| **Итого** | |

## Риски и митигации

| Риск | Severity | Митигация |
|------|----------|-----------|
| | | |

## Альтернативные стеки

| Альтернатива | Когда лучше |
|--------------|-------------|
| | |

## Связанные ансамбли

- [`docs/03-technology-combinations/combinations/...`](...)

---
_Создано: 2026-04-29_

<!-- see-also -->

---

**Смотрите также:**
- [ensemble](docs/templates/ensemble.md)
- [project-component](docs/templates/project-component.md)
- [tech-radar-entry](docs/templates/tech-radar-entry.md)
