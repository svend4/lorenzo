---
title: "Подключение к Claude Desktop"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[124-конфигурация-для-claude-desktop]] (сходство 0.23)
- [[130-отладка]] (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [[124-конфигурация-для-claude-desktop]]
- [[130-отладка]]
- [[28-appendix-a-minimal-working-example]]
- [[125-readme-mcp-md-инструкция-по-установке]]

<!-- backlinks-auto -->
## Упоминается в

- [[63-history|History]]
- [[132-planned-v0-2-0|Planned (v0.2.0)]]
- [[65-readme-md|README.md]]
- [[123-portal-mcp-py|portal-mcp.py]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]
- [[130-отладка|Отладка]]
- [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[123-portal-mcp-py|portal-mcp.py]] _33%_
- [[41-compatibility-level|Compatibility Level]] _29%_
- [[154-table-of-contents|Table of Contents]] _25%_
- [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] _25%_
- [[04-abstract|Abstract]] _21%_
- [[09-4-passport-passport-md|4. Passport (`passport.md`)]] _21%_
- [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] _21%_
- [[130-отладка|Отладка]] _21%_
## Связанные документы

- [[123-portal-mcp-py|portal-mcp.py]] _33%_
- [[04-abstract|Abstract]] _25%_
- [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] _25%_
- [[130-отладка|Отладка]] _25%_
- [[190-содержание|Содержание]] _25%_
- [[22-10-queryresult-structure|10. QueryResult Structure]] _25%_
- [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] _25%_
- [[326-содержание|Содержание]] _25%_
