"""
MCP Resources — CrewAI Documentation.

Exposes the entire scraped CrewAI documentation as MCP resources with
semantic URIs so any AI agent can browse and read docs on demand.

Resource URI scheme:
    crewai://docs/{category}/{topic}

Categories are auto-discovered from the docs/ directory structure.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from crewai_mcp.config import config
from crewai_mcp.app import mcp

logger = logging.getLogger("crewai-mcp.resources.docs")

# ── Helpers ──────────────────────────────────────────────────────────


def _docs_root() -> Path:
    """Return the resolved documentation root path."""
    return config.paths.docs_path


@lru_cache(maxsize=1)
def _build_docs_index() -> dict[str, dict[str, Path]]:
    """
    Scan the docs directory and build a {category: {topic: filepath}} index.

    Structure expected:
        docs/
        ├── concepts/agents.md      → category="concepts", topic="agents"
        ├── learn/create-custom-tools.md → category="learn", topic="create-custom-tools"
        ├── mcp/overview.md         → category="mcp", topic="overview"
        └── introduction.md         → category="root", topic="introduction"
    """
    root = _docs_root()
    index: dict[str, dict[str, Path]] = {}

    if not root.exists():
        logger.warning(f"Documentation root not found: {root}")
        return index

    for md_file in sorted(root.rglob("*.md")):
        rel = md_file.relative_to(root)
        parts = rel.parts

        if len(parts) == 1:
            category = "root"
            topic = rel.stem
        elif len(parts) == 2:
            category = parts[0]
            topic = Path(parts[1]).stem
        else:
            # Nested: tools/ai-ml/something.md → category="tools/ai-ml"
            category = "/".join(parts[:-1])
            topic = Path(parts[-1]).stem

        if category not in index:
            index[category] = {}
        index[category][topic] = md_file

    logger.info(f"Indexed {sum(len(v) for v in index.values())} docs across {len(index)} categories")
    return index


def _read_doc(category: str, topic: str) -> Optional[str]:
    """Read a documentation file by category and topic."""
    idx = _build_docs_index()
    cat_docs = idx.get(category, {})
    filepath = cat_docs.get(topic)
    if filepath and filepath.exists():
        return filepath.read_text(encoding="utf-8", errors="replace")
    return None


# ── MCP Resource: List all documentation categories ──────────────────


@mcp.resource("crewai://docs/index")
def docs_index() -> str:
    """
    List all available CrewAI documentation categories and topics.

    Returns a structured index of every documentation page available,
    organized by category. Use this to discover what documentation
    is available before reading specific topics.
    """
    idx = _build_docs_index()
    lines = ["# CrewAI Documentation Index\n"]

    for category in sorted(idx.keys()):
        topics = sorted(idx[category].keys())
        lines.append(f"\n## {category}/ ({len(topics)} docs)\n")
        for topic in topics:
            uri = f"crewai://docs/{category}/{topic}"
            lines.append(f"- [{topic}]({uri})")

    return "\n".join(lines)


# ── MCP Resource Templates: Read specific documentation ──────────────


@mcp.resource("crewai://docs/{category}/{topic}")
def read_doc(category: str, topic: str) -> str:
    """
    Read a specific CrewAI documentation page.

    Args:
        category: Documentation category (e.g., "concepts", "learn", "mcp", "tools/ai-ml")
        topic: Topic name without extension (e.g., "agents", "flows", "overview")

    Returns the full markdown content of the requested documentation page.
    """
    content = _read_doc(category, topic)
    if content is None:
        available = _build_docs_index()
        cat_docs = available.get(category, {})
        if not cat_docs:
            cats = ", ".join(sorted(available.keys()))
            return f"Category '{category}' not found. Available categories: {cats}"
        topics = ", ".join(sorted(cat_docs.keys()))
        return f"Topic '{topic}' not found in '{category}'. Available topics: {topics}"
    return content


# ── MCP Resource: Search documentation topics ────────────────────────


@mcp.resource("crewai://docs/search/{query}")
def search_docs(query: str) -> str:
    """
    Search documentation topics by keyword in title.

    Args:
        query: Search keyword (matched against topic names, case-insensitive)

    Returns a list of matching documentation pages with their URIs.
    """
    idx = _build_docs_index()
    query_lower = query.lower()
    results = []

    for category, topics in idx.items():
        for topic, filepath in topics.items():
            if query_lower in topic.lower() or query_lower in category.lower():
                results.append(f"- crewai://docs/{category}/{topic}")

    if not results:
        return f"No documentation found matching '{query}'. Try broader terms."

    header = f"# Search results for '{query}' ({len(results)} matches)\n"
    return header + "\n".join(results)


# ── MCP Resource: Full category listing ──────────────────────────────


@mcp.resource("crewai://docs/{category}")
def read_category(category: str) -> str:
    """
    List all topics in a documentation category.

    Args:
        category: Documentation category (e.g., "concepts", "learn", "mcp")

    Returns a list of all topics in the category with their URIs.
    """
    idx = _build_docs_index()
    cat_docs = idx.get(category, {})

    if not cat_docs:
        cats = ", ".join(sorted(idx.keys()))
        return f"Category '{category}' not found. Available categories: {cats}"

    lines = [f"# {category}/ — {len(cat_docs)} documents\n"]
    for topic in sorted(cat_docs.keys()):
        lines.append(f"- [{topic}](crewai://docs/{category}/{topic})")

    return "\n".join(lines)
