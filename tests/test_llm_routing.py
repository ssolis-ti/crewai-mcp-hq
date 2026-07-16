"""LLM provider connection + multi-agent model routing."""

from __future__ import annotations

import json
import py_compile

from tests.conftest import CREW_MODULE, CREW_PROJECT_DIR, call


def _env_text() -> str:
    return (CREW_PROJECT_DIR / ".env").read_text(encoding="utf-8")


async def test_provider_requires_base_when_gateway(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_configure_llm_provider",
                   {"project_name": crew_project, "provider": "litellm-proxy"})
    assert t.startswith("Error") and "api_base" in t


async def test_unknown_provider_lists_presets(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_configure_llm_provider",
                   {"project_name": crew_project, "provider": "nope"})
    assert t.startswith("Error") and "bifrost" in t and "litellm-proxy" in t


async def test_bifrost_default_base_and_env_merge(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_configure_llm_provider",
                   {"project_name": crew_project, "provider": "bifrost"})
    assert "OPENAI_API_BASE" in t
    env = _env_text()
    assert "OPENAI_API_BASE=http://localhost:8080/v1" in env

    # reconfigure with a custom base: merged in place, never duplicated
    await call(session, "crewai_configure_llm_provider",
               {"project_name": crew_project, "provider": "bifrost",
                "api_base": "http://gateway:9090/v1"})
    env = _env_text()
    assert "OPENAI_API_BASE=http://gateway:9090/v1" in env
    assert env.count("OPENAI_API_BASE=") == 1


async def test_list_agents_reports_effective_llm(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_list_agents", {"project_name": crew_project})
    data = json.loads(t)
    agents = {a["name"]: a for a in data["agents"]}
    assert "prd_architect" in agents and len(agents) >= 5
    assert all(a["effective_llm"] for a in agents.values())


async def test_assign_all_multiselect_and_map(crew_project, mcp):
    session, _ = mcp
    # all agents
    t = await call(session, "crewai_assign_llms",
                   {"project_name": crew_project, "llm": "openai/gpt-4o-mini"})
    assert "agent(s)" in t
    # multi-select
    t = await call(session, "crewai_assign_llms",
                   {"project_name": crew_project, "llm": "groq/llama-3.3-70b-versatile",
                    "agents": ["prd_architect", "qa_reviewer"]})
    assert "2 agent(s)" in t
    # per-agent map
    t = await call(session, "crewai_assign_llms",
                   {"project_name": crew_project,
                    "assignments": {"ai_developer": "ollama/llama3.1"}})
    assert "ai_developer → ollama/llama3.1" in t

    t = await call(session, "crewai_list_agents", {"project_name": crew_project})
    agents = {a["name"]: a for a in json.loads(t)["agents"]}
    assert agents["prd_architect"]["effective_llm"] == "groq/llama-3.3-70b-versatile"
    assert agents["ai_developer"]["effective_llm"] == "ollama/llama3.1"
    assert agents["system_designer"]["effective_llm"] == "openai/gpt-4o-mini"


async def test_assign_updates_crew_py_override(crew_project, mcp):
    """A hardcoded llm= in crew.py silently beats YAML — routing must fix it too."""
    session, _ = mcp
    await call(session, "crewai_edit_crew_py",
               {"project_name": crew_project, "agent_name": "documentation_engineer",
                "llm": "openai/old-model"})
    t = await call(session, "crewai_assign_llms",
                   {"project_name": crew_project,
                    "assignments": {"documentation_engineer": "openai/new-model"}})
    assert "crew.py override updated" in t

    crew_py = CREW_PROJECT_DIR / "src" / CREW_MODULE / "crew.py"
    content = crew_py.read_text(encoding="utf-8")
    assert 'llm="openai/new-model"' in content and "old-model" not in content
    py_compile.compile(str(crew_py), doraise=True)


async def test_assign_guards(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_assign_llms",
                   {"project_name": crew_project, "llm": "x", "agents": ["ghost"]})
    assert t.startswith("Error") and "Available" in t
    t = await call(session, "crewai_assign_llms", {"project_name": crew_project})
    assert t.startswith("Error")
