"""Citation graph из markdown ссылок + PageRank scoring."""
import re
from pathlib import Path


# Regex for standard markdown links: [text](path)
_MD_LINK_RE = re.compile(r'\[(?:[^\]]*)\]\(([^)]+)\)')
# Regex for wikilinks: [[target]] or [[target|label]]
_WIKI_LINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]')
# External URL detection
_EXTERNAL_RE = re.compile(r'^https?://')


def _normalize_target(target: str) -> str:
    """Нормализовать путь до doc_id: убрать ./ и .md."""
    t = target.strip()
    # Strip fragment
    if "#" in t:
        t = t[:t.index("#")]
    # Strip leading ./
    if t.startswith("./"):
        t = t[2:]
    # Strip .md suffix
    if t.endswith(".md"):
        t = t[:-3]
    return t


def extract_links(markdown_text: str, doc_id: str) -> list[str]:
    """Извлечь все внутренние ссылки из markdown-текста.

    Args:
        markdown_text: содержимое .md файла.
        doc_id: идентификатор текущего документа (для фильтрации само-ссылок).

    Returns:
        Список target doc_ids (нормализованных, без внешних URL и само-ссылок).
    """
    targets: list[str] = []

    # Standard markdown links
    for m in _MD_LINK_RE.finditer(markdown_text):
        raw = m.group(1).strip()
        if _EXTERNAL_RE.match(raw):
            continue
        norm = _normalize_target(raw)
        if norm and norm != doc_id:
            targets.append(norm)

    # Wikilinks
    for m in _WIKI_LINK_RE.finditer(markdown_text):
        raw = m.group(1).strip()
        if _EXTERNAL_RE.match(raw):
            continue
        norm = _normalize_target(raw)
        if norm and norm != doc_id:
            targets.append(norm)

    return targets


def build_citation_graph(corpus_dir: Path) -> dict[str, list[str]]:
    """Построить граф цитирований из директории с .md файлами.

    Args:
        corpus_dir: корень директории с markdown файлами.

    Returns:
        Словарь {doc_id: [cited_doc_id, ...]} — граф смежности.
    """
    graph: dict[str, list[str]] = {}
    corpus_dir = Path(corpus_dir).resolve()

    for md_file in sorted(corpus_dir.rglob("*.md")):
        try:
            rel = md_file.relative_to(corpus_dir)
        except ValueError:
            continue
        # doc_id: путь без .md, через /
        doc_id = str(rel.with_suffix("")).replace("\\", "/")
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except (OSError, PermissionError):
            text = ""

        links = extract_links(text, doc_id)
        if doc_id not in graph:
            graph[doc_id] = []
        graph[doc_id].extend(links)

    return graph


def pagerank(
    graph: dict[str, list[str]],
    alpha: float = 0.85,
    max_iter: int = 50,
    epsilon: float = 1e-6,
) -> dict[str, float]:
    """Стандартный PageRank итеративный алгоритм.

    Args:
        graph: граф смежности {node: [out_neighbors]}.
        alpha: damping factor (0.85 по умолчанию).
        max_iter: максимум итераций.
        epsilon: порог сходимости (sum of absolute changes).

    Returns:
        Словарь {node: pr_score}.
    """
    # Собрать все узлы (включая цели, которых нет как ключи)
    nodes: set[str] = set(graph.keys())
    for targets in graph.values():
        nodes.update(targets)

    if not nodes:
        return {}

    n = len(nodes)
    node_list = sorted(nodes)
    node_idx = {node: i for i, node in enumerate(node_list)}

    # Построить матрицу out-links
    out_links: list[list[int]] = [[] for _ in range(n)]
    for src, targets in graph.items():
        if src not in node_idx:
            continue
        si = node_idx[src]
        seen: set[int] = set()
        for t in targets:
            if t in node_idx:
                ti = node_idx[t]
                if ti not in seen and ti != si:
                    out_links[si].append(ti)
                    seen.add(ti)

    # Инициализация: равномерное распределение
    pr = [1.0 / n] * n

    for _ in range(max_iter):
        new_pr = [(1.0 - alpha) / n] * n

        # Собрать dangling nodes (нет исходящих рёбер)
        dangling_sum = sum(pr[i] for i in range(n) if not out_links[i])

        # Distribute dangling rank uniformly
        dangling_contrib = alpha * dangling_sum / n

        for i in range(n):
            new_pr[i] += dangling_contrib

        # Обычные рёбра
        for i in range(n):
            if out_links[i]:
                contrib = alpha * pr[i] / len(out_links[i])
                for j in out_links[i]:
                    new_pr[j] += contrib

        # Проверка сходимости
        delta = sum(abs(new_pr[i] - pr[i]) for i in range(n))
        pr = new_pr
        if delta < epsilon:
            break

    return {node_list[i]: pr[i] for i in range(n)}


def detect_orphans(graph: dict) -> list[str]:
    """Найти узлы с нулевым числом входящих рёбер (orphan nodes).

    Args:
        graph: граф смежности.

    Returns:
        Список orphan doc_ids (отсортированный).
    """
    all_nodes: set[str] = set(graph.keys())
    for targets in graph.values():
        all_nodes.update(targets)

    # Посчитать in-degree
    in_degree: dict[str, int] = {node: 0 for node in all_nodes}
    for src, targets in graph.items():
        for t in targets:
            if t in in_degree:
                in_degree[t] += 1

    return sorted(node for node, deg in in_degree.items() if deg == 0)


def detect_authorities(
    pr_scores: dict[str, float], top_k: int = 10
) -> list[tuple[str, float]]:
    """Топ-K узлов по PageRank score.

    Returns:
        Список [(doc_id, score), ...] отсортированный по убыванию.
    """
    items = sorted(pr_scores.items(), key=lambda x: -x[1])
    return items[:top_k]


def build_pagerank_report(corpus_dir: Path) -> str:
    """Построить полный Markdown-отчёт: топ-20 + orphans.

    Args:
        corpus_dir: директория с .md файлами.

    Returns:
        Строка Markdown-отчёта.
    """
    graph = build_citation_graph(corpus_dir)
    pr = pagerank(graph)
    top20 = detect_authorities(pr, top_k=20)
    orphans = detect_orphans(graph)

    total_nodes = len(pr)
    total_edges = sum(len(v) for v in graph.values())

    lines = [
        "# Citation Graph & PageRank Report",
        "",
        f"**Документов:** {total_nodes}  ",
        f"**Ссылок:** {total_edges}  ",
        f"**Orphan-узлов:** {len(orphans)}",
        "",
        "## Топ-20 авторитетов (PageRank)",
        "",
        "| # | doc_id | PR score |",
        "|---|--------|----------|",
    ]
    for rank, (doc_id, score) in enumerate(top20, 1):
        lines.append(f"| {rank} | `{doc_id}` | {score:.6f} |")

    lines += [
        "",
        "## Orphan-узлы (без входящих ссылок)",
        "",
    ]
    if orphans:
        for o in orphans[:50]:
            lines.append(f"- `{o}`")
        if len(orphans) > 50:
            lines.append(f"- ... и ещё {len(orphans) - 50}")
    else:
        lines.append("_Orphan-узлов нет._")

    return "\n".join(lines)
