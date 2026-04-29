# Подключение к Claude Desktop
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [Подключение к Claude Desktop](#подключение-к-claude-desktop)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Содержимое](#содержимое)


<!-- summary -->
> ~/Library/Application Support/Claude/claude_desktop_config.json

---



## Подключение к Claude Desktop

### macOS

Отредактировать:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows

Отредактировать:

```
%APPDATA%\Claude\claude_desktop_config.json
```

### Linux

Отредактировать:

```
~/.config/Claude/claude_desktop_config.json
```

### Содержимое

```json
{
  "mcpServers": {
    "nautilus-portal": {
      "command": "python3",
      "args": ["/absolute/path/to/nautilus/portal-mcp.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/nautilus"
      }
    }
  }
}
```

После сохранения перезапустить Claude Desktop. Иконка MCP в нижней 
части чата покажет статус подключения.

<!-- similar-docs -->

---

**Похожие документы:**
- [124-конфигурация-для-claude-desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) (сходство 0.23)
- [130-отладка](docs/02-anthropic-vacancies/130-отладка.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [124-конфигурация-для-claude-desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md)
- [130-отладка](docs/02-anthropic-vacancies/130-отладка.md)
- [28-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)
- [125-readme-mcp-md-инструкция-по-установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) _33%_
- [Abstract](docs/02-anthropic-vacancies/04-abstract.md) _25%_
- [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) _25%_
- [Отладка](docs/02-anthropic-vacancies/130-отладка.md) _25%_
- [Содержание](docs/02-anthropic-vacancies/190-содержание.md) _25%_
- [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) _25%_
- [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) _25%_
- [Содержание](docs/02-anthropic-vacancies/326-содержание.md) _25%_
