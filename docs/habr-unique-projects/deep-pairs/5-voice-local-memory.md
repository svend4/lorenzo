# Пара 5 — Голосовой ввод × Локальная память

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Yodoca, Whisper

---
<!-- tags: memory, knowledge, local-first, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 5. Голосовой ввод × Локальная память

Локальный голосовой ввод Whisper + Ollama (https://habr.com/ru/articles/1009538/) — push-to-talk с Pause-key, Whisper large-v3-turbo на NVIDIA 16GB или Apple Silicon M3, текст вставляется в любое поле, работает с Cursor/ChatGPT/Slack. Whisper.cpp Гергenov-а (тот же автор что llama.cpp). Голосовой ввод 2026: WisprFlow, Handy, OpenWhispr, GigaAM v3 (https://habr.com/ru/articles/1024634/). Локальный транскрибатор с диаризацией ЮMoney (https://habr.com/ru/companies/yoomoney/articles/1012870/) — Whisper + wespeaker-voxceleb-resnet34-LM + summary через LLM.

Дети:

Voice → Obsidian через MCP — Handy push-to-talk + Whisper.cpp локально + кастомный MCP-сервер, который пишет в твой vault как заметку с datetime, diarization-меткой и автоэкстрагированными wikilinks. Зажал клавишу после заседания, наговорил 10 минут — утром в vault'е лежит заметка по делу с проставленными ссылками на участников, статьи закона, дату следующего заседания.

Court hearing analyser — запись с Sozialgericht проходит Whisper + voice-эмбеддинги ЮMoney → разбивается по спикерам (судья / KSV / клиент / ты) → каждый блок передаётся в соответствующий skill. Получаешь не просто транскрипт, а структурированный протокол с automatic action items: «судья запросил Anlage X к следующему заседанию», «KSV возражают по пункту Y», «клиент подтвердил Z».

Daily voice journal — каждый вечер 5 минут устного рассказа о дне → Whisper транскрибирует → LLM извлекает события и сущности → Yodoca-консолидатор ночью кристаллизует факты → утром в Obsidian новые wikilinks. Life-log + research-log в одном пайплайне без печати. Особенно ценно для AI/ML research: идея о Q6 захвачена сразу, ничего не теряется.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Пара 5 Голосовой ввод Локальная память"
```

## Смотрите также
- [4-speech-to-text-llm](../software-pairs/4-speech-to-text-llm.md)
- [3-discovery-research](../final-ensembles/3-discovery-research.md)
- [2-document-rag](2-document-rag.md)
- 07-crawl4ai-docling-[yodoca-consolidator](../../technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (11):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [source-projects](../../ai-collaborations/source-projects.md)
- [components-by-name](../../glossary/components-by-name.md)
- [2-document-rag](2-document-rag.md)
- _...ещё 3_


<!-- similar-docs -->

---

**Похожие документы:**
- [5-voice-local-memory](../../obsidian/habr-unique-projects/deep-pairs/5-voice-local-memory.md) (сходство 0.95)
- [4-speech-to-text-llm](../software-pairs/4-speech-to-text-llm.md) (сходство 0.45)
- [4-speech-to-text-llm](../../obsidian/habr-unique-projects/software-pairs/4-speech-to-text-llm.md) (сходство 0.44)

