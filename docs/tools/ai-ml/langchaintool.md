# Source: https://docs.crewai.com/en/tools/ai-ml/langchaintool

AI & Machine Learning

# LangChain Tool


The `LangChainTool` is a wrapper for LangChain tools and query engines.


## 

​

`LangChainTool`

CrewAI seamlessly integrates with LangChain’s comprehensive [list of tools](https://python.langchain.com/docs/integrations/tools/), all of which can be used with CrewAI.

Code
    
    
    import os
    from dotenv import load_dotenv
    from crewai import Agent, Task, Crew
    from crewai.tools import BaseTool
    from pydantic import Field
    from langchain_community.utilities import GoogleSerperAPIWrapper
    
    # Set up your SERPER_API_KEY key in an .env file, eg:
    # SERPER_API_KEY=<your api key>
    load_dotenv()
    
    search = GoogleSerperAPIWrapper()
    
    class SearchTool(BaseTool):
        name: str = "Search"
        description: str = "Useful for search-based queries. Use this to find current information about markets, companies, and trends."
        search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper)
    
        def _run(self, query: str) -> str:
            """Execute the search query and return results"""
            try:
                return self.search.run(query)
            except Exception as e:
                return f"Error performing search: {str(e)}"
    
    # Create Agents
    researcher = Agent(
        role='Research Analyst',
        goal='Gather current market data and trends',
        backstory="""You are an expert research analyst with years of experience in
        gathering market intelligence. You're known for your ability to find
        relevant and up-to-date market information and present it in a clear,
        actionable format.""",
        tools=[SearchTool()],
        verbose=True
    )
    
    # rest of the code ...
    

## 

​

Conclusion

Tools are pivotal in extending the capabilities of CrewAI agents, enabling them to undertake a broad spectrum of tasks and collaborate effectively. When building solutions with CrewAI, leverage both custom and existing tools to empower your agents and enhance the AI ecosystem. Consider utilizing error handling, caching mechanisms, and the flexibility of tool arguments to optimize your agents’ performance and capabilities.

Was this page helpful?

YesNo

[LlamaIndex ToolPrevious](/en/tools/ai-ml/llamaindextool)[RAG ToolNext](/en/tools/ai-ml/ragtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)