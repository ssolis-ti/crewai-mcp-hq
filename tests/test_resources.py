"""MCP resources: documentation index, nested categories, search, templates."""

from __future__ import annotations

import re

from tests.conftest import read


async def test_docs_index_lists_categories(mcp):
    session, _ = mcp
    text = await read(session, "crewai://docs/index")
    assert text.startswith("# CrewAI Documentation Index")
    assert "crewai://docs/concepts/agents" in text


async def test_nested_category_docs_are_reachable(mcp):
    """Categories deeper than one level use dots and must resolve (regression)."""
    session, _ = mcp
    index = await read(session, "crewai://docs/index")
    m = re.search(r"crewai://docs/([\w.-]*\.[\w.-]*)/([\w-]+)", index)
    assert m, "no nested (dotted) category found in the index"
    doc = await read(session, f"crewai://docs/{m.group(1)}/{m.group(2)}")
    assert not doc.startswith("Category") and not doc.startswith("Topic"), doc[:200]
    assert len(doc) > 200


async def test_search_resource_not_shadowed(mcp):
    """crewai://docs/search/{q} must not be captured by {category}/{topic} (regression)."""
    session, _ = mcp
    text = await read(session, "crewai://docs/search/agent")
    assert text.startswith("# Search results"), text[:200]


async def test_template_resources(mcp):
    session, _ = mcp
    idx = await read(session, "crewai://templates/index")
    assert "crewai://templates/agent/researcher" in idx
    prebuilt = await read(session, "crewai://templates/prebuilt/index")
    assert "cyberops" in prebuilt
    full = await read(session, "crewai://templates/prebuilt/cyberops")
    assert "agents.yaml" in full and "crew.py" in full
