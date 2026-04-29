# Домен: немецкое социальное право

<!-- summary -->
> Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) LLM+Pydantic parses legal entities: class Bescheid(BaseModel): aktenzeichen: str; p
**Проекты:** Svyazi, CardIndex

---
<!-- tags: rag, knowledge, ingestion, architecture -->




Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) LLM+Pydantic parses legal entities: class Bescheid(BaseModel): aktenzeichen: str; paragraphs: List[SGB_Reference]; deadline: date Svyazi CardIndex deduplicates decisions by SHA256 Итог: self-updating knowledge base of 50k+ decisions, structured queries
2. Precedent search with semantic + structural filters Docling knows document structure (§, headings, footnotes) Pydantic enforces schema: type="Widerspruch" AND sgb="IX" AND paragraph="78 Abs. 6" Graph-RAG links precedents through citations ROI: 10 sec queries vs 2 hour manual search
Уникальность: Docling maintains structure, Pydantic validates legal schema, Svyazi deduplicates. Ни один SaaS не делает это для
