"""
MCP Resources — CrewAI Templates.

Pre-built templates for rapidly scaffolding CrewAI components:
agents, tasks, crews, flows, tools, and YAML configurations.
"""

from __future__ import annotations

import logging
import textwrap

from crewai_mcp.app import mcp

logger = logging.getLogger("crewai-mcp.resources.templates")

# ── Agent Templates ──────────────────────────────────────────────────

AGENT_TEMPLATES: dict[str, str] = {
    "researcher": textwrap.dedent("""\
        # Agent Template: Researcher

        ## YAML Configuration (agents.yaml)
        ```yaml
        researcher:
          role: Senior Research Analyst
          goal: >
            Conduct comprehensive research on {topic} and provide
            detailed, accurate findings with citations.
          backstory: >
            You are an experienced research analyst with a keen eye for detail.
            You excel at finding, analyzing, and synthesizing information from
            multiple sources to provide comprehensive insights.
          verbose: true
          allow_delegation: false
        ```

        ## Python Implementation (crew.py)
        ```python
        from crewai import Agent
        from crewai_tools import SerperDevTool, WebsiteSearchTool

        @agent
        def researcher(self) -> Agent:
            return Agent(
                config=self.agents_config["researcher"],
                tools=[SerperDevTool(), WebsiteSearchTool()],
            )
        ```
    """),
    "writer": textwrap.dedent("""\
        # Agent Template: Content Writer

        ## YAML Configuration (agents.yaml)
        ```yaml
        writer:
          role: Senior Content Writer
          goal: >
            Create engaging, well-structured content about {topic}
            that is informative and accessible to the target audience.
          backstory: >
            You are a skilled writer with a passion for technology.
            You transform complex information into clear, compelling narratives.
          verbose: true
          allow_delegation: false
        ```

        ## Python Implementation (crew.py)
        ```python
        from crewai import Agent
        from crewai_tools import FileReadTool, DirectoryReadTool

        @agent
        def writer(self) -> Agent:
            return Agent(
                config=self.agents_config["writer"],
                tools=[FileReadTool(), DirectoryReadTool()],
            )
        ```
    """),
    "analyst": textwrap.dedent("""\
        # Agent Template: Data Analyst

        ## YAML Configuration (agents.yaml)
        ```yaml
        analyst:
          role: Data Analyst
          goal: >
            Analyze data related to {topic} and extract actionable
            insights with statistical backing.
          backstory: >
            You are an expert data analyst with strong statistical skills.
            You turn raw data into meaningful insights that drive decisions.
          verbose: true
          allow_delegation: false
        ```

        ## Python Implementation (crew.py)
        ```python
        from crewai import Agent
        from crewai_tools import CSVSearchTool, JSONSearchTool

        @agent
        def analyst(self) -> Agent:
            return Agent(
                config=self.agents_config["analyst"],
                tools=[CSVSearchTool(), JSONSearchTool()],
            )
        ```
    """),
    "coder": textwrap.dedent("""\
        # Agent Template: Software Engineer

        ## YAML Configuration (agents.yaml)
        ```yaml
        coder:
          role: Senior Software Engineer
          goal: >
            Design and implement high-quality code solutions for {task}.
          backstory: >
            You are a senior software engineer with expertise in Python,
            software architecture, and best practices. You write clean,
            well-documented, and tested code.
          verbose: true
          allow_delegation: false
        ```

        ## Python Implementation (crew.py)
        ```python
        from crewai import Agent
        from crewai_tools import FileReadTool, DirectoryReadTool, CodeDocsSearchTool

        @agent
        def coder(self) -> Agent:
            return Agent(
                config=self.agents_config["coder"],
                tools=[FileReadTool(), DirectoryReadTool(), CodeDocsSearchTool()],
            )
        ```
    """),
    "reviewer": textwrap.dedent("""\
        # Agent Template: Code Reviewer

        ## YAML Configuration (agents.yaml)
        ```yaml
        reviewer:
          role: Senior Code Reviewer
          goal: >
            Review code for quality, security, and performance issues.
            Provide constructive feedback and actionable suggestions.
          backstory: >
            You are a meticulous code reviewer with years of experience
            in security auditing and performance optimization.
          verbose: true
          allow_delegation: false
        ```

        ## Python Implementation (crew.py)
        ```python
        from crewai import Agent
        from crewai_tools import GithubSearchTool, FileReadTool

        @agent
        def reviewer(self) -> Agent:
            return Agent(
                config=self.agents_config["reviewer"],
                tools=[GithubSearchTool(), FileReadTool()],
            )
        ```
    """),
}

# ── Crew Templates ───────────────────────────────────────────────────

CREW_TEMPLATES: dict[str, str] = {
    "sequential": textwrap.dedent("""\
        # Crew Template: Sequential Process

        Tasks are executed one after another in the order they are defined.
        Output of one task becomes context for the next.

        ```python
        from crewai import Crew, Process

        @crew
        def crew(self) -> Crew:
            return Crew(
                agents=self.agents,  # Auto-collected by @CrewBase
                tasks=self.tasks,    # Auto-collected by @CrewBase
                process=Process.sequential,
                verbose=True,
                memory=True,
                planning=True,
            )
        ```

        **Best for:** Linear workflows where each step depends on the previous.
        Examples: Research → Write → Review, Data Collection → Analysis → Report.
    """),
    "hierarchical": textwrap.dedent("""\
        # Crew Template: Hierarchical Process

        A manager agent coordinates other agents, delegating tasks and
        synthesizing results. Requires a manager LLM or custom manager agent.

        ```python
        from crewai import Crew, Process

        @crew
        def crew(self) -> Crew:
            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.hierarchical,
                manager_llm="openai/gpt-4o",  # or manager_agent=custom_agent
                verbose=True,
                memory=True,
            )
        ```

        **Best for:** Complex projects requiring coordination.
        Examples: Software development team, content production pipeline.
    """),
    "parallel": textwrap.dedent("""\
        # Crew Template: Parallel Execution

        Use `kickoff_for_each` to run the same crew across multiple inputs
        in parallel, or use async execution.

        ```python
        from crewai import Crew, Process

        @crew
        def crew(self) -> Crew:
            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True,
            )

        # Run for multiple inputs in parallel
        inputs = [
            {"topic": "AI Agents"},
            {"topic": "LLM Fine-tuning"},
            {"topic": "RAG Systems"},
        ]
        results = crew.kickoff_for_each(inputs=inputs)

        # Or use async
        import asyncio
        result = asyncio.run(crew.kickoff_async(inputs={"topic": "AI"}))
        ```

        **Best for:** Batch processing, multi-topic analysis, A/B testing.
    """),
}

# ── Flow Templates ───────────────────────────────────────────────────

FLOW_TEMPLATES: dict[str, str] = {
    "linear": textwrap.dedent("""\
        # Flow Template: Linear Flow

        Simple sequential flow with state management.

        ```python
        from crewai.flow.flow import Flow, listen, start
        from pydantic import BaseModel

        class LinearState(BaseModel):
            topic: str = ""
            research: str = ""
            report: str = ""

        class LinearFlow(Flow[LinearState]):
            @start()
            def gather_input(self):
                self.state.topic = "AI Agents"
                return self.state.topic

            @listen(gather_input)
            def research(self, topic):
                # Run a research crew here
                self.state.research = f"Research on {topic}"
                return self.state.research

            @listen(research)
            def write_report(self, research):
                self.state.report = f"Report based on: {research}"
                return self.state.report

        flow = LinearFlow()
        result = flow.kickoff()
        ```
    """),
    "branching": textwrap.dedent("""\
        # Flow Template: Branching Flow with Router

        Uses @router to conditionally branch execution paths.

        ```python
        from crewai.flow.flow import Flow, listen, router, start
        from pydantic import BaseModel

        class BranchState(BaseModel):
            input_type: str = ""
            result: str = ""

        class BranchFlow(Flow[BranchState]):
            @start()
            def classify_input(self):
                # Determine input type
                return self.state.input_type

            @router(classify_input)
            def route(self, classification):
                if classification == "technical":
                    return "technical_path"
                return "general_path"

            @listen("technical_path")
            def handle_technical(self):
                self.state.result = "Technical analysis complete"

            @listen("general_path")
            def handle_general(self):
                self.state.result = "General response complete"

        flow = BranchFlow()
        flow.kickoff()
        ```
    """),
    "human-in-loop": textwrap.dedent("""\
        # Flow Template: Human-in-the-Loop Flow

        Pauses execution for human review/approval before continuing.

        ```python
        from crewai.flow.flow import Flow, listen, start
        from crewai.flow.flow_decorators import human_feedback
        from pydantic import BaseModel

        class HILState(BaseModel):
            draft: str = ""
            feedback: str = ""
            final: str = ""

        class HILFlow(Flow[HILState]):
            @start()
            def create_draft(self):
                self.state.draft = "Initial draft content..."
                return self.state.draft

            @human_feedback(
                message="Please review the draft and provide feedback:",
                emit=["approved", "needs_revision"]
            )
            @listen(create_draft)
            def review(self, draft):
                return draft

            @listen("approved")
            def publish(self):
                self.state.final = self.state.draft

            @listen("needs_revision")
            def revise(self):
                # Incorporate feedback and re-draft
                self.state.draft = f"Revised: {self.state.feedback}"

        flow = HILFlow()
        flow.kickoff()
        ```
    """),
}

# ── Custom Tool Template ─────────────────────────────────────────────

TOOL_TEMPLATE = textwrap.dedent("""\
    # Custom Tool Template

    ## Option 1: Using @tool decorator (Quick)

    ```python
    from crewai.tools import tool

    @tool("My Custom Tool")
    def my_tool(query: str) -> str:
        \"\"\"Description of what this tool does.
        The agent uses this description to decide when to use the tool.\"\"\"
        # Your tool logic here
        return f"Result for: {query}"
    ```

    ## Option 2: Subclassing BaseTool (Full Control)

    ```python
    from typing import Type
    from crewai.tools import BaseTool
    from pydantic import BaseModel, Field

    class MyToolInput(BaseModel):
        \"\"\"Input schema for MyCustomTool.\"\"\"
        query: str = Field(..., description="The search query")
        limit: int = Field(default=10, description="Max results")

    class MyCustomTool(BaseTool):
        name: str = "my_custom_tool"
        description: str = "Searches for information based on a query."
        args_schema: Type[BaseModel] = MyToolInput

        def _run(self, query: str, limit: int = 10) -> str:
            # Synchronous implementation
            return f"Found {limit} results for: {query}"

        async def _arun(self, query: str, limit: int = 10) -> str:
            # Optional async implementation
            return f"Found {limit} results for: {query}"
    ```

    ## Option 3: Async Tool (Non-blocking I/O)

    ```python
    import aiohttp
    from crewai.tools import tool

    @tool("Async Fetcher")
    async def fetch_data(url: str) -> str:
        \"\"\"Fetch data from a URL asynchronously.\"\"\"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    ```
""")


# ── Register Resources ───────────────────────────────────────────────


@mcp.resource("crewai://templates/index")
def templates_index() -> str:
    """List all available CrewAI templates organized by type."""
    lines = [
        "# CrewAI Templates Index\n",
        "## Agent Templates",
    ]
    for name in AGENT_TEMPLATES:
        lines.append(f"- [{name}](crewai://templates/agent/{name})")

    lines.append("\n## Crew Templates")
    for name in CREW_TEMPLATES:
        lines.append(f"- [{name}](crewai://templates/crew/{name})")

    lines.append("\n## Flow Templates")
    for name in FLOW_TEMPLATES:
        lines.append(f"- [{name}](crewai://templates/flow/{name})")

    lines.append("\n## Tool Templates")
    lines.append("- [custom](crewai://templates/tool/custom)")

    return "\n".join(lines)


@mcp.resource("crewai://templates/agent/{agent_type}")
def agent_template(agent_type: str) -> str:
    """
    Get a pre-built agent template with YAML config and Python code.

    Args:
        agent_type: One of: researcher, writer, analyst, coder, reviewer
    """
    template = AGENT_TEMPLATES.get(agent_type)
    if template is None:
        available = ", ".join(AGENT_TEMPLATES.keys())
        return f"Unknown agent type '{agent_type}'. Available: {available}"
    return template


@mcp.resource("crewai://templates/crew/{pattern}")
def crew_template(pattern: str) -> str:
    """
    Get a crew template for a specific process pattern.

    Args:
        pattern: One of: sequential, hierarchical, parallel
    """
    template = CREW_TEMPLATES.get(pattern)
    if template is None:
        available = ", ".join(CREW_TEMPLATES.keys())
        return f"Unknown crew pattern '{pattern}'. Available: {available}"
    return template


@mcp.resource("crewai://templates/flow/{flow_type}")
def flow_template(flow_type: str) -> str:
    """
    Get a flow template with state management and decorators.

    Args:
        flow_type: One of: linear, branching, human-in-loop
    """
    template = FLOW_TEMPLATES.get(flow_type)
    if template is None:
        available = ", ".join(FLOW_TEMPLATES.keys())
        return f"Unknown flow type '{flow_type}'. Available: {available}"
    return template


@mcp.resource("crewai://templates/tool/custom")
def custom_tool_template() -> str:
    """Get the template for creating custom CrewAI tools with all three approaches."""
    return TOOL_TEMPLATE
