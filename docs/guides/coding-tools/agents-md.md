# Source: https://docs.crewai.com/en/guides/coding-tools/agents-md

Coding Tools

# Coding Tools


Use AGENTS.md to guide coding agents and IDEs across your CrewAI projects.


## 

​

Why AGENTS.md

`AGENTS.md` is a lightweight, repo-local instruction file that gives coding agents consistent, project-specific guidance. Keep it in the project root and treat it as the source of truth for how you want assistants to work: conventions, commands, architecture notes, and guardrails.

## 

​

Create a Project with the CLI

Use the CrewAI CLI to scaffold a project, then `AGENTS.md` will be automatically added at the root.
    
    
    # Crew
    crewai create crew my_crew
    
    # Flow
    crewai create flow my_flow
    
    # Tool repository
    crewai tool create my_tool
    

## 

​

Tool Setup: Point Assistants to AGENTS.md

### 

​

Codex

Codex can be guided by `AGENTS.md` files placed in your repository. Use them to supply persistent project context such as conventions, commands, and workflow expectations.

### 

​

Claude Code

Claude Code stores project memory in `CLAUDE.md`. You can bootstrap it with `/init` and edit it using `/memory`. Claude Code also supports imports inside `CLAUDE.md`, so you can add a single line like `@AGENTS.md` to pull in the shared instructions without duplicating them. You can simply use:
    
    
    mv AGENTS.md CLAUDE.md
    

### 

​

Gemini CLI and Google Antigravity

Gemini CLI and Antigravity load a project context file (default: `GEMINI.md`) from the repo root and parent directories. You can configure it to read `AGENTS.md` instead (or in addition) by setting `context.fileName` in your Gemini CLI settings. For example, set it to `AGENTS.md` only, or include both `AGENTS.md` and `GEMINI.md` if you want to keep each tool’s format. You can simply use:
    
    
    mv AGENTS.md GEMINI.md
    

### 

​

Cursor

Cursor supports `AGENTS.md` as a project instruction file. Place it at the project root to provide guidance for Cursor’s coding assistant.

### 

​

Windsurf

Claude Code provides an official integration with Windsurf. If you use Claude Code inside Windsurf, follow the Claude Code guidance above and import `AGENTS.md` from `CLAUDE.md`. If you are using Windsurf’s native assistant, configure its project rules or instructions feature (if available) to read from `AGENTS.md` or paste the contents directly.

Was this page helpful?

YesNo

[Publish Custom ToolsPrevious](/en/guides/tools/publish-custom-tools)[Build with AINext](/en/guides/coding-tools/build-with-ai)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)