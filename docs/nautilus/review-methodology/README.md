# Трёхфазная методология Review в Nautilus

DHLab paper #2. Формальная методология для критически важных документов: параллельная разработка двух вариантов в разных ветках с последующей ручной консолидацией. Решает проблему «два Claude-агента производят частично пересекающийся материал с уникальными insights».

| # | Раздел | Файл |
|---|---|---|
| — | TL;DR | [`00-tldr.md`](00-tldr.md) |
| 1 | Контекст и мотивация | [`01-context-motivation.md`](01-context-motivation.md) |
| 2 | Формальный workflow | [`02-formal-workflow.md`](02-formal-workflow.md) |
| 3 | Принципы консолидации (Фаза C) | [`03-consolidation-principles.md`](03-consolidation-principles.md) |
| — | Вопрос: fallback‑ratio как критический или осмысленный? | [`04-fallback-ratio-question.md`](04-fallback-ratio-question.md) |
| 4 | Условия применимости | [`05-conditions-of-applicability.md`](05-conditions-of-applicability.md) |
| 5 | Связь с существующими методологиями | [`06-relation-existing-methodologies.md`](06-relation-existing-methodologies.md) |
| 6 | Почему это валидный паттерн для AI‑assisted workflows | [`07-why-valid-for-ai.md`](07-why-valid-for-ai.md) |
| 7 | Реализация в проекте Nautilus | [`08-implementation-nautilus.md`](08-implementation-nautilus.md) |
| 8 | Ограничения и открытые вопросы | [`09-limitations-open-questions.md`](09-limitations-open-questions.md) |
| 9 | Checklist применения методологии | [`10-checklist.md`](10-checklist.md) |
| 10 | Конкретный план применения к текущим документам | [`11-application-plan-current-docs.md`](11-application-plan-current-docs.md) |
| — | Appendix A: Шаблон для header warning | [`12-appendix-a-header-warning.md`](12-appendix-a-header-warning.md) |
| — | Appendix B: Примеры расхождений и их разрешения | [`13-appendix-b-examples.md`](13-appendix-b-examples.md) |
| — | Главные технические риски | [`14-main-technical-risks.md`](14-main-technical-risks.md) |
| — | Appendix C: История изменений методологии | [`15-appendix-c-history.md`](15-appendix-c-history.md) |
| — | Глоссарий | [`16-glossary.md`](16-glossary.md) |

## Главная идея

> Два независимых AI‑агента (Claude в разных ветках) производят два варианта документа. Различия — это не баг, а insights, которые могут быть утеряны. Phase C — ручная консолидация по чётким правилам.

Ровно тот «conflict resolution layer between sub‑agents», о котором говорилось на теоретическом уровне в обсуждениях multi-agent systems — здесь это построено на практике.
