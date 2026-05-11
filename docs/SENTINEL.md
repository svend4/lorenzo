# SENTINEL Security Report

<!-- summary -->
> Дата: 2026-05-11 · Проблем: **3** · HTTP-ссылок: 212 · Лицензионных рисков: 4

<!-- tags: security, sentinel, privacy, license, audit -->

<!-- toc-auto -->
## Contents

- [Итог](#итог)
- [PII и секреты](#pii-и-секреты)
- [Небезопасный код](#небезопасный-код)
- [Файлы credentials](#файлы-credentials)
- [Лицензионные риски](#лицензионные-риски)
- [HTTP без TLS](#http-без-tls)
- [Использование](#использование)

> [!WARNING]
> Найдено 3 проблем безопасности

<!-- alert-added -->

## Итог

| Категория | Найдено |
|-----------|---------|
| PII / секреты в docs | 0 |
| Небезопасные паттерны в коде | 3 |
| Credential-файлы | 0 |
| HTTP (не HTTPS) ссылок | 212 |
| Лицензионных рисков | 4 |
| **Итого критических** | **3** |

## PII и секреты

✅ PII и секреты не найдены.


## Небезопасный код

| Файл | Строка | Проблема | Фрагмент |
|------|--------|----------|----------|
| `scripts/gateway.py` | 655 | __import__() dynamic import | `t0      = __import__("time").time()` |
| `scripts/gateway.py` | 657 | __import__() dynamic import | `latency = round(__import__("time").time(` |
| `scripts/improve_precision_eval.py` | 408 | __import__() dynamic import | `f"*Сгенерировано: {__import__('datetime'` |

## Файлы credentials

✅ Credential-файлы в репозитории не найдены.


## Лицензионные риски

_Компоненты с нестандартными лицензиями в архитектуре Svyazi 2.0:_

| Файл | Лицензия | Риск |
|------|----------|------|
| `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-` | BSL | Business Source License — не открытая, коммерческие ограниче |
| `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-` | неуточнено | Лицензия неизвестна — требует уточнения |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-` | BSL | Business Source License — не открытая, коммерческие ограниче |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-` | неуточнено | Лицензия неизвестна — требует уточнения |

## HTTP без TLS (212 ссылок)

_HTTP-ссылки могут быть перехвачены. Рекомендуется замена на HTTPS._

- `http://localhost:8000````` в `docs/SENTINEL.md`
- `http://localhost:8000`````` в `docs/SENTINEL.md`
- `http://localhost:8080````` в `docs/SENTINEL.md`
- `http://localhost:8080`````` в `docs/SENTINEL.md`
- `http://localhost:8000```` в `docs/SENTINEL.md`
- `http://localhost:8080```` в `docs/SENTINEL.md`
- `http://localhost:8000``` в `docs/SENTINEL.md`
- `http://localhost:8080``` в `docs/SENTINEL.md`
- `http://localhost:8000`` в `docs/SENTINEL.md`
- `http://localhost:8080`` в `docs/SENTINEL.md`
- `http://localhost:8000` в `docs/BROKEN_LINKS.md`
- `http://localhost:8080` в `docs/BROKEN_LINKS.md`

## Использование

```bash
python scripts/improve_sentinel_check.py
python scripts/improve_sentinel_check.py --strict
python scripts/improve_sentinel_check.py --section 05-habr-projects
```


<!-- see-also -->

---

**Смотрите также:**
- [security-routing-plane](svyazi-2-0/components/security-routing-plane.md)
- [BROKEN_LINKS](BROKEN_LINKS.md)
- [legal-rag](svyazi-2-0/components/legal-rag.md)
- [DEMO](DEMO.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [READABILITY](READABILITY.md)
- [SEARCH](SEARCH.md)
- [TABLES](TABLES.md)

