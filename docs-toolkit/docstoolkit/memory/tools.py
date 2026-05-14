"""Memory management tools for agent integration."""
from dataclasses import dataclass

from docstoolkit.memory.tiered import TieredMemory


@dataclass
class MemoryTools:
    """Memory management tools for agent integration."""
    memory: TieredMemory

    def search_recall(self, query: str, top_k: int = 5) -> str:
        """Search recall memory. Returns formatted string."""
        items = self.memory.recall_search(query, top_k=top_k)
        if not items:
            return "No recall items found for query."
        lines = [f"Recall results for '{query}':"]
        for item in items:
            lines.append(f"  [{item.ts}] {item.role}: {item.content}")
        return "\n".join(lines)

    def archive_fact(self, text: str, tags: str = "") -> str:
        """Archive a fact. tags is comma-separated. Returns confirmation."""
        tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
        fact_id = self.memory.archive(text, tags=tag_list)
        return f"Fact archived (id={fact_id}): {text[:80]}"

    def forget_fact(self, fact_id: str) -> str:
        """Remove a fact from archival. Returns confirmation."""
        removed = self.memory.forget(fact_id)
        if removed:
            return f"Fact {fact_id} removed from archival memory."
        return f"Fact {fact_id} not found in archival memory."

    def memory_stats(self) -> str:
        """Return stats as formatted string."""
        s = self.memory.stats()
        return (
            f"Memory stats — user: {s['user_id']} | "
            f"working: {s['working_messages']} msgs | "
            f"recall: {s['recall_count']} items | "
            f"archival: {s['archival_count']} facts"
        )

    def list_tools(self) -> list:
        """Return tool schemas for agent integration."""
        return [
            {
                "name": "search_recall",
                "description": "Search recall memory for relevant past interactions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "top_k": {"type": "integer", "description": "Max results", "default": 5},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "archive_fact",
                "description": "Archive a compressed fact or preference to long-term memory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The fact to archive"},
                        "tags": {"type": "string", "description": "Comma-separated tags"},
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "forget_fact",
                "description": "Remove a fact from archival memory by ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fact_id": {"type": "string", "description": "The fact ID to remove"},
                    },
                    "required": ["fact_id"],
                },
            },
            {
                "name": "memory_stats",
                "description": "Return statistics about current memory usage.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        ]


def build_memory_tools(db_path: str = ":memory:", user_id: str = "default") -> MemoryTools:
    """Convenience factory."""
    memory = TieredMemory(db_path=db_path, user_id=user_id)
    return MemoryTools(memory=memory)
