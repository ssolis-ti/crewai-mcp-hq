# Source: https://docs.crewai.com/en/concepts/planning

Core Concepts

# Planning


Learn how to add planning to your CrewAI Crew and improve their performance.


## 

​

Overview

The planning feature in CrewAI allows you to add planning capability to your crew. When enabled, before each Crew iteration, all Crew information is sent to an AgentPlanner that will plan the tasks step by step, and this plan will be added to each task description.

### 

​

Using the Planning Feature

Getting started with the planning feature is very easy, the only step required is to add `planning=True` to your Crew:

Code
    
    
    from crewai import Crew, Agent, Task, Process
    
    # Assemble your crew with planning capabilities
    my_crew = Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        planning=True,
    )
    

From this point on, your crew will have planning enabled, and the tasks will be planned before each iteration.

When planning is enabled, crewAI will use `gpt-4o-mini` as the default LLM for planning, which requires a valid OpenAI API key. Since your agents might be using different LLMs, this could cause confusion if you don’t have an OpenAI API key configured or if you’re experiencing unexpected behavior related to LLM API calls.

#### 

​

Planning LLM

Now you can define the LLM that will be used to plan the tasks. When running the base case example, you will see something like the output below, which represents the output of the `AgentPlanner` responsible for creating the step-by-step logic to add to the Agents’ tasks.

Code

Result
    
    
    from crewai import Crew, Agent, Task, Process
    
    # Assemble your crew with planning capabilities and custom LLM
    my_crew = Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        planning=True,
        planning_llm="gpt-4o"
    )
    
    # Run the crew
    my_crew.kickoff()
    

Was this page helpful?

YesNo

[ReasoningPrevious](/en/concepts/reasoning)[TestingNext](/en/concepts/testing)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)