# Конфигурация для Claude Desktop

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
