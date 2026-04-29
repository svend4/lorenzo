---
title: "Конфигурация для Claude Desktop"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# Конфигурация для Claude Desktop

<!-- summary -->
> После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. Путь зависит от ОС:

---
<!-- tags: anthropic -->




## Конфигурация для Claude Desktop
После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. Путь зависит от ОС:
- macOS : ~/Library/Application Support/Claude/claude_desktop_config.json
- Windows : %APPDATA%\Claude\claude_desktop_config.json
- Linux : ~/.config/Claude/claude_desktop_config.json
Для Termux на Android Claude Desktop напрямую недоступен, но MCP server может быть проверен через mcp-cli или через самописный тест-клиент. Для десктопной настройки конфигурация выглядит так:
json
```json
{
  "mcpServers": {
    "nautilus-portal": {
      "command": "python3",
      "args": [
        "/absolute/path/to/nautilus/portal-mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/nautilus"
      }
    }
  }
}
```
Замените /absolute/path/to/nautilus на реальный путь к вашему клонированному репо.
После сохранения конфигурации и перезапуска Claude Desktop в чате появится индикатор подключения MCP-сервера, и tools станут доступны для использования.
---

<!-- similar-docs -->

---

**Похожие документы:**
- [[127-подключение-к-claude-desktop]] (сходство 0.23)
- [[130-отладка]] (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [[127-подключение-к-claude-desktop]]
- [[130-отладка]]
- [[125-readme-mcp-md-инструкция-по-установке]]
- [[129-примеры-запросов-в-claude]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[130-отладка|Отладка]] _33%_
- [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]] _25%_
- [[122-глоссарий|Глоссарий]] _17%_
- [[77-2-terminology|2. Terminology]] _17%_
