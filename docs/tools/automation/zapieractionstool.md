# Source: https://docs.crewai.com/en/tools/automation/zapieractionstool

Automation

# Zapier Actions Tool


The `ZapierActionsAdapter` exposes Zapier actions as CrewAI tools for automation.


# 

​

`ZapierActionsAdapter`

## 

​

Description

Use the Zapier adapter to list and call Zapier actions as CrewAI tools. This enables agents to trigger automations across thousands of apps.

## 

​

Installation

This adapter is included with `crewai-tools`. No extra install required.

## 

​

Environment Variables

  * `ZAPIER_API_KEY` (required): Zapier API key. Get one from the Zapier Actions dashboard at <https://actions.zapier.com/> (create an account, then generate an API key). You can also pass `zapier_api_key` directly when constructing the adapter.

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools.adapters.zapier_adapter import ZapierActionsAdapter
    
    adapter = ZapierActionsAdapter(api_key="your_zapier_api_key")
    tools = adapter.tools()
    
    agent = Agent(
        role="Automator",
        goal="Execute Zapier actions",
        backstory="Automation specialist",
        tools=tools,
        verbose=True,
    )
    
    task = Task(
        description="Create a new Google Sheet and add a row using Zapier actions",
        expected_output="Confirmation with created resource IDs",
        agent=agent,
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    

## 

​

Notes & limits

  * The adapter lists available actions for your key and creates `BaseTool` wrappers dynamically.
  * Handle action‑specific required fields in your task instructions or tool call.
  * Rate limits depend on your Zapier plan; see the Zapier Actions docs.

## 

​

Notes

  * The adapter fetches available actions and generates `BaseTool` wrappers dynamically.

Was this page helpful?

YesNo

[MultiOn ToolPrevious](/en/tools/automation/multiontool)[CrewAI TracingNext](/en/observability/tracing)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)