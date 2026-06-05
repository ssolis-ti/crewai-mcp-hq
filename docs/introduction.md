# Source: https://docs.crewai.com/en/introduction

Get Started

# Introduction


Build AI agent teams that work together to tackle complex tasks


# 

​

What is CrewAI?

**CrewAI is the leading open-source framework for orchestrating autonomous AI agents and building complex workflows.** It empowers developers to build production-ready multi-agent systems by combining the collaborative intelligence of **Crews** with the precise control of **Flows**.

  * **[CrewAI Flows](/en/guides/flows/first-flow)** : The backbone of your AI application. Flows allow you to create structured, event-driven workflows that manage state and control execution. They provide the scaffolding for your AI agents to work within.
  * **[CrewAI Crews](/en/guides/crews/first-crew)** : The units of work within your Flow. Crews are teams of autonomous agents that collaborate to solve specific tasks delegated to them by the Flow.

With over 100,000 developers certified through our community courses, CrewAI is the standard for enterprise-ready AI automation.

### 

​

Watch: Building CrewAI Agents & Flows with Coding Agent Skills

Install our coding agent skills (Claude Code, Codex, …) to quickly get your coding agents up and running with CrewAI. You can install it with `npx skills add crewaiinc/skills`

## 

​

The CrewAI Architecture

CrewAI’s architecture is designed to balance autonomy with control.

### 

​

1\. Flows: The Backbone

Think of a Flow as the “manager” or the “process definition” of your application. It defines the steps, the logic, and how data moves through your system.

![CrewAI Framework Overview](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/flows.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=82ea168de2f004553dcea21410cd7d8a)

Flows provide:

  * **State Management** : Persist data across steps and executions.
  * **Event-Driven Execution** : Trigger actions based on events or external inputs.
  * **Control Flow** : Use conditional logic, loops, and branching.

### 

​

2\. Crews: The Intelligence

Crews are the “teams” that do the heavy lifting. Within a Flow, you can trigger a Crew to tackle a complex problem requiring creativity and collaboration.

![CrewAI Framework Overview](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crews.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=514fd0b06e4128e62f10728d44601975)

Crews provide:

  * **Role-Playing Agents** : Specialized agents with specific goals and tools.
  * **Autonomous Collaboration** : Agents work together to solve tasks.
  * **Task Delegation** : Tasks are assigned and executed based on agent capabilities.

## 

​

How It All Works Together

  1. **The Flow** triggers an event or starts a process.
  2. **The Flow** manages the state and decides what to do next.
  3. **The Flow** delegates a complex task to a **Crew**.
  4. **The Crew** ’s agents collaborate to complete the task.
  5. **The Crew** returns the result to the **Flow**.
  6. **The Flow** continues execution based on the result.

## 

​

Key Features

## Production-Grade Flows

Build reliable, stateful workflows that can handle long-running processes and complex logic.

## Autonomous Crews

Deploy teams of agents that can plan, execute, and collaborate to achieve high-level goals.

## Flexible Tools

Connect your agents to any API, database, or local tool.

## Enterprise Security

Designed with security and compliance in mind for enterprise deployments.

## 

​

When to Use Crews vs. Flows

**The short answer: Use both.** For any production-ready application, **start with a Flow**.

  * **Use a Flow** to define the overall structure, state, and logic of your application.
  * **Use a Crew** within a Flow step when you need a team of agents to perform a specific, complex task that requires autonomy.

Use Case| Architecture  
---|---  
**Simple Automation**|  Single Flow with Python tasks  
**Complex Research**|  Flow managing state -> Crew performing research  
**Application Backend**|  Flow handling API requests -> Crew generating content -> Flow saving to DB  
  
## 

​

Why Choose CrewAI?

  * 🧠 **Autonomous Operation** : Agents make intelligent decisions based on their roles and available tools
  * 📝 **Natural Interaction** : Agents communicate and collaborate like human team members
  * 🛠️ **Extensible Design** : Easy to add new tools, roles, and capabilities
  * 🚀 **Production Ready** : Built for reliability and scalability in real-world applications
  * 🔒 **Security-Focused** : Designed with enterprise security requirements in mind
  * 💰 **Cost-Efficient** : Optimized to minimize token usage and API calls

## 

​

Ready to Start Building?

## Build Your First Flow

Learn how to create structured, event-driven workflows with precise control over execution.

## Build Your First Crew

Step-by-step tutorial to create a collaborative AI team that works together to solve complex problems.

## Install CrewAI

Get started with CrewAI in your development environment.

## Quick Start

Scaffold a Flow, run a crew with one agent, and generate a report end to end.

## Join the Community

Connect with other developers, get help, and share your CrewAI experiences.

Was this page helpful?

YesNo

[Build with AINext](/en/guides/coding-tools/build-with-ai)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)