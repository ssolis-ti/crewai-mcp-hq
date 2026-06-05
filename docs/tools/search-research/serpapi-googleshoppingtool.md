# Source: https://docs.crewai.com/en/tools/search-research/serpapi-googleshoppingtool

Search & Research

# SerpApi Google Shopping Tool


The `SerpApiGoogleShoppingTool` searches Google Shopping results using SerpApi.


# 

​

`SerpApiGoogleShoppingTool`

## 

​

Description

Leverage `SerpApiGoogleShoppingTool` to query Google Shopping via SerpApi and retrieve product-oriented results.

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
    from crewai_tools import SerpApiGoogleShoppingTool
    
    tool = SerpApiGoogleShoppingTool()
    
    agent = Agent(
        role="Shopping Researcher",
        goal="Find relevant products",
        backstory="Expert in product search",
        tools=[tool],
        verbose=True,
    )
    
    task = Task(
        description="Search Google Shopping for 'wireless noise-canceling headphones'",
        expected_output="Top relevant products with titles and links",
        agent=agent,
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    

## 

​

Notes

  * Set `SERPAPI_API_KEY` in the environment. Create a key at <https://serpapi.com/>
  * See also Google Web Search via SerpApi: `/en/tools/search-research/serpapi-googlesearchtool`

## 

​

Parameters

### 

​

Run Parameters

  * `search_query` (str, required): Product search query.
  * `location` (str, optional): Geographic location parameter.

Was this page helpful?

YesNo

[SerpApi Google Search ToolPrevious](/en/tools/search-research/serpapi-googlesearchtool)[Databricks SQL Query ToolNext](/en/tools/search-research/databricks-query-tool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)