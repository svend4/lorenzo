# plan-mvp

Планирование MVP/прототипа из имеющихся компонентов и решений.

## Когда использовать

- "составь план MVP"
- "что нужно для прототипа Svyazi"
- "как собрать MVP из имеющихся проектов"
- "минимальный пайплайн для X"

## Шаги

1. **Уточнить цели MVP**
   - Какую задачу должен решать прототип
   - Метрика успеха («Bescheid распарсен правильно в 80%», «100 запросов/сек»)
   - Срок («2 недели», «спринт»)
   - Бюджет (LLM-tokens, локальное железо)

2. **Подобрать компоненты**

   Использовать карту слоёв:
   - Memory: `docs/05-habr-projects/memory/`
   - Knowledge: `docs/05-habr-projects/knowledge/`
   - Ingestion: `docs/svyazi-2-0/components/ingestion-*.md`
   - Orchestration: `docs/svyazi-2-0/components/orchestration-*.md`

   ```bash
   python scripts/improve_faceted_search.py --type projects --section "05-habr-projects"
   ```

3. **Проверить совместимость**

   ```bash
   Read: docs/COMPONENT_MATRIX.md
   ```

   Найти 3-5 компонентов с пересечением капабилити.

4. **Создать план через шаблон**

   ```bash
   python scripts/improve_template_init.py --type ensemble \
     --slug docs/svyazi-2-0/prototype/mvp-NNN.md \
     --vars ensemble_name="MVP Bescheid Parser" task="..." mvp_phase=1
   ```

5. **Проработать MVP-шаги**

   Декомпозиция по фазам:
   - **Фаза 0 — подготовка** (1-2 дня): репо, окружение, контакты
   - **Фаза 1 — minimal vertical slice** (3-5 дней): один сценарий end-to-end
   - **Фаза 2 — расширение** (1-2 недели): дополнительные сценарии
   - **Фаза 3 — оценка** (3-5 дней): метрики, ретро, решение go/no-go

6. **Идентифицировать риски**

   ```bash
   Read: docs/RISK_REGISTER.md
   ```

   Для каждого риска касающегося MVP — митигация.

7. **Создать action items**

   - Контакты, которым написать (`propose-collaboration`)
   - Зависимости для установки
   - Тесты, которые написать

8. **Финальный артефакт:**

   ```markdown
   # MVP: [Название]

   **Цель:** [конкретная]
   **Срок:** [дата]
   **Метрика успеха:** [значение]

   ## Состав
   | Слой | Компонент | Статус |
   |------|-----------|--------|
   | memory | Yodoca | известен, не тестировали |
   | ... | ... | ... |

   ## Фазы
   ### Фаза 0
   ...

   ## Риски и митигация
   ...

   ## Open questions
   ...
   ```

## Связанные скилы
- [`design-ensemble`](design-ensemble.md) — детальный дизайн ансамбля
- [`evaluate-tech`](evaluate-tech.md) — оценить кандидата на компонент
- [`propose-collaboration`](propose-collaboration.md) — кому писать
