# Source: https://docs.crewai.com/en/tools/web-scraping/firecrawlscrapewebsitetool

Web Scraping & Browsing

# Firecrawl Scrape Website


The `FirecrawlScrapeWebsiteTool` is designed to scrape websites and convert them into clean markdown or structured data.


# 

​

`FirecrawlScrapeWebsiteTool`

## 

​

Description

[Firecrawl](https://firecrawl.dev) is a platform for crawling and convert any website into clean markdown or structured data.

## 

​

Installation

  * Get an API key from [firecrawl.dev](https://firecrawl.dev) and set it in environment variables (`FIRECRAWL_API_KEY`).
  * Install the [Firecrawl SDK](https://github.com/mendableai/firecrawl) along with `crewai[tools]` package:

    
    
    pip install firecrawl-py 'crewai[tools]'
    

## 

​

Example

Utilize the FirecrawlScrapeWebsiteTool as follows to allow your agent to load websites:

Code
    
    
    from crewai_tools import FirecrawlScrapeWebsiteTool
    
    tool = FirecrawlScrapeWebsiteTool(url='firecrawl.dev')
    

## 

​

Arguments

  * `api_key`: Optional. Specifies Firecrawl API key. Defaults is the `FIRECRAWL_API_KEY` environment variable.
  * `url`: The URL to scrape.
  * `page_options`: Optional.
    * `onlyMainContent`: Optional. Only return the main content of the page excluding headers, navs, footers, etc.
    * `includeHtml`: Optional. Include the raw HTML content of the page. Will output a html key in the response.
  * `extractor_options`: Optional. Options for LLM-based extraction of structured information from the page content
    * `mode`: The extraction mode to use, currently supports ‘llm-extraction’
    * `extractionPrompt`: Optional. A prompt describing what information to extract from the page
    * `extractionSchema`: Optional. The schema for the data to be extracted
  * `timeout`: Optional. Timeout in milliseconds for the request

Was this page helpful?

YesNo

[Firecrawl Crawl WebsitePrevious](/en/tools/web-scraping/firecrawlcrawlwebsitetool)[Oxylabs ScrapersNext](/en/tools/web-scraping/oxylabsscraperstool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)