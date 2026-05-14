# Veai — AI-агент для JetBrains IDE (IntelliJ IDEA)

**Автор:** команда Veai  
**Хабр:** https://habr.com/ru/companies/veai/  
**GitHub:** плагин в JetBrains Marketplace  
**Слой:** orchestration / desktop-agent / ide  
**Дата:** 2025–2026 (v5.8 → v5.10+)  
**Уникальность:** Первый AI-агент для JetBrains IDE из реестра российского ПО: умеет дебажить, рефакторить и генерировать run-конфигурации — не только дополнять код. Поддерживает MCP-серверы и систему «скилов» (расшариваемых правил между коллегами).

## Возможности (по версиям)

### v5.8 — Debug + Refactor + Run Configs
- **Дебаг-агент**: смотрит стек ошибки, переменные, предлагает fix
- **Рефактор-агент**: реструктуризация кода с сохранением семантики
- **Run-конфигурации**: автогенерация launch.json / run configs под проект

### v5.10 — Shared Skills + Chat Hints
- **Shared Skills**: командные правила/паттерны — коллеги расшаривают через Git
- **Chat Hints**: подсказки в диалоге по контексту текущего файла

## Стек

- **Интеграция**: JetBrains Plugin API (IntelliJ IDEA, PyCharm, GoLand и др.)
- **MCP**: встроенная поддержка MCP-серверов
- **Контекст**: rules / skills / context — как в Cursor, но для JetBrains
- **Реестр**: включён в реестр российского ПО

## Архитектурный паттерн

```
IDE Event (ошибка / хоткей / команда)
        ↓
Veai Agent (видит файл + AST + стек)
        ↓
MCP Server (доп. инструменты) ← optional
        ↓
Patch / Run Config / Explanation
```

## Почему важно для Svyazi

Lorenzo сейчас работает через CLI. Veai показывает паттерн IDE-интеграции:  
**агент видит AST, а не только текст** → точнее понимает, что править.  
Shared Skills = аналог `improve_*.py` но в контексте IDE + командная синхронизация.  
MCP-поддержка означает: Veai может вызывать Lorenzo MCP-серверы из IDE напрямую.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Veai + Lorenzo MCP** | IDE-агент вызывает improve_*.py через MCP → рефактор документации из IDE |
| **Veai + openLight (R07)** | openLight safety + IDE-контекст = безопасный рефактор без hallucination |
| **Veai + SocratiCode (R08)** | AST-chunking (SocratiCode) + IDE-агент (Veai) = 61% меньше токенов в IDE |
| **Veai + DevClaw (R06)** | Veai дебажит → DevClaw создаёт PR → полный CI-цикл без выхода из IDE |

## Контакт

- Хабр компании: https://habr.com/ru/companies/veai/
- JetBrains Marketplace: поиск "Veai"
- Реестр РФ: подтверждён
