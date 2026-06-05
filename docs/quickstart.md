# Source: https://docs.crewai.com/en/quickstart

Get Started

# Quickstart


Build your first CrewAI Flow in minutes — orchestration, state, and an agent crew that produces a real report.


### 

​

Watch: Building CrewAI Agents & Flows with Coding Agent Skills

Install our coding agent skills (Claude Code, Codex, …) to quickly get your coding agents up and running with CrewAI. You can install it with `npx skills add crewaiinc/skills`

In this guide you will **create a Flow** that sets a research topic, runs a **crew with one agent** (a researcher using web search), and ends with a **markdown report** on disk. Flows are the recommended way to structure production apps: they own **state** and **execution order** , while **agents** do the work inside a crew step. If you have not installed CrewAI yet, follow the [installation guide](/en/installation) first.

## 

​

Prerequisites

  * Python environment and the CrewAI CLI (see [installation](/en/installation))
  * An LLM configured with the right API keys — see [LLMs](/en/concepts/llms#setting-up-your-llm)
  * A [Serper.dev](https://serper.dev/) API key (`SERPER_API_KEY`) for web search in this tutorial

## 

​

Build your first Flow

1

Create a Flow project

From your terminal, scaffold a Flow project (the folder name uses underscores, e.g. `latest_ai_flow`):

Terminal
    
    
    crewai create flow latest-ai-flow
    cd latest_ai_flow
    

This creates a Flow app under `src/latest_ai_flow/`, including a starter crew under `crews/content_crew/` that you will replace with a minimal **single-agent** research crew in the next steps.

2

Configure one agent in `agents.yaml`

Replace the contents of `src/latest_ai_flow/crews/content_crew/config/agents.yaml` with a single researcher. Variables like `{topic}` are filled from `crew.kickoff(inputs=...)`.

agents.yaml
    
    
    # src/latest_ai_flow/crews/content_crew/config/agents.yaml
    researcher:
      role: >
        {topic} Senior Data Researcher
      goal: >
        Uncover cutting-edge developments in {topic}
      backstory: >
        You're a seasoned researcher with a knack for uncovering the latest
        developments in {topic}. You find the most relevant information and
        present it clearly.
    

3

Configure one task in `tasks.yaml`

tasks.yaml
    
    
    # src/latest_ai_flow/crews/content_crew/config/tasks.yaml
    research_task:
      description: >
        Conduct thorough research about {topic}. Use web search to find current,
        credible information. The current year is 2026.
      expected_output: >
        A markdown report with clear sections: key trends, notable tools or companies,
        and implications. Aim for 800–1200 words. No fenced code blocks around the whole document.
      agent: researcher
      output_file: output/report.md
    

4

Wire the crew class (`content_crew.py`)

Point the generated crew at your YAML and attach `SerperDevTool` to the researcher.

content_crew.py
    
    
    # src/latest_ai_flow/crews/content_crew/content_crew.py
    from typing import List
    
    from crewai import Agent, Crew, Process, Task
    from crewai.agents.agent_builder.base_agent import BaseAgent
    from crewai.project import CrewBase, agent, crew, task
    from crewai_tools import SerperDevTool
    
    
    @CrewBase
    class ResearchCrew:
      """Single-agent research crew used inside the Flow."""
    
      agents: List[BaseAgent]
      tasks: List[Task]
    
      agents_config = "config/agents.yaml"
      tasks_config = "config/tasks.yaml"
    
      @agent
      def researcher(self) -> Agent:
        return Agent(
          config=self.agents_config["researcher"],  # type: ignore[index]
          verbose=True,
          tools=[SerperDevTool()],
        )
    
      @task
      def research_task(self) -> Task:
        return Task(
          config=self.tasks_config["research_task"],  # type: ignore[index]
        )
    
      @crew
      def crew(self) -> Crew:
        return Crew(
          agents=self.agents,
          tasks=self.tasks,
          process=Process.sequential,
          verbose=True,
        )
    

5

Define the Flow in `main.py`

Connect the crew to a Flow: a `@start()` step sets the topic in **state** , and a `@listen` step runs the crew. The task’s `output_file` still writes `output/report.md`.

main.py
    
    
    # src/latest_ai_flow/main.py
    from pydantic import BaseModel
    
    from crewai.flow import Flow, listen, start
    
    from latest_ai_flow.crews.content_crew.content_crew import ResearchCrew
    
    
    class ResearchFlowState(BaseModel):
      topic: str = ""
      report: str = ""
    
    
    class LatestAiFlow(Flow[ResearchFlowState]):
      @start()
      def prepare_topic(self, crewai_trigger_payload: dict | None = None):
        if crewai_trigger_payload:
          self.state.topic = crewai_trigger_payload.get("topic", "AI Agents")
        else:
          self.state.topic = "AI Agents"
        print(f"Topic: {self.state.topic}")
    
      @listen(prepare_topic)
      def run_research(self):
        result = ResearchCrew().crew().kickoff(inputs={"topic": self.state.topic})
        self.state.report = result.raw
        print("Research crew finished.")
    
      @listen(run_research)
      def summarize(self):
        print("Report path: output/report.md")
    
    
    def kickoff():
      LatestAiFlow().kickoff()
    
    
    def plot():
      LatestAiFlow().plot()
    
    
    if __name__ == "__main__":
      kickoff()
    

If your package name differs from `latest_ai_flow`, change the import of `ResearchCrew` to match your project’s module path.

6

Set environment variables

In `.env` at the project root, set:

  * `SERPER_API_KEY` — from [Serper.dev](https://serper.dev/)
  * Your model provider keys as required — see [LLM setup](/en/concepts/llms#setting-up-your-llm)

7

Install and run

Terminal
    
    
    crewai install
    crewai run
    

`crewai run` executes the Flow entrypoint defined in your project (same command as for crews; project type is `"flow"` in `pyproject.toml`).

8

Check the output

You should see logs from the Flow and the crew. Open **`output/report.md`** for the generated report (excerpt):

output/report.md
    
    
    # AI Agents in 2026: Landscape and Trends
    
    ## Executive summary
    …
    
    ## Key trends
    - **Tool use and orchestration** — …
    - **Enterprise adoption** — …
    
    ## Implications
    …
    

Your actual file will be longer and reflect live search results.

## 

​

How this run fits together

  1. **Flow** — `LatestAiFlow` runs `prepare_topic` first, then `run_research`, then `summarize`. State (`topic`, `report`) lives on the Flow.
  2. **Crew** — `ResearchCrew` runs one task with one agent: the researcher uses **Serper** to search the web, then writes the structured report.
  3. **Artifact** — The task’s `output_file` writes the report under `output/report.md`.

To go deeper on Flow patterns (routing, persistence, human-in-the-loop), see [Build your first Flow](/en/guides/flows/first-flow) and [Flows](/en/concepts/flows). For crews without a Flow, see [Crews](/en/concepts/crews). For a single `Agent` and `kickoff()` without tasks, see [Agents](/en/concepts/agents#direct-agent-interaction-with-kickoff).

You now have an end-to-end Flow with an agent crew and a saved report — a solid base to add more steps, crews, or tools.

### 

​

Naming consistency

YAML keys (`researcher`, `research_task`) must match the method names on your `@CrewBase` class. See [Crews](/en/concepts/crews) for the full decorator pattern.

## 

​

Deploying

Push your Flow to **[CrewAI AMP](https://app.crewai.com)** once it runs locally and your project is in a **GitHub** repository. From the project root:

Authenticate

Create deployment

Check status & logs

Ship updates after you change code

List or remove deployments
    
    
    crewai login
    

The first deploy usually takes **around 1 minute**. Full prerequisites and the web UI flow are in [Deploy to AMP](/en/enterprise/guides/deploy-to-amp).

## Deploy guide

Step-by-step AMP deployment (CLI and dashboard).

## Join the Community

Discuss ideas, share projects, and connect with other CrewAI developers.

Was this page helpful?

YesNo

[InstallationPrevious](/en/installation)[Evaluating Use Cases for CrewAINext](/en/guides/concepts/evaluating-use-cases)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)