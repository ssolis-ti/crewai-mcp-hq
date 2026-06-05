# Source: https://docs.crewai.com/en/tools/search-research/databricks-query-tool

Search & Research

# Databricks SQL Query Tool


The `DatabricksQueryTool` executes SQL queries against Databricks workspace tables.


# 

​

`DatabricksQueryTool`

## 

​

Description

Run SQL against Databricks workspace tables with either CLI profile or direct host/token authentication.

## 

​

Installation
    
    
    uv add crewai-tools[databricks-sdk]
    

## 

​

Environment Variables

  * `DATABRICKS_CONFIG_PROFILE` or (`DATABRICKS_HOST` \+ `DATABRICKS_TOKEN`)

Create a personal access token and find host details in the Databricks workspace under User Settings → Developer. Docs: <https://docs.databricks.com/en/dev-tools/auth/pat.html>

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import DatabricksQueryTool
    
    tool = DatabricksQueryTool(
        default_catalog="main", 
        default_schema="default",
    )
    
    agent = Agent(
        role="Data Analyst",
        goal="Query Databricks",
        tools=[tool],
        verbose=True,
    )
    
    task = Task(
        description="SELECT * FROM my_table LIMIT 10",
        expected_output="10 rows", 
        agent=agent,
    )
    
    crew = Crew(
        agents=[agent], 
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff()
    
    print(result)
    

## 

​

Parameters

  * `query` (required): SQL query to execute
  * `catalog` (optional): Override default catalog
  * `db_schema` (optional): Override default schema
  * `warehouse_id` (optional): Override default SQL warehouse
  * `row_limit` (optional): Maximum rows to return (default: 1000)

## 

​

Defaults on initialization

  * `default_catalog`
  * `default_schema`
  * `default_warehouse_id`

### 

​

Error handling & tips

  * Authentication errors: verify `DATABRICKS_HOST` begins with `https://` and token is valid.
  * Permissions: ensure your SQL warehouse and schema are accessible by your token.
  * Limits: long‑running queries should be avoided in agent loops; add filters/limits.

Was this page helpful?

YesNo

[SerpApi Google Shopping ToolPrevious](/en/tools/search-research/serpapi-googleshoppingtool)[You.com Search & Research ToolsNext](/en/tools/search-research/youai-search)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)