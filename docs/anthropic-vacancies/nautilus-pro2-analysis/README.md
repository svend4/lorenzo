# nautilus-pro2-analysis/ — два «Наутилуса» в репозиториях svend4

В диалоге пользователь спросил про **два разных «Наутилуса»** в собственных репозиториях svend4: pro2 (YiJing-Transformer / NautilusMoME) и nautilus (мета-оркестратор репозиториев). Это **прямой источник идеи Nautilus Portal Protocol**.

| # | Раздел | Файл |
|---|---|---|
| — | Вопрос | [`00-question-two-nautiluses.md`](00-question-two-nautiluses.md) |
| 1 | Раковина наутилуса как scale invariance — две проекции одной метафоры | [`01-shell-metaphor-two-projections.md`](01-shell-metaphor-two-projections.md) |
| 2 | **Наутилус A: pro2 + meta** — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети) | [`02-nautilus-A-pro2-meta.md`](02-nautilus-A-pro2-meta.md) |
| 3 | **Наутилус B: nautilus** — мета-оркестратор репозиториев (внешняя архитектура) | [`03-nautilus-B-meta-orchestrator.md`](03-nautilus-B-meta-orchestrator.md) |

## Главная мысль

> Раковина наутилуса — спираль вложенных камер, где каждая новая камера больше предыдущей, но построена по той же геометрии. Это **fractal scaling с сохранением пропорции** (scale invariance).

- **Наутилус A** реализует это **внутри одной нейросети** (MoE-эксперты как вложенные «камеры»).
- **Наутилус B** реализует это **между репозиториями** (мета-оркестратор обращается через общий протокол).

> Это не два разных проекта, а одна мета-идея, проявленная на двух масштабах: «как устроена модель» и «как устроена команда/экосистема, которая её разрабатывает». Это **scale invariance** в инженерии ИИ — сознательный архитектурный тезис.

## Связь с Nautilus Portal Protocol

[Наутилус B → NPP v1.0/v1.1](../../nautilus/npp-v1-1/README.md) — формальная спецификация мета-оркестратора превратилась в Portal Protocol с Q6 / federation / passport.
