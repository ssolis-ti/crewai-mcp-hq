# Source: https://docs.crewai.com/en/observability/neatlogs

Observability

# Neatlogs Integration


Understand, debug, and share your CrewAI agent runs


# 

​

Introduction

Neatlogs helps you **see what your agent did** , **why** , and **share it**. It captures every step: thoughts, tool calls, responses, evaluations. No raw logs. Just clear, structured traces. Great for debugging and collaboration.

## 

​

Why use Neatlogs?

CrewAI agents use multiple tools and reasoning steps. When something goes wrong, you need context — not just errors. Neatlogs lets you:

  * Follow the full decision path
  * Add feedback directly on steps
  * Chat with the trace using AI assistant
  * Share runs publicly for feedback
  * Turn insights into tasks

All in one place. Manage your traces effortlessly ![Traces](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=d01a5ce64066c6c7387b238068e71369) ![Trace Response](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=5b737699468781be25098c33040d2125) The best UX to view a CrewAI trace. Post comments anywhere you want. Use AI to debug. ![Trace Details](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-3.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=43cda9bcd83376dda4523ff0596b2043) ![Ai Chat Bot With A Trace](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-4.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=c9e7ad0653cae7bfaad2dd448d90eda0) ![Comments Drawer](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-5.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=a977655abb8cd26d9ed4cef5fdd7d859)

## 

​

Core Features

  * **Trace Viewer** : Track thoughts, tools, and decisions in sequence
  * **Inline Comments** : Tag teammates on any trace step
  * **Feedback & Evaluation**: Mark outputs as correct or incorrect
  * **Error Highlighting** : Automatic flagging of API/tool failures
  * **Task Conversion** : Convert comments into assigned tasks
  * **Ask the Trace (AI)** : Chat with your trace using Neatlogs AI bot
  * **Public Sharing** : Publish trace links to your community

## 

​

Quick Setup with CrewAI

1

Sign Up & Get API Key

Visit [neatlogs.com](https://neatlogs.com/?utm_source=crewAI-docs), create a project, copy the API key.

2

Install SDK
    
    
    pip install neatlogs
    

(Latest version 0.8.0, Python 3.8+; MIT license)

3

Initialize Neatlogs

Before starting Crew agents, add:
    
    
    import neatlogs
    neatlogs.init("YOUR_PROJECT_API_KEY")
    

Agents run as usual. Neatlogs captures everything automatically.

## 

​

Under the Hood

According to GitHub, Neatlogs:

  * Captures thoughts, tool calls, responses, errors, and token stats
  * Supports AI-powered task generation and robust evaluation workflows

All with just two lines of code.

## 

​

Watch It Work

### 

​

🔍 Full Demo (4 min)

### 

​

⚙️ CrewAI Integration (30 s)

## 

​

Links & Support

  * 📘 [Neatlogs Docs](https://docs.neatlogs.com/)
  * 🔐 [Dashboard & API Key](https://app.neatlogs.com/)
  * 🐦 [Follow on Twitter](https://twitter.com/neatlogs)
  * 📧 Contact: [hello@neatlogs.com](mailto:hello@neatlogs.com)
  * 🛠 [GitHub SDK](https://github.com/NeatLogs/neatlogs)

## 

​

TL;DR

With just:
    
    
    pip install neatlogs
    
    import neatlogs
    neatlogs.init("YOUR_API_KEY")
    
    You can now capture, understand, share, and act on your CrewAI agent runs in seconds.
    No setup overhead. Full trace transparency. Full team collaboration.
    

Was this page helpful?

YesNo

[MLflow IntegrationPrevious](/en/observability/mlflow)[OpenLIT IntegrationNext](/en/observability/openlit)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)