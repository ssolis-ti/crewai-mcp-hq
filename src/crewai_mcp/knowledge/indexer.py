"""
Knowledge Indexer — Document chunking and embedding for the RAG engine.

Parses all markdown documentation, splits into semantic chunks,
generates embeddings, and stores in ChromaDB for retrieval.
"""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger("crewai-mcp.knowledge.indexer")

# ── Chunk type ───────────────────────────────────────────────────────


class DocChunk:
    """A semantically meaningful chunk of documentation."""

    __slots__ = ("doc_id", "category", "topic", "section", "content", "metadata")

    def __init__(
        self,
        doc_id: str,
        category: str,
        topic: str,
        section: str,
        content: str,
        metadata: Optional[dict] = None,
    ):
        self.doc_id = doc_id
        self.category = category
        self.topic = topic
        self.section = section
        self.content = content
        self.metadata = metadata or {}

    @property
    def chunk_id(self) -> str:
        """Deterministic ID based on content hash."""
        raw = f"{self.doc_id}:{self.section}:{self.content[:200]}"
        return hashlib.md5(raw.encode()).hexdigest()


# ── Chunking logic ───────────────────────────────────────────────────

_HEADER_RE = re.compile(r"^(#{1,4})\s+(.+)", re.MULTILINE)


def chunk_markdown(
    content: str,
    category: str,
    topic: str,
    max_chunk_size: int = 1500,
    overlap: int = 200,
) -> list[DocChunk]:
    """
    Split markdown content into semantic chunks by headers.

    Strategy:
    1. Split on H1/H2/H3/H4 headers to get semantic sections
    2. If a section exceeds max_chunk_size, split on paragraph boundaries
    3. Each chunk carries its section header as metadata
    """
    doc_id = f"{category}/{topic}"

    # Find all headers and their positions
    headers = list(_HEADER_RE.finditer(content))

    if not headers:
        # No headers — treat entire content as one chunk, split if needed
        return _split_large_text(content, doc_id, category, topic, "root", max_chunk_size, overlap)

    chunks: list[DocChunk] = []

    # Process content before first header
    pre_header = content[: headers[0].start()].strip()
    if pre_header and len(pre_header) > 50:
        chunks.extend(
            _split_large_text(pre_header, doc_id, category, topic, "introduction", max_chunk_size, overlap)
        )

    # Process each header section
    for i, match in enumerate(headers):
        section_title = match.group(2).strip()
        section_start = match.start()
        section_end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
        section_content = content[section_start:section_end].strip()

        if len(section_content) < 30:
            continue

        chunks.extend(
            _split_large_text(section_content, doc_id, category, topic, section_title, max_chunk_size, overlap)
        )

    return chunks


def _split_large_text(
    text: str,
    doc_id: str,
    category: str,
    topic: str,
    section: str,
    max_size: int,
    overlap: int,
) -> list[DocChunk]:
    """Split text into chunks respecting paragraph boundaries."""
    if len(text) <= max_size:
        return [
            DocChunk(
                doc_id=doc_id,
                category=category,
                topic=topic,
                section=section,
                content=text,
                metadata={"char_count": len(text)},
            )
        ]

    # Split on double newlines (paragraphs)
    paragraphs = re.split(r"\n\n+", text)
    chunks: list[DocChunk] = []
    current = ""
    chunk_idx = 0

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_size and current:
            chunks.append(
                DocChunk(
                    doc_id=doc_id,
                    category=category,
                    topic=topic,
                    section=f"{section} (part {chunk_idx + 1})",
                    content=current.strip(),
                    metadata={"char_count": len(current), "part": chunk_idx + 1},
                )
            )
            # Overlap: keep last `overlap` chars
            current = current[-overlap:] if overlap and len(current) > overlap else ""
            chunk_idx += 1

        current += para + "\n\n"

    if current.strip():
        chunks.append(
            DocChunk(
                doc_id=doc_id,
                category=category,
                topic=topic,
                section=f"{section} (part {chunk_idx + 1})" if chunk_idx > 0 else section,
                content=current.strip(),
                metadata={"char_count": len(current), "part": chunk_idx + 1},
            )
        )

    return chunks


# ── Full indexing pipeline ───────────────────────────────────────────


def index_docs_directory(docs_root: Path) -> list[DocChunk]:
    """
    Index all markdown files in the docs directory.

    Returns all chunks ready for embedding and storage.
    """
    all_chunks: list[DocChunk] = []

    if not docs_root.exists():
        logger.warning(f"Docs root not found: {docs_root}")
        return all_chunks

    for md_file in sorted(docs_root.rglob("*.md")):
        rel = md_file.relative_to(docs_root)
        parts = rel.parts

        if len(parts) == 1:
            category = "root"
            topic = rel.stem
        elif len(parts) == 2:
            category = parts[0]
            topic = Path(parts[1]).stem
        else:
            category = "/".join(parts[:-1])
            topic = Path(parts[-1]).stem

        content = md_file.read_text(encoding="utf-8", errors="replace")
        chunks = chunk_markdown(content, category, topic)
        all_chunks.extend(chunks)

    logger.info(f"Indexed {len(all_chunks)} chunks from {docs_root}")
    return all_chunks
