# Source: https://docs.crewai.com/en/enterprise/guides/enable-crew-studio

How-To Guides

# Enable Crew Studio


Enabling Crew Studio on CrewAI AMP


Crew Studio is a powerful **no-code/low-code** tool that allows you to quickly scaffold or build Crews through a conversational interface.

## 

​

What is Crew Studio?

Crew Studio is an innovative way to create AI agent crews without writing code.

![Crew Studio Interface](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew-studio-interface.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=c4f5428b111816273b3b53d9cef14fad)

With Crew Studio, you can:

  * Chat with the Crew Assistant to describe your problem
  * Automatically generate agents and tasks
  * Select appropriate tools
  * Configure necessary inputs
  * Generate downloadable code for customization
  * Deploy directly to the CrewAI AMP platform

## 

​

Configuration Steps

Before you can start using Crew Studio, you need to configure your LLM connections:

1

Set Up LLM Connection

Go to the **LLM Connections** tab in your CrewAI AMP dashboard and create a new LLM connection.

Feel free to use any LLM provider you want that is supported by CrewAI.

Configure your LLM connection:

  * Enter a `Connection Name` (e.g., `OpenAI`)
  * Select your model provider: `openai` or `azure`
  * Select models you’d like to use in your Studio-generated Crews
    * We recommend at least `gpt-4o`, `o1-mini`, and `gpt-4o-mini`
  * Add your API key as an environment variable:
    * For OpenAI: Add `OPENAI_API_KEY` with your API key
    * For Azure OpenAI: Refer to [this article](https://blog.crewai.com/configuring-azure-openai-with-crewai-a-comprehensive-guide/) for configuration details
  * Click `Add Connection` to save your configuration

![LLM Connection Configuration](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/llm-connection-config.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=c06fcdb008733c7e1d6ec7fcd055ff2c)

2

Verify Connection Added

Once you complete the setup, you’ll see your new connection added to the list of available connections.

![Connection Added](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/connection-added.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=3726ffaa33f0bfdf221dd542ae729f69)

3

Configure LLM Defaults

In the main menu, go to **Settings → Defaults** and configure the LLM Defaults settings:

  * Select default models for agents and other components
  * Set default configurations for Crew Studio

Click `Save Settings` to apply your changes.

![LLM Defaults Configuration](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/llm-defaults.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=b773c2d7e8338e8dbf609ff45ce16eda)

## 

​

Using Crew Studio

Now that you’ve configured your LLM connection and default settings, you’re ready to start using Crew Studio!

1

Access Studio

Navigate to the **Studio** section in your CrewAI AMP dashboard.

2

Start a Conversation

Start a conversation with the Crew Assistant by describing the problem you want to solve:
    
    
    I need a crew that can research the latest AI developments and create a summary report.
    

The Crew Assistant will ask clarifying questions to better understand your requirements.

3

Review Generated Crew

Review the generated crew configuration, including:

  * Agents and their roles
  * Tasks to be performed
  * Required inputs
  * Tools to be used

This is your opportunity to refine the configuration before proceeding.

4

Deploy or Download

Once you’re satisfied with the configuration, you can:

  * Download the generated code for local customization
  * Deploy the crew directly to the CrewAI AMP platform
  * Modify the configuration and regenerate the crew

5

Test Your Crew

After deployment, test your crew with sample inputs to ensure it performs as expected.

For best results, provide clear, detailed descriptions of what you want your crew to accomplish. Include specific inputs and expected outputs in your description.

## 

​

Example Workflow

Here’s a typical workflow for creating a crew with Crew Studio:

1

Describe Your Problem

Start by describing your problem:
    
    
    I need a crew that can analyze financial news and provide investment recommendations
    

2

Answer Questions

Respond to clarifying questions from the Crew Assistant to refine your requirements.

3

Review the Plan

Review the generated crew plan, which might include:

  * A Research Agent to gather financial news
  * An Analysis Agent to interpret the data
  * A Recommendations Agent to provide investment advice

4

Approve or Modify

Approve the plan or request changes if necessary.

5

Download or Deploy

Download the code for customization or deploy directly to the platform.

6

Test and Refine

Test your crew with sample inputs and refine as needed.

## Need Help?

Contact our support team for assistance with Crew Studio or any other CrewAI AMP features.

Was this page helpful?

YesNo

[Update CrewPrevious](/en/enterprise/guides/update-crew)[OpenTelemetry ExportNext](/en/enterprise/guides/capture_telemetry_logs)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)