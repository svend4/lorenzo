"""Portal registry: peers с metadata."""
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


@dataclass
class Peer:
    """Один peer в federation."""
    name: str
    url: str                                # https://host/portal
    kind: str = "http"                      # http | local | mock
    capabilities: list[str] = field(default_factory=list)
                                             # ["search", "rag", "graph"]
    added_ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))
    last_seen: str = ""
    public_key: str = ""                    # для подписи (future)


class PortalRegistry:
    """Хранит peer'ов в JSON файле."""

    def __init__(self, path: Path | None = None):
        if path is None:
            cfg = load_config()
            path = cfg.root / ".docstoolkit" / "federation.json"
        self.path = Path(path)
        self.peers: dict[str, Peer] = {}
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            for name, info in data.get("peers", {}).items():
                self.peers[name] = Peer(**info)
        except Exception:
            pass

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "updated": datetime.now().isoformat(timespec='seconds'),
            "peers": {name: asdict(p) for name, p in self.peers.items()},
        }
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    def register(self, name: str, url: str, *,
                 kind: str = "http",
                 capabilities: list[str] | None = None) -> Peer:
        peer = Peer(name=name, url=url, kind=kind,
                    capabilities=capabilities or [])
        self.peers[name] = peer
        self._save()
        return peer

    def unregister(self, name: str) -> bool:
        if name in self.peers:
            del self.peers[name]
            self._save()
            return True
        return False

    def list(self) -> list[Peer]:
        return list(self.peers.values())

    def get(self, name: str) -> Peer | None:
        return self.peers.get(name)

    def update_last_seen(self, name: str):
        if name in self.peers:
            self.peers[name].last_seen = datetime.now().isoformat(timespec='seconds')
            self._save()
