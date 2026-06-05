#!/usr/bin/env python3
"""
rerun_workflows.py — N-кратный повторный запуск workflow для проверки стабильности.

Цель: после очистки истории — прогнать чистые тесты несколько раз подряд через
workflow_dispatch и проверить flake rate (нестабильность).

Запускает один workflow N раз на указанной ветке, ждёт завершения каждого
запуска, агрегирует pass/fail/cancelled статистику.

Запуск:
  export GITHUB_TOKEN=ghp_xxx  # с правом actions:write

  # 3 запуска test.yml на main:
  python scripts/rerun_workflows.py test.yml --count 3

  # 5 запусков enrich-docs.yml с dry_run=true на feature ветке:
  python scripts/rerun_workflows.py enrich-docs.yml \
    --count 5 --branch claude/X --input dry_run=true

  # Не ждать (fire-and-forget):
  python scripts/rerun_workflows.py test.yml --count 3 --no-wait

  # Sequential (последовательно, не параллельно):
  python scripts/rerun_workflows.py test.yml --count 3 --sequential

Зачем это нужно:
  - Обнаружить flaky-тесты (упал 1 из 3 = flake)
  - Подтвердить, что фикс действительно стабилен
  - Замерить разброс по времени выполнения
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

OWNER = "svend4"
REPO = "lorenzo"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"

POLL_INTERVAL_S = 15      # сколько ждать между опросами статуса
MAX_WAIT_S = 60 * 30      # 30 минут максимум на один run


def _gh_request(method: str, path: str, token: str,
                payload: dict | None = None) -> tuple[int, dict]:
    """GitHub API request."""
    url = f"{API_BASE}{path}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        method=method,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, {"error": body[:300]}


def trigger_workflow(token: str, workflow_file: str, branch: str,
                     inputs: dict[str, str]) -> tuple[bool, str]:
    """Trigger workflow_dispatch event."""
    payload = {"ref": branch}
    if inputs:
        payload["inputs"] = inputs
    status, body = _gh_request(
        "POST",
        f"/actions/workflows/{workflow_file}/dispatches",
        token,
        payload=payload,
    )
    if status == 204:
        return True, "dispatched"
    return False, f"HTTP {status}: {body.get('error', '?')[:200]}"


def find_latest_dispatch_run(token: str, workflow_file: str,
                             branch: str, since_ts: float) -> dict | None:
    """Find the workflow run we just dispatched (by branch + timestamp)."""
    status, body = _gh_request(
        "GET",
        f"/actions/workflows/{workflow_file}/runs?event=workflow_dispatch"
        f"&branch={branch}&per_page=5",
        token,
    )
    if status != 200:
        return None
    for run in body.get("workflow_runs", []):
        created = datetime.fromisoformat(
            run["created_at"].replace("Z", "+00:00")
        ).timestamp()
        if created >= since_ts:
            return run
    return None


def wait_for_completion(token: str, run_id: int,
                        max_wait: int = MAX_WAIT_S) -> dict:
    """Poll until run completes or times out."""
    start = time.time()
    last_status = None
    while time.time() - start < max_wait:
        status, body = _gh_request("GET", f"/actions/runs/{run_id}", token)
        if status != 200:
            return {"error": f"API HTTP {status}", "elapsed": time.time() - start}
        run_status = body.get("status")
        if run_status != last_status:
            elapsed = int(time.time() - start)
            print(f"    [{elapsed:3d}s] status: {run_status}")
            last_status = run_status
        if run_status == "completed":
            return body
        time.sleep(POLL_INTERVAL_S)
    return {"error": "timeout", "elapsed": time.time() - start}


def run_once(token: str, workflow: str, branch: str,
             inputs: dict[str, str], wait: bool, run_num: int,
             total: int) -> dict:
    """Trigger workflow + optionally wait. Returns result dict."""
    print(f"\n▶ Run {run_num}/{total}: triggering {workflow} on {branch}...")
    t0 = time.time()
    since = t0 - 5  # маленький запас для propagation

    ok, msg = trigger_workflow(token, workflow, branch, inputs)
    if not ok:
        return {"run_num": run_num, "status": "trigger_failed", "error": msg}

    print(f"  ✓ dispatched. Searching for run_id...")

    # Wait a bit for run to materialize
    run = None
    for _ in range(6):  # 6×3s = 18s max
        time.sleep(3)
        run = find_latest_dispatch_run(token, workflow, branch, since)
        if run:
            break
    if not run:
        return {"run_num": run_num, "status": "run_not_found"}

    run_id = run["id"]
    run_url = run["html_url"]
    print(f"  ✓ run_id={run_id}  {run_url}")

    if not wait:
        return {
            "run_num": run_num,
            "run_id": run_id,
            "url": run_url,
            "status": "dispatched_no_wait",
        }

    print(f"  ⏳ waiting for completion (max {MAX_WAIT_S//60} min)...")
    result = wait_for_completion(token, run_id)
    elapsed = int(time.time() - t0)

    if "error" in result:
        return {"run_num": run_num, "run_id": run_id, "url": run_url,
                "status": result["error"], "elapsed_s": elapsed}

    conclusion = result.get("conclusion") or "?"
    print(f"  → conclusion: {conclusion}  ({elapsed}s total)")
    return {
        "run_num": run_num,
        "run_id": run_id,
        "url": run_url,
        "conclusion": conclusion,
        "elapsed_s": elapsed,
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workflow",
                    help="Workflow filename (e.g. test.yml, enrich-docs.yml)")
    ap.add_argument("--count", type=int, default=3,
                    help="Сколько раз запустить (default 3)")
    ap.add_argument("--branch", default="main",
                    help="Branch для запуска (default main)")
    ap.add_argument("--input", action="append", default=[],
                    metavar="KEY=VALUE",
                    help="workflow_dispatch input (можно несколько раз)")
    ap.add_argument("--no-wait", action="store_true",
                    help="Не ждать завершения (fire-and-forget)")
    ap.add_argument("--sequential", action="store_true",
                    help="Последовательно (один за другим), не параллельно")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN не установлен.", file=sys.stderr)
        return 2

    # Parse --input KEY=VALUE pairs
    inputs: dict[str, str] = {}
    for kv in args.input:
        if "=" not in kv:
            print(f"❌ --input '{kv}': ожидается KEY=VALUE", file=sys.stderr)
            return 2
        k, v = kv.split("=", 1)
        inputs[k.strip()] = v.strip()

    print(f"🔄 Запуск {args.workflow} × {args.count} раз "
          f"на ветке {args.branch}")
    if inputs:
        print(f"   Inputs: {inputs}")
    print()

    results: list[dict] = []
    for i in range(1, args.count + 1):
        r = run_once(token, args.workflow, args.branch, inputs,
                     wait=not args.no_wait, run_num=i, total=args.count)
        results.append(r)
        # Если sequential — ждали уже. Если parallel — задержка между триггерами.
        if not args.sequential and not args.no_wait and i < args.count:
            time.sleep(5)
        elif args.sequential and i < args.count:
            pass  # Уже ждали в wait_for_completion

    # Summary
    print("\n" + "=" * 60)
    print(f"СВОДКА: {args.workflow} × {args.count}")
    print("=" * 60)

    if args.json:
        print(json.dumps({"results": results}, indent=2, default=str))
        return 0

    by_conclusion: dict[str, int] = {}
    elapsed_list: list[int] = []
    for r in results:
        c = r.get("conclusion") or r.get("status") or "?"
        by_conclusion[c] = by_conclusion.get(c, 0) + 1
        if "elapsed_s" in r:
            elapsed_list.append(r["elapsed_s"])

    for c, n in sorted(by_conclusion.items(), key=lambda x: -x[1]):
        bar = "█" * (n * 40 // args.count)
        print(f"  {c:25s} {n:3d} {bar}")

    if elapsed_list:
        avg = sum(elapsed_list) / len(elapsed_list)
        print(f"\nВремя: min={min(elapsed_list)}s  "
              f"max={max(elapsed_list)}s  avg={avg:.0f}s")

    success = by_conclusion.get("success", 0)
    flake_rate = (args.count - success) / args.count * 100 if args.count else 0
    print(f"\nFlake rate: {flake_rate:.1f}% ({args.count - success}/{args.count})")

    if flake_rate > 0:
        print("⚠️  Тесты нестабильны (flaky). Рекомендация: найти причину.")
        return 1
    if success == args.count:
        print("✅ Стабильно — все запуски прошли.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
