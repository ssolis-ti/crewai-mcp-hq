# Source: https://docs.crewai.com/en/tools/file-document/txtsearchtool

File & Document

# TXT RAG Search


The `TXTSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a text file.


## 

​

Overview

We are still working on improving tools, so there might be unexpected behavior or changes in the future.

This tool is used to perform a RAG (Retrieval-Augmented Generation) search within the content of a text file. It allows for semantic searching of a query within a specified text file’s content, making it an invaluable resource for quickly extracting information or finding specific sections of text based on the query provided.

## 

​

Installation

To use the `TXTSearchTool`, you first need to install the `crewai_tools` package. This can be done using pip, a package manager for Python. Open your terminal or command prompt and enter the following command:
    
    
    pip install 'crewai[tools]'
    

This command will download and install the TXTSearchTool along with any necessary dependencies.

## 

​

Example

The following example demonstrates how to use the TXTSearchTool to search within a text file. This example shows both the initialization of the tool with a specific text file and the subsequent search within that file’s content.

Code
    
    
    from crewai_tools import TXTSearchTool
    
    # Initialize the tool to search within any text file's content 
    # the agent learns about during its execution
    tool = TXTSearchTool()
    
    # OR
    
    # Initialize the tool with a specific text file, 
    # so the agent can search within the given text file's content
    tool = TXTSearchTool(txt='path/to/text/file.txt')
    

## 

​

Arguments

  * `txt` (str): **Optional**. The path to the text file you want to search. This argument is only required if the tool was not initialized with a specific text file; otherwise, the search will be conducted within the initially provided text file.

## 

​

Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:

Code
    
    
    from chromadb.config import Settings
    
    tool = TXTSearchTool(
        config={
            # Required: embeddings provider + config
            "embedding_model": {
                "provider": "openai",  # or google-generativeai, cohere, ollama, ...
                "config": {
                    "model": "text-embedding-3-small",
                    # "api_key": "sk-...",  # optional if env var is set (e.g., OPENAI_API_KEY or EMBEDDINGS_OPENAI_API_KEY)
                    # Provider examples:
                    # Google → model_name: "gemini-embedding-001", task_type: "RETRIEVAL_DOCUMENT"
                    # Cohere → model: "embed-english-v3.0"
                    # Ollama → model: "nomic-embed-text"
                },
            },
    
            # Required: vector database config
            "vectordb": {
                "provider": "chromadb",  # or "qdrant"
                "config": {
                    # Chroma settings (optional persistence)
                    # "settings": Settings(
                    #     persist_directory="/content/chroma",
                    #     allow_reset=True,
                    #     is_persistent=True,
                    # ),
    
                    # Qdrant vector params example:
                    # from qdrant_client.models import VectorParams, Distance
                    # "vectors_config": VectorParams(size=384, distance=Distance.COSINE),
    
                    # Note: collection name is controlled by the tool (default: "rag_tool_collection").
                }
            },
        }
    )
    

Was this page helpful?

YesNo

[XML RAG SearchPrevious](/en/tools/file-document/xmlsearchtool)[JSON RAG SearchNext](/en/tools/file-document/jsonsearchtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)