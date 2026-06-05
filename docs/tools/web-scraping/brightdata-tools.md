# Source: https://docs.crewai.com/en/tools/web-scraping/brightdata-tools

Web Scraping & Browsing

# Bright Data Tools


Bright Data integrations for SERP search, Web Unlocker scraping, and Dataset API.


# 

​

Bright Data Tools

This set of tools integrates Bright Data services for web extraction.

## 

​

Installation
    
    
    uv add crewai-tools requests aiohttp
    

## 

​

Environment Variables

  * `BRIGHT_DATA_API_KEY` (required)
  * `BRIGHT_DATA_ZONE` (for SERP/Web Unlocker)

Create credentials at <https://brightdata.com/> (sign up, then create an API token and zone). See their docs: <https://developers.brightdata.com/>

## 

​

Included Tools

  * `BrightDataSearchTool`: SERP search (Google/Bing/Yandex) with geo/language/device options.
  * `BrightDataWebUnlockerTool`: Scrape pages with anti-bot bypass and rendering.
  * `BrightDataDatasetTool`: Run Dataset API jobs and fetch results.

## 

​

Examples

### 

​

SERP Search

Code
    
    
    from crewai_tools import BrightDataSearchTool
    
    tool = BrightDataSearchTool(
        query="CrewAI", 
        country="us",
    )
    
    print(tool.run())
    

### 

​

Web Unlocker

Code
    
    
    from crewai_tools import BrightDataWebUnlockerTool
    
    tool = BrightDataWebUnlockerTool(
        url="https://example.com", 
        format="markdown",
    )
    
    print(tool.run(url="https://example.com"))
    

### 

​

Dataset API

Code
    
    
    from crewai_tools import BrightDataDatasetTool
    
    tool = BrightDataDatasetTool(
        dataset_type="ecommerce", 
        url="https://example.com/product",
    )
    
    print(tool.run())
    

## 

​

Troubleshooting

  * 401/403: verify `BRIGHT_DATA_API_KEY` and `BRIGHT_DATA_ZONE`.
  * Empty/blocked content: enable rendering or try a different zone.

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import BrightDataSearchTool
    
    tool = BrightDataSearchTool(
        query="CrewAI", 
        country="us",
    )
    
    agent = Agent(
        role="Web Researcher",
        goal="Search with Bright Data",
        backstory="Finds reliable results",
        tools=[tool],
        verbose=True,
    )
    
    task = Task(
        description="Search for CrewAI and summarize top results",
        expected_output="Short summary with links",
        agent=agent,
    )
    
    crew = Crew(
        agents=[agent], 
        tasks=[task],
        verbose=True,
    )
    
    result = crew.kickoff()
    

Was this page helpful?

YesNo

[Oxylabs ScrapersPrevious](/en/tools/web-scraping/oxylabsscraperstool)[You.com Content Extraction ToolNext](/en/tools/web-scraping/youai-contents)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)