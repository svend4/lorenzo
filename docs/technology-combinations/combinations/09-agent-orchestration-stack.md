# Комбинация 9: Agent Orchestration Stack

> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Agent-Bridge (habr.com/ru/articles/1016456/) - визуальное управление десятками CLI агентов из браузера, персистентные сессии

Conductor (habr.com/ru/articles/1001478/) - $2.8M YC, macOS-native parallel agent manager, 250% рост/месяц

Sequential Protocol (Dochkina's 8-16 small agents, 44% quality boost)

Дети:

Visual Multi-Agent IDE с persistent workspace

Agent-Bridge предоставляет infinite canvas для визуализации

Conductor управляет параллельным выполнением (workspace per task)

Sequential обеспечивает chain-of-agents без coordinator

Итог: один разработчик видит 10-20 агентов на доске, каждый в своём контейнере, работающих цепочкой

Cross-machine distributed agents с браузерным dashboard

Agent-Bridge + несколько нод (home PC + VPS + Cloud)

Conductor orchestrates tasks distribution

Sequential ensures chain completion across machines

ROI: Full stack development на $700/мес вместо $20k/мес team

Уникальность: Conductor — macOS only, Agent-Bridge — browser-based + multi-machine. Вместе = remote development paradise. Sequential устраняет bottleneck координатора.
