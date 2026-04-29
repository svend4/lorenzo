# propose-mega-stack

Предложение «мега-стека» — полного технологического стека для класса задач.

## Когда использовать

- "предложи mega-stack для X"
- "полный стек для legal AI"
- "что нам собрать для production"
- "от чего стартовать в новом домене"

## Шаги

1. **Уточнить домен и задачу**
   - Класс задач (legal-AI, knowledge-OS, agent-platform)
   - Целевые объёмы (1k / 1M / 1B документов)
   - SLA (latency, availability, durability)

2. **Изучить уже существующие mega-stack'и**
   ```bash
   find docs/03-technology-combinations -name "*mega*"
   find docs/technology-combinations/mega-stacks -name "*.md"
   ```

3. **Составить слои сверху вниз**

   | Слой | Что нужно | Кандидаты (из репо) |
   |---|---|---|
   | UI / Client | Интерфейс пользователя | … |
   | Agent Layer | Агенты с памятью | Companion / Representative |
   | Orchestration | Workflow, retries | Sequential / Coordinator |
   | RAG / Search | Поиск по корпусу | Hybrid RAG, Graph RAG |
   | Knowledge Graph | Сущности, связи | … |
   | Memory | Hot/Slow path | Yodoca, NGT Memory |
   | Storage | OLTP + OLAP | Postgres + ClickHouse |
   | Ingestion | PDF / HTML → text | Crawl4AI, Unstructured |
   | Infra | Контейнеры, сеть | Docker, Kubernetes |

4. **Заполнить кандидатами на каждый слой**
   - Если есть готовое — взять
   - Если нет — пометить «нужно искать» и `find-gaps` запустить

5. **Проверить cross-layer совместимость**
   ```bash
   Read: docs/COMPONENT_MATRIX.md
   ```

6. **Roadmap по фазам**
   - **Phase 1 (MVP):** только базовые слои (Storage + Ingestion + Search)
   - **Phase 2 (Beta):** + Memory + Orchestration
   - **Phase 3 (RC):** + Agent Layer + Knowledge Graph
   - **Phase 4 (GA):** + UI / SLA / scale

7. **Финансовый snapshot**
   - Стоимость LLM / месяц
   - Хостинг
   - Лицензии (если есть платные компоненты)

8. **Создать запись**
   ```bash
   python scripts/improve_template_init.py --type ensemble \
     --slug docs/03-technology-combinations/mega-stacks/<slug>.md \
     --vars ensemble_name="Mega-stack для <домен>" task="..." mvp_phase=1
   ```

## Антипаттерны
- ❌ «Слепить из всего»: 20 компонентов в стеке = адский ops
- ❌ Без SLA таргетов — нет критериев выбора
- ❌ Без бюджета — не видно reality check

## Связанные скилы
- [`design-ensemble`](design-ensemble.md) — для одного слоя
- [`evaluate-tech`](evaluate-tech.md) — для одного кандидата
- [`plan-mvp`](plan-mvp.md) — переход от стека к плану
