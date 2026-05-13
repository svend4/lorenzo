"""
improve_sentinel_check.py — SENTINEL security audit для Svyazi 2.0.

Проверяет репозиторий на:
  1. PII-утечки (email, телефоны, API-ключи в docs/)
  2. Небезопасные паттерны в скриптах (shell injection, hardcoded secrets)
  3. Лицензионные конфликты (BSL/proprietary vs MIT/Apache в одном ансамбле)
  4. Орфанные credentials (файлы .env, *.key, *.pem)
  5. Внешние URL без HTTPS

Создаёт docs/SENTINEL.md с отчётом.

Запуск:
    python scripts/improve_sentinel_check.py
    python scripts/improve_sentinel_check.py --strict   # строгий режим
    python scripts/improve_sentinel_check.py --section 05-habr-projects
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

STRICT = "--strict" in sys.argv
SECTION_IDX = sys.argv.index("--section") if "--section" in sys.argv else -1
SECTION = sys.argv[SECTION_IDX + 1] if SECTION_IDX >= 0 and SECTION_IDX + 1 < len(sys.argv) else ""

# ── Паттерны для PII / секретов ──────────────────────────────────────────────
PII_PATTERNS = [
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "email"),
    (r'\b(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b', "phone-RU"),
    (r'\bsk-[A-Za-z0-9]{20,}\b', "OpenAI API key"),
    (r'\bANTHROPIC_API_KEY\s*=\s*["\']?[A-Za-z0-9_-]{20,}', "Anthropic key"),
    (r'\b(?:password|passwd|secret|token)\s*[=:]\s*["\'][^"\']{6,}["\']', "hardcoded secret"),
    (r'\bghp_[A-Za-z0-9]{36}\b', "GitHub PAT"),
]

# ── Небезопасные паттерны в Python-скриптах ──────────────────────────────────
UNSAFE_CODE_PATTERNS = [
    (r'\bos\.system\s*\(', "os.system (shell injection risk)"),
    (r'\bsubprocess\.call\s*\(.+shell\s*=\s*True', "subprocess shell=True"),
    (r'\beval\s*\(', "eval() usage"),
    (r'\bexec\s*\(', "exec() usage"),
    (r'__import__\s*\(', "__import__() dynamic import"),
    (r'\bpickle\.loads?\s*\(', "pickle deserialization"),
]

# ── Лицензионные риски ────────────────────────────────────────────────────────
LICENSE_RISK = {
    "BSL": "Business Source License — не открытая, коммерческие ограничения",
    "AGPL": "AGPL — copyleft, требует открытия производных",
    "GPL": "GPL — copyleft, требует открытия производных",
    "proprietary": "Проприетарная — интеграция под вопросом",
    "неуточнено": "Лицензия неизвестна — требует уточнения",
}

HTTP_RE = re.compile(r'http://[^\s\)"\'>\]]+')


# Whitelist: намеренно присутствующие в репо значения (владелец проекта)
PII_WHITELIST = {
    "lorenzo@dhlab.ai",
}

def _scan_pii(filepath: Path) -> list[dict]:
    # Не сканируем сам отчёт (он копирует значения из других файлов)
    if filepath.name == "SENTINEL.md":
        return []
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return []
    results = []
    for pattern, label in PII_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            val = m.group(0)
            # Пропускаем явные заглушки
            if any(ph in val.lower() for ph in ["example", "test", "your_", "<", "foo@"]):
                continue
            # Пропускаем whitelist
            if val.strip() in PII_WHITELIST:
                continue
            results.append({
                "file": str(filepath.relative_to(ROOT)),
                "issue": label,
                "value": val[:60],
            })
    return results


def _scan_unsafe_code(filepath: Path) -> list[dict]:
    # Не сканируем себя (паттерны в строках дадут ложные срабатывания)
    if filepath.name == "improve_sentinel_check.py":
        return []
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return []
    results = []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # Пропускаем строки-паттерны (regex внутри строковых литералов)
        if stripped.startswith(("r'", 'r"', "(r'", '(r"')):
            continue
        for pattern, label in UNSAFE_CODE_PATTERNS:
            if re.search(pattern, line):
                results.append({
                    "file": str(filepath.relative_to(ROOT)),
                    "line": i,
                    "issue": label,
                    "snippet": stripped[:80],
                })
    return results


def _scan_license_risks(scan_root: Path) -> list[dict]:
    results = []
    for f in scan_root.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for lic, desc in LICENSE_RISK.items():
            # Лицензия упомянута явно в frontmatter или таблице
            if re.search(rf'\blicense\b.{{0,30}}{re.escape(lic)}\b', text, re.IGNORECASE):
                results.append({
                    "file": str(f.relative_to(ROOT)),
                    "license": lic,
                    "risk": desc,
                })
    return results


def _scan_credential_files() -> list[dict]:
    results = []
    dangerous = [".env", ".env.local", "*.key", "*.pem", "*.p12", "credentials.json"]
    for pattern in dangerous:
        for f in ROOT.rglob(pattern):
            if ".git" in str(f):
                continue
            results.append({
                "file": str(f.relative_to(ROOT)),
                "issue": "credential file in repo",
            })
    return results


def _scan_http_urls(scan_root: Path) -> list[dict]:
    results = []
    for f in scan_root.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in HTTP_RE.finditer(text):
            url = m.group(0).rstrip(".,;)")
            if len(url) > 10:
                results.append({
                    "file": str(f.relative_to(ROOT)),
                    "url": url[:80],
                })
    return results


def main():
    print("SENTINEL security check...")
    scan_root = (DOCS / SECTION) if SECTION else DOCS

    pii_issues    = []
    code_issues   = []
    cred_files    = _scan_credential_files()
    http_urls     = _scan_http_urls(scan_root)
    license_risks = _scan_license_risks(scan_root)

    # PII в docs/
    for f in scan_root.rglob("*.md"):
        rel = f.relative_to(ROOT)
        parts = rel.parts
        if any(p in {"obsidian", "confluence", "templates"} for p in parts):
            continue
        pii_issues.extend(_scan_pii(f))

    # Небезопасный код в scripts/
    for f in SCRIPTS.glob("*.py"):
        code_issues.extend(_scan_unsafe_code(f))

    # ── Отчёт ────────────────────────────────────────────────────────────────
    total_issues = len(pii_issues) + len(code_issues) + len(cred_files)
    status = "WARNING" if total_issues > 0 else "TIP"
    status_text = f"Найдено {total_issues} проблем безопасности" if total_issues else "Критических проблем безопасности не найдено"

    lines = [
        "# SENTINEL Security Report\n",
        f"<!-- summary -->\n> Дата: {date.today()} · Проблем: **{total_issues}** · HTTP-ссылок: {len(http_urls)} · Лицензионных рисков: {len(license_risks)}\n",
        "<!-- tags: security, sentinel, privacy, license, audit -->\n",
        "<!-- toc-auto -->\n## Contents\n\n"
        "- [Итог](#итог)\n"
        "- [PII и секреты](#pii-и-секреты)\n"
        "- [Небезопасный код](#небезопасный-код)\n"
        "- [Файлы credentials](#файлы-credentials)\n"
        "- [Лицензионные риски](#лицензионные-риски)\n"
        "- [HTTP без TLS](#http-без-tls)\n"
        "- [Использование](#использование)\n",
        f"> [!{status}]\n> {status_text}\n\n<!-- alert-added -->\n",
        "## Итог\n",
        f"| Категория | Найдено |",
        f"|-----------|---------|",
        f"| PII / секреты в docs | {len(pii_issues)} |",
        f"| Небезопасные паттерны в коде | {len(code_issues)} |",
        f"| Credential-файлы | {len(cred_files)} |",
        f"| HTTP (не HTTPS) ссылок | {len(http_urls)} |",
        f"| Лицензионных рисков | {len(license_risks)} |",
        f"| **Итого критических** | **{total_issues}** |\n",
    ]

    # PII
    lines.append("## PII и секреты\n")
    if not pii_issues:
        lines.append("✅ PII и секреты не найдены.\n")
    else:
        lines += [
            "| Файл | Тип | Значение |",
            "|------|-----|----------|",
        ]
        for item in pii_issues[:30]:
            lines.append(f"| `{item['file'][:60]}` | {item['issue']} | `{item['value'][:40]}` |")

    # Небезопасный код
    lines.append("\n## Небезопасный код\n")
    if not code_issues:
        lines.append("✅ Небезопасных паттернов в скриптах не найдено.\n")
    else:
        lines += [
            "| Файл | Строка | Проблема | Фрагмент |",
            "|------|--------|----------|----------|",
        ]
        for item in code_issues[:30]:
            lines.append(
                f"| `{item['file'][:50]}` | {item['line']} "
                f"| {item['issue']} | `{item['snippet'][:40]}` |"
            )

    # Credential files
    lines.append("\n## Файлы credentials\n")
    if not cred_files:
        lines.append("✅ Credential-файлы в репозитории не найдены.\n")
    else:
        for item in cred_files:
            lines.append(f"- ⚠️ `{item['file']}` — {item['issue']}")
        lines.append("")

    # Лицензионные риски
    lines.append("\n## Лицензионные риски\n")
    lines.append("_Компоненты с нестандартными лицензиями в архитектуре Svyazi 2.0:_\n")
    if not license_risks:
        lines.append("Лицензионных конфликтов не обнаружено.\n")
    else:
        seen = set()
        lines += [
            "| Файл | Лицензия | Риск |",
            "|------|----------|------|",
        ]
        for item in license_risks[:20]:
            key = (item["file"], item["license"])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"| `{item['file'][:60]}` | {item['license']} | {item['risk'][:60]} |")

    # HTTP URLs
    lines.append(f"\n## HTTP без TLS ({len(http_urls)} ссылок)\n")
    if not http_urls:
        lines.append("✅ HTTP-ссылок (без TLS) не найдено.\n")
    else:
        lines.append("_HTTP-ссылки могут быть перехвачены. Рекомендуется замена на HTTPS._\n")
        seen_urls = set()
        for item in http_urls[:20]:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                lines.append(f"- `{item['url']}` в `{item['file'][:50]}`")

    lines += [
        "\n## Использование\n",
        "```bash",
        "python scripts/improve_sentinel_check.py",
        "python scripts/improve_sentinel_check.py --strict",
        "python scripts/improve_sentinel_check.py --section 05-habr-projects",
        "```\n",
    ]

    out = DOCS / "SENTINEL.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  PII: {len(pii_issues)}, код: {len(code_issues)}, "
          f"creds: {len(cred_files)}, HTTP: {len(http_urls)}, "
          f"лицензии: {len(license_risks)}")
    if total_issues == 0:
        print("  ✅ Критических проблем безопасности не найдено")
    else:
        print(f"  ⚠️  Итого критических: {total_issues}")


if __name__ == "__main__":
    main()
