# Source: https://docs.crewai.com/en/tools/search-research/tavilygetresearchtool

Search & Research

# Tavily Get Research Tool


Retrieve the status and results of an existing Tavily research task


The `TavilyGetResearchTool` lets CrewAI agents check an existing Tavily research task by `request_id`. Use it when a research task was started earlier and you need to retrieve its current status or final results. If you need to start a new research job, use the [Tavily Research Tool](/en/tools/search-research/tavilyresearchtool). This tool is specifically for looking up an existing Tavily research request after you already have its `request_id`.

## 

​

Installation

To use the `TavilyGetResearchTool`, install the `tavily-python` library alongside `crewai-tools`:
    
    
    uv add 'crewai[tools]' tavily-python
    

## 

​

Environment Variables

Set your Tavily API key:
    
    
    export TAVILY_API_KEY='your_tavily_api_key'
    

Get an API key at <https://app.tavily.com/> (sign up, then create a key).

## 

​

Example Usage
    
    
    from crewai_tools import TavilyGetResearchTool
    
    tavily_get_research_tool = TavilyGetResearchTool()
    
    status_result = tavily_get_research_tool.run(
        request_id="your-research-request-id"
    )
    
    print(status_result)
    

## 

​

Common Workflow

Use `TavilyGetResearchTool` when your application or another service has already created a Tavily research task and saved its `request_id`. Typical cases include:

  * Polling for completion after kicking off research in a background job.
  * Looking up the latest status of a long-running research task.
  * Fetching final research output from a previously created Tavily request.

## 

​

Configuration Options

The `TavilyGetResearchTool` accepts the following argument when calling the `run` method:

  * `request_id` (str): **Required.** The existing Tavily research request ID to retrieve.

## 

​

Async Usage

Use `_arun` when your application is already running inside an async event loop:
    
    
    from crewai_tools import TavilyGetResearchTool
    
    tavily_get_research_tool = TavilyGetResearchTool()
    
    status_result = await tavily_get_research_tool._arun(
        request_id="your-research-request-id"
    )
    

## 

​

Features

  * **Research status retrieval** : Fetch the current status of an existing Tavily research task.
  * **Result retrieval** : Return available research output once Tavily has completed the task.
  * **Sync and async** : Use either `_run`/`run` or `_arun` depending on your application’s runtime.
  * **JSON output** : Returns Tavily responses as formatted JSON strings.

## 

​

Response Format

The tool returns a JSON string containing the current research task status and any available results from Tavily. The exact response shape depends on the task state returned by Tavily, so incomplete tasks may return status information before the final research output is available. Refer to the [Tavily API documentation](https://docs.tavily.com/) for full details on the Research API.

Was this page helpful?

YesNo

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)