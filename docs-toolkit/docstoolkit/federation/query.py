"""Query routing across federation."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from docstoolkit.federation.adapter import make_adapter
from docstoolkit.federation.registry import PortalRegistry


@dataclass
class FederatedResult:
    """Агрегированный результат от нескольких peer'ов."""
    query: str
    results: list[dict] = field(default_factory=list)
                                 # [{peer, title, path, snippet, score}, ...]
    peers_queried: int = 0
    peers_failed: int = 0
    total_results: int = 0
    duration_ms: int = 0


def query_federation(query: str,
                      registries: list[PortalRegistry] | None = None,
                      registry: PortalRegistry | None = None,
                      top_k_per_peer: int = 5,
                      timeout: int = 15,
                      max_workers: int = 5) -> FederatedResult:
    """Запрашивает всех peer'ов параллельно, агрегирует результаты.

    Сортирует по score (нормализованному внутри каждого peer'a через RRF).
    """
    import time
    t0 = time.time()

    # Объединяем peers из всех registry
    if registry and not registries:
        registries = [registry]
    registries = registries or []

    peers = []
    for reg in registries:
        peers.extend(reg.list())

    if not peers:
        return FederatedResult(query=query)

    # Параллельно опрашиваем
    results_per_peer: dict[str, list[dict]] = {}
    failed = 0

    def query_one(peer):
        try:
            adapter = make_adapter(peer)
            return peer.name, adapter.search(query, top_k_per_peer)
        except Exception as e:
            return peer.name, [{"error": str(e)}]

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(query_one, p): p for p in peers}
        for fut in as_completed(futures):
            try:
                peer_name, peer_results = fut.result(timeout=timeout)
                # Filter errors
                clean = [r for r in peer_results if "error" not in r]
                if not clean:
                    failed += 1
                else:
                    results_per_peer[peer_name] = clean
                    # Update last_seen
                    for reg in registries:
                        reg.update_last_seen(peer_name)
            except Exception:
                failed += 1

    # RRF (Reciprocal Rank Fusion) для агрегации
    rrf_scores: dict[str, float] = {}
    rrf_meta: dict[str, dict] = {}
    rrf_k = 60

    for peer_name, peer_results in results_per_peer.items():
        for rank, r in enumerate(peer_results):
            key = f"{peer_name}::{r.get('path', '')}"
            score = 1.0 / (rrf_k + rank + 1)
            rrf_scores[key] = rrf_scores.get(key, 0) + score
            rrf_meta.setdefault(key, {**r, "peer": peer_name})

    sorted_keys = sorted(rrf_scores.keys(), key=lambda k: -rrf_scores[k])
    aggregated = [
        {**rrf_meta[k], "fused_score": rrf_scores[k]}
        for k in sorted_keys
    ]

    return FederatedResult(
        query=query,
        results=aggregated,
        peers_queried=len(peers),
        peers_failed=failed,
        total_results=len(aggregated),
        duration_ms=int((time.time() - t0) * 1000),
    )
