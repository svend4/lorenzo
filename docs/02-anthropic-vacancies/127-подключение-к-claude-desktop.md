# Подключение к Claude Desktop

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

