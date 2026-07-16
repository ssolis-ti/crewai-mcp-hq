"""Heavy crewai runtime paths: install, kickoff, flows, RAG, memory, replay.

These exercise the real crewai runtime inside project venvs — the surface
most exposed to crewai version changes. Marked slow; the weekly CI job runs
them against the latest published crewai.
"""

from __future__ import annotations

import pytest

from tests.conftest import call

pytestmark = pytest.mark.slow


async def test_install_deps(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_install_deps", {"project_name": crew_project}, timeout=600)
    assert "crewai install" in t
    assert "exit 0" in t, t[:400]


async def test_kickoff_without_api_key_fails_gracefully(crew_project, mcp):
    """No API key -> the crew must fail with a readable error, never hang."""
    session, _ = mcp
    t = await call(session, "crewai_kickoff",
                   {"project_name": crew_project,
                    "inputs": {"project_description": "ci probe"},
                    "timeout": 300}, timeout=360)
    assert "failed" in t.lower() or "error" in t.lower(), t[:300]


async def test_flow_plot_generates_html(flow_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_flow_plot", {"project_name": flow_project}, timeout=600)
    assert "plotted successfully" in t.lower() or ".html" in t, t[:400]


async def test_flow_run_finds_flow_class(flow_project, mcp):
    """The runner must locate the Flow subclass; without keys it fails gracefully."""
    session, _ = mcp
    t = await call(session, "crewai_flow_run",
                   {"project_name": flow_project, "timeout": 300}, timeout=360)
    assert "RUNNER_ERROR" not in t, t[:400]
    assert "failed" in t.lower() or "error" in t.lower() or "successful" in t.lower(), t[:300]


async def test_query_knowledge_rag(mcp):
    session, _ = mcp
    t = await call(session, "crewai_query_knowledge",
                   {"query": "how to define an agent", "limit": 2}, timeout=600)
    assert t.startswith("# Documentation Search Results"), t[:200]
    assert "crewai://docs/" in t


async def test_query_knowledge_category_filter(mcp):
    session, _ = mcp
    import re
    t = await call(session, "crewai_query_knowledge",
                   {"query": "memory types", "limit": 3, "category": "concepts"}, timeout=600)
    cats = set(re.findall(r"crewai://docs/([\w.-]+)/", t))
    assert cats == {"concepts"}, cats


async def test_manage_memory_status_and_reset(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_manage_memory",
                   {"project_name": crew_project, "action": "status"})
    assert '"memory_enabled_in_code"' in t
    t = await call(session, "crewai_manage_memory",
                   {"project_name": crew_project, "action": "reset"}, timeout=300)
    assert "reset successfully" in t.lower() or "failed" in t.lower()


async def test_replay_invalid_task_id_is_controlled(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_replay_task",
                   {"project_name": crew_project, "task_id": "bogus"}, timeout=600)
    assert "Replay finished" in t or "Error" in t
