
<!-- summary -->
> Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Svyazi как базовый паттерн остаётся авторским закрытым п
**Проекты:** Svyazi, mclaude, AI Factory, Rufler, NGT Memory, AutoResearch, Whisper, Yttri

---
<!-- tags: memory, rag, orchestration, ingestion, local-first, architecture, roadmap, self-improvement, collaboration -->



## Ограничения, лицензии и что пока лучше не склеивать

Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Svyazi как базовый паттерн остаётся авторским закрытым прототипом в просмотренных материалах, NGT Memory использует BSL 1.1 и прямо говорит о бесплатности для личных проектов, а по ряду других систем лицензия в просмотренных источниках либо не акцентирована, либо требует проверки уже на стороне репозитория и бизнес‑сценария. Это означает, что для коммерчески чувствительного стека ранний выбор memory‑слоя — не только инженерный, но и лицензионный. citeturn41search0turn22view5turn18search1turn15search3

Второе ограничение относится к оркестрации. Хотя mclaude, AI Factory, Rufler и Sequential выглядят очень привлекательно, их не стоит собирать все сразу в один контур. mclaude хорошо решает синхронизацию нескольких сессий; AI Factory — spec/pipeline/patch evolution; Rufler — YAML‑рой; Sequential — reviewer‑логика. Если попытаться включить все четыре слоя одновременно до стабилизации card/evidence contracts, получится “очень умный операционный шум”. Поэтому на ранней стадии разумнее выбрать **один основной orchestration spine** и один review pattern, а не строить суперкомбайн. citeturn20view2turn20view3turn20view4turn20view11

Третье ограничение касается voice/local‑first mesh. Голосовой вход очень соблазнительно добавляет “живую ткань” системы, но именно здесь легко утонуть в необязательной инженерии: streaming transcription, diarization, semantic post‑processing, multi-device sync, offline UX, conflict resolution. Для первой публично полезной версии достаточно не “идеальной диктовки”, а простого и надёжного пути `voice → episode card → review`. Всё, что дальше, лучше добавлять после того, как уже появилась ценность от графа, evidence и review. Такой порядок согласуется и с Yttri‑подходом к workspace вокруг записей, и с простыми локальными whisper‑сценариями, и с идеей local-first sync как следующего, а не первого слоя сложности. citeturn21view10turn21view11turn35search0turn11search11

Последняя развилка — это уровень “самоулучшения”. AutoResearch и Sequential выглядят очень мощно, но только после того, как появилась **метрика качества**, benchmark set и отчетливое понимание, что считать регрессией. До этого автоматическая оптимизация будет скорее производить вариации, чем устойчивые улучшения. Поэтому self-improvement контур разумно активировать только тогда, когда вы уже можете померить quality of match, quality of evidence и false positive rate по review‑очереди. Это не консерватизм, а инженерная трезвость, полностью согласующаяся с духом AutoResearch — “изменяй только то, что умеешь измерить и откатывать”. citeturn20view19turn20view11turn20view6

Итоговое продолжение therefore выглядит так. Лучший следующий шаг — **не искать ещё двадцать новых проектов**, а собрать второй, более строгий слой поверх уже найденных: Card Envelope, Evidence Envelope, Memory Write Policy, Skill Policy и Review Record. На этом основании уже можно по‑настоящему проверить, превращается ли набор “скромных” pet‑проектов с Хабра в новую систему свойств — discovery, explainability, local ownership, controlled memory и cheap/safe execution. Если этот слой заработает, тогда уже есть смысл возвращаться к расширению ансамблей в сторону federation, richer voice UX и self-improving research loop. citeturn41search0turn27view0turn20view5turn21view0turn39view1turn20view10
