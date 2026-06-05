# Source: https://docs.crewai.com/en/learn/litellm-removal-guide

Learn

# Using CrewAI Without LiteLLM


How to use CrewAI with native provider integrations and remove the LiteLLM dependency from your project.


## 

​

Overview

CrewAI supports two paths for connecting to LLM providers:

  1. **Native integrations** — direct SDK connections to OpenAI, Anthropic, Google Gemini, Azure OpenAI, and AWS Bedrock
  2. **LiteLLM fallback** — a translation layer that supports 100+ additional providers

This guide explains how to use CrewAI exclusively with native provider integrations, removing any dependency on LiteLLM.

The `litellm` package was quarantined on PyPI due to a security/reliability incident. If you rely on LiteLLM-dependent providers, you should migrate to native integrations. CrewAI’s native integrations give you full functionality without LiteLLM.

## 

​

Why Remove LiteLLM?

  * **Reduced dependency surface** — fewer packages means fewer potential supply-chain risks
  * **Better performance** — native SDKs communicate directly with provider APIs, eliminating a translation layer
  * **Simpler debugging** — one less abstraction layer between your code and the provider
  * **Smaller install footprint** — LiteLLM brings in many transitive dependencies

## 

​

Native Providers (No LiteLLM Required)

These providers use their own SDKs and work without LiteLLM installed:

## OpenAI

GPT-4o, GPT-4o-mini, o1, o3-mini, and more.
    
    
    uv add "crewai[openai]"
    

## Anthropic

Claude Sonnet, Claude Haiku, and more.
    
    
    uv add "crewai[anthropic]"
    

## Google Gemini

Gemini 2.0 Flash, Gemini 2.0 Pro, and more.
    
    
    uv add "crewai[gemini]"
    

## Azure OpenAI

Azure-hosted OpenAI models.
    
    
    uv add "crewai[azure]"
    

## AWS Bedrock

Claude, Llama, Titan, and more via AWS.
    
    
    uv add "crewai[bedrock]"
    

If you only use native providers, you **never** need to install `crewai[litellm]`. The base `crewai` package plus your chosen provider extra is all you need.

## 

​

How to Check If You’re Using LiteLLM

### 

​

Check your model strings

If your code uses model prefixes like these, you’re routing through LiteLLM:

Prefix| Provider| Uses LiteLLM?  
---|---|---  
`ollama/`| Ollama| ✅ Yes  
`groq/`| Groq| ✅ Yes  
`together_ai/`| Together AI| ✅ Yes  
`mistral/`| Mistral| ✅ Yes  
`cohere/`| Cohere| ✅ Yes  
`huggingface/`| Hugging Face| ✅ Yes  
`openai/`| OpenAI| ❌ Native  
`anthropic/`| Anthropic| ❌ Native  
`gemini/`| Google Gemini| ❌ Native  
`azure/`| Azure OpenAI| ❌ Native  
`bedrock/`| AWS Bedrock| ❌ Native  
  
### 

​

Check if LiteLLM is installed
    
    
    # Using pip
    pip show litellm
    
    # Using uv
    uv pip show litellm
    

If the command returns package information, LiteLLM is installed in your environment.

### 

​

Check your dependencies

Look at your `pyproject.toml` for `crewai[litellm]`:
    
    
    # If you see this, you have LiteLLM as a dependency
    dependencies = [
        "crewai[litellm]>=0.100.0",  # ← Uses LiteLLM
    ]
    
    # Change to a native provider extra instead
    dependencies = [
        "crewai[openai]>=0.100.0",   # ← Native, no LiteLLM
    ]
    

## 

​

Migration Guide

### 

​

Step 1: Identify your current provider

Find all `LLM()` calls and model strings in your code:
    
    
    # Search your codebase for LLM model strings
    grep -r "LLM(" --include="*.py" .
    grep -r "llm=" --include="*.yaml" .
    grep -r "llm:" --include="*.yaml" .
    

### 

​

Step 2: Switch to a native provider

  * Switch to OpenAI

  * Switch to Anthropic

  * Switch to Gemini

  * Switch to Azure OpenAI

  * Switch to AWS Bedrock

    
    
    from crewai import LLM
    
    # Before (LiteLLM):
    # llm = LLM(model="groq/llama-3.1-70b")
    
    # After (Native):
    llm = LLM(model="openai/gpt-4o")
    
    
    
    # Install
    uv add "crewai[openai]"
    
    # Set your API key
    export OPENAI_API_KEY="sk-..."
    
    
    
    from crewai import LLM
    
    # Before (LiteLLM):
    # llm = LLM(model="together_ai/meta-llama/Meta-Llama-3.1-70B")
    
    # After (Native):
    llm = LLM(model="anthropic/claude-sonnet-4-20250514")
    
    
    
    # Install
    uv add "crewai[anthropic]"
    
    # Set your API key
    export ANTHROPIC_API_KEY="sk-ant-..."
    
    
    
    from crewai import LLM
    
    # Before (LiteLLM):
    # llm = LLM(model="mistral/mistral-large-latest")
    
    # After (Native):
    llm = LLM(model="gemini/gemini-2.0-flash")
    
    
    
    # Install
    uv add "crewai[gemini]"
    
    # Set your API key
    export GEMINI_API_KEY="..."
    
    
    
    from crewai import LLM
    
    # After (Native):
    llm = LLM(
        model="azure/your-deployment-name",
        api_key="your-azure-api-key",
        base_url="https://your-resource.openai.azure.com",
        api_version="2024-06-01"
    )
    
    
    
    # Install
    uv add "crewai[azure]"
    
    
    
    from crewai import LLM
    
    # After (Native):
    llm = LLM(
        model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
        aws_region_name="us-east-1"
    )
    
    
    
    # Install
    uv add "crewai[bedrock]"
    
    # Configure AWS credentials
    export AWS_ACCESS_KEY_ID="..."
    export AWS_SECRET_ACCESS_KEY="..."
    export AWS_DEFAULT_REGION="us-east-1"
    

### 

​

Step 3: Keep Ollama without LiteLLM

If you’re using Ollama and want to keep using it, you can connect via Ollama’s OpenAI-compatible API:
    
    
    from crewai import LLM
    
    # Before (LiteLLM):
    # llm = LLM(model="ollama/llama3")
    
    # After (OpenAI-compatible mode, no LiteLLM needed):
    llm = LLM(
        model="openai/llama3",
        base_url="http://localhost:11434/v1",
        api_key="ollama"  # Ollama doesn't require a real API key
    )
    

Many local inference servers (Ollama, vLLM, LM Studio, llama.cpp) expose an OpenAI-compatible API. You can use the `openai/` prefix with a custom `base_url` to connect to any of them natively.

### 

​

Step 4: Update your YAML configs
    
    
    # Before (LiteLLM providers):
    researcher:
      role: Research Specialist
      goal: Conduct research
      backstory: A dedicated researcher
      llm: groq/llama-3.1-70b          # ← LiteLLM
      
    # After (Native provider):
    researcher:
      role: Research Specialist
      goal: Conduct research
      backstory: A dedicated researcher
      llm: openai/gpt-4o               # ← Native
    

### 

​

Step 5: Remove LiteLLM

Once you’ve migrated all your model references:
    
    
    # Remove litellm from your project
    uv remove litellm
    
    # Or if using pip
    pip uninstall litellm
    
    # Update your pyproject.toml: change crewai[litellm] to your provider extra
    # e.g., crewai[openai], crewai[anthropic], crewai[gemini]
    

### 

​

Step 6: Verify

Run your project and confirm everything works:
    
    
    # Run your crew
    crewai run
    
    # Or run your tests
    uv run pytest
    

## 

​

Quick Reference: Model String Mapping

Here are common migration paths from LiteLLM-dependent providers to native ones:
    
    
    from crewai import LLM
    
    # ─── LiteLLM providers → Native alternatives ────────────────────
    
    # Groq → OpenAI or Anthropic
    # llm = LLM(model="groq/llama-3.1-70b")
    llm = LLM(model="openai/gpt-4o-mini")           # Fast & affordable
    llm = LLM(model="anthropic/claude-haiku-3-5")    # Fast & affordable
    
    # Together AI → OpenAI or Gemini
    # llm = LLM(model="together_ai/meta-llama/Meta-Llama-3.1-70B")
    llm = LLM(model="openai/gpt-4o")                 # High quality
    llm = LLM(model="gemini/gemini-2.0-flash")       # Fast & capable
    
    # Mistral → Anthropic or OpenAI
    # llm = LLM(model="mistral/mistral-large-latest")
    llm = LLM(model="anthropic/claude-sonnet-4-20250514")  # High quality
    
    # Ollama → OpenAI-compatible (keep using local models)
    # llm = LLM(model="ollama/llama3")
    llm = LLM(
        model="openai/llama3",
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    

## 

​

FAQ

Do I lose any functionality by removing LiteLLM?

No, if you use one of the five natively supported providers (OpenAI, Anthropic, Gemini, Azure, Bedrock). These native integrations support all CrewAI features including streaming, tool calling, structured output, and more. You only lose access to providers that are exclusively available through LiteLLM (like Groq, Together AI, Mistral as first-class providers).

Can I use multiple native providers at the same time?

Yes. Install multiple extras and use different providers for different agents:
    
    
    uv add "crewai[openai,anthropic,gemini]"
    
    
    
    researcher = Agent(llm="openai/gpt-4o", ...)
    writer = Agent(llm="anthropic/claude-sonnet-4-20250514", ...)
    

Is LiteLLM safe to use now?

Regardless of quarantine status, reducing your dependency surface is good security practice. If you only need providers that CrewAI supports natively, there’s no reason to keep LiteLLM installed.

What about environment variables like OPENAI_API_KEY?

Native providers use the same environment variables you’re already familiar with. No changes needed for `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, etc.

## 

​

Related Resources

  * [LLM Connections](/en/learn/llm-connections) — Full guide to connecting CrewAI with any LLM
  * [LLM Concepts](/en/concepts/llms) — Understanding LLMs in CrewAI
  * [LLM Selection Guide](/en/learn/llm-selection-guide) — Choosing the right model for your use case

Was this page helpful?

YesNo

[Connect to any LLMPrevious](/en/learn/llm-connections)[Using Multimodal AgentsNext](/en/learn/multimodal-agents)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)