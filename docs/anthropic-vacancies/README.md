# anthropic-vacancies/ — вакансии Anthropic по кластерам

## Источник

Файл в корне репозитория: [`Вакансии в Anthropic по кластерам - Claude`](../../%D0%92%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8%20%D0%B2%20Anthropic%20%D0%BF%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D1%80%D0%B0%D0%BC%20-%20Claude) — MHTML‑снимок диалога с claude.ai (~7.6 MB).

Затравка диалога — статья 3dnews.ru/1140248 («Глава Anthropic предрёк исчезновение инженерных профессий и открыл 429 вакансий с зарплатой до $405 000»).

## Файлы и подпапки

| Файл / папка | О чём |
|---|---|
| [`overview.md`](overview.md) | Сводка по всем 16 кластерам + распределение ролей |
| [`methodology.md`](methodology.md) | Методика разбивки (как и откуда брались цифры) |
| [`signals.md`](signals.md) | Что говорит структура вакансий о приоритетах Anthropic |
| [`clusters/`](clusters/) | По одному файлу на каждый из 16 официальных кластеров найма |
| [`profile-mapping/`](profile-mapping/) | Маппинг профиля svend4 на роли Anthropic — три итерации (FDE → Public Benefit → «платформа, а не должность») |
| [`extra-collaborator-findings/`](extra-collaborator-findings/) | Variant D: четыре новых collaborator-проекта (CoAlly, Виталий, Анастасия, Mem0) + финальный tier ranking 12 collaborators |
| [`beneficial-deployments-concept/`](beneficial-deployments-concept/) | Variant C: outline 8–15-страничного concept document для Anthropic Beneficial Deployments outreach (10 sections) |
| [`ai-managed-virtual-company/`](ai-managed-virtual-company/) | Идея разделить $500K зарплату на команду 5–10 фрилансеров; AI-managed distributed virtual company (Variants A/B/C) |
| [`mmorpg-for-programmers/`](mmorpg-for-programmers/) | Гипотеза MMORPG-RPG для программистов / технарей как способ организовать distributed work |
| [`hermes-comparison/`](hermes-comparison/) | Сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent (Nous Research, 95K+ stars) — где сходства, где различия, переоценка приоритетов |
| [`nautilus-vs-camel/`](nautilus-vs-camel/) | Можно ли скрестить пассивный Nautilus с активным CAMEL framework; разбор content из info repositories |
| [`nautilus-pro2-analysis/`](nautilus-pro2-analysis/) | Два «Наутилуса» в репозиториях svend4 — pro2 (YiJing-Transformer) и nautilus (мета-оркестратор), scale invariance — прямой источник идеи NPP |

## Главный вывод

См. [`signals.md`](signals.md). Коротко: тезис «кодинг исчезнет первым» и одновременный найм 68 Research Engineer — не противоречие; самый быстрорастущий блок — не разработка, а Sales + Applied AI (≈200 ролей).

## Замечание о размере исходника

Исходный MHTML‑файл — самый большой из всех (~7.6 MB), потому что в этом же диалоге обсуждались и другие темы (профиль `svend4`, репозитории `pro2`/`Nautilus`, маппинг профиля на роли Anthropic, GitHub‑токены, дальнейшее развитие проекта и т. д.). В эту папку вынесены **аналитическая часть про вакансии Anthropic** (16 кластеров — строки 150–240 расшифровки) и **маппинг профиля на роли** (три итерации — строки 250–340, 370–420, 1020–1100). Остальной контекст диалога (детали репозиториев, скрипты, обсуждение токенов, поток про Nautilus) остаётся в исходном MHTML.
