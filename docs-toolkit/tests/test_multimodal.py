"""Тесты image + diagram ingest."""
import tempfile
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.ingest.diagram import ingest as diagram_ingest, _parse_diagram, _extract_from_md
from docstoolkit.ingest.image import ingest as image_ingest
from docstoolkit.ingest.base import IngestError


def test_parse_mermaid_basic():
    code = """graph LR
    A[Start] --> B[End]
    """
    nodes, edges = _parse_diagram(code, "mermaid")
    assert "A" in nodes
    assert "B" in nodes
    assert ("A", "B") in edges


def test_parse_mermaid_with_label():
    code = """graph LR
    A --> |yes| B
    """
    nodes, edges = _parse_diagram(code, "mermaid")
    assert any(e[0] == "A" and e[1] == "B" and e[2] == "yes" for e in edges)


def test_parse_plantuml_participants():
    code = """
participant Alice
participant Bob
Alice -> Bob
"""
    nodes, edges = _parse_diagram(code, "plantuml")
    assert "Alice" in nodes
    assert "Bob" in nodes


def test_extract_from_md_mermaid():
    md = """# Doc

```mermaid
graph LR
A --> B
```

text
"""
    diagrams = _extract_from_md(md)
    assert len(diagrams) == 1
    assert diagrams[0]["kind"] == "mermaid"


def test_extract_from_md_plantuml_in_codefence():
    md = """text
```plantuml
@startuml
A -> B
@enduml
```
"""
    diagrams = _extract_from_md(md)
    # Может найти как plantuml fence или внутри @startuml...@enduml
    assert len(diagrams) >= 1


def test_diagram_ingest_md(tmp_path):
    md_path = tmp_path / "doc.md"
    md_path.write_text("""# Test

```mermaid
graph LR
X[start] --> Y[end]
```
""", encoding="utf-8")
    doc = diagram_ingest(md_path)
    assert doc.metadata["diagram_count"] == 1
    assert "X" in doc.content
    assert "mermaid" in doc.metadata["kinds"]


def test_diagram_ingest_no_diagrams_raises(tmp_path):
    md_path = tmp_path / "empty.md"
    md_path.write_text("# No diagrams here", encoding="utf-8")
    with pytest.raises(IngestError):
        diagram_ingest(md_path)


def test_diagram_unsupported_format(tmp_path):
    bad = tmp_path / "x.txt"
    bad.write_text("text")
    with pytest.raises(IngestError):
        diagram_ingest(bad)


def test_image_ingest_metadata_only(tmp_path):
    """Без OCR — просто metadata."""
    png = tmp_path / "tiny.png"
    # 1x1 PNG bytes
    png.write_bytes(bytes.fromhex(
        '89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000'
        '000d4944415478da636060600000000400015dd6e3590000000049454e44ae426082'
    ))
    doc = image_ingest(png)
    assert doc.title == "tiny"
    assert doc.source.format == "image"
    assert doc.metadata["format"] == "png"


def test_image_ingest_missing_raises():
    with pytest.raises(IngestError):
        image_ingest(Path("/tmp/nonexistent_img_12345.png"))
