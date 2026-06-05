# Source: https://docs.crewai.com/en/tools/file-document/xmlsearchtool

File & Document

# XML RAG Search


The `XMLSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a XML file.


# 

​

`XMLSearchTool`

We are still working on improving tools, so there might be unexpected behavior or changes in the future.

## 

​

Description

The XMLSearchTool is a cutting-edge RAG tool engineered for conducting semantic searches within XML files. Ideal for users needing to parse and extract information from XML content efficiently, this tool supports inputting a search query and an optional XML file path. By specifying an XML path, users can target their search more precisely to the content of that file, thereby obtaining more relevant search outcomes.

## 

​

Installation

To start using the XMLSearchTool, you must first install the crewai_tools package. This can be easily done with the following command:
    
    
    pip install 'crewai[tools]'
    

## 

​

Example

Here are two examples demonstrating how to use the XMLSearchTool. The first example shows searching within a specific XML file, while the second example illustrates initiating a search without predefining an XML path, providing flexibility in search scope.

Code
    
    
    from crewai_tools import XMLSearchTool
    
    # Allow agents to search within any XML file's content 
    #as it learns about their paths during execution
    tool = XMLSearchTool()
    
    # OR
    
    # Initialize the tool with a specific XML file path 
    #for exclusive search within that document
    tool = XMLSearchTool(xml='path/to/your/xmlfile.xml')
    

## 

​

Arguments

  * `xml`: This is the path to the XML file you wish to search. It is an optional parameter during the tool’s initialization but must be provided either at initialization or as part of the `run` method’s arguments to execute a search.

## 

​

Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:

Code
    
    
    from chromadb.config import Settings
    
    tool = XMLSearchTool(
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

[MDX RAG SearchPrevious](/en/tools/file-document/mdxsearchtool)[TXT RAG SearchNext](/en/tools/file-document/txtsearchtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)