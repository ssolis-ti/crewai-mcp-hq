# Source: https://docs.crewai.com/en/tools/search-research/tavilyresearchtool

Search & Research

# Tavily Research Tool


Run multi-step research tasks and get cited reports using the Tavily Research API


The `TavilyResearchTool` lets CrewAI agents kick off Tavily research tasks, returning a synthesized, cited report (or a stream of progress events) instead of raw search results. Use it when an agent needs an investigative answer rather than a single web search.

## 

​

Installation

To use the `TavilyResearchTool`, install the `tavily-python` library alongside `crewai-tools`:
    
    
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
    
    
    import os
    from crewai import Agent, Crew, Task
    from crewai_tools import TavilyResearchTool
    
    # Ensure TAVILY_API_KEY is set in your environment
    # os.environ["TAVILY_API_KEY"] = "YOUR_API_KEY"
    
    tavily_tool = TavilyResearchTool()
    
    researcher = Agent(
        role="Research Analyst",
        goal="Investigate questions and produce concise, well-cited briefings.",
        backstory=(
            "You are a meticulous analyst who delegates web research to the Tavily "
            "Research tool, then synthesizes the findings into short briefings."
        ),
        tools=[tavily_tool],
        verbose=True,
    )
    
    research_task = Task(
        description=(
            "Investigate notable open-source agent orchestration frameworks released "
            "in the last six months and summarize their differentiators."
        ),
        expected_output="A bulleted briefing with citations.",
        agent=researcher,
    )
    
    crew = Crew(agents=[researcher], tasks=[research_task])
    print(crew.kickoff())
    

## 

​

Configuration Options

The `TavilyResearchTool` accepts the following arguments — all can be set on the tool instance (defaults for every call) or per-call via the agent’s tool input:

  * `input` (str): **Required.** The research task or question to investigate.
  * `model` (Literal[“mini”, “pro”, “auto”]): The Tavily research model. `"auto"` lets Tavily pick; `"mini"` is faster/cheaper; `"pro"` is the most capable. Defaults to `"auto"`.
  * `output_schema` (dict | None): Optional JSON Schema that structures the research output. Useful when you want strictly typed results.
  * `stream` (bool): When `True`, the tool returns an iterator of SSE chunks emitting research progress and the final result instead of a single string. Defaults to `False`.
  * `citation_format` (Literal[“numbered”, “mla”, “apa”, “chicago”]): Citation format for the report. Defaults to `"numbered"`.

## 

​

Advanced Usage

### 

​

Configure defaults on the tool instance
    
    
    from crewai_tools import TavilyResearchTool
    
    tavily_tool = TavilyResearchTool(
        model="pro",                # use Tavily's most capable research model
        citation_format="apa",      # APA-style citations
    )
    

### 

​

Stream research progress

When `stream=True`, the tool returns a generator (or async generator from `_arun`) of SSE chunks so your application can surface incremental progress:
    
    
    tavily_tool = TavilyResearchTool(stream=True)
    
    for chunk in tavily_tool.run(input="Summarize recent advances in retrieval-augmented generation."):
        print(chunk)
    

### 

​

Structured output via JSON Schema

Pass an `output_schema` when you need a typed result instead of a free-form report:
    
    
    output_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "key_points": {"type": "array", "items": {"type": "string"}},
            "sources": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["summary", "key_points", "sources"],
    }
    
    tavily_tool = TavilyResearchTool(output_schema=output_schema)
    

## 

​

Features

  * **End-to-end research** : Returns a synthesized, cited report rather than raw search hits.
  * **Model selection** : Trade off cost, speed, and depth via `mini`, `pro`, or `auto`.
  * **Streaming** : Stream incremental progress and results as SSE chunks for responsive UIs.
  * **Structured output** : Coerce results to a JSON Schema you define.
  * **Multiple citation styles** : Choose from numbered, MLA, APA, or Chicago citations.
  * **Sync and async** : Use either `_run` or `_arun` depending on your application’s runtime.

Refer to the [Tavily API documentation](https://docs.tavily.com/) for full details on the Research API.

Was this page helpful?

YesNo

[Tavily Extractor ToolPrevious](/en/tools/search-research/tavilyextractortool)[Arxiv Paper ToolNext](/en/tools/search-research/arxivpapertool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)