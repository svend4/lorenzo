# Приватность: local-first by default

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «Безопасность, приватность и бюджетный роутинг».
**Проекты:** AgentFS

---
<!-- tags: security, knowledge, local-first -->




> Источник: `deep-research-report (1).md`, раздел «Безопасность, приватность и бюджетный роутинг».

С точки зрения приватности лучший режим для первых версий — **local-first by default, cloud by exception**. Голос, стенограммы, первичные профили, внутренние документы и memory‑база должны оставаться локально; в облако есть смысл отправлять только самые сложные этапы, где действительно нужен дорогой reasoning. Такой подход уже поддерживают и локальные voice‑пайплайны, и AgentFS/knowledge‑workspace‑подходы, и budget/privacy‑режимы RLM‑Toolkit. citeturn21view10turn35search0turn27view0turn20view18

<!-- see-also -->

---

**Смотрите также:**
- [budget-routing](docs/svyazi-2-0/security/budget-routing.md)
- [06-security-privacy](docs/01-svyazi/06-security-privacy.md)
- [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md)
- [voice-stack](docs/svyazi-2-0/components/voice-stack.md)

