# Source: https://docs.crewai.com/en/tools/search-research/websitesearchtool

Search & Research

# Website RAG Search


The `WebsiteSearchTool` is designed to perform a RAG (Retrieval-Augmented Generation) search within the content of a website.


# 

​

`WebsiteSearchTool`

The WebsiteSearchTool is currently in an experimental phase. We are actively working on incorporating this tool into our suite of offerings and will update the documentation accordingly.

## 

​

Description

The WebsiteSearchTool is designed as a concept for conducting semantic searches within the content of websites. It aims to leverage advanced machine learning models like Retrieval-Augmented Generation (RAG) to navigate and extract information from specified URLs efficiently. This tool intends to offer flexibility, allowing users to perform searches across any website or focus on specific websites of interest. Please note, the current implementation details of the WebsiteSearchTool are under development, and its functionalities as described may not yet be accessible.

## 

​

Installation

To prepare your environment for when the WebsiteSearchTool becomes available, you can install the foundational package with:
    
    
    pip install 'crewai[tools]'
    

This command installs the necessary dependencies to ensure that once the tool is fully integrated, users can start using it immediately.

## 

​

Example Usage

Below are examples of how the WebsiteSearchTool could be utilized in different scenarios. Please note, these examples are illustrative and represent planned functionality:

Code
    
    
    from crewai_tools import WebsiteSearchTool
    
    # Example of initiating tool that agents can use 
    # to search across any discovered websites
    tool = WebsiteSearchTool()
    
    # Example of limiting the search to the content of a specific website, 
    # so now agents can only search within that website
    tool = WebsiteSearchTool(website='https://example.com')
    

## 

​

Arguments

  * `website`: An optional argument intended to specify the website URL for focused searches. This argument is designed to enhance the tool’s flexibility by allowing targeted searches when necessary.

## 

​

Customization Options

By default, the tool uses OpenAI for both embeddings and summarization. To customize the model, you can use a config dictionary as follows:

Code
    
    
    tool = WebsiteSearchTool(
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

[Github SearchPrevious](/en/tools/search-research/githubsearchtool)[Code Docs RAG SearchNext](/en/tools/search-research/codedocssearchtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)