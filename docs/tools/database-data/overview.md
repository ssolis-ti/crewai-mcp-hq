# Source: https://docs.crewai.com/en/tools/database-data/overview

Database & Data

# Overview


Connect to databases, vector stores, and data warehouses for comprehensive data access


These tools enable your agents to interact with various database systems, from traditional SQL databases to modern vector stores and data warehouses.

## 

​

**Available Tools**

## MySQL Tool

Connect to and query MySQL databases with SQL operations.

## PostgreSQL Search

Search and query PostgreSQL databases efficiently.

## Snowflake Search

Access Snowflake data warehouse for analytics and reporting.

## NL2SQL Tool

Convert natural language queries to SQL statements automatically.

## Qdrant Vector Search

Search vector embeddings using Qdrant vector database.

## Weaviate Vector Search

Perform semantic search with Weaviate vector database.

## MongoDB Vector Search

Vector similarity search on MongoDB Atlas with indexing helpers.

## SingleStore Search

Safe SELECT/SHOW queries on SingleStore with pooling and validation.

## 

​

**Common Use Cases**

  * **Data Analysis** : Query databases for business intelligence and reporting
  * **Vector Search** : Find similar content using semantic embeddings
  * **ETL Operations** : Extract, transform, and load data between systems
  * **Real-time Analytics** : Access live data for decision making

    
    
    from crewai_tools import MySQLTool, QdrantVectorSearchTool, NL2SQLTool
    
    # Create database tools
    mysql_db = MySQLTool()
    vector_search = QdrantVectorSearchTool()
    nl_to_sql = NL2SQLTool()
    
    # Add to your agent
    agent = Agent(
        role="Data Analyst",
        tools=[mysql_db, vector_search, nl_to_sql],
        goal="Extract insights from various data sources"
    )
    

Was this page helpful?

YesNo

[You.com Search & Research ToolsPrevious](/en/tools/search-research/youai-search)[MySQL RAG SearchNext](/en/tools/database-data/mysqltool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)