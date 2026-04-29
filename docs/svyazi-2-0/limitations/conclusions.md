# Итоговые выводы и порядок сборки

> Источники: `deep-research-report (1).md` (раздел «Выводы») и итог из `deep-research-report (3).md`.

## Главный вывод первой части

По итогам поиска видно, что **Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей**, не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG и не оркестрация по отдельности: все они уже представлены на Хабре и в репозиториях. Дефицитный слой — **правильная сборка**: где CardIndex остаётся source of truth, где память умеет и усиливать, и забывать, где retrieval остаётся доказуемым, где агентность не ломает безопасность, и где стоимость не взрывается ещё до первой полезной операции. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn20view6turn20view11turn20view10turn39view1turn39view0

## Порядок практической сборки

1. **Svyazi + AgentFS + NGT/Yodoca + LiteParse** — это даёт уже полезный MVP.
2. **Добавить AI Factory / mclaude / Rufler / Sequential** как build‑ и moderation‑контур.
3. **Подключить voice/local-first sync** и только потом AutoResearch.

Другими словами, наиболее реалистичная стратегия — сначала собрать **машину обнаружения и объяснения коллабораций**, а уже затем превращать её в полностью самоулучшающуюся агентную фабрику. Именно такой порядок лучше всего соответствует зрелости найденных проектов и снижает интеграционный риск. citeturn41search0turn27view0turn21view0turn22view4turn20view5turn20view3turn20view2turn20view4turn20view11turn21view10turn11search11turn20view19

## Главный вывод второй части

Лучший следующий шаг — **не искать ещё двадцать новых проектов**, а собрать второй, более строгий слой поверх уже найденных: Card Envelope, Evidence Envelope, Memory Write Policy, Skill Policy и Review Record. На этом основании уже можно по‑настоящему проверить, превращается ли набор «скромных» pet‑проектов с Хабра в новую систему свойств — discovery, explainability, local ownership, controlled memory и cheap/safe execution. Если этот слой заработает, тогда уже есть смысл возвращаться к расширению ансамблей в сторону federation, richer voice UX и self-improving research loop. citeturn41search0turn27view0turn20view5turn21view0turn39view1turn20view10
