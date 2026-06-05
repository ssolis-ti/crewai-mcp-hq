# Source: https://docs.crewai.com/en/enterprise/guides/private-package-registry

How-To Guides

# Private Package Registries


Install private Python packages from authenticated PyPI registries in CrewAI AMP


This guide covers how to configure your CrewAI project to install Python packages from private PyPI registries (Azure DevOps Artifacts, GitHub Packages, GitLab, AWS CodeArtifact, etc.) when deploying to CrewAI AMP.

## 

​

When You Need This

If your project depends on internal or proprietary Python packages hosted on a private registry rather than the public PyPI, you’ll need to:

  1. Tell UV **where** to find the package (an index URL)
  2. Tell UV **which** packages come from that index (a source mapping)
  3. Provide **credentials** so UV can authenticate during install

CrewAI AMP uses [UV](https://docs.astral.sh/uv/) for dependency resolution and installation. UV supports authenticated private registries through `pyproject.toml` configuration combined with environment variables for credentials.

## 

​

Step 1: Configure pyproject.toml

Three pieces work together in your `pyproject.toml`:

### 

​

1a. Declare the dependency

Add the private package to your `[project.dependencies]` like any other dependency:
    
    
    [project]
    dependencies = [
        "crewai[tools]>=0.100.1,<1.0.0",
        "my-private-package>=1.2.0",
    ]
    

### 

​

1b. Define the index

Register your private registry as a named index under `[[tool.uv.index]]`:
    
    
    [[tool.uv.index]]
    name = "my-private-registry"
    url = "https://pkgs.dev.azure.com/my-org/_packaging/my-feed/pypi/simple/"
    explicit = true
    

The `name` field is important — UV uses it to construct the environment variable names for authentication (see Step 2 below).Setting `explicit = true` means UV won’t search this index for every package — only the ones you explicitly map to it in `[tool.uv.sources]`. This avoids unnecessary queries against your private registry and protects against dependency confusion attacks.

### 

​

1c. Map the package to the index

Tell UV which packages should be resolved from your private index using `[tool.uv.sources]`:
    
    
    [tool.uv.sources]
    my-private-package = { index = "my-private-registry" }
    

### 

​

Complete example
    
    
    [project]
    name = "my-crew-project"
    version = "0.1.0"
    requires-python = ">=3.10,<=3.13"
    dependencies = [
        "crewai[tools]>=0.100.1,<1.0.0",
        "my-private-package>=1.2.0",
    ]
    
    [tool.crewai]
    type = "crew"
    
    [[tool.uv.index]]
    name = "my-private-registry"
    url = "https://pkgs.dev.azure.com/my-org/_packaging/my-feed/pypi/simple/"
    explicit = true
    
    [tool.uv.sources]
    my-private-package = { index = "my-private-registry" }
    

After updating `pyproject.toml`, regenerate your lock file:
    
    
    uv lock
    

Always commit the updated `uv.lock` along with your `pyproject.toml` changes. The lock file is required for deployment — see [Prepare for Deployment](/en/enterprise/guides/prepare-for-deployment).

## 

​

Step 2: Set Authentication Credentials

UV authenticates against private indexes using environment variables that follow a naming convention based on the index name you defined in `pyproject.toml`:
    
    
    UV_INDEX_{UPPER_NAME}_USERNAME
    UV_INDEX_{UPPER_NAME}_PASSWORD
    

Where `{UPPER_NAME}` is your index name converted to **uppercase** with **hyphens replaced by underscores**. For example, an index named `my-private-registry` uses:

Variable| Value  
---|---  
`UV_INDEX_MY_PRIVATE_REGISTRY_USERNAME`| Your registry username or token name  
`UV_INDEX_MY_PRIVATE_REGISTRY_PASSWORD`| Your registry password or token/PAT  
  
These environment variables **must** be added via the CrewAI AMP **Environment Variables** settings — either globally or at the deployment level. They cannot be set in `.env` files or hardcoded in your project.See Setting Environment Variables in AMP below.

## 

​

Registry Provider Reference

The table below shows the index URL format and credential values for common registry providers. Replace placeholder values with your actual organization and feed details.

Provider| Index URL| Username| Password  
---|---|---|---  
**Azure DevOps Artifacts**| `https://pkgs.dev.azure.com/{org}/_packaging/{feed}/pypi/simple/`| Any non-empty string (e.g. `token`)| Personal Access Token (PAT) with Packaging Read scope  
**GitHub Packages**| `https://pypi.pkg.github.com/{owner}/simple/`| GitHub username| Personal Access Token (classic) with `read:packages` scope  
**GitLab Package Registry**| `https://gitlab.com/api/v4/projects/{project_id}/packages/pypi/simple/`| `__token__`| Project or Personal Access Token with `read_api` scope  
**AWS CodeArtifact**|  Use the URL from `aws codeartifact get-repository-endpoint`| `aws`| Token from `aws codeartifact get-authorization-token`  
**Google Artifact Registry**| `https://{region}-python.pkg.dev/{project}/{repo}/simple/`| `_json_key_base64`| Base64-encoded service account key  
**JFrog Artifactory**| `https://{instance}.jfrog.io/artifactory/api/pypi/{repo}/simple/`| Username or email| API key or identity token  
**Self-hosted (devpi, Nexus, etc.)**|  Your registry’s simple API URL| Registry username| Registry password  
  
For **AWS CodeArtifact** , the authorization token expires periodically. You’ll need to refresh the `UV_INDEX_*_PASSWORD` value when it expires. Consider automating this in your CI/CD pipeline.

## 

​

Setting Environment Variables in AMP

Private registry credentials must be configured as environment variables in CrewAI AMP. You have two options:

  * Web Interface

  * CLI Deployment

  1. Log in to [CrewAI AMP](https://app.crewai.com)
  2. Navigate to your automation
  3. Open the **Environment Variables** tab
  4. Add each variable (`UV_INDEX_*_USERNAME` and `UV_INDEX_*_PASSWORD`) with its value

See the [Deploy to AMP — Set Environment Variables](/en/enterprise/guides/deploy-to-amp#set-environment-variables) step for details.

Add the variables to your local `.env` file before running `crewai deploy create`. The CLI will securely transfer them to the platform:
    
    
    # .env
    OPENAI_API_KEY=sk-...
    UV_INDEX_MY_PRIVATE_REGISTRY_USERNAME=token
    UV_INDEX_MY_PRIVATE_REGISTRY_PASSWORD=your-pat-here
    
    
    
    crewai deploy create
    

**Never** commit credentials to your repository. Use AMP environment variables for all secrets. The `.env` file should be listed in `.gitignore`.

To update credentials on an existing deployment, see [Update Your Crew — Environment Variables](/en/enterprise/guides/update-crew).

## 

​

How It All Fits Together

When CrewAI AMP builds your automation, the resolution flow works like this:

1

Build starts

AMP pulls your repository and reads `pyproject.toml` and `uv.lock`.

2

UV resolves dependencies

UV reads `[tool.uv.sources]` to determine which index each package should come from.

3

UV authenticates

For each private index, UV looks up `UV_INDEX_{NAME}_USERNAME` and `UV_INDEX_{NAME}_PASSWORD` from the environment variables you configured in AMP.

4

Packages install

UV downloads and installs all packages — both public (from PyPI) and private (from your registry).

5

Automation runs

Your crew or flow starts with all dependencies available.

## 

​

Troubleshooting

### 

​

Authentication Errors During Build

**Symptom** : Build fails with `401 Unauthorized` or `403 Forbidden` when resolving a private package. **Check** :

  * The `UV_INDEX_*` environment variable names match your index name exactly (uppercased, hyphens → underscores)
  * Credentials are set in AMP environment variables, not just in a local `.env`
  * Your token/PAT has the required read permissions for the package feed
  * The token hasn’t expired (especially relevant for AWS CodeArtifact)

### 

​

Package Not Found

**Symptom** : `No matching distribution found for my-private-package`. **Check** :

  * The index URL in `pyproject.toml` ends with `/simple/`
  * The `[tool.uv.sources]` entry maps the correct package name to the correct index name
  * The package is actually published to your private registry
  * Run `uv lock` locally with the same credentials to verify resolution works

### 

​

Lock File Conflicts

**Symptom** : `uv lock` fails or produces unexpected results after adding a private index. **Solution** : Set the credentials locally and regenerate:
    
    
    export UV_INDEX_MY_PRIVATE_REGISTRY_USERNAME=token
    export UV_INDEX_MY_PRIVATE_REGISTRY_PASSWORD=your-pat
    uv lock
    

Then commit the updated `uv.lock`.

## 

​

Related Guides

## Prepare for Deployment

Verify project structure and dependencies before deploying.

## Deploy to AMP

Deploy your crew or flow and configure environment variables.

## Update Your Crew

Update environment variables and push changes to a running deployment.

Was this page helpful?

YesNo

[Monorepo DeploymentsPrevious](/en/enterprise/guides/monorepo-deployments)[Kickoff CrewNext](/en/enterprise/guides/kickoff-crew)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)