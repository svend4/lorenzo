"""
Извлекает текст из MHTML-файлов (Claude.ai и ChatGPT).
Конвертирует HTML-структуру в чистый Markdown.
"""

import email
import re
from bs4 import BeautifulSoup, Tag


def _el_to_md(el: Tag, depth: int = 0) -> str:
    """Рекурсивно конвертирует HTML-элемент в Markdown."""
    if isinstance(el, str):
        return el.strip()

    tag = el.name if hasattr(el, 'name') else None
    if not tag:
        return el.get_text(strip=True) if hasattr(el, 'get_text') else str(el).strip()

    children_md = '\n'.join(
        _el_to_md(child, depth) for child in el.children
        if (hasattr(child, 'name') and child.name) or
        (hasattr(child, 'strip') and child.strip())
    ).strip()

    if tag in ('h1',):
        return f"# {el.get_text(strip=True)}"
    if tag in ('h2',):
        return f"## {el.get_text(strip=True)}"
    if tag in ('h3',):
        return f"### {el.get_text(strip=True)}"
    if tag in ('h4',):
        return f"#### {el.get_text(strip=True)}"
    if tag in ('h5', 'h6'):
        return f"##### {el.get_text(strip=True)}"

    if tag == 'p':
        return el.get_text(separator=' ', strip=True)

    if tag in ('strong', 'b'):
        t = el.get_text(strip=True)
        return f"**{t}**" if t else ''

    if tag in ('em', 'i'):
        t = el.get_text(strip=True)
        return f"*{t}*" if t else ''

    if tag == 'code' and el.parent and el.parent.name != 'pre':
        t = el.get_text(strip=True)
        return f"`{t}`" if t else ''

    if tag == 'pre':
        code_el = el.find('code')
        code_text = code_el.get_text() if code_el else el.get_text()
        lang_class = ''
        if code_el:
            for cls in code_el.get('class', []):
                if cls.startswith('language-'):
                    lang_class = cls.replace('language-', '')
                    break
        return f"```{lang_class}\n{code_text.strip()}\n```"

    if tag in ('ul', 'ol'):
        items = []
        for i, li in enumerate(el.find_all('li', recursive=False)):
            content = li.get_text(separator=' ', strip=True)
            prefix = f"{i+1}." if tag == 'ol' else "-"
            items.append(f"{prefix} {content}")
        return '\n'.join(items)

    if tag == 'li':
        return f"- {el.get_text(separator=' ', strip=True)}"

    if tag == 'table':
        rows = el.find_all('tr')
        if not rows:
            return el.get_text(strip=True)
        lines = []
        for i, row in enumerate(rows):
            cells = row.find_all(['th', 'td'])
            line = '| ' + ' | '.join(c.get_text(strip=True) for c in cells) + ' |'
            lines.append(line)
            if i == 0:
                lines.append('| ' + ' | '.join('---' for _ in cells) + ' |')
        return '\n'.join(lines)

    if tag == 'blockquote':
        inner = el.get_text(separator='\n', strip=True)
        return '\n'.join(f"> {line}" for line in inner.split('\n') if line.strip())

    if tag == 'hr':
        return '---'

    if tag == 'br':
        return '\n'

    if tag in ('a',):
        href = el.get('href', '')
        text = el.get_text(strip=True)
        if href and href.startswith('http'):
            return f"[{text}]({href})"
        return text

    if tag in ('span', 'div', 'section', 'article', 'main'):
        return children_md

    return el.get_text(separator=' ', strip=True)


def _extract_claude_response(response_div: Tag) -> str:
    """Конвертирует div.font-claude-response в markdown."""
    parts = []
    for child in response_div.children:
        if not hasattr(child, 'name') or not child.name:
            txt = str(child).strip()
            if txt:
                parts.append(txt)
            continue
        md = _el_to_md(child)
        if md:
            parts.append(md)
    return '\n\n'.join(p for p in parts if p.strip())


def extract_text_from_mhtml(filepath: str) -> str:
    """Парсит MHTML и возвращает clean Markdown."""
    with open(filepath, 'rb') as f:
        msg = email.message_from_binary_file(f)

    html = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            payload = part.get_payload(decode=True)
            if payload:
                html = payload.decode('utf-8', errors='replace')
                break

    if not html:
        return ""

    soup = BeautifulSoup(html, 'lxml')

    is_claude = 'claude.ai' in html[:3000]
    is_chatgpt = 'chatgpt.com' in html[:3000] or ('openai' in html[:3000].lower() and 'chatgpt' in html[:3000].lower())

    sections = []

    if is_claude:
        # Пользовательские сообщения
        user_msgs = soup.find_all(attrs={'data-testid': 'user-message'})
        # Ответы Claude
        claude_responses = soup.find_all(
            lambda tag: tag.name == 'div' and
            tag.get('class') and
            any('font-claude-response' in c and 'body' not in c for c in tag.get('class', []))
        )

        # Собрать все блоки в порядке появления в документе
        all_blocks = []
        for um in user_msgs:
            txt = um.get_text(separator=' ', strip=True)
            if txt and len(txt) > 5:
                all_blocks.append(('user', um, txt))
        for cr in claude_responses:
            txt = cr.get_text(strip=True)
            if txt and len(txt) > 50:
                all_blocks.append(('claude', cr, txt))

        # Сортировать по позиции в документе
        all_elements = list(soup.descendants)
        def doc_order(block):
            try:
                return all_elements.index(block[1])
            except ValueError:
                return 999999

        all_blocks.sort(key=doc_order)

        for kind, el, _ in all_blocks:
            if kind == 'user':
                txt = el.get_text(separator=' ', strip=True)
                sections.append(f"**[Запрос]** {txt}")
            else:
                md = _extract_claude_response(el)
                if md:
                    sections.append(md)

    elif is_chatgpt:
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()

        # ChatGPT: ищем div с data-message-author-role
        msg_divs = soup.find_all(attrs={'data-message-author-role': True})
        if msg_divs:
            for mdiv in msg_divs:
                role = mdiv.get('data-message-author-role', '')
                txt = mdiv.get_text(separator='\n', strip=True)
                if txt and len(txt) > 20:
                    if role == 'user':
                        sections.append(f"**[Запрос]** {txt}")
                    else:
                        sections.append(txt)
        else:
            # Fallback
            for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'pre', 'table']):
                txt = el.get_text(separator=' ', strip=True)
                if txt and len(txt) > 30:
                    sections.append(txt)
    else:
        for tag in soup(['script', 'style', 'nav']):
            tag.decompose()
        for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'pre', 'table']):
            txt = el.get_text(separator=' ', strip=True)
            if txt and len(txt) > 30:
                sections.append(txt)

    result = '\n\n'.join(s for s in sections if s.strip())
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    return result.strip()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_mhtml.py <file>")
        sys.exit(1)
    result = extract_text_from_mhtml(sys.argv[1])
    print(result[:5000])
    print(f"\n\n[Всего символов: {len(result)}]")
