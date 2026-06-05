# Source: https://docs.crewai.com/en/guides/coding-tools/build-with-ai

Get Started

# Build with AI


Everything AI coding agents need to build, deploy, and scale with CrewAI — skills, machine-readable docs, deployment, and enterprise features.


# 

​

Build with AI

CrewAI is AI-native. This page brings together everything an AI coding agent needs to build with CrewAI — whether you’re Claude Code, Codex, Cursor, Gemini CLI, or any other assistant helping a developer ship crews and flows.

### 

​

Supported Coding Agents

## Claude Code

## Cursor

## Codex

## Windsurf

## Gemini CLI

This page is designed to be consumed by both humans and AI assistants. If you’re a coding agent, start with **Skills** to get CrewAI context, then use **llms.txt** for full docs access.

* * *

## 

​

1\. Skills — Teach Your Agent CrewAI

**Skills** are instruction packs that give coding agents deep CrewAI knowledge — how to scaffold Flows, configure Crews, use tools, and follow framework conventions.

  * Claude Code (Plugin Marketplace)

  * npx (Any Agent)

![Anthropic](https://cdn.simpleicons.org/anthropic/D97706)CrewAI skills are available in the **Claude Code plugin marketplace** — the same distribution channel used by top AI-native companies:
    
    
    /plugin marketplace add crewAIInc/skills
    /plugin install crewai-skills@crewai-plugins
    /reload-plugins
    

Four skills activate automatically when you ask relevant CrewAI questions:

Skill| When it runs  
---|---  
`getting-started`| Scaffolding new projects, choosing between `LLM.call()` / `Agent` / `Crew` / `Flow`, wiring `crew.py` / `main.py`  
`design-agent`| Configuring agents — role, goal, backstory, tools, LLMs, memory, guardrails  
`design-task`| Writing task descriptions, dependencies, structured output (`output_pydantic`, `output_json`), human review  
`ask-docs`| Querying the live [CrewAI docs MCP server](https://docs.crewai.com/mcp) for up-to-date API details  
  
Works with Claude Code, Codex, Cursor, Gemini CLI, or any coding agent:
    
    
    npx skills add crewaiinc/skills
    

Pulls from the [skills.sh registry](https://skills.sh/crewaiinc/skills).

1

Install the official skill pack

Use either method above — the Claude Code plugin marketplace or `npx skills add`. Both install the official [crewAIInc/skills](https://github.com/crewAIInc/skills) pack.

2

Your agent gets instant CrewAI expertise

The skill pack teaches your agent:

  * **Flows** — stateful apps, steps, and crew kickoffs
  * **Crews & Agents** — YAML-first patterns, roles, tasks, delegation
  * **Tools & Integrations** — search, APIs, MCP servers, and common CrewAI tools
  * **Project layout** — CLI scaffolds and repo conventions
  * **Up-to-date patterns** — tracks current CrewAI docs and best practices

3

Start building

Your agent can now scaffold and build CrewAI projects without you re-explaining the framework each session.

## Skills concept

How skills work in CrewAI agents — injection, activation, and patterns.

## Skills landing page

Overview of the crewAIInc/skills pack and what it includes.

## AGENTS.md & coding tools

Set up AGENTS.md for Claude Code, Codex, Cursor, and Gemini CLI.

## Skills registry (skills.sh)

Official listing — skills, install stats, and audits.

* * *

## 

​

2\. llms.txt — Machine-Readable Docs

CrewAI publishes an `llms.txt` file that gives AI assistants direct access to the full documentation in a machine-readable format.
    
    
    https://docs.crewai.com/llms.txt
    

  * What is llms.txt?

  * How to use it

  * Why it matters

[`llms.txt`](https://llmstxt.org/) is an emerging standard for making documentation consumable by large language models. Instead of scraping HTML, your agent can fetch a single structured text file with all the content it needs.CrewAI’s `llms.txt` is **already live** — your agent can use it right now.

Point your coding agent at the URL when it needs CrewAI reference docs:
    
    
    Fetch https://docs.crewai.com/llms.txt for CrewAI documentation.
    

Many coding agents (Claude Code, Cursor, etc.) can fetch URLs directly. The file contains structured documentation covering all CrewAI concepts, APIs, and guides.

  * **No scraping required** — clean, structured content in one request
  * **Always up-to-date** — served directly from docs.crewai.com
  * **Optimized for LLMs** — formatted for context windows, not browsers
  * **Complements skills** — skills teach patterns, llms.txt provides reference

* * *

## 

​

3\. Deploy to Enterprise

Go from a local crew to production on **CrewAI AMP** (Agent Management Platform) in minutes.

1

Build locally

Scaffold and test your crew or flow:
    
    
    crewai create crew my_crew
    cd my_crew
    crewai run
    

2

Prepare for deployment

Ensure your project structure is ready:
    
    
    crewai deploy --prepare
    

See the [preparation guide](/en/enterprise/guides/prepare-for-deployment) for details on project structure and requirements.

3

Deploy to AMP

Push to the CrewAI AMP platform:
    
    
    crewai deploy
    

You can also deploy via [GitHub integration](/en/enterprise/guides/deploy-to-amp) or [Crew Studio](/en/enterprise/guides/enable-crew-studio).

4

Access via API

Your deployed crew gets a REST API endpoint. Integrate it into any application:
    
    
    curl -X POST https://app.crewai.com/api/v1/crews/<crew-id>/kickoff \
      -H "Authorization: Bearer $CREWAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"inputs": {"topic": "AI agents"}}'
    

## Deploy to AMP

Full deployment guide — CLI, GitHub, and Crew Studio methods.

## AMP introduction

Platform overview — what AMP provides for production crews.

* * *

## 

​

4\. Enterprise Features

CrewAI AMP is built for production teams. Here’s what you get beyond deployment.

## Observability

Detailed execution traces, logs, and performance metrics for every crew run. Monitor agent decisions, tool calls, and task completion in real time.

## Crew Studio

No-code/low-code interface to create, customize, and deploy crews visually — then export to code or deploy directly.

## Webhook Streaming

Stream real-time events from crew executions to your systems. Integrate with Slack, Zapier, or any webhook consumer.

## Team Management

SSO, RBAC, and organization-level controls. Manage who can create, deploy, and access crews across your team.

## Tool Repository

Publish and share custom tools across your organization. Install community tools from the registry.

## Factory (Self-Hosted)

Run CrewAI AMP on your own infrastructure. Full platform capabilities with data residency and compliance controls.

Who is AMP for?

AMP is for teams that need to move AI agent workflows from prototypes to production — with observability, access controls, and scalable infrastructure. Whether you’re a startup or enterprise, AMP handles the operational complexity so you can focus on building agents.

What deployment options are available?

  * **Cloud (app.crewai.com)** — managed by CrewAI, fastest path to production
  * **Factory (self-hosted)** — run on your own infrastructure for full data control
  * **Hybrid** — mix cloud and self-hosted based on sensitivity requirements

## Explore CrewAI AMP →

Sign up and deploy your first crew to production.

Was this page helpful?

YesNo

[IntroductionPrevious](/en/introduction)[SkillsNext](/en/skills)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)