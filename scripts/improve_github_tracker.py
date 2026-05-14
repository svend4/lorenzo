"""
improve_github_tracker.py — Мониторинг GitHub-репозиториев авторов Хабр-проектов.

Читает docs/contacts/*.md → извлекает GitHub-URL авторов → через GitHub API
получает последние коммиты, релизы и issues → создаёт Card Envelope события.

Каждое событие (новый коммит, релиз, issue) становится карточкой в docs/04-ai-collaborations/events/
с card_type=event, state=raw и ребром на проект.

Без токена: публичные репо, лимит 60 req/час.
С токеном (GITHUB_TOKEN): 5000 req/час.

Использование:
  python scripts/improve_github_tracker.py --dry-run    # показать что нашли
  python scripts/improve_github_tracker.py --apply      # создать карточки
  python scripts/improve_github_tracker.py --days 7     # события за 7 дней (по умолч.)
  python scripts/improve_github_tracker.py --days 30    # за месяц
  python scripts/improve_github_tracker.py --author kksudo  # только один автор
  python scripts/improve_github_tracker.py --stats      # статистика без запросов
"""
import re
import os
import sys
import json
import hashlib
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta, timezone

ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"
EVENTS_DIR = DOCS / "04-ai-collaborations" / "events"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Репозитории авторов (из docs/contacts/*.md и CONTACTS.md)
KNOWN_REPOS = {
    "kksudo":         ["kksudo/svyazi", "kksudo/agentfs"],
    "spbmolot":       ["spbmolot/ngt-memory"],
    "vitalyoborin":   ["VitalyOborin/yodoca", "VitalyOborin/wikontic"],
    "anastasiyaw":    ["AnastasiyaW/knowledge-space", "AnastasiyaW/mclaude"],
    "vitalysemenov":  ["VitaliySemenov/agent-memory-mcp"],
    "antipozitive":   ["Antipozitive/memnet"],
    "zodigancode":    ["zodigancode/rufler"],
    "nlaik":          ["nlaik/research-docs", "nlaik/liteparse"],
}


# ── GitHub API ───────────────────────────────────────────────────────────────

def _gh_get(url: str) -> dict | list | None:
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "lorenzo-tracker/1.0")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        if e.code == 403:
            print(f"  ⚠ Rate limit или приватный репо: {url}", file=sys.stderr)
            return None
        return None
    except Exception:
        return None


def _get_commits(repo: str, since_dt: datetime) -> list[dict]:
    since_iso = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    url  = f"https://api.github.com/repos/{repo}/commits?since={since_iso}&per_page=10"
    data = _gh_get(url)
    if not isinstance(data, list):
        return []
    events = []
    for c in data:
        commit = c.get("commit", {})
        message = commit.get("message", "").split("\n")[0][:200]
        sha = c.get("sha", "")[:8]
        author = commit.get("author", {}).get("name", "?")
        date_str = commit.get("author", {}).get("date", "")
        events.append({
            "type":    "commit",
            "repo":    repo,
            "sha":     sha,
            "message": message,
            "author":  author,
            "date":    date_str,
            "url":     c.get("html_url", ""),
        })
    return events


def _get_releases(repo: str, since_dt: datetime) -> list[dict]:
    url  = f"https://api.github.com/repos/{repo}/releases?per_page=5"
    data = _gh_get(url)
    if not isinstance(data, list):
        return []
    events = []
    for r in data:
        published = r.get("published_at", "")
        if published:
            try:
                pub_dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if pub_dt < since_dt.replace(tzinfo=timezone.utc):
                    continue
            except ValueError:
                pass
        events.append({
            "type":    "release",
            "repo":    repo,
            "name":    r.get("name") or r.get("tag_name", "?"),
            "body":    (r.get("body") or "")[:400],
            "date":    published,
            "url":     r.get("html_url", ""),
            "tag":     r.get("tag_name", ""),
        })
    return events


def _get_issues(repo: str, since_dt: datetime) -> list[dict]:
    since_iso = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    url  = f"https://api.github.com/repos/{repo}/issues?since={since_iso}&state=open&per_page=5"
    data = _gh_get(url)
    if not isinstance(data, list):
        return []
    events = []
    for i in data:
        if i.get("pull_request"):
            continue  # пропустить PR
        events.append({
            "type":   "issue",
            "repo":   repo,
            "number": i.get("number", "?"),
            "title":  i.get("title", "")[:200],
            "body":   (i.get("body") or "")[:300],
            "date":   i.get("created_at", ""),
            "url":    i.get("html_url", ""),
            "state":  i.get("state", "open"),
        })
    return events


# ── Карточки событий ─────────────────────────────────────────────────────────

def _event_to_card(ev: dict, author_handle: str) -> dict:
    repo  = ev["repo"]
    etype = ev["type"]
    date  = ev.get("date", datetime.now().strftime("%Y-%m-%d"))[:10]
    url   = ev.get("url", "")

    if etype == "commit":
        title   = f"[commit] {repo}: {ev['message'][:60]}"
        content = (
            f"**Репозиторий:** [{repo}](https://github.com/{repo})\n"
            f"**Коммит:** `{ev['sha']}`\n"
            f"**Автор:** {ev['author']}\n"
            f"**Дата:** {date}\n\n"
            f"**Сообщение:** {ev['message']}\n\n"
            f"[Открыть коммит]({url})"
        )
        tags = ["commit", "github-event", author_handle, repo.split("/")[-1]]

    elif etype == "release":
        title   = f"[release] {repo} {ev['name']}"
        content = (
            f"**Репозиторий:** [{repo}](https://github.com/{repo})\n"
            f"**Релиз:** {ev['name']} (тег: `{ev['tag']}`)\n"
            f"**Дата:** {date}\n\n"
            + (f"**Описание:**\n{ev['body']}\n\n" if ev.get("body") else "")
            + f"[Открыть релиз]({url})"
        )
        tags = ["release", "github-event", author_handle, repo.split("/")[-1]]

    else:  # issue
        title   = f"[issue] {repo} #{ev['number']}: {ev['title'][:50]}"
        content = (
            f"**Репозиторий:** [{repo}](https://github.com/{repo})\n"
            f"**Issue #{ev['number']}:** {ev['title']}\n"
            f"**Статус:** {ev.get('state', 'open')}\n"
            f"**Дата:** {date}\n\n"
            + (f"**Описание:**\n{ev['body']}\n\n" if ev.get("body") else "")
            + f"[Открыть issue]({url})"
        )
        tags = ["issue", "github-event", author_handle, repo.split("/")[-1]]

    card_id = hashlib.sha256(f"{etype}{repo}{ev.get('sha', ev.get('number', title))}".encode()).hexdigest()[:12]
    slug    = re.sub(r"[^a-z0-9]+", "-", title.lower())[:60].strip("-")

    return {
        "card_id":   card_id,
        "card_type": "event",
        "state":     "raw",
        "title":     title,
        "content":   content,
        "tags":      tags,
        "date":      date,
        "slug":      slug,
        "repo":      repo,
        "author":    author_handle,
    }


def _card_exists(card_id: str) -> bool:
    for f in EVENTS_DIR.rglob("*.md"):
        if card_id in f.read_text(encoding="utf-8", errors="ignore"):
            return True
    return False


def _write_card(card: dict) -> Path:
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    tags_str = ", ".join(card["tags"])
    md = f"""---
title: "{card['title']}"
date: {card['date']}
card_id: {card['card_id']}
card_type: {card['card_type']}
state: {card['state']}
tags: [{tags_str}]
repo: {card['repo']}
source: github-tracker
---

# {card['title']}

<!-- summary -->
> Событие GitHub: {card['card_type']} в {card['repo']}

<!-- tags: {tags_str} -->

{card['content']}

---
_Обнаружено github-tracker: {datetime.now().strftime('%Y-%m-%d')}_
"""
    filepath = EVENTS_DIR / f"{card['slug']}.md"
    filepath.write_text(md, encoding="utf-8")
    return filepath


# ── Главная логика ───────────────────────────────────────────────────────────

def run(dry_run: bool, days: int, author_filter: str, stats_only: bool):
    since_dt = datetime.now() - timedelta(days=days)

    if stats_only:
        existing = list(EVENTS_DIR.rglob("*.md")) if EVENTS_DIR.exists() else []
        print(f"📊 GitHub Tracker статистика:")
        print(f"  Существующих event-карточек: {len(existing)}")
        print(f"  Репозиториев отслеживается: {sum(len(v) for v in KNOWN_REPOS.values())}")
        print(f"  Авторов: {len(KNOWN_REPOS)}")
        if GITHUB_TOKEN:
            print(f"  GITHUB_TOKEN: ✅ (5000 req/час)")
        else:
            print(f"  GITHUB_TOKEN: ⬜ (60 req/час, только публичные)")
        return

    mode = "dry-run" if dry_run else "apply"
    print(f"🔍 GitHub Tracker [{mode}] — события за последние {days} дней")
    if not GITHUB_TOKEN:
        print("  ⚠ GITHUB_TOKEN не задан, лимит 60 req/час")

    all_events: list[dict] = []

    repos_to_check: dict[str, list[str]] = {}
    if author_filter:
        key = author_filter.lower()
        for k, v in KNOWN_REPOS.items():
            if key in k:
                repos_to_check[k] = v
    else:
        repos_to_check = KNOWN_REPOS

    for author, repos in repos_to_check.items():
        for repo in repos:
            print(f"  Проверяю {repo}...", end=" ", flush=True)
            commits  = _get_commits(repo, since_dt)
            releases = _get_releases(repo, since_dt)
            issues   = _get_issues(repo, since_dt)
            total    = len(commits) + len(releases) + len(issues)
            print(f"commits={len(commits)} releases={len(releases)} issues={len(issues)}")
            for ev in commits + releases + issues:
                card = _event_to_card(ev, author)
                all_events.append(card)

    print(f"\nНайдено событий: {len(all_events)}")

    new_cards = 0
    skipped   = 0
    for card in all_events:
        if _card_exists(card["card_id"]):
            skipped += 1
            continue
        if dry_run:
            print(f"  [dry] {card['title'][:70]}")
        else:
            path = _write_card(card)
            print(f"  ✅ {path.relative_to(ROOT)}")
            new_cards += 1

    if not dry_run and new_cards:
        import subprocess
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, timeout=60,
        )
        print(f"\n✅ Создано карточек: {new_cards} | Пропущено дублей: {skipped}")
    elif dry_run:
        print(f"\nℹ️  Запустите с --apply чтобы создать карточки ({len(all_events) - skipped} новых)")

    # Записать отчёт
    _write_tracker_report(all_events, new_cards if not dry_run else 0, days)


def _write_tracker_report(events: list, new_cards: int, days: int):
    report_path = DOCS / "GITHUB_TRACKER.md"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    by_repo: dict[str, list] = {}
    for ev in events:
        by_repo.setdefault(ev["repo"], []).append(ev)
    lines = [
        f"# GitHub Tracker Report\n",
        f"_Обновлено: {date} | За {days} дней | Создано: {new_cards} карточек_\n",
    ]
    for repo, evs in sorted(by_repo.items()):
        lines.append(f"\n## {repo} ({len(evs)} событий)")
        for ev in evs[:5]:
            lines.append(f"- [{ev['card_type']}] {ev['title'][:80]}")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="GitHub Tracker: мониторинг репозиториев авторов")
    parser.add_argument("--dry-run",  action="store_true", default=True,  help="Показать без создания")
    parser.add_argument("--apply",    action="store_true",                 help="Создать карточки")
    parser.add_argument("--days",     type=int, default=7,                 help="За сколько дней (по умолч. 7)")
    parser.add_argument("--author",   default="",                          help="Фильтр по автору")
    parser.add_argument("--stats",    action="store_true",                 help="Только статистика")
    args = parser.parse_args()
    run(dry_run=not args.apply, days=args.days, author_filter=args.author, stats_only=args.stats)


if __name__ == "__main__":
    main()
