"""CSV → markdown ingest plugin (демо).

Конвертирует CSV в markdown-таблицу.
"""
import csv
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path: Path) -> Document:
    if not path.exists():
        raise IngestError(f"Не найден: {path}")

    rows = []
    try:
        with path.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        raise IngestError(f"CSV parse error: {e}")

    if not rows:
        raise IngestError("CSV: пустой файл")

    # Markdown table
    lines = ["| " + " | ".join(rows[0]) + " |",
             "|" + "|".join("---" for _ in rows[0]) + "|"]
    for row in rows[1:]:
        # Дополняем строки до длины header
        padded = row + [""] * (len(rows[0]) - len(row))
        lines.append("| " + " | ".join(padded[:len(rows[0])]) + " |")

    return Document(
        title=path.stem,
        content="\n".join(lines),
        source=Source.from_path(path, "csv"),
        metadata={"rows": len(rows) - 1, "columns": len(rows[0])},
    )
