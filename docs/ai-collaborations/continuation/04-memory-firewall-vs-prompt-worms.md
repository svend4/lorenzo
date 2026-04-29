# Memory Firewall против prompt worms (ансамбль I)

> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

4. Четвёртый новый слой: защита от prompt worms и заражения памяти

Чем больше Svyazi‑2.0 становится агентной системой, тем больше она становится потенциальным переносчиком атак. На Хабре есть сильная линия материалов про Prompt Worms и аудит OpenClaw. Главная мысль: если агент читает недоверенный контент, имеет доступ к данным и может отправлять сообщения наружу, он превращается в вектор атаки. В статье про Prompt Worms отдельно выделен риск persistent memory: вредоносные инструкции могут быть записаны в долговременную память фрагментами и позже собраны в исполняемое поведение. Habr

Аудит OpenClaw показал практический слой этой проблемы: zero‑sanitization pipeline, timeout‑as‑approval, arbitrary exec через plugin system, plaintext credential storage, memory exfiltration/injection, default‑open command gating и другие критические/high‑risk проблемы. Habr

Ансамбль I — Memory Firewall

Родители: Svyazi privacy‑by‑design + SENTINEL/Prompt Worms lessons + LangGraph HITL + Card/Evidence/Memory contracts.

Что рождается: память, в которую нельзя просто “записать всё, что сказал агент”.

Mermaid

Практическое правило: внешний текст не должен иметь права становиться instruction memory. Он может стать episode, source, evidence, observation, но не system rule и не trusted fact без review. Это особенно важно для Svyazi‑2.0, потому что профили людей, чаты, PDF, сайты, GitHub‑issues и сообщения агентов будут смешиваться в одном graph‑пространстве.
