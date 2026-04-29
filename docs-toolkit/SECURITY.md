# Security Policy

## Поддерживаемые версии

Безопасность гарантируется только для последней minor-версии.

| Версия | Поддерживается |
|---------|----------------|
| 0.1.x   | ✅            |
| < 0.1   | ❌            |

## Reporting a Vulnerability

**НЕ открывайте публичный issue для security багов.**

Отправьте email с темой `[SECURITY] docs-toolkit`:
- свяжитесь через GitHub: открыть private security advisory
  на https://github.com/svend4/lorenzo/security/advisories/new

Включите:
- Описание уязвимости
- Шаги воспроизведения
- Версия `docs-toolkit`, Python, ОС
- Возможный impact (код-инъекция, DoS, утечка данных)

## SLA ответа

- **Acknowledgment:** 72 часа
- **Initial assessment:** 1 неделя
- **Fix release:** в зависимости от severity:
  - Critical (RCE, secret leak): 7 дней
  - High (privilege escalation, XSS): 14 дней
  - Medium (DoS): 30 дней
  - Low: следующий minor релиз

## Scope

В scope:
- `docstoolkit/*` модули
- `scripts/mcp_*_server.py` (MCP-серверы Lorenzo)
- CI/CD workflows (`.github/workflows/`)
- Dockerfile

Out of scope:
- Сторонние плагины (entry_points) — обращайтесь к их авторам
- LLM-output (содержимое возвращаемого текста — ответственность пользователя)
- Документация в `docs/` (контент, а не код)

## Известные ограничения безопасности

### MCP сервера

- **Read-only сервера** (`lorenzo-search`, `lorenzo-graph`, `lorenzo-templates`,
  `lorenzo-embed`) безопасны для подключения любого MCP-клиента.
- **Mutating сервера** (`lorenzo-contacts`, `lorenzo-runner`,
  `lorenzo-watch`) могут изменять файлы. Не подключайте к недоверенным клиентам.
- **lorenzo-llm** делает вызовы к Anthropic API — стоит денег. Кэш в
  `.claude/llm_cache.jsonl` не зашифрован, не храните секреты в запросах.

### Web ingest

- `fetch_url()` следует HTTP-редиректам без ограничений → потенциальная SSRF.
  Рекомендуется не передавать URL от недоверенных источников.
- `fetch_habr()` парсит HTML — теоретически уязвим к подложному HTML с большим
  payload (DoS через память). Лимит на размер ответа: TODO.

### docstoolkit serve

- Web dashboard биндится по умолчанию на `127.0.0.1` (только localhost).
- Path traversal защищён через `relative_to` check.
- XSS protected: все динамические данные экранируются через `_escape()`.
- **Не используйте `--bind 0.0.0.0` без reverse proxy** — нет auth, нет HTTPS.

### Embeddings cache

- SQLite БД в `.docstoolkit/cache/embeddings.sqlite` хранит pickled vectors.
- **Не загружайте чужие cache файлы** — pickle.load может выполнить произвольный
  код. Если кэш повреждён, удалите его: `docstoolkit index clear`.

## Best practices

1. Запускать в виртуальном окружении (venv / conda)
2. Включить `pip install --require-hashes` в production
3. Использовать `pip-audit` для проверки зависимостей
4. Закрепить версии: `docs-toolkit==0.X.Y`, не `>=0.X.Y`
5. Для MCP серверов в Claude Desktop — отключать `lorenzo-runner` если не нужен
