# evaluate-tech

Оценка одной технологии для использования в Svyazi 2.0 / Lorenzo.

## Когда использовать

- "стоит ли брать ClickHouse"
- "оцени Yodoca для memory layer"
- "подходит ли X для Y"
- "плюсы/минусы Z"

## Шаги

1. **Собрать факты о технологии**
   ```bash
   find docs -iname "*<tech>*"
   python scripts/improve_passage_retrieval.py --query "<tech>" --top 10
   ```

2. **Базовая карточка**
   - Версия, лицензия, язык, репо
   - Зрелость (commits/year, releases, последний релиз)
   - Сообщество (★, ответы maintainer'ов)
   - Документация (хорошая / посредственная / плохая)

3. **Применимость к нашим задачам**

   Использовать матрицу:

   | Капабилити (нужно нам) | Покрывается? | Как |
   |---|---|---|
   | [X] | ✅ | [нативно / через плагин] |
   | [Y] | ⚠️ | [нужна доработка] |
   | [Z] | ❌ | [не покрывается] |

4. **Tech Radar позиция**
   - **Adopt** — производственно зрелая, в нашей экосистеме можно использовать
   - **Trial** — стоит попробовать в одном проекте
   - **Assess** — изучить, может пригодиться
   - **Hold** — избегать (объяснить почему)

5. **Риски использования**
   ```bash
   Read: docs/RISK_REGISTER.md
   ```
   Какие риски усугубляет, какие создаёт.

6. **Альтернативы**
   ```bash
   python scripts/improve_faceted_search.py --query "<категория>"
   ```
   Минимум 2 альтернативы с пояснением «когда лучше».

7. **Создать запись в Tech Radar**
   ```bash
   python scripts/improve_template_init.py --type tech-radar-entry \
     --slug docs/tech-radar/entries/<tech>.md \
     --vars tech_name="<tech>" quadrant=tools ring=trial
   ```

8. **Создать ADR если есть commitment**
   ```bash
   python scripts/improve_template_init.py --type decision-record \
     --slug docs/decisions/ADR-NNNN.md \
     --vars adr_id=ADR-NNNN title="Использовать <tech>"
   ```

## Чеклист «зрелости» технологии

- [ ] Релиз ≥ 1.0
- [ ] Активность: commit за последний месяц
- [ ] Не от 1 автора (минимум 3 contributor'a активных)
- [ ] Issue response time < 1 неделя
- [ ] Docs покрывают 80% API
- [ ] Тесты в CI
- [ ] Лицензия совместима с нашими

## Связанные скилы
- [`compare`](compare.md) — сравнить с альтернативой
- [`design-ensemble`](design-ensemble.md) — после оценки добавить в ансамбль
- [`track-decisions`](track-decisions.md) — посмотреть, оценивали ли уже
