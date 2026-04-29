"""Image ingest: OCR через pytesseract если установлен.

Без OCR — просто метаданные изображения (size, format).
"""
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path: Path) -> Document:
    """Извлекает текст через OCR (опц.) + метаданные изображения."""
    if not path.exists():
        raise IngestError(f"Не найден: {path}")

    metadata = {"format": path.suffix.lstrip(".").lower()}

    # Попробуем OCR через pytesseract
    ocr_text = ""
    ocr_available = False
    try:
        import pytesseract
        from PIL import Image
        ocr_available = True
        try:
            img = Image.open(path)
            metadata["width"] = img.width
            metadata["height"] = img.height
            metadata["mode"] = img.mode
            # OCR обоими языками — eng + rus
            ocr_text = pytesseract.image_to_string(
                img, lang="eng+rus", config="--psm 6"
            ).strip()
        except Exception as e:
            metadata["ocr_error"] = str(e)
    except ImportError:
        metadata["ocr_status"] = "Not available (pip install pytesseract Pillow)"

    # Попробуем PIL без OCR — для метаданных
    if not ocr_available:
        try:
            from PIL import Image
            img = Image.open(path)
            metadata["width"] = img.width
            metadata["height"] = img.height
            metadata["mode"] = img.mode
        except (ImportError, Exception):
            pass

    title = path.stem
    parts = [f"# {title}"]
    if metadata.get("width"):
        parts.append(f"\n**Размер:** {metadata['width']}×{metadata['height']} ({metadata.get('format', '?')})")
    if ocr_text:
        parts.append(f"\n## Извлечённый текст (OCR)\n\n{ocr_text}")
    elif metadata.get("ocr_status"):
        parts.append(f"\n_OCR не выполнен: {metadata['ocr_status']}_")

    return Document(
        title=title,
        content="\n".join(parts),
        source=Source.from_path(path, "image"),
        metadata=metadata,
    )
