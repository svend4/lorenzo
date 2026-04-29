"""Prompt library: версионируемые промпты с A/B variants и рендерингом.

Использование:
    from docstoolkit.prompts import PromptLibrary, Prompt

    lib = PromptLibrary()
    lib.register(Prompt(
        id="rag.system",
        version=1,
        template="Ты помощник. Используй [{n}] для цитат. Контекст:\\n{context}",
        variables=["context"],
    ))

    text = lib.render("rag.system", {"context": "..."})

    # A/B variant:
    lib.register(Prompt(id="rag.system", version=2,
                         template="Be concise. Cite [{n}].\\n{context}",
                         variables=["context"]))
    lib.set_active_variant("rag.system", version=2, weight=0.5)  # 50/50
    # render() будет рандомно выбирать v1/v2
"""
from docstoolkit.prompts.library import (
    Prompt, PromptLibrary, PromptRenderError,
)

__all__ = ["Prompt", "PromptLibrary", "PromptRenderError"]
