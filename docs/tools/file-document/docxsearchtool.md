# Source: https://docs.crewai.com/en/tools/file-document/docxsearchtool

File & Document

# DOCX RAG Search


The `DOCXSearchTool` is a RAG tool designed for semantic searching within DOCX documents.


# 

​

`DOCXSearchTool`

We are still working on improving tools, so there might be unexpected behavior or changes in the future.

## 

​

Description

The `DOCXSearchTool` is a RAG tool designed for semantic searching within DOCX documents. It enables users to effectively search and extract relevant information from DOCX files using query-based searches. This tool is invaluable for data analysis, information management, and research tasks, streamlining the process of finding specific information within large document collections.

## 

​

Installation

Install the crewai_tools package by running the following command in your terminal:
    
    
    uv pip install docx2txt 'crewai[tools]'
    

## 

​

Example

The following example demonstrates initializing the DOCXSearchTool to search within any DOCX file’s content or with a specific DOCX file path.

Code
    
    
    from crewai_tools import DOCXSearchTool
    
    # Initialize the tool to search within any DOCX file's content
    tool = DOCXSearchTool()
    
    # OR
    
    # Initialize the tool with a specific DOCX file, 
    # so the agent can only search the content of the specified DOCX file
    tool = DOCXSearchTool(docx='path/to/your/document.docx')
    

## 

​

Arguments

The following parameters can be used to customize the `DOCXSearchTool`’s behavior:

Argument| Type| Description  
---|---|---  
**docx**| `string`|  _Optional_. An argument that specifies the path to the DOCX file you want to search. If not provided during initialization, the tool allows for later specification of any DOCX file’s content path for searching.  
  
## 

​

Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:

Code
    
    
    from chromadb.config import Settings
    
    tool = DOCXSearchTool(
        config={
            "embedding_model": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small",
                    # "api_key": "sk-...",
                },
            },
            "vectordb": {
                "provider": "chromadb",  # or "qdrant"
                "config": {
                    # "settings": Settings(persist_directory="/content/chroma", allow_reset=True, is_persistent=True),
                    # from qdrant_client.models import VectorParams, Distance
                    # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),
                }
            },
        }
    )
    

Was this page helpful?

YesNo

[PDF RAG SearchPrevious](/en/tools/file-document/pdfsearchtool)[MDX RAG SearchNext](/en/tools/file-document/mdxsearchtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)