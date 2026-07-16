"""
MCP Tools — LLM Provider Connection & Routing.

Tools for connecting a project to an LLM provider (API keys / base URLs)
and routing models to one, several, or all agents (multi-select).
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Optional

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.tools.utils import get_module_dir, get_project_path

logger = logging.getLogger("crewai-mcp.tools.llm_config")

# ── Provider presets (LiteLLM naming convention) ─────────────────────

PROVIDERS: dict[str, dict[str, Any]] = {
    "openai": {
        "key_env": "OPENAI_API_KEY",
        "base_env": "OPENAI_API_BASE",
        "model_prefix": "openai/",
        "example_model": "openai/gpt-4o",
    },
    "anthropic": {
        "key_env": "ANTHROPIC_API_KEY",
        "base_env": "ANTHROPIC_API_BASE",
        "model_prefix": "anthropic/",
        "example_model": "anthropic/claude-opus-4-8",
    },
    "gemini": {
        "key_env": "GEMINI_API_KEY",
        "base_env": None,
        "model_prefix": "gemini/",
        "example_model": "gemini/gemini-1.5-pro",
    },
    "groq": {
        "key_env": "GROQ_API_KEY",
        "base_env": None,
        "model_prefix": "groq/",
        "example_model": "groq/llama-3.3-70b-versatile",
    },
    "openrouter": {
        "key_env": "OPENROUTER_API_KEY",
        "base_env": None,
        "model_prefix": "openrouter/",
        "example_model": "openrouter/deepseek/deepseek-chat",
    },
    "ollama": {
        "key_env": None,
        "base_env": "OLLAMA_BASE_URL",
        "default_base": "http://localhost:11434",
        "model_prefix": "ollama/",
        "example_model": "ollama/llama3.1",
    },
    # Any OpenAI-compatible gateway: LiteLLM proxy, vLLM, LM Studio, NIM...
    "litellm-proxy": {
        "key_env": "OPENAI_API_KEY",
        "base_env": "OPENAI_API_BASE",
        "model_prefix": "openai/",
        "example_model": "openai/llama-3.3-70b-nim",
        "note": "Set api_base to your proxy URL; model names use the 'openai/' prefix.",
    },
    # Bifrost gateway (maximhq/bifrost) — OpenAI-compatible, default port 8080
    "bifrost": {
        "key_env": "OPENAI_API_KEY",
        "base_env": "OPENAI_API_BASE",
        "default_base": "http://localhost:8080/v1",
        "model_prefix": "openai/",
        "example_model": "openai/gpt-4o-mini",
        "note": "Bifrost manages the real provider keys at the gateway — the client "
        "key can be any dummy value unless you enabled auth on Bifrost.",
    },
}

_KEY_PLACEHOLDER = "your-api-key-here"


def _merge_env(env_file: Path, updates: dict[str, str]) -> None:
    """Merge KEY=VALUE pairs into a .env file, preserving other lines/comments."""
    lines = env_file.read_text(encoding="utf-8").splitlines() if env_file.exists() else []
    done: set[str] = set()
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        key = None
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
        if key in updates:
            out.append(f"{key}={updates[key]}")
            done.add(key)
        else:
            out.append(line)
    for key, value in updates.items():
        if key not in done:
            out.append(f"{key}={value}")
    env_file.write_text("\n".join(out) + "\n", encoding="utf-8")


@mcp.tool()
def crewai_configure_llm_provider(
    project_name: str = Field(..., description="Project name in the workspace"),
    provider: str = Field(
        ...,
        description=f"Provider preset: {', '.join(PROVIDERS)}. "
        "Use 'litellm-proxy' for any OpenAI-compatible gateway (LiteLLM, vLLM, LM Studio, NIM).",
    ),
    api_base: str = Field(
        default="",
        description="Custom base URL (required for litellm-proxy/ollama gateways, optional otherwise)",
    ),
    api_key: str = Field(
        default="",
        description="Optional API key to write into the project .env. Prefer leaving it empty "
        "and asking the user to fill it in — keys should not travel through the conversation.",
    ),
) -> str:
    """
    Connect a project to an LLM provider by writing its .env configuration.

    Merges the provider's environment variables into the project's .env
    (existing unrelated entries are preserved). If no api_key is given, a
    placeholder is written and the user must fill it in manually.

    After configuring the provider, route models to agents with
    crewai_assign_llms using the provider's model prefix
    (e.g. 'openai/gpt-4o', 'anthropic/claude-opus-4-8', 'ollama/llama3.1').
    """
    preset = PROVIDERS.get(provider)
    if preset is None:
        return f"Error: Unknown provider '{provider}'. Available: {', '.join(PROVIDERS)}"

    project_path = get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    updates: dict[str, str] = {}
    notes: list[str] = []

    if preset["key_env"]:
        updates[preset["key_env"]] = api_key or _KEY_PLACEHOLDER
        if not api_key:
            notes.append(
                f"⚠ {preset['key_env']} was written as a placeholder — the user must "
                f"set the real key in {project_path / '.env'} before running the crew."
            )

    base = api_base or preset.get("default_base", "")
    if base:
        if not preset["base_env"]:
            return f"Error: provider '{provider}' does not use a custom base URL."
        updates[preset["base_env"]] = base
    elif provider in ("litellm-proxy",):
        return "Error: 'litellm-proxy' requires api_base (the URL of your gateway)."

    try:
        _merge_env(project_path / ".env", updates)
    except OSError as e:
        return f"Error writing .env: {e}"

    if preset.get("note"):
        notes.append(preset["note"])

    written = "\n".join(
        f"  {k}={'<hidden>' if 'KEY' in k and api_key else v}" for k, v in updates.items()
    )
    notes_str = ("\n" + "\n".join(notes)) if notes else ""
    return (
        f"✅ Provider '{provider}' configured for '{project_name}'.\n"
        f"Written to {project_path / '.env'}:\n{written}\n"
        f"Model naming for agents: {preset['example_model']} "
        f"(prefix '{preset['model_prefix']}')."
        f"{notes_str}\n"
        f"Next: route models with crewai_assign_llms."
    )


# ── Agent LLM routing (multi-select) ─────────────────────────────────


def _agents_yaml_path(project_name: str) -> tuple[Optional[Path], Optional[Path], str]:
    """Resolve (agents.yaml, crew.py, error) for a project."""
    project_path = get_project_path(project_name)
    if not project_path.exists():
        return None, None, f"Error: Project '{project_name}' not found."
    module_dir = get_module_dir(project_path)
    if module_dir is None:
        return None, None, f"Error: Could not find the source module of '{project_name}'."
    agents_yaml = module_dir / "config" / "agents.yaml"
    if not agents_yaml.exists():
        return None, None, f"Error: {agents_yaml} not found."
    return agents_yaml, module_dir / "crew.py", ""


def _update_crew_py_llm_override(crew_py: Path, agent_name: str, model: str) -> Optional[str]:
    """If the agent method in crew.py hardcodes llm=..., update it (it beats YAML).

    Returns a status string when an override was updated, else None.
    """
    if not crew_py.exists():
        return None
    content = crew_py.read_text(encoding="utf-8")
    m = re.search(rf"@agent\s+def\s+{re.escape(agent_name)}\b", content)
    if not m:
        return None
    nxt = re.search(r"\n[ \t]*@(agent|task|crew)\b", content[m.end():])
    block_end = m.end() + (nxt.start() if nxt else len(content) - m.end())
    block = content[m.start():block_end]
    new_block, n = re.subn(r"llm\s*=\s*[\"'][^\"']*[\"']", f'llm="{model}"', block)
    if n == 0:
        return None
    crew_py.write_text(content[: m.start()] + new_block + content[block_end:], encoding="utf-8")
    return f"crew.py override updated ({n} occurrence(s))"


@mcp.tool()
def crewai_assign_llms(
    project_name: str = Field(..., description="Project name in the workspace"),
    llm: str = Field(
        default="",
        description="Model to assign (e.g. 'openai/gpt-4o'). Used with 'agents'; ignored if 'assignments' is given.",
    ),
    agents: Optional[list[str]] = Field(
        default=None,
        description="Multi-select: agent names to assign 'llm' to. Omit to target ALL agents.",
    ),
    assignments: Optional[dict[str, str]] = Field(
        default=None,
        description="Per-agent routing map {agent_name: model}. Takes precedence over llm/agents.",
    ),
) -> str:
    """
    Route LLM models to one, several, or all agents of a project (multi-select).

    Three modes:
    - assignments={'researcher': 'openai/gpt-4o', 'writer': 'groq/llama-3.3-70b-versatile'}
      → per-agent routing in a single call.
    - llm='openai/gpt-4o', agents=['researcher', 'writer'] → same model for a selection.
    - llm='openai/gpt-4o' (no agents) → same model for ALL agents.

    Updates agents.yaml, and also fixes any hardcoded llm= override in crew.py
    (which would otherwise take precedence over YAML). Use crewai_list_agents
    first to see agent names and current models.
    """
    import yaml

    agents_yaml, crew_py, err = _agents_yaml_path(project_name)
    if err:
        return err

    try:
        agents_data = yaml.safe_load(agents_yaml.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return f"Error reading agents.yaml: {e}"

    if not agents_data:
        return "Error: agents.yaml is empty — define agents first."

    # Build the routing map
    if assignments:
        mapping = dict(assignments)
    elif llm:
        targets = agents if agents else list(agents_data.keys())
        mapping = {a: llm for a in targets}
    else:
        return "Error: provide either 'assignments' or 'llm' (optionally with 'agents')."

    unknown = [a for a in mapping if a not in agents_data]
    if unknown:
        return (
            f"Error: Unknown agent(s): {', '.join(unknown)}. "
            f"Available: {', '.join(agents_data.keys())}"
        )

    report: list[str] = []
    for agent_name, model in mapping.items():
        agents_data[agent_name]["llm"] = model
        line = f"  {agent_name} → {model}"
        override = _update_crew_py_llm_override(crew_py, agent_name, model)
        if override:
            line += f" ({override})"
        report.append(line)

    try:
        with agents_yaml.open("w", encoding="utf-8") as f:
            yaml.dump(agents_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    except Exception as e:
        return f"Error writing agents.yaml: {e}"

    return (
        f"✅ LLM routing applied to '{project_name}' ({len(mapping)} agent(s)):\n"
        + "\n".join(report)
        + "\nReminder: the provider credentials for these models must exist in the "
        "project .env (crewai_configure_llm_provider)."
    )


@mcp.tool()
def crewai_list_agents(
    project_name: str = Field(..., description="Project name in the workspace"),
) -> str:
    """
    List a project's agents with their role and current LLM (JSON).

    Use this before crewai_assign_llms to know the exact agent names for
    multi-select routing, and to see which model each agent currently uses.
    An agent's effective model is crew.py's llm= override when present,
    otherwise the agents.yaml value, otherwise the crewai default.
    """
    import yaml

    agents_yaml, crew_py, err = _agents_yaml_path(project_name)
    if err:
        return err

    try:
        agents_data = yaml.safe_load(agents_yaml.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return f"Error reading agents.yaml: {e}"

    crew_content = crew_py.read_text(encoding="utf-8") if crew_py.exists() else ""

    result = []
    for name, cfg in agents_data.items():
        cfg = cfg or {}
        entry: dict[str, Any] = {
            "name": name,
            "role": " ".join(str(cfg.get("role", "")).split()),
            "llm_yaml": cfg.get("llm"),
        }
        m = re.search(rf"@agent\s+def\s+{re.escape(name)}\b", crew_content)
        if m:
            nxt = re.search(r"\n[ \t]*@(agent|task|crew)\b", crew_content[m.end():])
            block_end = m.end() + (nxt.start() if nxt else len(crew_content) - m.end())
            ov = re.search(r"llm\s*=\s*[\"']([^\"']*)[\"']", crew_content[m.start():block_end])
            if ov:
                entry["llm_crew_py_override"] = ov.group(1)
        entry["effective_llm"] = (
            entry.get("llm_crew_py_override") or entry["llm_yaml"] or "(crewai default)"
        )
        result.append(entry)

    return json.dumps({"project": project_name, "agents": result}, indent=2, ensure_ascii=False)
