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
<!-- tags: anthropic -->




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
- [124-конфигурация-для-claude-desktop](124-конфигурация-для-claude-desktop.md) (сходство 0.23)
- [130-отладка](130-отладка.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [124-конфигурация-для-claude-desktop](124-конфигурация-для-claude-desktop.md)
- [130-отладка](130-отладка.md)
- [28-appendix-a-minimal-working-example](28-appendix-a-minimal-working-example.md)
- [125-readme-mcp-md-инструкция-по-установке](125-readme-mcp-md-инструкция-по-установке.md)

<!-- backlinks-auto -->
## Упоминается в

- [History](63-history.md)
- [Planned (v0.2.0)](132-planned-v0-2-0.md)
- [README.md](65-readme-md.md)
- [portal-mcp.py](123-portal-mcp-py.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Конфигурация для Claude Desktop](124-конфигурация-для-claude-desktop.md)
- [Отладка](130-отладка.md)
- [Что ты ВСЕГДА делаешь](360-что-ты-всегда-делаешь.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [portal-mcp.py](123-portal-mcp-py.md) _33%_
- [Compatibility Level](41-compatibility-level.md) _29%_
- [Table of Contents](154-table-of-contents.md) _25%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _25%_
- [Abstract](04-abstract.md) _21%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _21%_
- [Конфигурация для Claude Desktop](124-конфигурация-для-claude-desktop.md) _21%_
- [Отладка](130-отладка.md) _21%_
## Связанные документы

- [portal-mcp.py](123-portal-mcp-py.md) _33%_
- [Abstract](04-abstract.md) _25%_
- [Конфигурация для Claude Desktop](124-конфигурация-для-claude-desktop.md) _25%_
- [Отладка](130-отладка.md) _25%_
- [Содержание](190-содержание.md) _25%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _25%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _25%_
- [Содержание](326-содержание.md) _25%_
