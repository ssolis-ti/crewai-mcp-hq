# Source: https://docs.crewai.com/en/tools/web-scraping/browserbaseloadtool

Web Scraping & Browsing

# Browserbase Web Loader


Browserbase is a developer platform to reliably run, manage, and monitor headless browsers.


# 

​

`BrowserbaseLoadTool`

## 

​

Description

[Browserbase](https://browserbase.com) is a developer platform to reliably run, manage, and monitor headless browsers. Power your AI data retrievals with:

  * [Serverless Infrastructure](https://docs.browserbase.com/under-the-hood) providing reliable browsers to extract data from complex UIs
  * [Stealth Mode](https://docs.browserbase.com/features/stealth-mode) with included fingerprinting tactics and automatic captcha solving
  * [Session Debugger](https://docs.browserbase.com/features/sessions) to inspect your Browser Session with networks timeline and logs
  * [Live Debug](https://docs.browserbase.com/guides/session-debug-connection/browser-remote-control) to quickly debug your automation

## 

​

Installation

  * Get an API key and Project ID from [browserbase.com](https://browserbase.com) and set it in environment variables (`BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`).
  * Install the [Browserbase SDK](http://github.com/browserbase/python-sdk) along with `crewai[tools]` package:

    
    
    pip install browserbase 'crewai[tools]'
    

## 

​

Example

Utilize the BrowserbaseLoadTool as follows to allow your agent to load websites:

Code
    
    
    from crewai_tools import BrowserbaseLoadTool
    
    # Initialize the tool with the Browserbase API key and Project ID
    tool = BrowserbaseLoadTool()
    

## 

​

Arguments

The following parameters can be used to customize the `BrowserbaseLoadTool`’s behavior:

Argument| Type| Description  
---|---|---  
**api_key**| `string`|  _Optional_. Browserbase API key. Default is `BROWSERBASE_API_KEY` env variable.  
**project_id**| `string`|  _Optional_. Browserbase Project ID. Default is `BROWSERBASE_PROJECT_ID` env variable.  
**text_content**| `bool`|  _Optional_. Retrieve only text content. Default is `False`.  
**session_id**| `string`|  _Optional_. Provide an existing Session ID.  
**proxy**| `bool`|  _Optional_. Enable/Disable Proxies. Default is `False`.  
  
Was this page helpful?

YesNo

[Spider ScraperPrevious](/en/tools/web-scraping/spidertool)[Hyperbrowser Load ToolNext](/en/tools/web-scraping/hyperbrowserloadtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)