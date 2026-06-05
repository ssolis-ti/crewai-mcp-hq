# Source: https://docs.crewai.com/en/tools/search-research/overview

Search & Research

# Overview


Perform web searches, find repositories, and research information across the internet


These tools enable your agents to search the web, research topics, and find information across various platforms including search engines, GitHub, and YouTube.

## 

​

**Available Tools**

## Serper Dev Tool

Google search API integration for comprehensive web search capabilities.

## Brave Search Tool

Privacy-focused search with Brave’s independent search index.

## Exa Search Tool

AI-powered search for finding specific and relevant content.

## LinkUp Search Tool

Real-time web search with fresh content indexing.

## GitHub Search Tool

Search GitHub repositories, code, issues, and documentation.

## Website Search Tool

Search within specific websites and domains.

## Code Docs Search Tool

Search through code documentation and technical resources.

## YouTube Channel Search

Search YouTube channels for specific content and creators.

## YouTube Video Search

Find and analyze YouTube videos by topic, keyword, or criteria.

## Tavily Search Tool

Comprehensive web search using Tavily’s AI-powered search API.

## Tavily Extractor Tool

Extract structured content from web pages using the Tavily API.

## Tavily Research Tool

Run multi-step research tasks and get cited reports using the Tavily Research API.

## Tavily Get Research Tool

Retrieve the status and results of an existing Tavily research task.

## Arxiv Paper Tool

Search arXiv and optionally download PDFs.

## SerpApi Google Search

Google search via SerpApi with structured results.

## SerpApi Google Shopping

Google Shopping queries via SerpApi.

## 

​

**Common Use Cases**

  * **Market Research** : Search for industry trends and competitor analysis
  * **Content Discovery** : Find relevant articles, videos, and resources
  * **Code Research** : Search repositories and documentation for solutions
  * **Lead Generation** : Research companies and individuals
  * **Academic Research** : Find scholarly articles and technical papers

    
    
    from crewai_tools import (
        GitHubSearchTool,
        SerperDevTool,
        TavilyExtractorTool,
        TavilyGetResearchTool,
        TavilyResearchTool,
        TavilySearchTool,
        YoutubeVideoSearchTool,
    )
    
    # Create research tools
    web_search = SerperDevTool()
    code_search = GitHubSearchTool()
    video_research = YoutubeVideoSearchTool()
    tavily_search = TavilySearchTool()
    content_extractor = TavilyExtractorTool()
    tavily_research = TavilyResearchTool()
    tavily_get_research = TavilyGetResearchTool()
    
    # Add to your agent
    agent = Agent(
        role="Research Analyst",
        tools=[
            web_search,
            code_search,
            video_research,
            tavily_search,
            content_extractor,
            tavily_research,
            tavily_get_research,
        ],
        goal="Gather comprehensive information on any topic"
    )
    

Was this page helpful?

YesNo

[You.com Content Extraction ToolPrevious](/en/tools/web-scraping/youai-contents)[Google Serper SearchNext](/en/tools/search-research/serperdevtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)