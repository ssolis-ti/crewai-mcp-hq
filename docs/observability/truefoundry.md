# Source: https://docs.crewai.com/en/observability/truefoundry

Observability

# TrueFoundry Integration



TrueFoundry provides an enterprise-ready [AI Gateway](https://www.truefoundry.com/ai-gateway) which can integrate with agentic frameworks like CrewAI and provides governance and observability for your AI Applications. TrueFoundry AI Gateway serves as a unified interface for LLM access, providing:

  * **Unified API Access** : Connect to 250+ LLMs (OpenAI, Claude, Gemini, Groq, Mistral) through one API
  * **Low Latency** : Sub-3ms internal latency with intelligent routing and load balancing
  * **Enterprise Security** : SOC 2, HIPAA, GDPR compliance with RBAC and audit logging
  * **Quota and cost management** : Token-based quotas, rate limiting, and comprehensive usage tracking
  * **Observability** : Full request/response logging, metrics, and traces with customizable retention

## 

​

How TrueFoundry Integrates with CrewAI

### 

​

Installation & Setup

1

Install CrewAI
    
    
    pip install crewai
    

2

Get TrueFoundry Access Token

  1. Sign up for a [TrueFoundry account](https://www.truefoundry.com/register)
  2. Follow the steps here in [Quick start](https://docs.truefoundry.com/gateway/quick-start)

3

Configure CrewAI with TrueFoundry

![TrueFoundry Code Configuration](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/new-code-snippet.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=746c0bd23a77535f35b0b2bcf3320bf5)
    
    
    from crewai import LLM
    
    # Create an LLM instance with TrueFoundry AI Gateway
    truefoundry_llm = LLM(
        model="openai-main/gpt-4o",  # Similarly, you can call any model from any provider
        base_url="your_truefoundry_gateway_base_url",
        api_key="your_truefoundry_api_key"
    )
    
    # Use in your CrewAI agents
    from crewai import Agent
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=truefoundry_llm,
            verbose=True
        )
    

### 

​

Complete CrewAI Example
    
    
    from crewai import Agent, Task, Crew, LLM
    
    # Configure LLM with TrueFoundry
    llm = LLM(
        model="openai-main/gpt-4o",
        base_url="your_truefoundry_gateway_base_url", 
        api_key="your_truefoundry_api_key"
    )
    
    # Create agents
    researcher = Agent(
        role='Research Analyst',
        goal='Conduct detailed market research',
        backstory='Expert market analyst with attention to detail',
        llm=llm,
        verbose=True
    )
    
    writer = Agent(
        role='Content Writer', 
        goal='Create comprehensive reports',
        backstory='Experienced technical writer',
        llm=llm,
        verbose=True
    )
    
    # Create tasks
    research_task = Task(
        description='Research AI market trends for 2024',
        agent=researcher,
        expected_output='Comprehensive research summary'
    )
    
    writing_task = Task(
        description='Create a market research report',
        agent=writer,
        expected_output='Well-structured report with insights',
        context=[research_task]
    )
    
    # Create and execute crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=True
    )
    
    result = crew.kickoff()
    

### 

​

Observability and Governance

Monitor your CrewAI agents through TrueFoundry’s metrics tab: ![TrueFoundry metrics](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/gateway-metrics.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=33755ff848cb457e162e806c20c98216) With Truefoundry’s AI gateway, you can monitor and analyze:

  * **Performance Metrics** : Track key latency metrics like Request Latency, Time to First Token (TTFS), and Inter-Token Latency (ITL) with P99, P90, and P50 percentiles
  * **Cost and Token Usage** : Gain visibility into your application’s costs with detailed breakdowns of input/output tokens and the associated expenses for each model
  * **Usage Patterns** : Understand how your application is being used with detailed analytics on user activity, model distribution, and team-based usage
  * **Rate limit and Load balancing** : You can set up rate limiting, load balancing and fallback for your models

## 

​

Tracing

For a more detailed understanding on tracing, please see [getting-started-tracing](https://docs.truefoundry.com/docs/tracing/tracing-getting-started).For tracing, you can add the Traceloop SDK: For tracing, you can add the Traceloop SDK:
    
    
    pip install traceloop-sdk
    
    
    
    from traceloop.sdk import Traceloop
    
    # Initialize enhanced tracing
    Traceloop.init(
        api_endpoint="https://your-truefoundry-endpoint/api/tracing",
        headers={
            "Authorization": f"Bearer {your_truefoundry_pat_token}",
            "TFY-Tracing-Project": "your_project_name",
        },
    )
    

This provides additional trace correlation across your entire CrewAI workflow. ![TrueFoundry CrewAI Tracing](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/tracing_crewai.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=90623834e0ba9f4ccb09890f6824912d)

Was this page helpful?

YesNo

[Weave IntegrationPrevious](/en/observability/weave)[OverviewNext](/en/learn/overview)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)