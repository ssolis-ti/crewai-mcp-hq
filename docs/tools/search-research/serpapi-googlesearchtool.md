# Source: https://docs.crewai.com/en/tools/search-research/serpapi-googlesearchtool

Search & Research

# SerpApi Google Search Tool


The `SerpApiGoogleSearchTool` performs Google searches using the SerpApi service.


# 

​

`SerpApiGoogleSearchTool`

## 

​

Description

Use the `SerpApiGoogleSearchTool` to run Google searches with SerpApi and retrieve structured results. Requires a SerpApi API key.

## 

​

Installation
    
    
    uv add crewai-tools[serpapi]
    

## 

​

Environment Variables

  * `SERPAPI_API_KEY` (required): API key for SerpApi. Create one at <https://serpapi.com/> (free tier available).

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import SerpApiGoogleSearchTool
    
    tool = SerpApiGoogleSearchTool()
    
    agent = Agent(
        role="Researcher",
        goal="Answer questions using Google search",
        backstory="Search specialist",
        tools=[tool],
        verbose=True,
    )
    
    task = Task(
        description="Search for the latest CrewAI releases",
        expected_output="A concise list of relevant results with titles and links",
        agent=agent,
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    

## 

​

Notes

  * Set `SERPAPI_API_KEY` in the environment. Create a key at <https://serpapi.com/>
  * See also Google Shopping via SerpApi: `/en/tools/search-research/serpapi-googleshoppingtool`

## 

​

Parameters

### 

​

Run Parameters

  * `search_query` (str, required): The Google query.
  * `location` (str, optional): Geographic location parameter.

## 

​

Notes

  * This tool wraps SerpApi and returns structured search results.

Was this page helpful?

YesNo

[Arxiv Paper ToolPrevious](/en/tools/search-research/arxivpapertool)[SerpApi Google Shopping ToolNext](/en/tools/search-research/serpapi-googleshoppingtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)