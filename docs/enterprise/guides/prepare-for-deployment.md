# Source: https://docs.crewai.com/en/enterprise/guides/prepare-for-deployment

How-To Guides

# Prepare for Deployment


Ensure your Crew or Flow is ready for deployment to CrewAI AMP


Before deploying to CrewAI AMP, it’s crucial to verify your project is correctly structured. Both Crews and Flows can be deployed as “automations,” but they have different project structures and requirements that must be met for successful deployment.

## 

​

Understanding Automations

In CrewAI AMP, **automations** is the umbrella term for deployable Agentic AI projects. An automation can be either:

  * **A Crew** : A standalone team of AI agents working together on tasks
  * **A Flow** : An orchestrated workflow that can combine multiple crews, direct LLM calls, and procedural logic

Understanding which type you’re deploying is essential because they have different project structures and entry points.

## 

​

Crews vs Flows: Key Differences

## Crew Projects

Standalone AI agent teams with `crew.py` defining agents and tasks. Best for focused, collaborative tasks.

## Flow Projects

Orchestrated workflows with embedded crews in a `crews/` folder. Best for complex, multi-stage processes.

Aspect| Crew| Flow  
---|---|---  
**Project structure**| `src/project_name/` with `crew.py`| `src/project_name/` with `crews/` folder  
**Main logic location**| `src/project_name/crew.py`| `src/project_name/main.py` (Flow class)  
**Entry point function**| `run()` in `main.py`| `kickoff()` in `main.py`  
**pyproject.toml type**| `type = "crew"`| `type = "flow"`  
**CLI create command**| `crewai create crew name`| `crewai create flow name`  
**Config location**| `src/project_name/config/`| `src/project_name/crews/crew_name/config/`  
**Can contain other crews**|  No| Yes (in `crews/` folder)  
  
## 

​

Project Structure Reference

### 

​

Crew Project Structure

When you run `crewai create crew my_crew`, you get this structure:
    
    
    my_crew/
    ├── .gitignore
    ├── pyproject.toml          # Must have type = "crew"
    ├── README.md
    ├── .env
    ├── uv.lock                  # REQUIRED for deployment
    └── src/
        └── my_crew/
            ├── __init__.py
            ├── main.py          # Entry point with run() function
            ├── crew.py          # Crew class with @CrewBase decorator
            ├── tools/
            │   ├── custom_tool.py
            │   └── __init__.py
            └── config/
                ├── agents.yaml  # Agent definitions
                └── tasks.yaml   # Task definitions
    

The nested `src/project_name/` structure is critical for Crews. Placing files at the wrong level will cause deployment failures.

### 

​

Flow Project Structure

When you run `crewai create flow my_flow`, you get this structure:
    
    
    my_flow/
    ├── .gitignore
    ├── pyproject.toml          # Must have type = "flow"
    ├── README.md
    ├── .env
    ├── uv.lock                  # REQUIRED for deployment
    └── src/
        └── my_flow/
            ├── __init__.py
            ├── main.py          # Entry point with kickoff() function + Flow class
            ├── crews/           # Embedded crews folder
            │   └── poem_crew/
            │       ├── __init__.py
            │       ├── poem_crew.py  # Crew with @CrewBase decorator
            │       └── config/
            │           ├── agents.yaml
            │           └── tasks.yaml
            └── tools/
                ├── __init__.py
                └── custom_tool.py
    

Both Crews and Flows use the `src/project_name/` structure. The key difference is that Flows have a `crews/` folder for embedded crews, while Crews have `crew.py` directly in the project folder.

## 

​

Pre-Deployment Checklist

Use this checklist to verify your project is ready for deployment.

### 

​

1\. Verify pyproject.toml Configuration

Your `pyproject.toml` must include the correct `[tool.crewai]` section:

  * For Crews

  * For Flows

    
    
    [tool.crewai]
    type = "crew"
    
    
    
    [tool.crewai]
    type = "flow"
    

If the `type` doesn’t match your project structure, the build will fail or the automation won’t run correctly.

### 

​

2\. Ensure uv.lock File Exists

CrewAI uses `uv` for dependency management. The `uv.lock` file ensures reproducible builds and is **required** for deployment.
    
    
    # Generate or update the lock file
    uv lock
    
    # Verify it exists
    ls -la uv.lock
    

If the file doesn’t exist, run `uv lock` and commit it to your repository:
    
    
    uv lock
    git add uv.lock
    git commit -m "Add uv.lock for deployment"
    git push
    

### 

​

3\. Validate CrewBase Decorator Usage

**Every crew class must use the`@CrewBase` decorator.** This applies to:

  * Standalone crew projects
  * Crews embedded inside Flow projects

    
    
    from crewai import Agent, Crew, Process, Task
    from crewai.project import CrewBase, agent, crew, task
    from crewai.agents.agent_builder.base_agent import BaseAgent
    from typing import List
    
    @CrewBase  # This decorator is REQUIRED
    class MyCrew():
        """My crew description"""
    
        agents: List[BaseAgent]
        tasks: List[Task]
    
        @agent
        def my_agent(self) -> Agent:
            return Agent(
                config=self.agents_config['my_agent'],  # type: ignore[index]
                verbose=True
            )
    
        @task
        def my_task(self) -> Task:
            return Task(
                config=self.tasks_config['my_task']  # type: ignore[index]
            )
    
        @crew
        def crew(self) -> Crew:
            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True,
            )
    

If you forget the `@CrewBase` decorator, your deployment will fail with errors about missing agents or tasks configurations.

### 

​

4\. Check Project Entry Points

Both Crews and Flows have their entry point in `src/project_name/main.py`:

  * For Crews

  * For Flows

The entry point uses a `run()` function:
    
    
    # src/my_crew/main.py
    from my_crew.crew import MyCrew
    
    def run():
        """Run the crew."""
        inputs = {'topic': 'AI in Healthcare'}
        result = MyCrew().crew().kickoff(inputs=inputs)
        return result
    
    if __name__ == "__main__":
        run()
    

The entry point uses a `kickoff()` function with a Flow class:
    
    
    # src/my_flow/main.py
    from crewai.flow import Flow, listen, start
    from my_flow.crews.poem_crew.poem_crew import PoemCrew
    
    class MyFlow(Flow):
        @start()
        def begin(self):
            # Flow logic here
            result = PoemCrew().crew().kickoff(inputs={...})
            return result
    
    def kickoff():
        """Run the flow."""
        MyFlow().kickoff()
    
    if __name__ == "__main__":
        kickoff()
    

### 

​

5\. Prepare Environment Variables

Before deployment, ensure you have:

  1. **LLM API keys** ready (OpenAI, Anthropic, Google, etc.)
  2. **Tool API keys** if using external tools (Serper, etc.)

If your project depends on packages from a **private PyPI registry** , you’ll also need to configure registry authentication credentials as environment variables. See the [Private Package Registries](/en/enterprise/guides/private-package-registry) guide for details.

Test your project locally with the same environment variables before deploying to catch configuration issues early.

## 

​

Quick Validation Commands

Run these commands from your project root to quickly verify your setup:
    
    
    # 1. Check project type in pyproject.toml
    grep -A2 "\[tool.crewai\]" pyproject.toml
    
    # 2. Verify uv.lock exists
    ls -la uv.lock || echo "ERROR: uv.lock missing! Run 'uv lock'"
    
    # 3. Verify src/ structure exists
    ls -la src/*/main.py 2>/dev/null || echo "No main.py found in src/"
    
    # 4. For Crews - verify crew.py exists
    ls -la src/*/crew.py 2>/dev/null || echo "No crew.py (expected for Crews)"
    
    # 5. For Flows - verify crews/ folder exists
    ls -la src/*/crews/ 2>/dev/null || echo "No crews/ folder (expected for Flows)"
    
    # 6. Check for CrewBase usage
    grep -r "@CrewBase" . --include="*.py"
    

## 

​

Common Setup Mistakes

Mistake| Symptom| Fix  
---|---|---  
Missing `uv.lock`| Build fails during dependency resolution| Run `uv lock` and commit  
Wrong `type` in pyproject.toml| Build succeeds but runtime fails| Change to correct type  
Missing `@CrewBase` decorator| ”Config not found” errors| Add decorator to all crew classes  
Files at root instead of `src/`| Entry point not found| Move to `src/project_name/`  
Missing `run()` or `kickoff()`| Cannot start automation| Add correct entry function  
  
## 

​

Next Steps

Once your project passes all checklist items, you’re ready to deploy:

## Deploy to AMP

Follow the deployment guide to deploy your Crew or Flow to CrewAI AMP using the CLI, web interface, or CI/CD integration.

Was this page helpful?

YesNo

[Build CrewPrevious](/en/enterprise/guides/build-crew)[Deploy to AMPNext](/en/enterprise/guides/deploy-to-amp)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)