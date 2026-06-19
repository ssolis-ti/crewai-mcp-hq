"""
MCP Resources — Prebuilt Full Crew Templates.

Complete, ready-to-apply crew configurations for specific domains.
Each template includes: agents YAML, tasks YAML, crew.py code, and metadata.
"""

from __future__ import annotations

import json
import logging
import textwrap

from crewai_mcp.app import mcp

logger = logging.getLogger("crewai-mcp.resources.crew_templates")

# ── Prebuilt Crew Templates ──────────────────────────────────────────

PREBUILT_CREWS: dict[str, dict] = {
    "cyberops": {
        "name": "CyberOps — AI-First Software Development Crew",
        "description": (
            "5-agent sequential crew for MVP creation. Generates PRD, architecture, "
            "production code with AI-first conventions, documentation, and QA audit. "
            "Models: 5 different LLMs via LiteLLM (DeepSeek, Llama, Qwen, Nemotron). "
            "Input variable: {project_description}"
        ),
        "process": "sequential",
        "tools": [
            "FileWriterTool",
            "FileReadTool",
            "DirectoryReadTool",
        ],
        "agents_yaml": textwrap.dedent("""\
            prd_architect:
              role: >
                PRD Architect & Product Strategist
              goal: >
                Design a comprehensive Product Requirements Document (PRD) for {project_description}.
                Define user stories, MVP scope, success criteria, and technical constraints.
              backstory: >
                You are a senior product strategist. Your PRDs are the single source of truth
                that aligns both human and AI teams. Every requirement is testable.
              llm: openai/deepseek-ai/deepseek-v4-pro
              max_iter: 25
              allow_delegation: false
              verbose: true

            system_designer:
              role: >
                Software Architect & System Designer
              goal: >
                Design the complete software architecture based on the PRD.
                Produce ADRs, C4 diagrams, API contracts, and data models.
              backstory: >
                You design AI-first architectures where every component has a single
                responsibility and the overall structure minimizes context window usage.
              llm: openai/meta/llama-3.3-70b-instruct
              max_iter: 30
              allow_delegation: false
              verbose: true

            ai_developer:
              role: >
                AI-First Full-Stack Developer
              goal: >
                Implement the MVP according to PRD and architecture. Each file <100 lines,
                complete type hints and docstrings, TDD, feature-slice pattern.
              backstory: >
                You write code optimized for AI comprehension and maintenance.
                Every function includes Examples usable as tests.
              llm: openai/meta/llama-4-maverick-17b-128e-instruct
              max_iter: 40
              allow_delegation: false
              verbose: true

            documentation_engineer:
              role: >
                Technical Documentation Engineer for AI
              goal: >
                Generate README, CONTRIBUTING, ai-context.md, and API docs.
                All with AI-consumable metadata blocks.
              backstory: >
                You write docs that teach other AI agents how to navigate and extend
                the project without breaking existing patterns.
              llm: openai/qwen/qwen3-next-80b-a3b-instruct
              max_iter: 25
              allow_delegation: false
              verbose: true

            qa_reviewer:
              role: >
                Quality Assurance & Consistency Auditor
              goal: >
                Audit complete project: PRD traceability, architecture compliance,
                AI-first standards, test coverage, documentation accuracy.
              backstory: >
                You cross-reference every requirement against implementation and produce
                structured quality reports with severity levels and fix instructions.
              llm: openai/meta/llama-3.1-70b-instruct
              max_iter: 25
              allow_delegation: false
              verbose: true
        """),
        "tasks_yaml": textwrap.dedent("""\
            prd_task:
              description: >
                Create a comprehensive PRD for: {project_description}
                Include: Executive Summary, User Personas, User Stories (As a/I want/So that
                with acceptance criteria), MVP Scope, Technical Constraints, Success Metrics,
                Open Questions. Write directly as clean markdown.
              expected_output: >
                Complete PRD in clean markdown with all 7 sections. AI-parseable.
              agent: prd_architect
              output_file: docs/PRD.md
              markdown: true

            architecture_task:
              description: >
                Based on the PRD, design the software architecture.
                Read PRD with FileReadTool, write each file with FileWriterTool:
                docs/architecture/README.md, decisions/001-tech-stack.md,
                decisions/002-database.md, decisions/003-deployment.md,
                api-spec.yaml, data-model.md. Each file under 100 lines.
              expected_output: >
                docs/architecture/ with 6+ separate files.
              agent: system_designer
              output_file: docs/architecture/README.md
              markdown: true

            development_task:
              description: >
                Implement MVP code based on PRD and architecture.
                Create under src/features/: data_downloader, etl_pipeline, data_analysis,
                dashboard, ai_agents. Each feature gets model.py, service.py, repository.py.
                Tests under tests/. Every file <100 lines, full type hints, docstrings with
                Description/Args/Returns/Raises/Examples. WRITE EACH FILE WITH FileWriterTool.
              expected_output: >
                25+ files in src/ and tests/. All follow AI-first conventions.
              agent: ai_developer
              output_file: docs/dev-summary.md
              markdown: true

            documentation_task:
              description: >
                Using FileReadTool to inspect code, generate: README.md, CONTRIBUTING.md,
                docs/ai-context.md, docs/api.md. Each doc needs metadata blocks:
                "Read this when...", "Prerequisites", "See also".
              expected_output: >
                5 markdown files with AI-consumable metadata.
              agent: documentation_engineer
              output_file: docs/doc-summary.md
              markdown: true

            qa_task:
              description: >
                Audit all generated files with FileReadTool/DirectoryReadTool.
                Check: PRD traceability, architecture compliance, AI-first standards,
                file completeness, documentation accuracy.
                Output quality report to docs/quality-report.md with severity levels,
                fix instructions, and overall score.
              expected_output: >
                docs/quality-report.md with traceability matrix and fix instructions.
              agent: qa_reviewer
              output_file: docs/quality-report.md
              markdown: true
        """),
        "crew_py": textwrap.dedent("""\
            from crewai import Agent, Crew, Process, Task
            from crewai.project import CrewBase, agent, crew, task
            from crewai.agents.agent_builder.base_agent import BaseAgent
            from crewai_tools import FileWriterTool, FileReadTool, DirectoryReadTool


            @CrewBase
            class {class_name}():
                \"\"\"{description}\"\"\"

                agents: list[BaseAgent]
                tasks: list[Task]

                @agent
                def prd_architect(self) -> Agent:
                    return Agent(
                        config=self.agents_config['prd_architect'],
                        verbose=True,
                        tools=[FileWriterTool()],
                    )

                @agent
                def system_designer(self) -> Agent:
                    return Agent(
                        config=self.agents_config['system_designer'],
                        verbose=True,
                        tools=[FileReadTool(), FileWriterTool(), DirectoryReadTool()],
                    )

                @agent
                def ai_developer(self) -> Agent:
                    return Agent(
                        config=self.agents_config['ai_developer'],
                        verbose=True,
                        tools=[FileReadTool(), FileWriterTool(), DirectoryReadTool()],
                    )

                @agent
                def documentation_engineer(self) -> Agent:
                    return Agent(
                        config=self.agents_config['documentation_engineer'],
                        verbose=True,
                        tools=[FileReadTool(), FileWriterTool(), DirectoryReadTool()],
                    )

                @agent
                def qa_reviewer(self) -> Agent:
                    return Agent(
                        config=self.agents_config['qa_reviewer'],
                        verbose=True,
                        tools=[FileReadTool(), DirectoryReadTool()],
                    )

                @task
                def prd_task(self) -> Task:
                    return Task(config=self.tasks_config['prd_task'])

                @task
                def architecture_task(self) -> Task:
                    return Task(config=self.tasks_config['architecture_task'])

                @task
                def development_task(self) -> Task:
                    return Task(config=self.tasks_config['development_task'])

                @task
                def documentation_task(self) -> Task:
                    return Task(config=self.tasks_config['documentation_task'])

                @task
                def qa_task(self) -> Task:
                    return Task(config=self.tasks_config['qa_task'])

                @crew
                def crew(self) -> Crew:
                    return Crew(
                        agents=self.agents,
                        tasks=self.tasks,
                        process=Process.sequential,
                        verbose=True,
                    )
        """),
    },
}

# ── MCP Resources ────────────────────────────────────────────────────


@mcp.resource("crewai://templates/prebuilt/index")
def prebuilt_crews_index() -> str:
    """List all available prebuilt crew templates."""
    lines = ["# Prebuilt Crew Templates\n"]
    for name, crew in PREBUILT_CREWS.items():
        lines.append(f"## {name}")
        lines.append(f"**{crew['name']}**")
        lines.append(f"{crew['description']}\n")
        lines.append(f"- Process: {crew['process']}")
        lines.append(f"- Tools: {', '.join(crew['tools'])}")
        lines.append(f"- Agents: {_count_agents(crew)}")
        lines.append(f"- Tasks: {_count_tasks(crew)}")
        lines.append(f"\n> View full config: `crewai://templates/prebuilt/{name}`")
        lines.append(f"> Apply to project: `crewai_apply_template(project_name, '{name}')`\n")
    return "\n".join(lines)


@mcp.resource("crewai://templates/prebuilt/{template_name}")
def prebuilt_crew_template(template_name: str) -> str:
    """Get a prebuilt crew template with full YAML and Python code.

    Args:
        template_name: Name of the prebuilt crew (e.g., 'cyberops')
    """
    crew = PREBUILT_CREWS.get(template_name)
    if crew is None:
        available = ", ".join(PREBUILT_CREWS.keys())
        return f"Unknown template '{template_name}'. Available: {available}"

    return (
        f"# {crew['name']}\n\n"
        f"{crew['description']}\n\n"
        f"**Process**: {crew['process']}  \n"
        f"**Tools**: {', '.join(crew['tools'])}  \n"
        f"**Agents**: {_count_agents(crew)}  \n"
        f"**Tasks**: {_count_tasks(crew)}\n\n"
        f"---\n\n"
        f"## agents.yaml\n```yaml\n{crew['agents_yaml']}\n```\n\n"
        f"## tasks.yaml\n```yaml\n{crew['tasks_yaml']}\n```\n\n"
        f"## crew.py\n```python\n{crew['crew_py']}\n```"
    )


def _count_agents(crew: dict) -> int:
    return crew["agents_yaml"].count("\n  role:")


def _count_tasks(crew: dict) -> int:
    return crew["tasks_yaml"].count("\n  description:")


def get_prebuilt_crew(name: str) -> dict | None:
    """Get a prebuilt crew config dict by name. Returns None if not found."""
    return PREBUILT_CREWS.get(name)


def list_prebuilt_crew_names() -> list[str]:
    """List all available prebuilt crew template names."""
    return list(PREBUILT_CREWS.keys())
