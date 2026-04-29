# Дерево метрик Svyazi 2.0

> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

6. Метрики, без которых Svyazi‑2.0 нельзя масштабировать

Для Svyazi‑2.0 нужна не одна “accuracy”, а дерево метрик.

| Уровень | Метрика | Что измеряет
| Extraction | schema_valid_rate | Доля LLM‑ответов, прошедших JSON/schema validation
| Normalization | canonicalization_rate | Доля skills/company/roles, сведённых к канону
| Evidence | evidence_coverage | Доля выводов с source/page/span/bbox
| Matching | match_precision@k | Сколько top‑k рекомендаций человек признал полезными
| Matching | serendipity_score | Сколько рекомендаций были неочевидны, но полезны
| Memory | proposal_to_fact_rate | Сколько гипотез после review стали фактами
| Memory | false_association_rate | Сколько ассоциаций отклонено как шум
| Safety | unsafe_tool_block_rate | Сколько risky actions остановлено policy/HITL
| Cost | cost_per_card | Цена обработки одной карточки
| AgentOps | trace_completeness | Доля операций с полным trace envelope
| UX | time_to_explain_match | За сколько секунд пользователь понимает “почему эта связь”

Особенно важны false_association_rate и evidence_coverage. Без них система легко станет “магическим рекомендателем”, которому нельзя доверять.
