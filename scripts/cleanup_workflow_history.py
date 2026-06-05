#!/usr/bin/env python3
"""
cleanup_workflow_history.py — автоматическая очистка истории GitHub Actions.

Цель: удалить дубликаты и устаревшие workflow runs, оставив чистую историю.

Что считается «дубликатом»:
  - Несколько runs одного workflow на одном head_sha с одинаковым conclusion
    (например, 3 ручных запуска test.yml на одном коммите main → оставляем 1)
  - Cancelled runs (нет полезной информации)
  - Старые failed runs, к которым уже есть позднее successful run

Что НЕ удаляется (защита):
  - Runs в статусе queued / in_progress / waiting (могут быть нужны)
  - Самый свежий run каждого workflow на main (контрольная точка)
  - Runs за последние N дней (--keep-days, default 7)

Запуск:
  # 1. Получить токен (Personal Access Token с правами actions:write):
  #    https://github.com/settings/tokens?type=beta
  #    Permissions: Actions: Read and write
  export GITHUB_TOKEN=ghp_xxx

  # 2. Dry-run (только показать что было бы удалено):
  python scripts/cleanup_workflow_history.py

  # 3. Реальное удаление:
  python scripts/cleanup_workflow_history.py --apply

  # 4. Фильтры:
  python scripts/cleanup_workflow_history.py --workflow test.yml      # только один
  python scripts/cleanup_workflow_history.py --keep-days 30           # старше 30 дней
  python scripts/cleanup_workflow_history.py --status cancelled       # только cancelled
  python scripts/cleanup_workflow_history.py --max-delete 100         # лимит для безопасности

Альтернатива: gh CLI (если установлен):
  gh run list --status cancelled --limit 100 --json databaseId \
    -q '.[].databaseId' | xargs -I{} gh run delete {}
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

OWNER = "svend4"
REPO = "lorenzo"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _gh_request(method: str, path: str, token: str,
                page: int | None = None) -> tuple[int, dict]:
    """GitHub API request. Returns (status_code, json_body)."""
    url = f"{API_BASE}{path}"
    if page is not None:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}per_page=100&page={page}"
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, {"error": body[:200]}


def list_all_runs(token: str, workflow: str | None = None) -> list[dict]:
    """Fetch all workflow runs (auto-paginate)."""
    path = "/actions/runs"
    if workflow:
        path = f"/actions/workflows/{workflow}/runs"
    runs: list[dict] = []
    for page in range(1, 50):  # safety cap
        status, body = _gh_request("GET", path, token, page=page)
        if status != 200:
            print(f"⚠️ API error {status}: {body.get('error', '?')[:200]}",
                  file=sys.stderr)
            break
        batch = body.get("workflow_runs", [])
        runs.extend(batch)
        if len(batch) < 100:
            break
    return runs


def delete_run(run_id: int, token: str) -> tuple[bool, str]:
    """Delete one workflow run. Returns (success, message)."""
    status, body = _gh_request("DELETE", f"/actions/runs/{run_id}", token)
    if status == 204:
        return True, "deleted"
    return False, f"HTTP {status}: {body.get('error', '?')[:100]}"


# ── Dedup logic ───────────────────────────────────────────────────────────────

def is_active(run: dict) -> bool:
    """True if run shouldn't be touched (queued/running/waiting)."""
    return run.get("status") in {"queued", "in_progress", "waiting", "pending"}


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def find_runs_to_delete(
    runs: list[dict],
    keep_days: int = 7,
    status_filter: str | None = None,
    keep_latest_per_group: int = 1,
) -> tuple[list[dict], dict]:
    """Returns (runs_to_delete, stats_dict)."""
    now = datetime.now(timezone.utc)
    keep_threshold = now - timedelta(days=keep_days)

    stats = {
        "total": len(runs),
        "active_skipped": 0,
        "recent_skipped": 0,
        "kept_as_latest": 0,
        "to_delete": 0,
        "by_workflow": defaultdict(int),
        "by_conclusion": defaultdict(int),
    }

    to_delete: list[dict] = []

    # Group by (workflow_name, head_sha, conclusion)
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for run in runs:
        if is_active(run):
            stats["active_skipped"] += 1
            continue

        created = parse_iso(run["created_at"])
        if created > keep_threshold:
            stats["recent_skipped"] += 1
            continue

        if status_filter and run.get("conclusion") != status_filter:
            continue

        key = (run["name"], run["head_sha"], run.get("conclusion"))
        groups[key].append(run)

    # Within each group: keep latest N, mark rest for deletion
    for key, group_runs in groups.items():
        group_runs.sort(key=lambda r: r["created_at"], reverse=True)
        keep = group_runs[:keep_latest_per_group]
        delete = group_runs[keep_latest_per_group:]
        stats["kept_as_latest"] += len(keep)
        for r in delete:
            to_delete.append(r)
            stats["by_workflow"][r["name"]] += 1
            stats["by_conclusion"][r.get("conclusion") or "unknown"] += 1

    stats["to_delete"] = len(to_delete)
    return to_delete, stats


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="Реально удалить (по умолчанию dry-run)")
    ap.add_argument("--workflow",
                    help="Только конкретный workflow (file name, e.g. test.yml)")
    ap.add_argument("--keep-days", type=int, default=7,
                    help="Защитить runs за последние N дней (default 7)")
    ap.add_argument("--status",
                    choices=["success", "failure", "cancelled", "skipped",
                             "timed_out", "action_required"],
                    help="Удалять только runs с этим conclusion")
    ap.add_argument("--max-delete", type=int, default=500,
                    help="Жёсткий лимит удалений (default 500)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN не установлен.", file=sys.stderr)
        print("   Получить токен: https://github.com/settings/tokens?type=beta",
              file=sys.stderr)
        print("   Нужно permission: Actions: Read and write", file=sys.stderr)
        print("   Затем: export GITHUB_TOKEN=ghp_xxx", file=sys.stderr)
        return 2

    print(f"🔍 Получаю историю workflow runs из {OWNER}/{REPO}...",
          file=sys.stderr)
    runs = list_all_runs(token, args.workflow)
    if not runs:
        print("❌ Не удалось получить runs (или их 0).", file=sys.stderr)
        return 1
    print(f"   Получено: {len(runs)} runs\n", file=sys.stderr)

    to_delete, stats = find_runs_to_delete(
        runs,
        keep_days=args.keep_days,
        status_filter=args.status,
    )

    if args.json:
        print(json.dumps({
            "stats": stats,
            "to_delete": [{"id": r["id"], "name": r["name"],
                          "head_sha": r["head_sha"][:8],
                          "conclusion": r.get("conclusion"),
                          "created_at": r["created_at"]}
                         for r in to_delete[:args.max_delete]],
        }, ensure_ascii=False, indent=2, default=str))
        return 0

    # Human-readable report
    print("=" * 72)
    print(f"ОТЧЁТ ОЧИСТКИ WORKFLOW RUNS — {OWNER}/{REPO}")
    print("=" * 72)
    print(f"Всего runs:                   {stats['total']}")
    print(f"Active (skipped, защищены):   {stats['active_skipped']}")
    print(f"Recent (skipped, < {args.keep_days} дней): {stats['recent_skipped']}")
    print(f"Оставлено как latest:          {stats['kept_as_latest']}")
    print(f"К удалению:                    {stats['to_delete']}")

    if stats["by_workflow"]:
        print("\nПо workflow:")
        for wf, count in sorted(stats["by_workflow"].items(),
                                key=lambda x: -x[1]):
            print(f"  {wf:30s} {count:5d}")

    if stats["by_conclusion"]:
        print("\nПо conclusion:")
        for concl, count in sorted(stats["by_conclusion"].items(),
                                   key=lambda x: -x[1]):
            print(f"  {concl:15s} {count:5d}")

    if not to_delete:
        print("\n✅ Нечего удалять.")
        return 0

    # Show first/last 5 for sanity check
    print("\nПримеры (первые 5):")
    for r in to_delete[:5]:
        print(f"  #{r['id']:12d} {r['name']:25.25s} "
              f"sha={r['head_sha'][:8]} "
              f"{r.get('conclusion') or '?':10s} "
              f"{r['created_at'][:16]}")

    if len(to_delete) > 5:
        print(f"  … и ещё {len(to_delete) - 5}")

    # Safety cap
    actual_delete = to_delete[:args.max_delete]
    if len(to_delete) > args.max_delete:
        print(f"\n⚠️  --max-delete={args.max_delete} применён, "
              f"к удалению из {len(to_delete)} → {len(actual_delete)}")

    if not args.apply:
        print("\n💡 Это DRY-RUN. Реально не удалено ничего.")
        print(f"   Для удаления: python {sys.argv[0]} --apply ...")
        return 0

    # Real delete
    print(f"\n🗑  Удаляю {len(actual_delete)} runs...")
    deleted = 0
    failed = 0
    for i, r in enumerate(actual_delete, 1):
        ok, msg = delete_run(r["id"], token)
        if ok:
            deleted += 1
            if i % 10 == 0 or i == len(actual_delete):
                print(f"  [{i}/{len(actual_delete)}] deleted={deleted} "
                      f"failed={failed}")
        else:
            failed += 1
            print(f"  ❌ #{r['id']}: {msg}", file=sys.stderr)
        # Rate limit safety
        if i % 25 == 0:
            time.sleep(1)

    print(f"\n✅ Готово. Удалено: {deleted}, ошибок: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
