# Source: https://docs.crewai.com/en/guides/migration/upgrading-crewai

## On this page

  * Overview
  * The Two Things You Might Want to Upgrade
  * Why crewai install Alone Doesn’t Upgrade
  * How to Upgrade Your Project
  * Upgrading the Global CLI
  * Verify Both Are in Sync
  * Breaking Changes & Migration Notes
    * Import paths: tools and BaseTool
    * Agent parameter changes
    * Crew parameters
    * Task structured output
    * Memory & embedder config

Migration

# Upgrading CrewAI


How to upgrade CrewAI in your project and adapt to breaking changes between versions.


## 

​

Overview

CrewAI releases ship new capabilities regularly. This guide walks you through the practical steps to keep your installation up to date — both the CLI and your project’s virtual environment. If you’re starting fresh, see [Installation](/en/installation). If you’re coming from another framework, see [Migrating from LangGraph](/en/guides/migration/migrating-from-langgraph).

* * *

## 

​

The Two Things You Might Want to Upgrade

CrewAI lives in two places on your machine, and they upgrade independently:

What| How it’s installed| How to upgrade  
---|---|---  
The **global`crewai` CLI**| `uv tool install crewai`| `uv tool install crewai --upgrade`  
The **project venv** (what your code runs)| `crewai install` / `uv sync`| `uv add "crewai[...]>=X.Y.Z"` then `crewai install`  
  
These can — and often do — get out of sync. Running `crewai --version` tells you the CLI version. Running `uv pip show crewai` inside your project tells you the venv version. If they differ, that’s normal; what matters for your running code is the venv version.

## 

​

Why `crewai install` Alone Doesn’t Upgrade

`crewai install` is a thin wrapper around `uv sync`. It installs exactly what the current `uv.lock` file says — it does **not** bump any version constraints. If your `pyproject.toml` says `crewai>=1.11.1` and the lock file resolved to `1.11.1`, running `crewai install` will keep you on `1.11.1` forever, even if `1.14.4` is available. To actually upgrade, you need to:

  1. Update the version constraint in `pyproject.toml`
  2. Re-solve the lock file
  3. Sync the venv

`uv add` does all three in one shot.

## 

​

How to Upgrade Your Project
    
    
    # Bump the constraint and re-lock in one command
    uv add "crewai[tools]>=1.14.4"
    
    # Sync the venv (crewai install calls uv sync under the hood)
    crewai install
    
    # Verify
    uv pip show crewai
    # → Version: 1.14.4
    

Replace `[tools]` with whatever extras your project uses (e.g. `[tools,anthropic]`). Check your `pyproject.toml` `dependencies` list if you’re unsure.

`uv add` updates both `pyproject.toml` **and** `uv.lock` atomically. If you edit `pyproject.toml` manually, you still need to run `uv lock --upgrade-package crewai` to re-solve the lock file before `crewai install` will pick up the new version.

## 

​

Upgrading the Global CLI

The global CLI is separate from your project. Upgrade it with:
    
    
    uv tool install crewai --upgrade
    

If your shell warns about `PATH` after the upgrade, refresh it:
    
    
    uv tool update-shell
    

This does **not** touch your project’s venv — you still need `uv add` \+ `crewai install` inside the project.

## 

​

Verify Both Are in Sync
    
    
    # Global CLI version
    crewai --version
    
    # Project venv version
    uv pip show crewai | grep Version
    

They don’t need to match — but your project venv version is what matters for runtime behavior.

CrewAI requires `Python >=3.10, <3.14`. If `uv` was installed against an older interpreter, recreate the project venv with a supported Python before running `crewai install`.

* * *

## 

​

Breaking Changes & Migration Notes

Most upgrades only require small adjustments. The areas below are the ones that break silently or with confusing tracebacks.

### 

​

Import paths: tools and `BaseTool`

The canonical import location for tools is `crewai.tools`. Older paths still surface in tutorials but should be updated.
    
    
    # Before
    from crewai_tools import BaseTool
    from crewai.agents.tools import tool
    
    # After
    from crewai.tools import BaseTool, tool
    

The `@tool` decorator and `BaseTool` subclass both live in `crewai.tools`. `AgentFinish` and other internal-agent symbols are no longer part of the public surface — if you were importing them, switch to event listeners or `Task` callbacks instead.

### 

​

`Agent` parameter changes
    
    
    from crewai import Agent
    
    agent = Agent(
        role="Researcher",
        goal="Find authoritative sources on {topic}",
        backstory="You are a careful, source-driven researcher.",
        llm="gpt-4o-mini",   # string model name OR an LLM object
        verbose=True,        # bool, not an int level
        max_iter=15,         # default has changed across versions — set explicitly
        allow_delegation=False,
    )
    

  * `llm` accepts either a string model name (resolved via the configured provider) or an `LLM` object for fine-grained control.
  * `verbose` is a plain `bool`. Passing an integer no longer toggles log levels.
  * `max_iter` defaults have shifted between releases. If your agent silently stops looping after the first tool call, set `max_iter` explicitly.

### 

​

`Crew` parameters
    
    
    from crewai import Crew, Process
    
    crew = Crew(
        agents=[...],
        tasks=[...],
        process=Process.sequential,   # or Process.hierarchical
        memory=True,
        cache=True,
        embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}},
    )
    

  * `process=Process.hierarchical` requires either `manager_llm=` or `manager_agent=`. Without one, kickoff raises at validation time.
  * `memory=True` with a non-default embedding provider needs an `embedder` dict — see Memory & embedder config below.

### 

​

`Task` structured output

Use `output_pydantic`, `output_json`, or `output_file` to coerce a task’s result into a typed shape:
    
    
    from pydantic import BaseModel
    from crewai import Task
    
    class Article(BaseModel):
        title: str
        body: str
    
    write = Task(
        description="Write an article about {topic}",
        expected_output="A short article with a title and body",
        agent=writer,
        output_pydantic=Article,        # the class, NOT an instance
        output_file="output/article.md",
    )
    

`output_pydantic` takes the **class** itself. Passing `Article(title="", body="")` is a common mistake and fails with a confusing validation error.

### 

​

Memory & embedder config

If `memory=True` and you’re not using the default OpenAI embeddings, you must pass an `embedder`:
    
    
    crew = Crew(
        agents=[...],
        tasks=[...],
        memory=True,
        embedder={
            "provider": "ollama",
            "config": {"model": "nomic-embed-text"},
        },
    )
    

Set the relevant provider credentials (`OPENAI_API_KEY`, `OLLAMA_HOST`, etc.) in your `.env` file. Memory storage paths are project-local by default — delete the project’s memory directory if you change embedders, since dimensions don’t mix.

Was this page helpful?

YesNo

[Moving from LangGraph to CrewAI: A Practical Guide for EngineersPrevious](/en/guides/migration/migrating-from-langgraph)[AgentsNext](/en/concepts/agents)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)