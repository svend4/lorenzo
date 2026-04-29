"""
improve_export_html.py — экспортирует все docs/ в единый HTML-сайт.
Создаёт docs/index.html с навигацией и содержимым всех файлов.
Запуск: python scripts/improve_export_html.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

CSS = """
body { font-family: -apple-system, sans-serif; margin: 0; display: flex; }
nav { width: 260px; min-height: 100vh; background: #1e1e2e; color: #cdd6f4;
      padding: 16px; position: fixed; overflow-y: auto; font-size: 13px; }
nav h2 { color: #89b4fa; margin: 0 0 12px; font-size: 14px; }
nav a { color: #a6e3a1; text-decoration: none; display: block;
        padding: 2px 0; line-height: 1.5; }
nav a:hover { color: #cba6f7; }
nav .section { color: #f38ba8; font-weight: bold; margin: 10px 0 4px; }
main { margin-left: 276px; padding: 24px 40px; max-width: 900px; }
h1 { color: #1e66f5; }
h2 { color: #179299; border-bottom: 1px solid #eee; padding-bottom: 4px; }
h3 { color: #40a02b; }
code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 13px; }
pre { background: #1e1e2e; color: #cdd6f4; padding: 16px; border-radius: 6px;
      overflow-x: auto; font-size: 13px; }
blockquote { border-left: 3px solid #89b4fa; padding-left: 12px; color: #555; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th { background: #1e66f5; color: white; padding: 6px 10px; text-align: left; }
td { border: 1px solid #ddd; padding: 6px 10px; }
tr:nth-child(even) { background: #f9f9f9; }
.doc-section { border-top: 3px solid #1e66f5; margin: 40px 0 20px; padding-top: 20px; }
.tag { background: #e0f2fe; color: #0369a1; padding: 1px 6px;
       border-radius: 10px; font-size: 11px; margin-right: 4px; }
.summary-box { background: #f0fdf4; border-left: 3px solid #22c55e;
               padding: 8px 12px; margin: 8px 0; font-size: 14px; }
"""


def md_to_html(text: str) -> str:
    """Простой Markdown → HTML конвертер."""
    # Убираем теги-комментарии
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    lines = text.split('\n')
    html = []
    in_code = False
    in_table = False

    for line in lines:
        # Код-блок
        if line.startswith('```'):
            if in_code:
                html.append('</code></pre>')
                in_code = False
            else:
                lang = line[3:].strip()
                html.append(f'<pre><code class="language-{lang}">')
                in_code = True
            continue

        if in_code:
            html.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            continue

        # Таблица
        if line.startswith('|'):
            if not in_table:
                html.append('<table>')
                in_table = True
            if re.match(r'\|[-| :]+\|', line):
                continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            tag = 'th' if not any('<td>' in h for h in html[-3:]) else 'td'
            html.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
            continue
        elif in_table:
            html.append('</table>')
            in_table = False

        # Заголовки
        if line.startswith('# '):
            html.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html.append(f'<h4>{line[5:]}</h4>')
        elif line.startswith('> '):
            html.append(f'<blockquote>{line[2:]}</blockquote>')
        elif line.startswith('- ') or line.startswith('* '):
            html.append(f'<li>{line[2:]}</li>')
        elif line.strip() == '---':
            html.append('<hr>')
        elif line.strip():
            # Инлайн форматирование
            l = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            l = re.sub(r'\*(.+?)\*', r'<em>\1</em>', l)
            l = re.sub(r'`(.+?)`', r'<code>\1</code>', l)
            l = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', l)
            html.append(f'<p>{l}</p>')
        else:
            html.append('<br>')

    if in_table:
        html.append('</table>')
    return '\n'.join(html)


def build_nav(sections: dict) -> str:
    nav = ['<nav>', '<h2>📚 Lorenzo Docs</h2>']
    for section, files in sections.items():
        nav.append(f'<div class="section">{section}</div>')
        for fpath, title in files:
            anchor = fpath.replace('/', '-').replace('.md', '')
            nav.append(f'<a href="#{anchor}">· {title[:35]}</a>')
    nav.append('</nav>')
    return '\n'.join(nav)


def main():
    print("Экспорт в HTML...")

    sections: dict[str, list] = {}
    all_content = []

    for folder in sorted(DOCS.iterdir()):
        if not folder.is_dir():
            continue
        sec_name = folder.name
        sections[sec_name] = []
        for f in sorted(folder.rglob("*.md")):
            text = f.read_text(encoding="utf-8")
            if len(text) < 50:
                continue
            rel = str(f.relative_to(DOCS))

            # Заголовок файла
            title = rel
            for line in text.split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()[:50]
                    break

            sections[sec_name].append((rel, title))
            anchor = rel.replace('/', '-').replace('.md', '')
            body = md_to_html(text)
            all_content.append(
                f'<div class="doc-section" id="{anchor}">{body}</div>'
            )

    nav_html = build_nav(sections)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lorenzo Repository Docs</title>
<style>{CSS}</style>
</head>
<body>
{nav_html}
<main>
<h1>Lorenzo — Монорепозиторий исследований</h1>
{''.join(all_content)}
</main>
</body>
</html>"""

    out = DOCS / "index.html"
    out.write_text(html, encoding="utf-8")
    size_kb = out.stat().st_size // 1024
    print(f"  wrote: {out.relative_to(ROOT)} ({size_kb} KB)")
    print(f"  разделов: {len(sections)}, файлов: {sum(len(v) for v in sections.values())}")


if __name__ == "__main__":
    main()
