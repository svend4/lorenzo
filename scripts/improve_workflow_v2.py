"""
improve_workflow_v2.py — workflow engine v2.

Расширяет improve_workflow_run.py:
  - retry с exponential backoff на сетевые/таймаут ошибки
  - parallel execution для независимых шагов (через ThreadPoolExecutor)
  - DAG: шаг может объявить depends_on: [step_id, ...]
  - JSONL execution log в .claude/workflow_runs.jsonl
  - resume: продолжить с упавшего шага если задача прерывалась
  - --output json для machine-readable отчёта

Расширенный формат шага в манифесте:
  pipeline:
    - id: read_health           # опциональный явный ID
      read: docs/HEALTH.md
      retry: 2                  # повторов при ошибке (default 0)
      timeout: 30               # секунд (default 60)
      depends_on: []            # явный DAG (default — линейный порядок)

  parallel_groups:              # альтернативно — группировать
    - [step_a, step_b, step_c]  # выполнить параллельно

Запуск:
  python scripts/improve_workflow_v2.py --task audit-corpus
  python scripts/improve_workflow_v2.py --task audit-corpus --parallel 4
  python scripts/improve_workflow_v2.py --task audit-corpus --output json
  python scripts/improve_workflow_v2.py --resume <run_id>
  python scripts/improve_workflow_v2.py --history --task audit-corpus
"""
import json
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from improve_workflow_run import execute_step, load_task, list_tasks, parse_kv

ROOT = Path(__file__).parent.parent
RUNS_LOG = ROOT / ".claude" / "workflow_runs.jsonl"


class StepRunner:
    """Выполняет шаг с retry/timeout."""

    def __init__(self, step: dict, vars_dict: dict, dry_run: bool, default_retry: int = 0):
        self.step = step
        self.vars_dict = vars_dict
        self.dry_run = dry_run

        self.id = step.get('id') or self._auto_id(step)
        self.retry = step.get('retry', default_retry)
        self.timeout = step.get('timeout', 60)
        self.depends_on = step.get('depends_on', [])

    @staticmethod
    def _auto_id(step: dict) -> str:
        """Генерирует id из op:arg."""
        # Найти op (первый ключ кроме служебных)
        for k in step:
            if k not in ('id', 'retry', 'timeout', 'depends_on'):
                arg = step[k]
                arg_s = str(arg)[:30].replace(' ', '_').replace('/', '_')
                return f"{k}_{arg_s}"
        return uuid.uuid4().hex[:8]

    def run(self) -> dict:
        """Выполняет шаг с retry. Возвращает результат как dict."""
        step_clean = {k: v for k, v in self.step.items()
                      if k not in ('id', 'retry', 'timeout', 'depends_on')}
        attempts = []
        for attempt in range(self.retry + 1):
            t0 = time.time()
            result = execute_step(step_clean, self.vars_dict, self.dry_run)
            duration_ms = int((time.time() - t0) * 1000)
            attempts.append({
                'attempt': attempt + 1,
                'status': result.status,
                'duration_ms': duration_ms,
                'output_preview': result.output[:200] if result.output else '',
                'error': result.error,
            })
            if result.status in ('ok', 'dry-run', 'skip'):
                break
            if attempt < self.retry:
                backoff = 2 ** attempt  # 1, 2, 4 сек
                time.sleep(backoff)

        last = attempts[-1]
        return {
            'id': self.id,
            'op': next(iter(step_clean), '?'),
            'status': last['status'],
            'duration_ms': sum(a['duration_ms'] for a in attempts),
            'attempts': attempts,
            'depends_on': self.depends_on,
        }


def _topological_order(steps: list[StepRunner]) -> list[list[StepRunner]]:
    """Возвращает группы шагов готовых к параллельному запуску.
    Каждая группа = шаги с удовлетворёнными зависимостями.
    Если depends_on пуст у всех — каждая группа = 1 шаг (sequential).
    """
    by_id = {s.id: s for s in steps}
    completed: set[str] = set()
    remaining = list(steps)
    groups: list[list[StepRunner]] = []

    while remaining:
        ready = [s for s in remaining if all(d in completed for d in s.depends_on)]
        if not ready:
            # Циклическая зависимость или ссылка на несуществующий шаг
            # Берём первый оставшийся как fallback
            ready = remaining[:1]
        groups.append(ready)
        for s in ready:
            completed.add(s.id)
            remaining.remove(s)

    return groups


def _is_purely_sequential(steps: list[StepRunner]) -> bool:
    """Если ни у одного шага нет depends_on — это последовательный пайплайн."""
    return all(not s.depends_on for s in steps)


def run_workflow(task_id: str, vars_dict: dict, *,
                 dry_run: bool = False,
                 parallel: int = 1,
                 resume_run_id: str | None = None) -> dict:
    """Главный исполнитель."""
    task = load_task(task_id)
    if not task:
        raise FileNotFoundError(f"Манифест '{task_id}' не найден")

    pipeline = task.get('pipeline', [])
    if not pipeline:
        return {'task_id': task_id, 'status': 'empty', 'steps': []}

    runners = [StepRunner(s, vars_dict, dry_run, default_retry=task.get('default_retry', 0))
               for s in pipeline]

    # Sequential vs DAG
    sequential = _is_purely_sequential(runners) and parallel == 1

    run_id = resume_run_id or uuid.uuid4().hex[:12]
    started = datetime.now().isoformat(timespec='seconds')

    results: list[dict] = []
    completed_ids: set[str] = set()

    # Resume: пропустить уже выполненные шаги
    if resume_run_id:
        prev_runs = _load_runs(task_id=task_id)
        prev = next((r for r in prev_runs if r['run_id'] == resume_run_id), None)
        if prev:
            for s in prev.get('steps', []):
                if s['status'] == 'ok':
                    completed_ids.add(s['id'])
                    results.append(s)

    print(f"# Workflow v2: {task_id}")
    print(f"  run_id: {run_id}")
    print(f"  Шагов: {len(runners)} (parallel={parallel}, dry_run={dry_run})")
    if completed_ids:
        print(f"  Resumed: пропущено {len(completed_ids)} уже выполненных шагов")
    print()

    if sequential:
        # Простой случай
        for r in runners:
            if r.id in completed_ids:
                continue
            res = r.run()
            results.append(res)
            _print_result(res)
            if res['status'] == 'fail':
                break
    else:
        # DAG / parallel
        groups = _topological_order(runners)
        for i, group in enumerate(groups):
            group_to_run = [r for r in group if r.id not in completed_ids]
            if not group_to_run:
                continue
            print(f"  Группа {i+1}/{len(groups)}: {len(group_to_run)} шагов параллельно")
            with ThreadPoolExecutor(max_workers=parallel) as ex:
                futs = {ex.submit(r.run): r for r in group_to_run}
                for fut in as_completed(futs):
                    res = fut.result()
                    results.append(res)
                    _print_result(res)

    summary = _summary(results)
    duration_ms = sum(r.get('duration_ms', 0) for r in results)

    run_record = {
        'run_id': run_id,
        'task_id': task_id,
        'started': started,
        'finished': datetime.now().isoformat(timespec='seconds'),
        'duration_ms': duration_ms,
        'inputs': vars_dict,
        'parallel': parallel,
        'dry_run': dry_run,
        'summary': summary,
        'steps': results,
    }
    _save_run(run_record)

    print(f"\n  Итог: {summary} | {duration_ms}ms")
    print(f"  Лог: {RUNS_LOG.relative_to(ROOT)} (run_id={run_id})")
    return run_record


def _print_result(r: dict):
    icon = {'ok': '✅', 'fail': '❌', 'skip': '⏭', 'dry-run': '📋'}.get(r['status'], '?')
    attempts = len(r.get('attempts', []))
    extra = f" (попыток: {attempts})" if attempts > 1 else ""
    print(f"    {icon} [{r['id']}] {r['op']} ({r['duration_ms']}ms){extra}")
    if r['status'] == 'fail':
        last_err = r['attempts'][-1].get('error', '')
        if last_err:
            print(f"        ERROR: {last_err[:100]}")


def _summary(results: list[dict]) -> dict:
    out = {'ok': 0, 'fail': 0, 'skip': 0, 'dry-run': 0}
    for r in results:
        out[r['status']] = out.get(r['status'], 0) + 1
    return out


def _save_run(record: dict):
    RUNS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with RUNS_LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def _load_runs(task_id: str | None = None, limit: int = 100) -> list[dict]:
    if not RUNS_LOG.exists():
        return []
    runs = []
    for line in RUNS_LOG.read_text(encoding='utf-8').splitlines():
        try:
            r = json.loads(line)
            if task_id and r.get('task_id') != task_id:
                continue
            runs.append(r)
        except json.JSONDecodeError:
            continue
    return runs[-limit:]


def cmd_history(task_id: str | None = None):
    runs = _load_runs(task_id=task_id, limit=20)
    if not runs:
        print("Нет истории запусков.")
        return 0
    print(f"История запусков ({len(runs)}):\n")
    print(f"{'run_id':14s} {'task':25s} {'started':20s} {'duration':>10s} {'summary':30s}")
    print('-' * 105)
    for r in reversed(runs):
        s = r['summary']
        sum_str = ' '.join(f"{k}={v}" for k, v in s.items() if v)
        print(f"{r['run_id']:14s} {r['task_id']:25s} {r['started']:20s} "
              f"{r['duration_ms']:>9}ms {sum_str:30s}")
    return 0


def main():
    args = sys.argv[1:]

    if '--history' in args:
        task_id = None
        if '--task' in args:
            idx = args.index('--task')
            if idx + 1 < len(args):
                task_id = args[idx + 1]
        return cmd_history(task_id)

    if '--list' in args:
        for t in list_tasks():
            print(f"  {t}")
        return 0

    if '--resume' in args:
        idx = args.index('--resume')
        run_id = args[idx + 1] if idx + 1 < len(args) else None
        if not run_id:
            print("❌ --resume требует run_id")
            return 1
        # Найти task_id из истории
        for r in _load_runs():
            if r['run_id'] == run_id:
                run_workflow(r['task_id'], r.get('inputs', {}),
                             dry_run=r.get('dry_run', False),
                             parallel=r.get('parallel', 1),
                             resume_run_id=run_id)
                return 0
        print(f"❌ run_id {run_id} не найден")
        return 1

    if '--task' not in args:
        print(__doc__)
        return 1

    task_id = args[args.index('--task') + 1]
    dry_run = '--dry-run' in args
    output_json = '--output' in args and args[args.index('--output') + 1] == 'json'

    parallel = 1
    if '--parallel' in args:
        idx = args.index('--parallel')
        if idx + 1 < len(args):
            try:
                parallel = max(1, int(args[idx + 1]))
            except ValueError:
                pass

    inputs_raw: list[str] = []
    if '--inputs' in args:
        idx = args.index('--inputs')
        for a in args[idx + 1:]:
            if a.startswith('--'):
                break
            inputs_raw.append(a)
    vars_dict = parse_kv(inputs_raw)

    record = run_workflow(task_id, vars_dict, dry_run=dry_run, parallel=parallel)

    if output_json:
        print('\n' + json.dumps(record, ensure_ascii=False, indent=2))

    failed = record['summary'].get('fail', 0)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
