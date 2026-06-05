# Source: https://docs.crewai.com/en/enterprise/guides/tool-repository

How-To Guides

# Tool Repository


Using the Tool Repository to manage your tools


## 

​

Overview

The Tool Repository is a package manager for CrewAI tools. It allows users to publish, install, and manage tools that integrate with CrewAI crews and flows. Tools can be:

  * **Private** : accessible only within your organization (default)
  * **Public** : accessible to all CrewAI users if published with the `--public` flag

The repository is not a version control system. Use Git to track code changes and enable collaboration.

## 

​

Prerequisites

Before using the Tool Repository, ensure you have:

  * A [CrewAI AMP](https://app.crewai.com) account
  * [CrewAI CLI](/en/concepts/cli#cli) installed
  * uv>=0.5.0 installed. Check out [how to upgrade](https://docs.astral.sh/uv/getting-started/installation/#upgrading-uv)
  * [Git](https://git-scm.com) installed and configured
  * Access permissions to publish or install tools in your CrewAI AMP organization

## 

​

Installing Tools

To install a tool:
    
    
    crewai tool install <tool-name>
    

This installs the tool and adds it to `pyproject.toml`. You can use the tool by importing it and adding it to your agents:
    
    
    from your_tool.tool import YourTool
    
    custom_tool = YourTool()
    
    researcher = Agent(
        role='Market Research Analyst',
        goal='Provide up-to-date market analysis of the AI industry',
        backstory='An expert analyst with a keen eye for market trends.',
        tools=[custom_tool],
        verbose=True
    )
    

## 

​

Adding other packages after installing a tool

After installing a tool from the CrewAI AMP Tool Repository, you need to use the `crewai uv` command to add other packages to your project. Using pure `uv` commands will fail due to authentication to tool repository being handled by the CLI. By using the `crewai uv` command, you can add other packages to your project without having to worry about authentication. Any `uv` command can be used with the `crewai uv` command, making it a powerful tool for managing your project’s dependencies without the hassle of managing authentication through environment variables or other methods. Say that you have installed a custom tool from the CrewAI AMP Tool Repository called “my-tool”:
    
    
    crewai tool install my-tool
    

And now you want to add another package to your project, you can use the following command:
    
    
    crewai uv add requests
    

Other commands like `uv sync` or `uv remove` can also be used with the `crewai uv` command:
    
    
    crewai uv sync
    
    
    
    crewai uv remove requests
    

This will add the package to your project and update `pyproject.toml` accordingly.

## 

​

Creating and Publishing Tools

To create a new tool project:
    
    
    crewai tool create <tool-name>
    

This generates a scaffolded tool project locally. After making changes, initialize a Git repository and commit the code:
    
    
    git init
    git add .
    git commit -m "Initial version"
    

To publish the tool:
    
    
    crewai tool publish
    

By default, tools are published as private. To make a tool public:
    
    
    crewai tool publish --public
    

For more details on how to build tools, see [Creating your own tools](/en/concepts/tools#creating-your-own-tools).

## 

​

Updating Tools

To update a published tool:

  1. Modify the tool locally
  2. Update the version in `pyproject.toml` (e.g., from `0.1.0` to `0.1.1`)
  3. Commit the changes and publish

    
    
    git commit -m "Update version to 0.1.1"
    crewai tool publish
    

## 

​

Deleting Tools

To delete a tool:

  1. Go to [CrewAI AMP](https://app.crewai.com)
  2. Navigate to **Tools**
  3. Select the tool
  4. Click **Delete**

Deletion is permanent. Deleted tools cannot be restored or re-installed.

## 

​

Security Checks

Every published version undergoes automated security checks, and are only available to install after they pass. You can check the security check status of a tool at: `CrewAI AMP > Tools > Your Tool > Versions`

## Need Help?

Contact our support team for assistance with API integration or troubleshooting.

Was this page helpful?

YesNo

[Vertex AI with Workload IdentityPrevious](/en/enterprise/guides/vertex-ai-workload-identity-setup)[Custom MCP ServersNext](/en/enterprise/guides/custom-mcp-server)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)