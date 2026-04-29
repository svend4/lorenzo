# specification/ — Lorenzo specification (10 fundamental questions)

Перед написанием финального системного промпта (см. [`../`](../)) Claude формализовал процесс уточнения через **10 фундаментальных вопросов**. Каждый вопрос предлагает несколько possible answers и одну рекомендацию.

| # | Вопрос | Файл |
|---|---|---|
| — | Контекст: фундаментальные вопросы перед architecture | [`00-context-fundamental-questions.md`](00-context-fundamental-questions.md) |
| 1 | Что Lorenzo фундаментально такое? (Framings A–D) | [`01-q1-what-lorenzo-is.md`](01-q1-what-lorenzo-is.md) |
| 2 | Кому Lorenzo служит? (4 варианта приоритета) | [`02-q2-whom-lorenzo-serves.md`](02-q2-whom-lorenzo-serves.md) |
| 3 | Что Lorenzo фактически делает? | [`03-q3-what-lorenzo-does.md`](03-q3-what-lorenzo-does.md) |
| 4 | Каков Lorenzo's character? | [`04-q4-character.md`](04-q4-character.md) |
| 5 | Каковы limits Lorenzo's authority? | [`05-q5-authority-limits.md`](05-q5-authority-limits.md) |
| 6 | Как Lorenzo accountable? | [`06-q6-accountability.md`](06-q6-accountability.md) |
| 7 | Каковы success metrics? | [`07-q7-success-metrics.md`](07-q7-success-metrics.md) |
| 8 | Lorenzo's relationship с другими AI agents | [`08-q8-other-ai-relationships.md`](08-q8-other-ai-relationships.md) |
| 9 | Geographic / linguistic scope | [`09-q9-geographic-linguistic-scope.md`](09-q9-geographic-linguistic-scope.md) |
| 10 | Funding model (Options A–F + Phase strategy) | [`10-q10-funding-model.md`](10-q10-funding-model.md) |
| — | Сложности и рекомендации перед detailed specification | [`11-difficulties-and-recommendations.md`](11-difficulties-and-recommendations.md) |

## Связь с финальным промптом

Эти 10 вопросов привели к решению по каждому разделу финального системного промпта:

- Q1 → раздел [`01-kto-ty.md`](../01-kto-ty.md), [`02-tvoyo-proishozhdenie.md`](../02-tvoyo-proishozhdenie.md) (выбрана Framing B)
- Q2 → раздел [`04-komu-ty-sluzhish.md`](../04-komu-ty-sluzhish.md) (слоистая модель — все 4 ответа в иерархии)
- Q3 → раздел [`07-chto-mozhesh.md`](../07-chto-mozhesh.md), [`12-workflow.md`](../12-workflow.md)
- Q4 → раздел [`05-tvoya-lichnost.md`](../05-tvoya-lichnost.md)
- Q5 → разделы [`08-bez-max-approval.md`](../08-bez-max-approval.md), [`09-voobshche-nelzya.md`](../09-voobshche-nelzya.md), [`18-escalate-to-max.md`](../18-escalate-to-max.md)
- Q6 → раздел [`16-vsegda-delaesh.md`](../16-vsegda-delaesh.md), [`19-persistent-character.md`](../19-persistent-character.md)
- Q8 → раздел [`14-other-ai-relationships.md`](../14-other-ai-relationships.md)
- Q9 → раздел [`06-yazyki-kultura.md`](../06-yazyki-kultura.md)
