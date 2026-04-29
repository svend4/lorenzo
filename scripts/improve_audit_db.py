"""
improve_audit_db.py — SQLite audit log для всех событий системы.

Собирает 4 типа событий из jsonl-файлов в единую SQLite БД:
  - mcp_calls (.claude/mcp_calls.jsonl)
  - workflow_runs (.claude/workflow_runs.jsonl)
  - skill_metrics (.claude/skill_metrics.jsonl)
  - llm_cache (.claude/llm_cache.jsonl)

Запросы:
    python scripts/improve_audit_db.py --rebuild        # пересоздать
    python scripts/improve_audit_db.py --query "SELECT server, COUNT(*) FROM mcp_calls GROUP BY server"
    python scripts/improve_audit_db.py --top-tools 10
    python scripts/improve_audit_db.py --slow-calls 100  # вызовы > 100ms
    python scripts/improve_audit_db.py --recent 10
    python scripts/improve_audit_db.py --workflow-stats
"""
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
CLAUDE_DIR = ROOT / ".claude"
DB_PATH = CLAUDE_DIR / "audit.sqlite"


SCHEMA = """
CREATE TABLE IF NOT EXISTS mcp_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    server TEXT NOT NULL,
    tool TEXT NOT NULL,
    args_json TEXT,
    duration_ms INTEGER,
    status TEXT
);
CREATE INDEX IF NOT EXISTS idx_mcp_ts ON mcp_calls(ts);
CREATE INDEX IF NOT EXISTS idx_mcp_server_tool ON mcp_calls(server, tool);
CREATE INDEX IF NOT EXISTS idx_mcp_status ON mcp_calls(status);

CREATE TABLE IF NOT EXISTS workflow_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT UNIQUE NOT NULL,
    task_id TEXT NOT NULL,
    started TEXT NOT NULL,
    finished TEXT,
    duration_ms INTEGER,
    parallel INTEGER DEFAULT 1,
    dry_run INTEGER DEFAULT 0,
    summary_json TEXT,
    inputs_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_wf_task ON workflow_runs(task_id);
CREATE INDEX IF NOT EXISTS idx_wf_started ON workflow_runs(started);

CREATE TABLE IF NOT EXISTS workflow_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    step_id TEXT NOT NULL,
    op TEXT,
    status TEXT,
    duration_ms INTEGER,
    attempts INTEGER DEFAULT 1,
    FOREIGN KEY(run_id) REFERENCES workflow_runs(run_id)
);
CREATE INDEX IF NOT EXISTS idx_step_run ON workflow_steps(run_id);

CREATE TABLE IF NOT EXISTS skill_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    skill TEXT NOT NULL,
    request TEXT,
    helpful INTEGER,
    honest INTEGER,
    complete INTEGER,
    efficient INTEGER,
    feedback TEXT
);
CREATE INDEX IF NOT EXISTS idx_skill_ts ON skill_metrics(ts);
CREATE INDEX IF NOT EXISTS idx_skill_name ON skill_metrics(skill);
"""


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def rebuild():
    """Пересоздаёт БД из jsonl логов."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = get_db()

    counts = {'mcp_calls': 0, 'workflow_runs': 0, 'workflow_steps': 0, 'skill_metrics': 0}

    # mcp_calls.jsonl
    mcp_log = CLAUDE_DIR / "mcp_calls.jsonl"
    if mcp_log.exists():
        for line in mcp_log.read_text(encoding='utf-8').splitlines():
            try:
                e = json.loads(line)
                conn.execute(
                    "INSERT INTO mcp_calls (ts, server, tool, args_json, duration_ms, status) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (e.get('ts', ''), e.get('server', ''), e.get('tool', ''),
                     json.dumps(e.get('args', {}), ensure_ascii=False),
                     e.get('duration_ms', 0), e.get('status', 'ok'))
                )
                counts['mcp_calls'] += 1
            except (json.JSONDecodeError, sqlite3.Error):
                continue

    # workflow_runs.jsonl
    wf_log = CLAUDE_DIR / "workflow_runs.jsonl"
    if wf_log.exists():
        for line in wf_log.read_text(encoding='utf-8').splitlines():
            try:
                r = json.loads(line)
                conn.execute(
                    "INSERT OR IGNORE INTO workflow_runs "
                    "(run_id, task_id, started, finished, duration_ms, parallel, dry_run, "
                    "summary_json, inputs_json) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (r['run_id'], r.get('task_id', ''),
                     r.get('started', ''), r.get('finished', ''),
                     r.get('duration_ms', 0),
                     r.get('parallel', 1),
                     1 if r.get('dry_run') else 0,
                     json.dumps(r.get('summary', {}), ensure_ascii=False),
                     json.dumps(r.get('inputs', {}), ensure_ascii=False))
                )
                counts['workflow_runs'] += 1
                for s in r.get('steps', []):
                    conn.execute(
                        "INSERT INTO workflow_steps (run_id, step_id, op, status, duration_ms, attempts) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (r['run_id'], s.get('id', ''), s.get('op', ''),
                         s.get('status', ''), s.get('duration_ms', 0),
                         len(s.get('attempts', [])))
                    )
                    counts['workflow_steps'] += 1
            except (json.JSONDecodeError, sqlite3.Error, KeyError):
                continue

    # skill_metrics.jsonl
    sk_log = CLAUDE_DIR / "skill_metrics.jsonl"
    if sk_log.exists():
        for line in sk_log.read_text(encoding='utf-8').splitlines():
            try:
                e = json.loads(line)
                scores = e.get('scores', {})
                conn.execute(
                    "INSERT INTO skill_metrics (ts, skill, request, helpful, honest, complete, efficient, feedback) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (e.get('ts', ''), e.get('skill', ''), e.get('request', ''),
                     scores.get('helpful'), scores.get('honest'),
                     scores.get('complete'), scores.get('efficient'),
                     e.get('feedback', ''))
                )
                counts['skill_metrics'] += 1
            except (json.JSONDecodeError, sqlite3.Error):
                continue

    conn.commit()
    conn.close()
    print(f"✓ Пересоздана БД: {DB_PATH.relative_to(ROOT)}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


def cmd_query(sql: str):
    conn = get_db()
    try:
        rows = conn.execute(sql).fetchall()
    except sqlite3.Error as e:
        print(f"❌ {e}")
        return 1
    if not rows:
        print("(пусто)")
        return 0
    cols = rows[0].keys()
    widths = [max(len(c), max(len(str(r[c])) for r in rows)) for c in cols]
    print(" | ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("-+-".join('-' * w for w in widths))
    for r in rows:
        print(" | ".join(str(r[c]).ljust(w) for c, w in zip(cols, widths)))
    return 0


def cmd_top_tools(n: int = 10):
    return cmd_query(
        f"SELECT server, tool, COUNT(*) AS calls, "
        f"AVG(duration_ms) AS avg_ms, MAX(duration_ms) AS max_ms "
        f"FROM mcp_calls GROUP BY server, tool "
        f"ORDER BY calls DESC LIMIT {n}"
    )


def cmd_slow_calls(threshold_ms: int = 100):
    return cmd_query(
        f"SELECT ts, server, tool, duration_ms, status "
        f"FROM mcp_calls WHERE duration_ms > {threshold_ms} "
        f"ORDER BY duration_ms DESC LIMIT 20"
    )


def cmd_recent(n: int = 10):
    return cmd_query(
        f"SELECT ts, server, tool, duration_ms, status FROM mcp_calls "
        f"ORDER BY id DESC LIMIT {n}"
    )


def cmd_workflow_stats():
    return cmd_query(
        "SELECT task_id, COUNT(*) AS runs, "
        "AVG(duration_ms) AS avg_ms, "
        "SUM(CASE WHEN dry_run = 0 THEN 1 ELSE 0 END) AS real_runs "
        "FROM workflow_runs GROUP BY task_id ORDER BY runs DESC"
    )


def main():
    args = sys.argv[1:]

    if '--rebuild' in args:
        rebuild()
        return 0

    if '--query' in args:
        idx = args.index('--query')
        if idx + 1 >= len(args):
            print("❌ --query требует SQL")
            return 1
        return cmd_query(args[idx + 1])

    if '--top-tools' in args:
        idx = args.index('--top-tools')
        n = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 10
        return cmd_top_tools(n)

    if '--slow-calls' in args:
        idx = args.index('--slow-calls')
        thr = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 100
        return cmd_slow_calls(thr)

    if '--recent' in args:
        idx = args.index('--recent')
        n = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 10
        return cmd_recent(n)

    if '--workflow-stats' in args:
        return cmd_workflow_stats()

    # Default: rebuild + summary
    rebuild()
    print("\n— Топ-5 инструментов —")
    cmd_top_tools(5)
    print("\n— Workflow stats —")
    cmd_workflow_stats()
    return 0


if __name__ == '__main__':
    sys.exit(main())
