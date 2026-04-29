"""Jupyter Notebook (.ipynb) → markdown.

Конвертирует ячейки:
  - markdown → как есть
  - code → обёрнутый в ```python ... ``` блок + (опционально) text/plain output
  - raw → как есть (с пометкой)
"""
import json
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path: Path) -> Document:
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise IngestError(f"Jupyter: невалидный JSON: {e}")

    cells = nb.get("cells", [])
    if not cells:
        raise IngestError("Jupyter: ноутбук без ячеек")

    parts: list[str] = []
    title = path.stem
    metadata = nb.get("metadata", {})
    language = (
        metadata.get("kernelspec", {}).get("language")
        or metadata.get("language_info", {}).get("name")
        or "python"
    )

    title_extracted = False
    code_count = 0
    md_count = 0

    for cell in cells:
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))

        if cell_type == "markdown":
            md_count += 1
            if not title_extracted and source.lstrip().startswith("# "):
                lines = source.lstrip().split("\n")
                title = lines[0].lstrip("# ").strip()
                title_extracted = True
            parts.append(source)

        elif cell_type == "code":
            code_count += 1
            parts.append(f"```{language}\n{source}\n```")
            outputs = cell.get("outputs", [])
            for out in outputs:
                if out.get("output_type") in ("stream", "execute_result", "display_data"):
                    text = out.get("text") or out.get("data", {}).get("text/plain", "")
                    if isinstance(text, list):
                        text = "".join(text)
                    if text and len(text) < 5000:
                        parts.append(f"```\n{text.strip()}\n```")

        elif cell_type == "raw":
            parts.append(f"<!-- raw cell -->\n\n{source}")

    content = "\n\n".join(p for p in parts if p)

    return Document(
        title=title,
        content=content,
        source=Source.from_path(path, "jupyter"),
        metadata={
            "language": language,
            "cell_count": len(cells),
            "code_cells": code_count,
            "markdown_cells": md_count,
        },
    )
