# AI Agent Security Audit — 18 уязвимостей в открытом агенте

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Дмитрий Лабинцев + bgauryy (GitHub Gist)  
**Хабр:** https://habr.com/ru/articles/989764/  
**GitHub:** https://github.com/doneyli/ai-agent-security-audit (5-фазный фреймворк)  
**Слой:** quality / security / orchestration  
**Дата:** 2026  
**Уникальность:** Первый code-verified security audit открытого AI-агента (Clawdbot/Moltbot, ~1300 TypeScript файлов): найдено **18 уязвимостей** с подтверждёнными CVE. Результат — переиспользуемый **5-фазный фреймворк аудита агентов**. Из 31 000 проанализированных agent skills — **26% содержат минимум одну уязвимость**.

## Найденные уязвимости (топ)

| Уязвимость | Серьёзность | Описание |
|------------|-------------|----------|
| eval() без sandbox | Критичная | Plugin система выполняется с полными привилегиями ОС |
| Prompt injection | Критичная | Внешние данные (email, web) → инструкции агенту без санитизации |
| Plaintext memory | Высокая | API-токены, credentials в незашифрованных .md и .json |
| Data leakage | Высокая | WhatsApp сообщения + GPS → Anthropic/OpenAI без согласия |
| No rate limiting | Средняя | Нет ограничений на частоту вызовов инструментов |
| Supply chain skills | Высокая | 26% из 31k навыков содержат уязвимость |

## 5-фазный фреймворк аудита агентов

```
Фаза 1: Статический анализ кода (eval, exec, shell, subprocess)
        ↓
Фаза 2: Анализ потоков данных (внешние данные → промпт)
        ↓
Фаза 3: Проверка memory и persistence (шифрование, доступ)
        ↓
Фаза 4: Аудит инструментов/skills (permissions, sandbox)
        ↓
Фаза 5: Тест prompt injection (сценарии атак)
```

## Принципы безопасного агента

1. **Sandbox tools**: каждый инструмент — отдельный процесс с минимальными правами
2. **Sanitize inputs**: внешние данные не попадают в промпт без фильтрации
3. **Encrypt memory**: никаких credentials в plaintext
4. **Rate limit**: ограничения на частоту и стоимость вызовов
5. **Skill provenance**: откуда взят навык, проверена ли его безопасность

## openLight (R07) как ответ

openLight принцип (R07) решает ключевую уязвимость:  
→ LLM **выбирает из каталога готовых инструментов** (improve_*.py),  
  а не генерирует произвольный shell-код.  
→ Это устраняет eval() / exec() и сужает attack surface до known-good скриптов.

## Применение к Lorenzo

Lorenzo имеет 12 MCP-серверов и `improve_watcher.py` с автозапуском скриптов.  
**Уязвимые паттерны в Lorenzo:**

| Риск | Где | Рекомендация |
|------|-----|--------------|
| Exec скриптов | `improve_watcher.py` | openLight: только whitelist скриптов |
| Plaintext secrets | ENV переменные в .env | Не хранить ANTHROPIC_API_KEY в файлах |
| Внешние URL | `improve_link_preview.py` | Sanitize перед передачей агенту |

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Security Audit + openLight (R07)** | openLight = практическое воплощение рекомендаций аудита |
| **Security Audit + Observability (R13)** | Langfuse трейсит все tool-вызовы → аномальные паттерны = alert |
| **Security Audit + ADD (R13)** | ADD feedback loop: агент учится на security incidents |
| **Security Audit framework + Lorenzo MCP** | Применить 5 фаз аудита к 12 MCP-серверам Lorenzo |

## Контакт

- Статья: https://habr.com/ru/articles/989764/
- GitHub фреймворк: https://github.com/doneyli/ai-agent-security-audit
- Оригинальный аудит: https://gist.github.com/bgauryy/72b8a35d1849ad15469ba58e09428f58
- DEV.to: https://dev.to/dmitry_labintcev_9e611e04/riding-the-hype-security-audit-of-ai-agent-clawdbot-2ffl
