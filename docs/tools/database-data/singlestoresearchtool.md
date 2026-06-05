# Source: https://docs.crewai.com/en/tools/database-data/singlestoresearchtool

Database & Data

# SingleStore Search Tool


The `SingleStoreSearchTool` safely executes SELECT/SHOW queries on SingleStore with pooling.


# 

​

`SingleStoreSearchTool`

## 

​

Description

Execute read‑only queries (`SELECT`/`SHOW`) against SingleStore with connection pooling and input validation.

## 

​

Installation
    
    
    uv add crewai-tools[singlestore]
    

## 

​

Environment Variables

Variables like `SINGLESTOREDB_HOST`, `SINGLESTOREDB_USER`, `SINGLESTOREDB_PASSWORD`, etc., can be used, or `SINGLESTOREDB_URL` as a single DSN. Generate the API key from the SingleStore dashboard, [docs here](https://docs.singlestore.com/cloud/reference/management-api/#generate-an-api-key).

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import SingleStoreSearchTool
    
    tool = SingleStoreSearchTool(
        tables=["products"], 
        host="host", 
        user="user", 
        password="pass", 
        database="db",
    )
    
    agent = Agent(
        role="Analyst", 
        goal="Query SingleStore", 
        tools=[tool], 
        verbose=True,
    )
    
    task = Task(
        description="List 5 products", 
        expected_output="5 rows as JSON/text", 
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

[MongoDB Vector Search ToolPrevious](/en/tools/database-data/mongodbvectorsearchtool)[OverviewNext](/en/tools/ai-ml/overview)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)