# Source: https://docs.crewai.com/en/concepts/agent-capabilities

Core Concepts

# Agent Capabilities


Understand the five ways to extend CrewAI agents: Tools, MCPs, Apps, Skills, and Knowledge.


## 

​

Overview

CrewAI agents can be extended with **five distinct capability types** , each serving a different purpose. Understanding when to use each one — and how they work together — is key to building effective agents.

## Tools

**Callable functions** — give agents the ability to take action. Web searches, file operations, API calls, code execution.

## MCP Servers

**Remote tool servers** — connect agents to external tool servers via the Model Context Protocol. Same effect as tools, but hosted externally.

## Apps

**Platform integrations** — connect agents to SaaS apps (Gmail, Slack, Jira, Salesforce) via CrewAI’s platform. Runs locally with a platform integration token.

## Skills

**Domain expertise** — inject instructions, guidelines, and reference material into agent prompts. Skills tell agents _how to think_.

## Knowledge

**Retrieved facts** — provide agents with data from documents, files, and URLs via semantic search (RAG). Knowledge gives agents _what to know_.

* * *

## 

​

The Key Distinction

The most important thing to understand: **these capabilities fall into two categories**.

### 

​

Action Capabilities (Tools, MCPs, Apps)

These give agents the ability to **do things** — call APIs, read files, search the web, send emails. At execution time, all three resolve into the same internal format (`BaseTool` instances) and appear in a unified tool list the agent can call.
    
    
    from crewai import Agent
    from crewai_tools import SerperDevTool, FileReadTool
    
    agent = Agent(
        role="Researcher",
        goal="Find and compile market data",
        backstory="Expert market analyst",
        tools=[SerperDevTool(), FileReadTool()],  # Local tools
        mcps=["https://mcp.example.com/sse"],     # Remote MCP server tools
        apps=["gmail", "google_sheets"],           # Platform integrations
    )
    

### 

​

Context Capabilities (Skills, Knowledge)

These modify the agent’s **prompt** — injecting expertise, instructions, or retrieved data before the agent starts reasoning. They don’t give agents new actions; they shape how agents think and what information they have access to.
    
    
    from crewai import Agent
    
    agent = Agent(
        role="Security Auditor",
        goal="Audit cloud infrastructure for vulnerabilities",
        backstory="Expert in cloud security with 10 years of experience",
        skills=["./skills/security-audit"],        # Domain instructions
        knowledge_sources=[pdf_source, url_source], # Retrieved facts
    )
    

* * *

## 

​

When to Use What

You need…| Use| Example  
---|---|---  
Agent to search the web| **Tools**| `tools=[SerperDevTool()]`  
Agent to call a remote API via MCP| **MCPs**| `mcps=["https://api.example.com/sse"]`  
Agent to send emails via Gmail| **Apps**| `apps=["gmail"]`  
Agent to follow specific procedures| **Skills**| `skills=["./skills/code-review"]`  
Agent to reference company docs| **Knowledge**| `knowledge_sources=[pdf_source]`  
Agent to search the web AND follow review guidelines| **Tools + Skills**|  Use both together  
  
* * *

## 

​

Combining Capabilities

In practice, agents often use **multiple capability types together**. Here’s a realistic example:
    
    
    from crewai import Agent
    from crewai_tools import SerperDevTool, FileReadTool, CodeInterpreterTool
    
    # A fully-equipped research agent
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Produce comprehensive market analysis reports",
        backstory="Expert analyst with deep industry knowledge",
    
        # ACTION: What the agent can DO
        tools=[
            SerperDevTool(),         # Search the web
            FileReadTool(),          # Read local files
            CodeInterpreterTool(),   # Run Python code for analysis
        ],
        mcps=["https://data-api.example.com/sse"],  # Access remote data API
        apps=["google_sheets"],                      # Write to Google Sheets
    
        # CONTEXT: What the agent KNOWS
        skills=["./skills/research-methodology"],    # How to conduct research
        knowledge_sources=[company_docs],            # Company-specific data
    )
    

* * *

## 

​

Comparison Table

Feature| Tools| MCPs| Apps| Skills| Knowledge  
---|---|---|---|---|---  
**Gives agent actions**|  ✅| ✅| ✅| ❌| ❌  
**Modifies prompt**|  ❌| ❌| ❌| ✅| ✅  
**Requires code**|  Yes| Config only| Config only| Markdown only| Config only  
**Runs locally**|  Yes| Depends| Yes (with env var)| N/A| Yes  
**Needs API keys**|  Per tool| Per server| Integration token| No| Embedder only  
**Set on Agent**| `tools=[]`| `mcps=[]`| `apps=[]`| `skills=[]`| `knowledge_sources=[]`  
**Set on Crew**|  ❌| ❌| ❌| `skills=[]`| `knowledge_sources=[]`  
  
* * *

## 

​

Deep Dives

Ready to learn more about each capability type?

## Tools

Create custom tools, use the 75+ OSS catalog, configure caching and async execution.

## MCP Integration

Connect to MCP servers via stdio, SSE, or HTTP. Filter tools, configure auth.

## Skills

Build skill packages with SKILL.md, inject domain expertise, use progressive disclosure.

## Knowledge

Add knowledge from PDFs, CSVs, URLs, and more. Configure embedders and retrieval.

Was this page helpful?

YesNo

[AgentsPrevious](/en/concepts/agents)[TasksNext](/en/concepts/tasks)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)