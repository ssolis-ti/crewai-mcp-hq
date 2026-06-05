# Source: https://docs.crewai.com/en/observability/langtrace

Observability

# Langtrace Integration


How to monitor cost, latency, and performance of CrewAI Agents using Langtrace, an external observability tool.


# 

​

Langtrace Overview

Langtrace is an open-source, external tool that helps you set up observability and evaluations for Large Language Models (LLMs), LLM frameworks, and Vector Databases. While not built directly into CrewAI, Langtrace can be used alongside CrewAI to gain deep visibility into the cost, latency, and performance of your CrewAI Agents. This integration allows you to log hyperparameters, monitor performance regressions, and establish a process for continuous improvement of your Agents. ![Overview of a select series of agent session runs](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langtrace1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=85b67e42028ca9383087737279f8931f) ![Overview of agent traces](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langtrace2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=24f08e5c56b6200e386d305a7bee347c) ![Overview of llm traces in details](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langtrace3.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=f1a8624e0c05d59deded640e4751a986)

## 

​

Setup Instructions

1

Sign up for Langtrace

Sign up by visiting <https://langtrace.ai/signup>.

2

Create a project

Set the project type to `CrewAI` and generate an API key.

3

Install Langtrace in your CrewAI project

Use the following command:
    
    
    pip install langtrace-python-sdk
    

4

Import Langtrace

Import and initialize Langtrace at the beginning of your script, before any CrewAI imports:
    
    
    from langtrace_python_sdk import langtrace
    langtrace.init(api_key='<LANGTRACE_API_KEY>')
    
    # Now import CrewAI modules
    from crewai import Agent, Task, Crew
    

### 

​

Features and Their Application to CrewAI

  1. **LLM Token and Cost Tracking**
     * Monitor the token usage and associated costs for each CrewAI agent interaction.
  2. **Trace Graph for Execution Steps**
     * Visualize the execution flow of your CrewAI tasks, including latency and logs.
     * Useful for identifying bottlenecks in your agent workflows.
  3. **Dataset Curation with Manual Annotation**
     * Create datasets from your CrewAI task outputs for future training or evaluation.
  4. **Prompt Versioning and Management**
     * Keep track of different versions of prompts used in your CrewAI agents.
     * Useful for A/B testing and optimizing agent performance.
  5. **Prompt Playground with Model Comparisons**
     * Test and compare different prompts and models for your CrewAI agents before deployment.
  6. **Testing and Evaluations**
     * Set up automated tests for your CrewAI agents and tasks.

Was this page helpful?

YesNo

[Langfuse IntegrationPrevious](/en/observability/langfuse)[Maxim IntegrationNext](/en/observability/maxim)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)