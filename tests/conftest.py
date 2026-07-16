"""Shared fixtures: one real MCP server over stdio for the whole test session.

These tests are the compatibility gate for crewai upgrades — they exercise
the full MCP contract (tools, resources, prompts) against a live server,
exactly as an MCP client would.
"""

from __future__ import annotations

import asyncio
import shutil
import sys
from pathlib import Path

import pytest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = ROOT / "workspace"

# Test projects (underscore variants are what the CLI actually creates)
CREW_PROJECT = "ci-qa-crew"
CREW_PROJECT_DIR = WORKSPACE / "ci_qa_crew"
CREW_MODULE = "ci_qa_crew"
FLOW_PROJECT = "ci-qa-flow"
FLOW_PROJECT_DIR = WORKSPACE / "ci_qa_flow"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def call(session: ClientSession, tool: str, args: dict, timeout: int = 300) -> str:
    """Call an MCP tool and return its text content."""
    out = await asyncio.wait_for(session.call_tool(tool, args), timeout=timeout)
    return out.content[0].text if out.content else ""


async def read(session: ClientSession, uri: str) -> str:
    """Read an MCP resource and return its text content."""
    res = await asyncio.wait_for(session.read_resource(uri), timeout=60)
    return res.contents[0].text


@pytest_asyncio.fixture(scope="session")
async def mcp():
    """(session, init_result) against a real stdio server subprocess.

    The client contexts are owned by a dedicated task so they enter and exit
    in the SAME task — anyio cancel scopes forbid cross-task exit, which is
    exactly what a plain async-generator fixture teardown would do.
    """
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "crewai_mcp.server"], cwd=str(ROOT)
    )
    holder: dict = {}
    started = asyncio.Event()
    stop = asyncio.Event()

    async def runner():
        try:
            async with stdio_client(params) as (r, w):
                async with ClientSession(r, w) as session:
                    holder["session"] = session
                    holder["info"] = await session.initialize()
                    started.set()
                    await stop.wait()
        except BaseException as e:  # surface startup failures instead of hanging
            holder["error"] = e
            started.set()
            raise

    task = asyncio.create_task(runner())
    await asyncio.wait_for(started.wait(), timeout=120)
    if "error" in holder:
        raise RuntimeError(f"MCP server failed to start: {holder['error']}")

    yield holder["session"], holder["info"]

    stop.set()
    await asyncio.wait_for(task, timeout=30)


@pytest_asyncio.fixture(scope="session")
async def crew_project(mcp):
    """A real crew project with the cyberops template applied (removed on teardown)."""
    session, _ = mcp
    shutil.rmtree(CREW_PROJECT_DIR, ignore_errors=True)

    t = await call(session, "crewai_create_project",
                   {"name": CREW_PROJECT, "project_type": "crew"}, timeout=300)
    assert "Successfully created" in t, f"create_project failed: {t}"

    t = await call(session, "crewai_apply_template",
                   {"project_name": CREW_PROJECT, "template_name": "cyberops"})
    assert "applied to project" in t, f"apply_template failed: {t}"

    yield CREW_PROJECT
    shutil.rmtree(CREW_PROJECT_DIR, ignore_errors=True)


@pytest_asyncio.fixture(scope="session")
async def flow_project(mcp):
    """A real flow project (removed on teardown)."""
    session, _ = mcp
    shutil.rmtree(FLOW_PROJECT_DIR, ignore_errors=True)

    t = await call(session, "crewai_create_project",
                   {"name": FLOW_PROJECT, "project_type": "flow"}, timeout=300)
    assert "Successfully created" in t, f"create_project (flow) failed: {t}"

    yield FLOW_PROJECT
    shutil.rmtree(FLOW_PROJECT_DIR, ignore_errors=True)
