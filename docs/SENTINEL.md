# SENTINEL Security Report

<!-- toc-auto -->
## Contents

- [Итог](#итог)
- [PII и секреты](#pii-и-секреты)
- [Небезопасный код](#небезопасный-код)
- [Файлы credentials](#файлы-credentials)
- [Лицензионные риски](#лицензионные-риски)
- [HTTP без TLS (47 ссылок)](#http-без-tls-47-ссылок)
- [Использование](#использование)


<!-- summary -->
> Дата: 2026-05-11 · Проблем: **0** · HTTP-ссылок: 47 · Лицензионных рисков: 4

<!-- tags: security, sentinel, privacy, license, audit -->

> [!TIP]
> Критических проблем безопасности не найдено

<!-- alert-added -->

## Итог

| Категория | Найдено |
|-----------|---------|
| PII / секреты в docs | 0 |
| Небезопасные паттерны в коде | 0 |
| Credential-файлы | 0 |
| HTTP (не HTTPS) ссылок | 47 |
| Лицензионных рисков | 4 |
| **Итого критических** | **0** |

## PII и секреты

✅ PII и секреты не найдены.


## Небезопасный код

✅ Небезопасных паттернов в скриптах не найдено.


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

## HTTP без TLS (47 ссылок)

_HTTP-ссылки могут быть перехвачены. Рекомендуется замена на HTTPS._

- `http://localhost:8000```` в `docs/SENTINEL.md`
- `http://localhost:8000````` в `docs/SENTINEL.md`
- `http://localhost:8080```` в `docs/SENTINEL.md`
- `http://localhost:8080````` в `docs/SENTINEL.md`
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


<!-- similar-docs -->

---

**Похожие документы:**
- [SENTINEL](obsidian/SENTINEL.md) (сходство 0.96)
- [security-routing-plane](svyazi-2-0/components/security-routing-plane.md) (сходство 0.10)
- [security-routing-plane](obsidian/svyazi-2-0/components/security-routing-plane.md) (сходство 0.10)

