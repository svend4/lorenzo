---
title: "Ансамбль 3 — Forensic RAG"
tags:
  - ai-collaborations
date: 2026-04-29
---

# Ансамбль 3 — Forensic RAG

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** LiteParse, Legal RAG, Hybrid RAG, Graph RAG

---
<!-- tags: rag, knowledge, architecture, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

3. Forensic RAG: «RAG, которому можно верить глазами»

Родители: LiteParse research-docs + Hybrid RAG с pdfplumber + Legal RAG Challenge + Graph RAG + JuliaLM/NotebookLM-подход.

Обычный RAG часто отвечает правдоподобно, но плохо доказывает. На Хабре нашёлся набор кубиков для другой архитектуры: доказательный RAG с визуальными цитатами.

Research-docs от LlamaIndex/LiteParse — это Claude Code skill, который берёт папку с PDF/DOCX/PPTX/XLSX/изображениями, парсит документы и создаёт HTML-отчёт с цитатами и bounding box’ами прямо на странице PDF. Автор подчёркивает, что это критично для юридических документов, финансовых отчётов и регуляторики. Habr

Hybrid RAG knowledge base за 15 минут добавляет координатную подсветку источника через pdfplumber: ответ открывает PDF на нужной странице и подсвечивает конкретный фрагмент; также там есть двухстадийная логика — сначала ответ по всему пулу документов, потом диалог строго в выбранном документе. Habr

Legal RAG Challenge даёт строгую оценочную рамку: корпус PDF-документов, вопросы разных типов, page-level grounding, формула скоринга с детерминированной частью, LLM-судьёй, grounding factor, telemetry factor и TTFT factor. Habr

Graph RAG-система с точностью 96.7% решает другой класс проблем: связи, multi-hop reasoning, глобальные вопросы и кросс-языковые запросы; автор использует Skeleton Indexing, KNN-граф, PageRank и извлечение сущностей только из top-25% «скелетных» чанков. Habr

JuliaLM/аналог NotebookLM добавляет продуктовый слой: источники живут в блокноте постоянно, система сама решает, сколько контекста взять из каждого источника, плюс есть инсайты, заметки и флешкарточки. Habr

Что рождается при склейке:

Получается Forensic RAG — RAG не как чат, а как система расследования.

Схема:

LiteParse/pdfplumber → визуальные координаты → Hybrid retrieval → Graph RAG → answer-type scoring → HTML/PDF proof report

Дети этой связки:

Legal Evidence RAG — для судов, Bescheid, Sozialgericht, BSG, регуляторики: каждый тезис имеет страницу, координату, тип ответа, уровень уверенности и проверяемый источник.

Scientific Contradiction Finder — загрузить 40–100 статей и найти противоречия, повторяющиеся гипотезы, слабые доказательства, связанные методы.

Technical Docs Investigator — для больших кодовых/инженерных корпусов: «где в документации реально написано, что этот API deprecated?» — и сразу подсветка места.

Главное новое свойство: ответ можно проверить за секунду. Не «модель сказала», а «модель сказала, вот страница, вот прямоугольник, вот scoring, вот тип доказательства».

<!-- see-also -->

---

**Смотрите также:**
- [[B-forensic-rag]]
- [[7-domain-agent-app-factory]]
- [[8-budget-aware-intelligence-stack]]
- [[1-agentic-knowledge-os]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[7-domain-agent-app-factory]] (сходство 0.15)
- [[8-budget-aware-intelligence-stack]] (сходство 0.15)
- [[6-continuous-eval-loop]] (сходство 0.15)

