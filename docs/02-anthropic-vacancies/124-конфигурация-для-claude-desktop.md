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
- [127-подключение-к-claude-desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) (сходство 0.23)
- [130-отладка](docs/02-anthropic-vacancies/130-отладка.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [127-подключение-к-claude-desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md)
- [130-отладка](docs/02-anthropic-vacancies/130-отладка.md)
- [125-readme-mcp-md-инструкция-по-установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)
- [129-примеры-запросов-в-claude](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [Отладка](docs/02-anthropic-vacancies/130-отладка.md) _33%_
- [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) _25%_
- [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) _17%_
- [2. Terminology](docs/02-anthropic-vacancies/77-2-terminology.md) _17%_
