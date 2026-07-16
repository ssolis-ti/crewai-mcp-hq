"""MCP protocol contract: tools, prompts, and server instructions."""

from __future__ import annotations

from tests.conftest import call

EXPECTED_TOOLS = {
    "crewai_create_project", "crewai_install_deps", "crewai_project_info",
    "crewai_apply_template",
    "crewai_define_agent", "crewai_define_task", "crewai_edit_crew_py", "crewai_kickoff",
    "crewai_configure_llm_provider", "crewai_assign_llms", "crewai_list_agents",
    "crewai_flow_plot", "crewai_flow_run",
    "crewai_query_knowledge", "crewai_manage_memory",
    "crewai_test_crew", "crewai_train_crew", "crewai_replay_task",
}

EXPECTED_PROMPTS = {"design_crew", "design_flow", "debug_crew", "create_custom_tool", "select_llm"}


async def test_initialize_exposes_workflow_instructions(mcp):
    _, info = mcp
    instr = info.instructions or ""
    assert "WORKFLOW" in instr
    assert "RULES" in instr
    for tool in ("crewai_create_project", "crewai_kickoff", "crewai_assign_llms"):
        assert tool in instr, f"instructions no longer mention {tool}"


async def test_all_tools_registered_with_descriptions(mcp):
    session, _ = mcp
    tools = (await session.list_tools()).tools
    names = {t.name for t in tools}
    assert names == EXPECTED_TOOLS, f"tool set drifted: {names ^ EXPECTED_TOOLS}"
    missing = [t.name for t in tools if not (t.description or "").strip()]
    assert not missing, f"tools without description: {missing}"


async def test_prompts_registered_and_renderable(mcp):
    session, _ = mcp
    prompts = (await session.list_prompts()).prompts
    assert {p.name for p in prompts} == EXPECTED_PROMPTS
    gp = await session.get_prompt("design_crew", {"use_case": "test", "complexity": "low"})
    assert gp.messages and gp.messages[0].content.text


async def test_unknown_project_returns_clear_error(mcp):
    session, _ = mcp
    t = await call(session, "crewai_project_info", {"project_name": "does-not-exist"})
    assert t.startswith("Error") and "not found" in t
