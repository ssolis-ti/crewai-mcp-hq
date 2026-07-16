"""Project scaffolding + agent/task lifecycle tools (crewai CLI + file editing)."""

from __future__ import annotations

import py_compile

import yaml

from tests.conftest import CREW_MODULE, CREW_PROJECT_DIR, WORKSPACE, call


def _crew_py():
    return CREW_PROJECT_DIR / "src" / CREW_MODULE / "crew.py"


def _config(name: str) -> dict:
    path = CREW_PROJECT_DIR / "src" / CREW_MODULE / "config" / name
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


async def test_scaffold_structure(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_project_info", {"project_name": crew_project})
    assert f'"module": "{CREW_MODULE}"' in t
    assert "agents.yaml" in t and "tasks.yaml" in t
    # cyberops template interpolated correctly
    content = _crew_py().read_text(encoding="utf-8")
    assert "class CiQaCrew()" in content and "{class_name}" not in content


async def test_create_duplicate_is_rejected(crew_project, mcp):
    """Duplicate check must catch the underscore-normalized dir (regression)."""
    session, _ = mcp
    t = await call(session, "crewai_create_project",
                   {"name": crew_project, "project_type": "crew"})
    assert t.startswith("Error") and "already exists" in t


async def test_create_rejects_invalid_type(mcp):
    session, _ = mcp
    t = await call(session, "crewai_create_project",
                   {"name": "x", "project_type": "swarm"})
    assert t.startswith("Error") and "Invalid project_type" in t


async def test_create_sanitizes_path_traversal(mcp):
    """'../name' must never escape the workspace (security regression)."""
    session, _ = mcp
    t = await call(session, "crewai_create_project",
                   {"name": "../ci-qa-escape", "project_type": "crew"}, timeout=300)
    outside = (WORKSPACE.parent / "ci_qa_escape").exists() or (WORKSPACE.parent / "ci-qa-escape").exists()
    inside = (WORKSPACE / "ci_qa_escape").exists()
    # cleanup before asserting
    import shutil
    shutil.rmtree(WORKSPACE / "ci_qa_escape", ignore_errors=True)
    shutil.rmtree(WORKSPACE.parent / "ci_qa_escape", ignore_errors=True)
    assert not outside, f"project escaped the workspace! ({t[:200]})"
    assert inside, f"sanitized project not created in workspace: {t[:200]}"


async def test_define_agent_updates_yaml_and_crew_py(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_define_agent", {
        "project_name": crew_project, "agent_name": "qa_researcher",
        "role": "QA Researcher", "goal": "Research {topic}", "backstory": "Meticulous.",
        "llm": "openai/gpt-4o", "tools": ["SerperDevTool()"],
        "options": {"max_iter": 10},
    })
    assert "Successfully added agent" in t and "crew.py" in t

    agents = _config("agents.yaml")
    assert agents["qa_researcher"]["llm"] == "openai/gpt-4o"
    assert agents["qa_researcher"]["max_iter"] == 10

    content = _crew_py().read_text(encoding="utf-8")
    assert "def qa_researcher" in content
    assert "SerperDevTool" in content and "from crewai_tools import" in content


async def test_define_task_with_context(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_define_task", {
        "project_name": crew_project, "task_name": "qa_check",
        "description": "Check {topic}", "expected_output": "Report",
        "agent": "qa_researcher", "context": ["prd_task"],
    })
    assert "Successfully added task" in t
    tasks = _config("tasks.yaml")
    assert tasks["qa_check"]["context"] == ["prd_task"]


async def test_edit_crew_py_and_still_compiles(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_edit_crew_py", {
        "project_name": crew_project, "agent_name": "prd_architect",
        "llm": "openai/gpt-4o-mini", "other_params": {"max_rpm": 10},
    })
    assert "Successfully updated agent" in t

    content = _crew_py().read_text(encoding="utf-8")
    assert 'llm="openai/gpt-4o-mini"' in content and "max_rpm=10" in content
    py_compile.compile(str(_crew_py()), doraise=True)


async def test_edit_unknown_agent_errors(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_edit_crew_py",
                   {"project_name": crew_project, "agent_name": "ghost", "llm": "x"})
    assert t.startswith("Error") and "not found" in t


async def test_apply_unknown_template_lists_available(crew_project, mcp):
    session, _ = mcp
    t = await call(session, "crewai_apply_template",
                   {"project_name": crew_project, "template_name": "nope"})
    assert "Unknown template" in t and "cyberops" in t
