"""
improve_rss.py — генерирует RSS/Atom фид из истории git-коммитов.

Каждый коммит, затрагивающий docs/, становится элементом фида.
Фид описывает изменения в Knowledge Base Lorenzo/Svyazi 2.0.

Создаёт:
  docs/feed.rss  — RSS 2.0
  docs/feed.atom — Atom 1.0

Запуск:
    python scripts/improve_rss.py
    python scripts/improve_rss.py --max-items 30
    python scripts/improve_rss.py --base-url https://example.com/docs
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import formatdate
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MAX_ITEMS = 20
if "--max-items" in sys.argv:
    idx = sys.argv.index("--max-items")
    if idx + 1 < len(sys.argv):
        MAX_ITEMS = int(sys.argv[idx + 1])

BASE_URL = "https://github.com/svend4/lorenzo/blob/main"
if "--base-url" in sys.argv:
    idx = sys.argv.index("--base-url")
    if idx + 1 < len(sys.argv):
        BASE_URL = sys.argv[idx + 1]

FEED_TITLE = "Lorenzo / Svyazi 2.0 — обновления базы знаний"
FEED_DESC  = "Автоматический фид изменений документации Svyazi 2.0"


def _get_commits() -> list[dict]:
    """Получает последние коммиты, затрагивающие docs/."""
    result = subprocess.run(
        ["git", "log", f"--max-count={MAX_ITEMS * 3}", "--format=%H%n%ae%n%at%n%s%n---END---",
         "--", "docs/"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []

    commits = []
    for block in result.stdout.split("---END---\n"):
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n', 3)
        if len(lines) < 4:
            continue
        hash_, email, ts_str, subject = lines[0], lines[1], lines[2], lines[3]
        try:
            ts = int(ts_str)
        except ValueError:
            continue

        # Файлы в этом коммите
        files_result = subprocess.run(
            ["git", "show", "--name-only", "--format=", hash_],
            cwd=ROOT, capture_output=True, text=True,
        )
        changed_files = [f for f in files_result.stdout.strip().split('\n')
                         if f.startswith("docs/") and f.endswith(".md")]

        commits.append({
            "hash": hash_[:8],
            "full_hash": hash_,
            "email": email,
            "timestamp": ts,
            "subject": subject.strip(),
            "files": changed_files[:10],
        })

    return commits[:MAX_ITEMS]


def _rfc822(ts: int) -> str:
    return formatdate(ts, usegmt=True)


def _iso8601(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _build_description(commit: dict) -> str:
    lines = [f"<p><strong>{commit['subject']}</strong></p>"]
    if commit["files"]:
        lines.append("<p>Изменённые файлы:</p><ul>")
        for f in commit["files"]:
            url = f"{BASE_URL}/{f}"
            lines.append(f'<li><a href="{url}">{f}</a></li>')
        lines.append("</ul>")
    lines.append(f"<p>Коммит: <code>{commit['hash']}</code></p>")
    return "".join(lines)


def build_rss(commits: list[dict]) -> str:
    now_rfc = formatdate(usegmt=True)
    items = []
    for c in commits:
        desc = _build_description(c)
        link = f"https://github.com/svend4/lorenzo/commit/{c['full_hash']}"
        items.append(f"""    <item>
      <title>{_escape_xml(c['subject'])}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{_rfc822(c['timestamp'])}</pubDate>
      <description><![CDATA[{desc}]]></description>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{FEED_TITLE}</title>
    <link>https://github.com/svend4/lorenzo</link>
    <description>{FEED_DESC}</description>
    <language>ru</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


def build_atom(commits: list[dict]) -> str:
    now_iso = _iso8601(int(datetime.now(timezone.utc).timestamp()))
    entries = []
    for c in commits:
        desc = _build_description(c)
        link = f"https://github.com/svend4/lorenzo/commit/{c['full_hash']}"
        entries.append(f"""  <entry>
    <id>{link}</id>
    <title>{_escape_xml(c['subject'])}</title>
    <link href="{link}"/>
    <updated>{_iso8601(c['timestamp'])}</updated>
    <content type="html"><![CDATA[{desc}]]></content>
  </entry>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{FEED_TITLE}</title>
  <link href="https://github.com/svend4/lorenzo"/>
  <id>https://github.com/svend4/lorenzo</id>
  <updated>{now_iso}</updated>
  <subtitle>{FEED_DESC}</subtitle>
{chr(10).join(entries)}
</feed>
"""


def _escape_xml(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def main() -> None:
    print("📡 improve_rss.py — генерация RSS/Atom фида")
    print(f"   Макс. элементов: {MAX_ITEMS}\n")

    commits = _get_commits()
    if not commits:
        print("  ⚠️  Нет коммитов в docs/ (или git недоступен)")
        # Создаём пустой фид
        commits = []

    print(f"  Коммитов: {len(commits)}")

    rss = build_rss(commits)
    atom = build_atom(commits)

    rss_out = DOCS / "feed.rss"
    atom_out = DOCS / "feed.atom"

    rss_out.write_text(rss, encoding="utf-8")
    atom_out.write_text(atom, encoding="utf-8")

    print(f"  wrote: {rss_out.relative_to(ROOT)}")
    print(f"  wrote: {atom_out.relative_to(ROOT)}")
    if commits:
        print(f"  Последнее обновление: {commits[0]['subject'][:60]}")


if __name__ == "__main__":
    main()
