# Source: https://docs.crewai.com/en/observability/maxim

Observability

# Maxim Integration


Start Agent monitoring, evaluation, and observability


# 

​

Maxim Overview

Maxim AI provides comprehensive agent monitoring, evaluation, and observability for your CrewAI applications. With Maxim’s one-line integration, you can easily trace and analyse agent interactions, performance metrics, and more.

## 

​

Features

### 

​

Prompt Management

Maxim’s Prompt Management capabilities enable you to create, organize, and optimize prompts for your CrewAI agents. Rather than hardcoding instructions, leverage Maxim’s SDK to dynamically retrieve and apply version-controlled prompts.

  * Prompt Playground

  * Prompt Versions

  * Prompt Comparisons

Create, refine, experiment and deploy your prompts via the playground. Organize of your prompts using folders and versions, experimenting with the real world cases by linking tools and context, and deploying based on custom logic.Easily experiment across models by [**configuring models**](https://www.getmaxim.ai/docs/introduction/quickstart/setting-up-workspace#add-model-api-keys) and selecting the relevant model from the dropdown at the top of the prompt playground.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_playground.png)

As teams build their AI applications, a big part of experimentation is iterating on the prompt structure. In order to collaborate effectively and organize your changes clearly, Maxim allows prompt versioning and comparison runs across versions.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_versions.png)

Iterating on Prompts as you evolve your AI application would need experiments across models, prompt structures, etc. In order to compare versions and make informed decisions about changes, the comparison playground allows a side by side view of results.

## 

​

**Why use Prompt comparison?**

Prompt comparison combines multiple single Prompts into one view, enabling a streamlined approach for various workflows:

  1. **Model comparison** : Evaluate the performance of different models on the same Prompt.
  2. **Prompt optimization** : Compare different versions of a Prompt to identify the most effective formulation.
  3. **Cross-Model consistency** : Ensure consistent outputs across various models for the same Prompt.
  4. **Performance benchmarking** : Analyze metrics like latency, cost, and token count across different models and Prompts.

### 

​

Observability & Evals

Maxim AI provides comprehensive observability & evaluation for your CrewAI agents, helping you understand exactly what’s happening during each execution.

  * Agent Tracing

  * Analytics + Evals

  * Alerting

  * Dashboards

Track your agent’s complete lifecycle, including tool calls, agent trajectories, and decision flows effortlessly.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_agent_tracking.png)

Run detailed evaluations on full traces or individual nodes with support for:

  * Multi-step interactions and granular trace analysis
  * Session Level Evaluations
  * Simulations for real-world testing

![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_trace_eval.png)

## Auto Evals on Logs

Evaluate captured logs automatically from the UI based on filters and sampling

## Human Evals on Logs

Use human evaluation or rating to assess the quality of your logs and evaluate them.

## Node Level Evals

Evaluate any component of your trace or log to gain insights into your agent’s behavior.

* * *

Set thresholds on **error** , **cost, token usage, user feedback, latency** and get real-time alerts via Slack or PagerDuty.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_alerts_1.png)

Visualize Traces over time, usage metrics, latency & error rates with ease.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_dashboard_1.png)

## 

​

Getting Started

### 

​

Prerequisites

  * Python version >=3.10
  * A Maxim account ([sign up here](https://getmaxim.ai/))
  * Generate Maxim API Key
  * A CrewAI project

### 

​

Installation

Install the Maxim SDK via pip:
    
    
    pip install maxim-py
    

Or add it to your `requirements.txt`:
    
    
    maxim-py
    

### 

​

Basic Setup

### 

​

1\. Set up environment variables
    
    
    ### Environment Variables Setup
    
    # Create a `.env` file in your project root:
    
    # Maxim API Configuration
    MAXIM_API_KEY=your_api_key_here
    MAXIM_LOG_REPO_ID=your_repo_id_here
    

### 

​

2\. Import the required packages
    
    
    from crewai import Agent, Task, Crew, Process
    from maxim import Maxim
    from maxim.logger.crewai import instrument_crewai
    

### 

​

3\. Initialise Maxim with your API key
    
    
    # Instrument CrewAI with just one line
    instrument_crewai(Maxim().logger())
    

### 

​

4\. Create and run your CrewAI application as usual
    
    
    # Create your agent
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Uncover cutting-edge developments in AI',
        backstory="You are an expert researcher at a tech think tank...",
        verbose=True,
        llm=llm
    )
    
    # Define the task
    research_task = Task(
        description="Research the latest AI advancements...",
        expected_output="",
        agent=researcher
    )
    
    # Configure and run the crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True
    )
    
    try:
        result = crew.kickoff()
    finally:
        maxim.cleanup()  # Ensure cleanup happens even if errors occur
    

That’s it! All your CrewAI agent interactions will now be logged and available in your Maxim dashboard. Check this Google Colab Notebook for a quick reference - [Notebook](https://colab.research.google.com/drive/1ZKIZWsmgQQ46n8TH9zLsT1negKkJA6K8?usp=sharing)

## 

​

Viewing Your Traces

After running your CrewAI application:

  1. Log in to your [Maxim Dashboard](https://app.getmaxim.ai/login)
  2. Navigate to your repository
  3. View detailed agent traces, including:
     * Agent conversations
     * Tool usage patterns
     * Performance metrics
     * Cost analytics
![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/crewai_traces.gif)

## 

​

Troubleshooting

### 

​

Common Issues

  * **No traces appearing** : Ensure your API key and repository ID are correct
  * Ensure you’ve **`called instrument_crewai()`** _**before**_ running your crew. This initializes logging hooks correctly.
  * Set `debug=True` in your `instrument_crewai()` call to surface any internal errors:
        
        instrument_crewai(logger, debug=True)
        

  * Configure your agents with `verbose=True` to capture detailed logs:
        
        agent = CrewAgent(..., verbose=True)
        

  * Double-check that `instrument_crewai()` is called **before** creating or executing agents. This might be obvious, but it’s a common oversight.

## 

​

Resources

## CrewAI Docs

Official CrewAI documentation

## Maxim Docs

Official Maxim documentation

## Maxim Github

Maxim Github

Was this page helpful?

YesNo

[Langtrace IntegrationPrevious](/en/observability/langtrace)[MLflow IntegrationNext](/en/observability/mlflow)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)