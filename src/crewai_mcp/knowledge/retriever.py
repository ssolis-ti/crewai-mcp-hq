"""
Knowledge Retriever — Semantic search over indexed CrewAI documentation.

Uses ChromaDB as the vector store and provides search functionality
that powers the `crewai_query_knowledge` MCP tool.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("crewai-mcp.knowledge.retriever")


@dataclass
class SearchResult:
    """A single search result from the knowledge base."""

    content: str
    category: str
    topic: str
    section: str
    score: float
    doc_id: str
    metadata: dict = field(default_factory=dict)


class KnowledgeRetriever:
    """
    Semantic search engine over the indexed CrewAI documentation.

    Lazy-initializes ChromaDB and builds the index on first query.
    """

    # v2: category metadata switched to dot-separated nesting (tools.ai-ml) —
    # bumping the collection name forces a rebuild of stale v1 databases.
    COLLECTION_NAME = "crewai_docs_v2"

    def __init__(self, docs_path: Path, db_path: Path):
        self._docs_path = docs_path
        self._db_path = db_path
        self._client = None
        self._collection = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization: create DB and index docs if needed."""
        if self._initialized:
            return

        try:
            import chromadb

            self._db_path.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(self._db_path))

            # Check if collection already exists and has data
            try:
                self._collection = self._client.get_collection(self.COLLECTION_NAME)
                count = self._collection.count()
                if count > 0:
                    logger.info(f"Knowledge base loaded: {count} chunks in '{self.COLLECTION_NAME}'")
                    self._initialized = True
                    return
            except Exception:
                pass

            # Need to build the index
            logger.info("Building knowledge index from documentation...")
            self._build_index()
            self._initialized = True

        except ImportError:
            logger.error("chromadb not installed. Knowledge search disabled. Run: uv add chromadb")
            self._initialized = True  # Don't retry

    def _build_index(self) -> None:
        """Index all documentation into ChromaDB."""
        from crewai_mcp.knowledge.indexer import index_docs_directory

        chunks = index_docs_directory(self._docs_path)
        if not chunks:
            logger.warning("No documentation chunks to index.")
            return


        # Create or get collection
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "CrewAI documentation knowledge base"},
        )

        # Deduplicate chunks to prevent ChromaDB crash on duplicate IDs
        unique_chunks = {}
        for c in chunks:
            unique_chunks[c.chunk_id] = c
        deduped_chunks = list(unique_chunks.values())

        # Batch insert (ChromaDB handles embeddings with its default model)
        batch_size = 100
        for i in range(0, len(deduped_chunks), batch_size):
            batch = deduped_chunks[i : i + batch_size]
            self._collection.add(
                ids=[c.chunk_id for c in batch],
                documents=[c.content for c in batch],
                metadatas=[
                    {
                        "category": c.category,
                        "topic": c.topic,
                        "section": c.section,
                        "doc_id": c.doc_id,
                        **c.metadata,
                    }
                    for c in batch
                ],
            )

        logger.info(f"Indexed {len(chunks)} chunks into ChromaDB.")

    def search(
        self,
        query: str,
        limit: int = 5,
        category_filter: Optional[str] = None,
    ) -> list[SearchResult]:
        """
        Search the knowledge base with a natural language query.

        Args:
            query: Natural language search query
            limit: Maximum number of results to return
            category_filter: Optional category to filter results (e.g., "concepts", "learn")

        Returns:
            List of SearchResult objects, sorted by relevance
        """
        self._ensure_initialized()

        if self._collection is None:
            return []

        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}

        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=min(limit, 20),
                where=where_filter,
            )
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

        search_results = []
        if results and results["documents"] and results["documents"][0]:
            docs = results["documents"][0]
            metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(docs)
            distances = results["distances"][0] if results["distances"] else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metadatas, distances):
                score = 1.0 / (1.0 + dist)  # Convert distance to similarity score
                search_results.append(
                    SearchResult(
                        content=doc,
                        category=meta.get("category", "unknown"),
                        topic=meta.get("topic", "unknown"),
                        section=meta.get("section", ""),
                        score=score,
                        doc_id=meta.get("doc_id", ""),
                        metadata=meta,
                    )
                )

        return search_results

    def get_stats(self) -> dict:
        """Return statistics about the knowledge base."""
        self._ensure_initialized()

        if self._collection is None:
            return {"status": "not_initialized", "chunks": 0}

        count = self._collection.count()
        return {
            "status": "ready",
            "chunks": count,
            "collection": self.COLLECTION_NAME,
            "db_path": str(self._db_path),
        }

    def rebuild_index(self) -> dict:
        """Force rebuild the entire knowledge index."""
        if self._client and self._collection:
            try:
                self._client.delete_collection(self.COLLECTION_NAME)
            except Exception:
                pass

        self._collection = None
        self._initialized = False
        self._ensure_initialized()

        return self.get_stats()


# ── Singleton retriever ──────────────────────────────────────────────

_retriever: Optional[KnowledgeRetriever] = None


def get_retriever() -> KnowledgeRetriever:
    """Get or create the singleton KnowledgeRetriever instance."""
    global _retriever
    if _retriever is None:
        from crewai_mcp.config import config

        _retriever = KnowledgeRetriever(
            docs_path=config.paths.docs_path,
            db_path=config.paths.knowledge_db,
        )
    return _retriever
