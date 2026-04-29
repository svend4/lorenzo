# Пара 5 — Голосовой ввод × Локальная память

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Yodoca, Whisper

---
<!-- tags: memory, knowledge, local-first, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 5. Голосовой ввод × Локальная память

Локальный голосовой ввод Whisper + Ollama (https://habr.com/ru/articles/1009538/) — push-to-talk с Pause-key, Whisper large-v3-turbo на NVIDIA 16GB или Apple Silicon M3, текст вставляется в любое поле, работает с Cursor/ChatGPT/Slack. Whisper.cpp Гергenov-а (тот же автор что llama.cpp). Голосовой ввод 2026: WisprFlow, Handy, OpenWhispr, GigaAM v3 (https://habr.com/ru/articles/1024634/). Локальный транскрибатор с диаризацией ЮMoney (https://habr.com/ru/companies/yoomoney/articles/1012870/) — Whisper + wespeaker-voxceleb-resnet34-LM + summary через LLM.

Дети:

Voice → Obsidian через MCP — Handy push-to-talk + Whisper.cpp локально + кастомный MCP-сервер, который пишет в твой vault как заметку с datetime, diarization-меткой и автоэкстрагированными wikilinks. Зажал клавишу после заседания, наговорил 10 минут — утром в vault'е лежит заметка по делу с проставленными ссылками на участников, статьи закона, дату следующего заседания.

Court hearing analyser — запись с Sozialgericht проходит Whisper + voice-эмбеддинги ЮMoney → разбивается по спикерам (судья / KSV / клиент / ты) → каждый блок передаётся в соответствующий skill. Получаешь не просто транскрипт, а структурированный протокол с automatic action items: «судья запросил Anlage X к следующему заседанию», «KSV возражают по пункту Y», «клиент подтвердил Z».

Daily voice journal — каждый вечер 5 минут устного рассказа о дне → Whisper транскрибирует → LLM извлекает события и сущности → Yodoca-консолидатор ночью кристаллизует факты → утром в Obsidian новые wikilinks. Life-log + research-log в одном пайплайне без печати. Особенно ценно для AI/ML research: идея о Q6 захвачена сразу, ничего не теряется.

<!-- see-also -->

---

**Смотрите также:**
- [4-speech-to-text-llm](docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md)
- [3-discovery-research](docs/habr-unique-projects/final-ensembles/3-discovery-research.md)
- [2-document-rag](docs/habr-unique-projects/deep-pairs/2-document-rag.md)
- [07-crawl4ai-docling-yodoca-consolidator](docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [4-speech-to-text-llm](docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md) (сходство 0.42)
- [3-discovery-research](docs/habr-unique-projects/final-ensembles/3-discovery-research.md) (сходство 0.20)
- [2-document-rag](docs/habr-unique-projects/deep-pairs/2-document-rag.md) (сходство 0.18)

