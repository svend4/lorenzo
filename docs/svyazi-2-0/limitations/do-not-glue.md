# Что пока лучше не склеивать

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Ограничения, лицензии и что пока лучше не склеивать».
**Проекты:** mclaude, AI Factory, Rufler, AutoResearch, Whisper, Yttri

---
<!-- tags: memory, rag, orchestration, local-first, self-improvement -->




> Источник: `deep-research-report (3).md`, раздел «Ограничения, лицензии и что пока лучше не склеивать».

## Оркестрация — выбрать один spine

Хотя mclaude, AI Factory, Rufler и Sequential выглядят очень привлекательно, их не стоит собирать все сразу в один контур. mclaude хорошо решает синхронизацию нескольких сессий; AI Factory — spec/pipeline/patch evolution; Rufler — YAML‑рой; Sequential — reviewer‑логика. Если попытаться включить все четыре слоя одновременно до стабилизации card/evidence contracts, получится «очень умный операционный шум». Поэтому на ранней стадии разумнее выбрать **один основной orchestration spine** и один review pattern, а не строить суперкомбайн. citeturn20view2turn20view3turn20view4turn20view11

## Voice/local‑first mesh — не идеализировать

Голосовой вход очень соблазнительно добавляет «живую ткань» системы, но именно здесь легко утонуть в необязательной инженерии: streaming transcription, diarization, semantic post‑processing, multi-device sync, offline UX, conflict resolution. Для первой публично полезной версии достаточно не «идеальной диктовки», а простого и надёжного пути `voice → episode card → review`. Всё, что дальше, лучше добавлять после того, как уже появилась ценность от графа, evidence и review. Такой порядок согласуется и с Yttri‑подходом к workspace вокруг записей, и с простыми локальными whisper‑сценариями, и с идеей local-first sync как следующего, а не первого слоя сложности. citeturn21view10turn21view11turn35search0turn11search11

## Self‑improvement — только после метрики

AutoResearch и Sequential выглядят очень мощно, но только после того, как появилась **метрика качества**, benchmark set и отчётливое понимание, что считать регрессией. До этого автоматическая оптимизация будет скорее производить вариации, чем устойчивые улучшения. Поэтому self-improvement контур разумно активировать только тогда, когда вы уже можете померить quality of match, quality of evidence и false positive rate по review‑очереди. Это не консерватизм, а инженерная трезвость, полностью согласующаяся с духом AutoResearch — «изменяй только то, что умеешь измерить и откатывать». citeturn20view19turn20view11turn20view6

<!-- see-also -->

---

**Смотрите также:**
- [14-limitations](docs/01-svyazi/14-limitations.md)
- [license-tree](docs/svyazi-2-0/limitations/license-tree.md)
- [14-ограничения-лицензии-и-что-пока-лучше-не-склеивать](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)
- [conclusions](docs/svyazi-2-0/limitations/conclusions.md)

