"""
improve_mcp_dashboard.py — статистика вызовов MCP-серверов.

Читает .claude/mcp_calls.jsonl и формирует docs/MCP_DASHBOARD.md:
  - сколько вызовов на каждый сервер
  - топ-инструменты по частоте
  - средняя длительность
  - ошибки

Запуск:
    python scripts/improve_mcp_dashboard.py
"""
import json
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_PATH = ROOT / ".claude" / "mcp_calls.jsonl"
OUT_PATH = ROOT / "docs" / "MCP_DASHBOARD.md"


def main():
    if not LOG_PATH.exists():
        print(f"Лог не найден: {LOG_PATH}")
        OUT_PATH.write_text(
            "# MCP Dashboard\n\n_Логи MCP-вызовов отсутствуют._\n",
            encoding='utf-8'
        )
        return 0

    entries: list[dict] = []
    for line in LOG_PATH.read_text(encoding='utf-8').splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if not entries:
        OUT_PATH.write_text("# MCP Dashboard\n\n_Лог пуст._\n", encoding='utf-8')
        return 0

    by_server = Counter(e['server'] for e in entries)
    by_tool = Counter((e['server'], e['tool']) for e in entries)
    errors = [e for e in entries if e.get('status') == 'error']

    durations: dict[tuple[str, str], list[int]] = {}
    for e in entries:
        key = (e['server'], e['tool'])
        durations.setdefault(key, []).append(e.get('duration_ms', 0))

    lines = ['# MCP Dashboard\n', f'_Обновлено: {date.today().isoformat()}_\n']
    lines.append(f'**Всего вызовов:** {len(entries)}')
    lines.append(f'**Ошибок:** {len(errors)}')
    if entries:
        first_ts = entries[0].get('ts', '?')
        last_ts = entries[-1].get('ts', '?')
        lines.append(f'**Период:** {first_ts} — {last_ts}')

    lines.append('\n## По серверам\n')
    lines.append('| Сервер | Вызовов | Доля |')
    lines.append('|--------|---------|------|')
    total = sum(by_server.values())
    for srv, cnt in by_server.most_common():
        pct = round(cnt * 100 / total, 1)
        lines.append(f'| `{srv}` | {cnt} | {pct}% |')

    lines.append('\n## Топ-15 инструментов\n')
    lines.append('| Сервер | Инструмент | Вызовов | Avg ms | p95 ms |')
    lines.append('|--------|------------|---------|--------|--------|')
    for (srv, tool), cnt in by_tool.most_common(15):
        ds = durations[(srv, tool)]
        avg = round(sum(ds) / len(ds))
        p95 = sorted(ds)[int(len(ds) * 0.95)] if len(ds) >= 20 else max(ds)
        lines.append(f'| `{srv}` | `{tool}` | {cnt} | {avg} | {p95} |')

    if errors:
        lines.append('\n## Последние ошибки (топ-10)\n')
        for e in errors[-10:]:
            lines.append(f'- `{e.get("ts", "?")}` `{e.get("server", "?")}.{e.get("tool", "?")}` args={e.get("args", {})}')

    OUT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"→ {OUT_PATH.relative_to(ROOT)}")
    print(f"  {len(entries)} вызовов, {len(by_server)} серверов, {len(errors)} ошибок")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
