"""Git-based time-travel: чтение/diff любого commit'а через git CLI."""
import subprocess
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


class GitError(Exception):
    pass


def _git(*args: str, cwd: Path = None) -> str:
    """Запуск git с capture. Возвращает stdout, raises GitError при ошибке."""
    cwd = cwd or load_config().root
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def snapshot_at(path: str, ref: str = "HEAD") -> str:
    """Содержимое файла на указанный ref (commit / tag / branch)."""
    try:
        return _git("show", f"{ref}:{path}")
    except GitError as e:
        if "exists on disk, but not in" in str(e) or "does not exist" in str(e):
            return ""
        raise


def list_commits(path: str = "", limit: int = 50,
                  since: str = "", until: str = "") -> list[dict]:
    """Список коммитов которые трогали path (или весь репо если path пуст).

    Возвращает [{sha, short_sha, ts, author, message}, ...]
    """
    args = ["log", f"-{limit}", "--pretty=format:%H|%h|%ai|%an|%s"]
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")
    if path:
        args.extend(["--", path])

    output = _git(*args)
    commits = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue
        commits.append({
            "sha": parts[0],
            "short_sha": parts[1],
            "ts": parts[2],
            "author": parts[3],
            "message": parts[4],
        })
    return commits


def diff_between(path: str, ref_from: str, ref_to: str = "HEAD") -> str:
    """Unified diff между двумя ref'ами для файла или директории."""
    try:
        return _git("diff", f"{ref_from}..{ref_to}", "--", path)
    except GitError as e:
        return f"# Error: {e}"


def file_history(path: str, limit: int = 20) -> list[dict]:
    """История одного файла: [{commit, ts, additions, deletions}]."""
    args = ["log", f"-{limit}", "--pretty=format:%H|%ai", "--numstat", "--", path]
    output = _git(*args)

    history = []
    current = None
    for line in output.splitlines():
        line = line.strip()
        if not line:
            if current:
                history.append(current)
                current = None
            continue
        if "|" in line and len(line.split("|")) == 2 and len(line.split("|")[0]) == 40:
            if current:
                history.append(current)
            sha, ts = line.split("|")
            current = {"sha": sha, "short_sha": sha[:7], "ts": ts,
                       "additions": 0, "deletions": 0}
        elif current and "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 3:
                try:
                    current["additions"] += int(parts[0]) if parts[0] != "-" else 0
                    current["deletions"] += int(parts[1]) if parts[1] != "-" else 0
                except ValueError:
                    pass

    if current:
        history.append(current)
    return history


def list_dates(start: str = "", end: str = "") -> list[str]:
    """Уникальные даты коммитов в репо."""
    args = ["log", "--pretty=format:%ai"]
    if start:
        args.append(f"--since={start}")
    if end:
        args.append(f"--until={end}")
    output = _git(*args)
    dates = set()
    for line in output.splitlines():
        if line:
            dates.add(line[:10])  # YYYY-MM-DD
    return sorted(dates)


def find_introduced(token: str, file_pattern: str = "",
                     limit_commits: int = 200) -> dict | None:
    """Бинарный поиск: какой commit ввёл token в репо.

    Простая реализация — линейная (не настоящий bisect).
    Для большой истории — slow, но даёт точный ответ.
    """
    commits = list_commits(limit=limit_commits)
    if not commits:
        return None

    # Найти первый commit где token присутствует
    found_in = None
    for commit in commits:  # от newest к oldest
        try:
            args = ["grep", "--cached", "-l", token, commit["sha"]]
            try:
                output = _git("grep", "-l", token, commit["sha"], "--",
                               file_pattern or ".")
                if output.strip():
                    found_in = commit
                else:
                    break  # дальше старее — token уже не было
            except GitError:
                break
        except Exception:
            continue

    return found_in
