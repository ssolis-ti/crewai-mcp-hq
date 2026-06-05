# Source: https://docs.crewai.com/en/tools/web-scraping/scrapewebsitetool

Web Scraping & Browsing

# Scrape Website


The `ScrapeWebsiteTool` is designed to extract and read the content of a specified website.


# 

​

`ScrapeWebsiteTool`

We are still working on improving tools, so there might be unexpected behavior or changes in the future.

## 

​

Description

A tool designed to extract and read the content of a specified website. It is capable of handling various types of web pages by making HTTP requests and parsing the received HTML content. This tool can be particularly useful for web scraping tasks, data collection, or extracting specific information from websites.

## 

​

Installation

Install the crewai_tools package
    
    
    pip install 'crewai[tools]'
    

## 

​

Example
    
    
    from crewai_tools import ScrapeWebsiteTool
    
    # To enable scrapping any website it finds during it's execution
    tool = ScrapeWebsiteTool()
    
    # Initialize the tool with the website URL, 
    # so the agent can only scrap the content of the specified website
    tool = ScrapeWebsiteTool(website_url='https://www.example.com')
    
    # Extract the text from the site
    text = tool.run()
    print(text)
    

## 

​

Arguments

Argument| Type| Description  
---|---|---  
**website_url**| `string`| **Mandatory** website URL to read the file. This is the primary input for the tool, specifying which website’s content should be scraped and read.  
  
Was this page helpful?

YesNo

[OverviewPrevious](/en/tools/web-scraping/overview)[Scrape Element From Website ToolNext](/en/tools/web-scraping/scrapeelementfromwebsitetool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)