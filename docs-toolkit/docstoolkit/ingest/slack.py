"""Slack ingest — экспортный JSON / ZIP.

Slack даёт workspace export как ZIP с JSON-файлами (по каналам).
Этот плагин работает с распакованным каталогом или одним JSON-файлом.
"""
import json
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path: Path) -> Document:
    """Принимает:
      - .json файл (один канал-день)
      - директорию канала (объединяет все .json внутри)
    """
    p = Path(path)
    if not p.exists():
        raise IngestError(f"Не найден: {p}")

    if p.is_dir():
        return _ingest_channel(p)
    if p.suffix == ".json":
        return _ingest_day(p)
    raise IngestError(f"Slack ingest: неподдерживаемый формат {p}")


def _ingest_day(json_path: Path) -> Document:
    try:
        messages = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise IngestError(f"Slack JSON parse error: {e}")
    if not isinstance(messages, list):
        raise IngestError("Slack JSON: ожидался список сообщений")

    md_lines = [f"# Slack: {json_path.stem}\n"]
    for msg in messages:
        ts = msg.get("ts", "0")
        try:
            dt = datetime.fromtimestamp(float(ts)).isoformat(timespec='seconds')
        except (ValueError, TypeError):
            dt = ts
        user = msg.get("user_profile", {}).get("real_name") or msg.get("user", "?")
        text = msg.get("text", "")
        md_lines.append(f"**{user}** _{dt}_\n\n{text}\n")

    return Document(
        title=f"Slack/{json_path.stem}",
        content="\n".join(md_lines),
        source=Source.from_path(json_path, "slack"),
        metadata={"messages": len(messages)},
    )


def _ingest_channel(channel_dir: Path) -> Document:
    """Объединяет все .json в директории канала."""
    json_files = sorted(channel_dir.glob("*.json"))
    if not json_files:
        raise IngestError(f"В {channel_dir} нет .json файлов")

    all_md = [f"# Slack channel: {channel_dir.name}\n"]
    total_msgs = 0
    for jf in json_files:
        try:
            doc = _ingest_day(jf)
            all_md.append(f"\n## {jf.stem}\n")
            # Берём только сообщения (отрезаем заголовок дня)
            day_content = doc.content.split("\n", 2)[2] if "\n" in doc.content else doc.content
            all_md.append(day_content)
            total_msgs += doc.metadata.get("messages", 0)
        except IngestError:
            continue

    return Document(
        title=f"Slack channel: {channel_dir.name}",
        content="\n".join(all_md),
        source=Source.from_path(channel_dir, "slack"),
        metadata={"channel": channel_dir.name, "days": len(json_files),
                  "total_messages": total_msgs},
    )
