# design-ensemble

Дизайн ансамбля компонентов под конкретную задачу Svyazi 2.0.

## Когда использовать

- "собери ансамбль для слоя X"
- "какие компоненты подходят для Y"
- "придумай комбинацию проектов под задачу Z"

## Шаги

1. **Уточнить задачу**
   - Слой (memory / knowledge / orchestration / ingestion / ui)
   - Что входит/выходит
   - Ограничения: лицензия, язык, перформанс
   - Сценарии использования

2. **Составить требования**

   | Капабилити | Обязательно | Желательно |
   |------------|-------------|-----------|
   | [Capability 1] | ✓ | |
   | [Capability 2] | | ✓ |

3. **Подобрать кандидатов**
   ```bash
   Read: docs/COMPONENT_MATRIX.md          # уже размеченные
   python scripts/improve_faceted_search.py --type projects --section "05-habr-projects/<layer>"
   ```

4. **Проверить совместимость**
   - Лицензии (можно ли смешивать MIT + AGPL?)
   - Языки (Python + Rust = FFI / IPC)
   - Зрелость (production-stable не сочетать с experimental)

5. **Спроектировать контракт**
   ```yaml
   ensemble:
     name: "...":
     layer: "..."
     components:
       - name: A
         role: ingestion
         interface: HTTP REST
       - name: B
         role: storage
         interface: Postgres
       - name: C
         role: query
         interface: gRPC
     data_flow:
       - source: A
         sink: B
         format: JSON
       - source: B
         sink: C
         format: SQL
   ```

6. **Создать через шаблон**
   ```bash
   python scripts/improve_template_init.py --type ensemble \
     --slug docs/svyazi-2-0/ensembles/<slug>.md \
     --vars ensemble_name="..." task="..."
   ```

7. **Валидация на 5 угроз**
   - **Single-author bus factor:** ни один компонент не зависит от 1 автора
   - **License lock-in:** замена возможна
   - **Ops complexity:** не нужен PhD для развёртывания
   - **Backward incompat:** упоминается в `RISK_REGISTER.md`?
   - **Performance bottleneck:** есть метрики?

8. **MVP-roadmap (3 фазы):**
   - **Фаза 1:** только ядро (2-3 компонента)
   - **Фаза 2:** добавить интеграции
   - **Фаза 3:** полный ансамбль

## Связанные скилы
- [`plan-mvp`](plan-mvp.md) — план развёртывания
- [`evaluate-tech`](evaluate-tech.md) — оценить отдельный кандидат
- [`compare`](compare.md) — выбор между кандидатами
