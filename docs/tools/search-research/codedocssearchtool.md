# Source: https://docs.crewai.com/en/tools/search-research/codedocssearchtool

Search & Research

# Code Docs RAG Search


The `CodeDocsSearchTool` is a powerful RAG (Retrieval-Augmented Generation) tool designed for semantic searches within code documentation.


# 

​

`CodeDocsSearchTool`

**Experimental** : We are still working on improving tools, so there might be unexpected behavior or changes in the future.

## 

​

Description

The CodeDocsSearchTool is a powerful RAG (Retrieval-Augmented Generation) tool designed for semantic searches within code documentation. It enables users to efficiently find specific information or topics within code documentation. By providing a `docs_url` during initialization, the tool narrows down the search to that particular documentation site. Alternatively, without a specific `docs_url`, it searches across a wide array of code documentation known or discovered throughout its execution, making it versatile for various documentation search needs.

## 

​

Installation

To start using the CodeDocsSearchTool, first, install the crewai_tools package via pip:
    
    
    pip install 'crewai[tools]'
    

## 

​

Example

Utilize the CodeDocsSearchTool as follows to conduct searches within code documentation:

Code
    
    
    from crewai_tools import CodeDocsSearchTool
    
    # To search any code documentation content 
    # if the URL is known or discovered during its execution:
    tool = CodeDocsSearchTool()
    
    # OR
    
    # To specifically focus your search on a given documentation site 
    # by providing its URL:
    tool = CodeDocsSearchTool(docs_url='https://docs.example.com/reference')
    

Substitute ‘<https://docs.example.com/reference>’ with your target documentation URL and ‘How to use search tool’ with the search query relevant to your needs.

## 

​

Arguments

The following parameters can be used to customize the `CodeDocsSearchTool`’s behavior:

Argument| Type| Description  
---|---|---  
**docs_url**| `string`|  _Optional_. Specifies the URL of the code documentation to be searched.  
  
## 

​

Custom model and embeddings

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:

Code
    
    
    tool = CodeDocsSearchTool(
        config=dict(
            llm=dict(
                provider="ollama", # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="llama2",
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="google-generativeai", # or openai, ollama, ...
                config=dict(
                    model_name="gemini-embedding-001",
                    task_type="RETRIEVAL_DOCUMENT",
                    # title="Embeddings",
                ),
            ),
        )
    )
    

Was this page helpful?

YesNo

[Website RAG SearchPrevious](/en/tools/search-research/websitesearchtool)[YouTube Channel RAG SearchNext](/en/tools/search-research/youtubechannelsearchtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)