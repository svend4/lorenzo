# Round 11 — Лог поисковой сессии

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** десктопные AI-агенты, edge AI / IoT, голосовые ассистенты на специализированном железе

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Союз (Souz) | команда souz.app | desktop-agent / accessibility / MCP | `projects/souz-desktop-agent.md` |
| Vera | неизвестен | desktop-agent / local / GGUF / privacy | `projects/vera-desktop-agent.md` |
| RPi Visual Agent | Simone Marculli | edge-AI / RPi / tiny models | `projects/rpi-visual-agent.md` |
| Orrin (MTS AI) | MTS AI | voice / embedded / Rockchip RK3588 | `projects/orrin-rockchip-voice.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Союз + Lorenzo runner | MCP | Голосовая команда → run_improve → изменение файла | ⭐⭐⭐⭐⭐ |
| RPi Agent + Ирина (R02) | faster-whisper + TTS | Полный русский offline voice pipeline (STT+LLM+TTS) | ⭐⭐⭐⭐ |
| Vera + Ботинок (R06) | llama-cpp | Vera = десктоп, Ботинок = SSH: единая GGUF экосистема | ⭐⭐⭐⭐ |
| Orrin RK3588 + News System (R05) | edge hardware | Автономный новостной пайплайн на RK3588 без облака | ⭐⭐⭐ |

## Главная находка раунда

**Союз** — первый найденный за все 11 раундов десктопный агент с **MCP-архитектурой**, 70+ инструментами и открытым исходным кодом. Изначально создан для слабовидящих, что обеспечивает максимально надёжный контроль над каждым инструментом. Применим к Lorenzo как desktop shell.

**Orrin на RK3588** — показывает путь к дешёвому production edge AI: RK3588-устройства (Orange Pi 5, Radxa ROCK 5) стоят в 10–20 раз дешевле GPU. Это открывает возможность для Svyazi-агентов на embedded hardware.

**Полная offline voice экосистема** из трёх проектов: RPi Agent (STT) + Ирина R02 (TTS) + любой локальный LLM = конкурент Алисе без облака.

## Сводная карта R01–R11

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |
| R06 | 4 | Video AI, CLI agents, GitHub automation | Memory MCP v2, DevClaw паттерн |
| R07 | 4 | Multi-agent architecture, agent safety | openLight принцип, 9-агентный паттерн |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI | SocratiCode, Paper2Agent |
| R09 | 4 | GraphRAG, decentralized AI, coding agent | GraphRAG pipeline, HMP, OpenCode |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust | MiroFish, n8n AI Stack |
| R11 | 4 | Desktop agents, edge AI, voice embedded | Союз (MCP desktop), RPi+Ирина voice pipeline |

**Итого: 48 проектов, 26+ авторов**

## Что осталось на R12

- AI-инструменты для аналитики данных (pandas-agent, SQL-agent, BI-автоматизация)
- Генерация музыки / аудио с AI (open source альтернативы Suno)
- Специализированные векторные базы данных для агентов (pgvector, Weaviate, Chroma)
- AI-системы для code refactoring (не просто ревью, а автоматические рефакторинги)
