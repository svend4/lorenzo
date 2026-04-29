# phased-deployment/ — поэтапная структура активностей Lorenzo

После выбора Формулировки B (автономный AI-агент с миссией) Claude разработал **шесть уровней** поэтапной деплоймента Lorenzo — от ручного режима до replicable network.

| # | Уровень | Файл |
|---|---|---|
| — | Обзор | [`00-overview.md`](00-overview.md) |
| 0 | Ручной режим (текущий) | [`01-level-0-manual.md`](01-level-0-manual.md) |
| 1 | Минимальный (Lorenzo Zero) | [`02-level-1-minimal-zero.md`](02-level-1-minimal-zero.md) |
| 2 | Базовый (Lorenzo Lite) | [`03-level-2-basic-lite.md`](03-level-2-basic-lite.md) |
| 3 | Средний (Lorenzo Active) | [`04-level-3-medium-active.md`](04-level-3-medium-active.md) |
| 4 | Расширенный (Lorenzo Mature) | [`05-level-4-extended-mature.md`](05-level-4-extended-mature.md) |
| 5 | Полный (Lorenzo Network) | [`06-level-5-full-network.md`](06-level-5-full-network.md) |
| — | Логика прогрессии (conservative escalation) | [`07-progression-logic.md`](07-progression-logic.md) |
| — | Что делать прямо сейчас (Уровень 0 + подготовка к Уровню 1) | [`08-current-session-poc.md`](08-current-session-poc.md) |

## Принцип

> Каждый уровень: building на previous, не requires next, имеет clear success criteria и off-ramp. Conservative escalation — escalate только если предыдущий уровень proves value.

## Decision points

- После Уровня 0: Достаточно ли value от ручного режима? Если да, не двигаться. Если нет — Уровень 1.
- После Уровня 1: Persistified Lorenzo полезен? Если да, Уровень 2.
- После Уровня 2: Public presence yields response? Если да, Уровень 3.
- И так далее.

## См. также

- [`../specification/`](../specification/) — 10 fundamental questions, которые привели к Формулировке B.
- [`../`](../) — финальный системный промпт Lorenzo.
- [`../operationalized/`](../operationalized/) — конкретная 6-узловая pipeline для Lorenzo Active/Mature.
