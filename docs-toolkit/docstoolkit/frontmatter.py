"""YAML-frontmatter парсер (без зависимостей)."""
import re

FRONTMATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.DOTALL)


def parse_yaml(text: str) -> dict:
    """Минимальный YAML-парсер для frontmatter: scalars, lists, null, ints."""
    result: dict = {}
    current_list: list | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith('#'):
            continue

        if line.lstrip().startswith('- ') and current_list is not None:
            value = line.lstrip()[2:].strip()
            current_list.append(_coerce(value))
            continue

        m = re.match(r'^([A-Za-z_][\w-]*)\s*:\s*(.*)$', line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        current_list = None

        if value == '':
            current_list = []
            result[key] = current_list
        elif value == '[]':
            result[key] = []
        elif value.startswith('[') and value.endswith(']'):
            inner = value[1:-1].strip()
            if not inner:
                result[key] = []
            else:
                items = [s.strip().strip('"\'') for s in inner.split(',')]
                result[key] = [_coerce(x) for x in items]
        else:
            result[key] = _coerce(value)

    return result


def _coerce(s: str):
    if s == '' or s == 'null' or s == '~':
        return None
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if re.fullmatch(r'-?\d+', s):
        return int(s)
    if re.fullmatch(r'-?\d+\.\d+', s):
        return float(s)
    return s


def extract_frontmatter(text: str) -> tuple[dict | None, str]:
    """Возвращает (frontmatter dict | None, остаток текста)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    try:
        fm = parse_yaml(m.group(1))
    except Exception:
        return None, text
    return fm, text[m.end():]
