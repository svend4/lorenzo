# Security Policy

## Поддерживаемые версии

Безопасность гарантируется только для последней minor-версии.

| Версия | Поддерживается |
|---------|----------------|
| 0.2.x (готовится) | ✅            |
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

### Auth / RBAC (Sprint 39)

- `docstoolkit/auth/` обеспечивает scope-based access control.
- **Wildcard scopes** (`rag:*`, `admin:*`) предоставляют broad permissions —
  выдавайте только trusted users.
- Tokens хранятся в SQLite plain-text (для local-first дизайна).
  Не делитесь `.docstoolkit/auth.sqlite`.
- Для production: encrypt at rest или используйте OS keyring как backend.

### Budget guards (Sprint 45)

- Per-scope лимиты (`day` / `week` / `month` / `total`) защищают от runaway costs.
- **`enforce()` raises BudgetExceeded** — обязательно catchить, иначе LLM-вызовы
  будут падать.
- Не используйте wildcard `*` для critical scope — kill-switch для всех.

### Agent tools (Sprint 30+, planner Sprint 50)

- `Tool.fn` вызывается с user-controllable arguments — **не передавайте небезопасные
  fns** (например, `os.system`, `eval`).
- Built-in tools (`builtin_tools.py`) safe; custom tools — на ответственности автора.
- Output capped at 5000 chars per tool call для DoS protection.
- `plan_and_execute` создаёт subtasks из user input — потенциально prompt injection
  через task description. Не доверяйте multi-agent output без review.

### Federation / NPP (Sprint 36)

- `federation/` подключается к peer-нодам через HTTP.
- **Нет встроенной authentication** — peer обязан быть в trusted network
  или за reverse-proxy с auth.
- Query payloads логируются в audit — не передавайте секреты в queries.
- Peer responses не санитайзятся — malicious peer может вернуть HTML/JS которые
  ваш UI отрендерит.

### Webhooks (Sprint 52)

- `WebhookDispatcher` отправляет POST на user-configured URLs.
- **HMAC-SHA256 signing включён по умолчанию** через `secret` параметр —
  всегда заполняйте.
- **Default http_send (urllib)** не валидирует SSL hostname — для production
  передайте custom http_send с requests/httpx.
- Dead-letter queue хранит payloads — могут содержать sensitive data.

### Conversation memory (Sprint 49)

- SQLite `.docstoolkit/conversations.sqlite` хранит полные user/assistant messages.
- **Не зашифровано** — для multi-tenant используйте per-user database files.
- `squash_old` сжимает но не удаляет — explicit `delete_session(sid)` для GDPR.

### Prompt library (Sprint 51)

- A/B variants разные пользователи могут получать разные prompts —
  используйте deterministic seed для воспроизводимости в audit.
- `render(strict=False)` оставляет `{placeholder}` в output —
  потенциальный template injection. **Default strict=True в этой версии**.

## Best practices

1. Запускать в виртуальном окружении (venv / conda)
2. Включить `pip install --require-hashes` в production
3. Использовать `pip-audit` для проверки зависимостей
4. Закрепить версии: `docs-toolkit==0.X.Y`, не `>=0.X.Y`
5. Для MCP серверов в Claude Desktop — отключать `lorenzo-runner` если не нужен
6. **Auth / Budget**: настройте лимиты до production rollout
7. **Webhooks**: всегда указывайте `secret` в Subscription
8. **Federation**: peer trust model — explicitly документируйте кто peer
9. **Conversation**: per-user encrypted DB для compliance
10. **Agent tools**: review каждый custom tool на injection / RCE
