# Source: https://docs.crewai.com/en/installation

Get Started

# Installation


Get started with CrewAI - Install, configure, and build your first AI crew


### 

​

Watch: Building CrewAI Agents & Flows with Coding Agent Skills

Install our coding agent skills (Claude Code, Codex, …) to quickly get your coding agents up and running with CrewAI. You can install it with `npx skills add crewaiinc/skills`

## 

​

Video Tutorial

Watch this video tutorial for a step-by-step demonstration of the installation process:

## 

​

Text Tutorial

**Python Version Requirements** CrewAI requires `Python >=3.10 and <3.14`. Here’s how to check your version:
    
    
    python3 --version
    

If you need to update Python, visit [python.org/downloads](https://python.org/downloads)

**OpenAI SDK Requirement** CrewAI 0.175.0 requires `openai >= 1.13.3`. If you manage dependencies yourself, ensure your environment satisfies this constraint to avoid import/runtime issues.

CrewAI uses the `uv` as its dependency management and package handling tool. It simplifies project setup and execution, offering a seamless experience. If you haven’t installed `uv` yet, follow **step 1** to quickly get it set up on your system, else you can skip to **step 2**.

1

Install uv

  * **On macOS/Linux:** Use `curl` to download the script and execute it with `sh`:
        
        curl -LsSf https://astral.sh/uv/install.sh | sh
        

If your system doesn’t have `curl`, you can use `wget`:
        
        wget -qO- https://astral.sh/uv/install.sh | sh
        

  * **On Windows:** Use `irm` to download the script and `iex` to execute it:
        
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        

If you run into any issues, refer to [UV’s installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more information.

2

Install CrewAI 🚀

  * Run the following command to install `crewai` CLI:
        
        uv tool install crewai
        

If you encounter a `PATH` warning, run this command to update your shell:
        
        uv tool update-shell
        

If you encounter the `chroma-hnswlib==0.7.6` build error (`fatal error C1083: Cannot open include file: 'float.h'`) on Windows, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with _Desktop development with C++_.

  * To verify that `crewai` is installed, run:
        
        uv tool list
        

  * You should see something like:
        
        crewai v0.102.0
        - crewai
        

  * If you need to update `crewai`, run:
        
        uv tool install crewai --upgrade
        

This upgrades the **global`crewai` CLI tool** only. To upgrade the `crewai` version inside your project’s virtual environment, see [Upgrading CrewAI in a project](/en/guides/migration/upgrading-crewai).

Installation successful! You’re ready to create your first crew! 🎉

# 

​

Creating a CrewAI Project

We recommend using the `YAML` template scaffolding for a structured approach to defining agents and tasks. Here’s how to get started:

1

Generate Project Scaffolding

  * Run the `crewai` CLI command:
        
        crewai create crew <your_project_name>
        

  * This creates a new project with the following structure:
        
        my_project/
        ├── .gitignore
        ├── knowledge/
        ├── pyproject.toml
        ├── README.md
        ├── .env
        └── src/
            └── my_project/
                ├── __init__.py
                ├── main.py
                ├── crew.py
                ├── tools/
                │   ├── custom_tool.py
                │   └── __init__.py
                └── config/
                    ├── agents.yaml
                    └── tasks.yaml
        

2

Customize Your Project

  * Your project will contain these essential files:

File| Purpose  
---|---  
`agents.yaml`| Define your AI agents and their roles  
`tasks.yaml`| Set up agent tasks and workflows  
`.env`| Store API keys and environment variables  
`main.py`| Project entry point and execution flow  
`crew.py`| Crew orchestration and coordination  
`tools/`| Directory for custom agent tools  
`knowledge/`| Directory for knowledge base  
  
  * Start by editing `agents.yaml` and `tasks.yaml` to define your crew’s behavior.
  * Keep sensitive information like API keys in `.env`.

3

Run your Crew

  * Before you run your crew, make sure to run:
        
        crewai install
        

  * If you need to install additional packages, use:
        
        uv add <package-name>
        

As a supply-chain security measure, CrewAI’s internal packages use `exclude-newer = "3 days"` in their `pyproject.toml` files. This means transitive dependencies pulled in by CrewAI won’t resolve packages released less than 3 days ago. Your own direct dependencies are not affected by this policy. If you notice a transitive dependency is behind, you can pin the version you want explicitly in your project’s dependencies.

  * To run your crew, execute the following command in the root of your project:
        
        crewai run
        

## 

​

Enterprise Installation Options

For teams and organizations, CrewAI offers enterprise deployment options that eliminate setup complexity:

### 

​

CrewAI AMP (SaaS)

  * Zero installation required - just sign up for free at [app.crewai.com](https://app.crewai.com)
  * Automatic updates and maintenance
  * Managed infrastructure and scaling
  * Build Crews with no Code

### 

​

CrewAI Factory (Self-hosted)

  * Containerized deployment for your infrastructure
  * Supports any hyperscaler including on prem deployments
  * Integration with your existing security systems

## Explore Enterprise Options

Learn about CrewAI’s enterprise offerings and schedule a demo

## 

​

Next Steps

## Quickstart: Flow + agent

Follow the quickstart to scaffold a Flow, run a one-agent crew, and produce a report.

## Join the Community

Connect with other developers, get help, and share your CrewAI experiences.

Was this page helpful?

YesNo

[SkillsPrevious](/en/skills)[QuickstartNext](/en/quickstart)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)