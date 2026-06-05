# Source: https://docs.crewai.com/en/tools/overview

Tools

# Tools Overview


Discover CrewAI’s extensive library of 40+ tools to supercharge your AI agents


CrewAI provides an extensive library of pre-built tools to enhance your agents’ capabilities. From file processing to web scraping, database queries to AI services - we’ve got you covered.

## 

​

**Tool Categories**

## File & Document

Read, write, and search through various file formats including PDF, DOCX, JSON, CSV, and more. Perfect for document processing workflows.

## Web Scraping & Browsing

Extract data from websites, automate browser interactions, and scrape content at scale with tools like Firecrawl, Selenium, and more.

## Search & Research

Perform web searches, find code repositories, research YouTube content, and discover information across the internet.

## Database & Data

Connect to SQL databases, vector stores, and data warehouses. Query MySQL, PostgreSQL, Snowflake, Qdrant, and Weaviate.

## AI & Machine Learning

Generate images with DALL-E, process vision tasks, integrate with LangChain, build RAG systems, and leverage code interpreters.

## Cloud & Storage

Interact with cloud services including AWS S3, Amazon Bedrock, and other cloud storage and AI services.

## Automation

Automate workflows with Apify, Composio, and other platforms to connect your agents with external services.

## Integrations

Integrate CrewAI with external systems like Amazon Bedrock and the CrewAI Automation toolkit.

## 

​

**Quick Access**

Need a specific tool? Here are some popular choices:

## RAG Tool

Implement Retrieval-Augmented Generation

## Serper Dev

Google search API

## File Read

Read any file type

## Scrape Website

Extract web content

## Code Interpreter

Execute Python code

## S3 Reader

Access AWS S3 files

## 

​

**Getting Started**

To use any tool in your CrewAI project:

  1. **Import** the tool in your crew configuration
  2. **Add** it to your agent’s tools list
  3. **Configure** any required API keys or settings

    
    
    from crewai_tools import FileReadTool, SerperDevTool
    
    # Add tools to your agent
    agent = Agent(
        role="Research Analyst",
        tools=[FileReadTool(), SerperDevTool()],
        # ... other configuration
    )
    

## 

​

**Max Usage Count**

You can set a maximum usage count for a tool to prevent it from being used more than a certain number of times. By default, the max usage count is unlimited.
    
    
    from crewai_tools import FileReadTool
    
    tool = FileReadTool(max_usage_count=5, ...)
    

Ready to explore? Pick a category above to discover tools that fit your use case!

Was this page helpful?

YesNo

[MCP Security ConsiderationsPrevious](/en/mcp/security)[OverviewNext](/en/tools/file-document/overview)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)