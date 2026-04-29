# lorenzo — монорепозиторий

info

Это монорепозиторий с исследованиями, заметками и материалами по проекту **Svyazi 2.0** и смежным темам. Главные исходные документы остаются в корне без изменений; их содержимое продублировано и разбито на маленькие тематические документы внутри `docs/`, организованных по папкам и подпапкам.

## Структура

```
lorenzo/
├── README.md                              # этот файл
├── deep-research-report (1).md            # ОРИГИНАЛ — не изменён
├── deep-research-report (2).md            # ОРИГИНАЛ — не изменён
├── deep-research-report (3).md            # ОРИГИНАЛ — не изменён
├── deep-research-report (4).md            # ОРИГИНАЛ — не изменён
├── Вакансии в Anthropic ...               # ОРИГИНАЛ MHTML — не изменён
├── Комбинирование технологий ...          # ОРИГИНАЛ MHTML — не изменён
├── Поиск коллабораций AI проектов         # ОРИГИНАЛ MHTML — не изменён
├── Поиск уникальных проектов на Хабре ... # ОРИГИНАЛ MHTML — не изменён
├── docs/                                  # разделённые тематические документы
│   ├── svyazi-2-0/                        # основная тема: проект Svyazi 2.0
│   │   ├── overview/                      # обзор и методика
│   │   ├── components/                    # отдельные проекты-кирпичики
│   │   ├── ensembles/                     # ансамбли и их новые свойства
│   │   ├── architecture/                  # интеграционные контракты
│   │   ├── prototype/                     # MVP, риски, дорожная карта
│   │   ├── security/                      # безопасность, приватность, бюджет
│   │   ├── outreach/                      # контактная стратегия
│   │   └── limitations/                   # лицензии и ограничения
│   ├── anthropic-vacancies/               # вакансии Anthropic по кластерам + маппинг профиля
│   ├── nautilus/                          # NPP v1.1 RFC + 8 companion papers (OKWF, RAL, PCA, CSA, Double-Triangle, Layer-B, InGit+Cowork)
│   ├── lorenzo-agent/                     # системный промпт Lorenzo Catalyst Agent (источник имени репо)
│   ├── technology-combinations/           # комбинирование технологий
│   ├── ai-collaborations/                 # поиск коллабораций AI проектов
│   ├── habr-unique-projects/              # уникальные проекты на Хабре
│   └── glossary/                          # кросс-ссылочный словарь компонентов/авторов/понятий
├── packages/                              # workspace-пакеты (зарезервировано)
└── sources/                               # индексы исходных документов
```

## Принцип

1. **Ничего не удалено.** Все исходные документы в корне сохранены as-is.
2. **Разделено, а не сжато.** Содержимое исходных документов перенесено в маленькие тематические файлы — каждый файл посвящён одной теме или подтеме.
3. **Папки по темам, подпапки по подтемам.** Каждая большая тема имеет свою папку, внутри неё — подпапки для подтем.
4. **Индексы (`README.md`) в каждой папке.** Всегда понятно, что внутри и как навигировать.

## Точка входа

- Если хотите понять **что такое Lorenzo** (по которому назван этот репозиторий) — [docs/lorenzo-agent/README.md](docs/lorenzo-agent/README.md).
- Если вы изучаете **Svyazi 2.0** — начните с [docs/svyazi-2-0/README.md](docs/svyazi-2-0/README.md).
- Если ищете **компонент по имени** — [docs/glossary/components-by-name.md](docs/glossary/components-by-name.md).
- Если интересуют **архитектурные специфики Nautilus / DHLab** — [docs/nautilus/README.md](docs/nautilus/README.md).
- Если нужно **разобрать карьерные опции** — [docs/anthropic-vacancies/profile-mapping/README.md](docs/anthropic-vacancies/profile-mapping/README.md).
- Если интересуют **другие темы** — см. соответствующую подпапку в `docs/`.
- Если нужны **исходные документы** — см. [sources/README.md](sources/README.md) или сами файлы в корне.
# Lorenzo — Монорепозиторий исследований
<!-- badges -->
![docs](docs/badges/docs.svg) ![words](docs/badges/words.svg) ![scripts](docs/badges/scripts.svg) ![health](docs/badges/health.svg) ![go/no-go](docs/badges/scoring.svg) ![license](docs/badges/license.svg) ![branch](docs/badges/branch.svg) 


Организованные документы по темам. Исходные файлы сохранены в корне репозитория.

## Разделы

| Раздел | Описание |
|--------|----------|
| [01-svyazi](docs/01-svyazi/) | Svyazi 2.0: архитектура, компоненты, ансамбли, MVP |
| [02-anthropic-vacancies](docs/02-anthropic-vacancies/) | Анализ 436 вакансий Anthropic по 12 кластерам |
| [03-technology-combinations](docs/03-technology-combinations/) | 40+ синергетических комбинаций технологий |
| [04-ai-collaborations](docs/04-ai-collaborations/) | 5 ансамблей OSS-проектов для Svyazi |
| [05-habr-projects](docs/05-habr-projects/) | Проекты на Хабре: память, граф знаний, коллаборации |

## Исходные файлы

- `deep-research-report (1).md` — исходник для 01-svyazi (часть 1)
- `deep-research-report (2).md` — дубликат отчёта 1
- `deep-research-report (3).md` — исходник для 01-svyazi (часть 2)
- `deep-research-report (4).md` — дубликат отчёта 3
- `Вакансии в Anthropic по кластерам - Claude` — MHTML для 02-anthropic-vacancies
- `Комбинирование технологий для новых свойств - Claude` — MHTML для 03-technology-combinations
- `Поиск коллабораций AI проектов` — MHTML для 04-ai-collaborations
- `Поиск уникальных проектов на Хабре для совместной разработки - Claude` — MHTML для 05-habr-projects
- `Поиск уникальных проектов на Хабре для совместной разработки - Claude (1)` — дубликат

## Скрипты

- `scripts/organize_docs.py` — главный скрипт (этот файл)
- `scripts/extract_mhtml.py` — парсер MHTML → Markdown
- `scripts/part*.py` — модули по темам
