# Source: https://docs.crewai.com/en/enterprise/guides/monorepo-deployments

How-To Guides

# Monorepo Deployments


Deploy a Crew or Flow from a subfolder in a larger repository


Use a working directory when your Crew or Flow lives inside a larger repository. CrewAI AMP validates, builds, tests, and runs the automation from that subfolder instead of the repository root.

## 

​

When to Use This

Monorepo deployments are useful when one repository contains multiple automations, shared packages, or other application code:
    
    
    company-ai/
    |-- uv.lock
    |-- packages/
    |   `-- shared_tools/
    `-- crews/
        |-- support_agent/
        |   |-- pyproject.toml
        |   `-- src/
        |       `-- support_agent/
        |           |-- main.py
        |           `-- crew.py
        `-- research_flow/
            |-- pyproject.toml
            `-- src/
                `-- research_flow/
                    `-- main.py
    

To deploy `support_agent`, set the working directory to:
    
    
    crews/support_agent
    

AMP still pulls or uploads the whole repository, but it treats the selected folder as the automation project root.

## 

​

What the Working Directory Controls

When a working directory is set, AMP uses that folder for:

  * Project validation, including `pyproject.toml`, `src/`, and the Crew or Flow entry point
  * Dependency installation with `uv`
  * The running process working directory
  * The `CREW_ROOT_DIR` environment variable

Leaving the field empty keeps the existing behavior and uses the repository root.

## 

​

Supported Sources

You can set a working directory when creating a deployment from:

  * A connected GitHub repository
  * A Git repository configured in AMP
  * A ZIP upload

Configure working directories in the AMP web interface. The `crewai deploy create` CLI flow does not prompt for this field.

You can also add or change the working directory on an existing deployment from the deployment’s **Settings** page. The change takes effect on the next deploy.

Working directories and auto-deploy cannot be used together. If a deployment has a working directory, auto-deploy is disabled for that deployment. Turn auto-deploy off before setting a working directory.

## 

​

Configure a New Deployment

1

Open Deploy from Code

In CrewAI AMP, create a new deployment and choose your source: GitHub, Git Repository, or ZIP upload.

2

Select the repository, branch, or ZIP file

Choose the repository and branch that contain your monorepo, or upload a ZIP file whose root contains the monorepo contents.

3

Open Advanced settings

Expand the **Advanced** section in the deploy form.

4

Enter the working directory

Enter the path from the repository root to the Crew or Flow project:
    
    
    crews/support_agent
    

Do not include a leading slash.

5

Deploy

Add any required environment variables, then start the deployment.

## 

​

Configure an Existing Deployment

1

Open the deployment settings

Go to your automation in AMP and open **Settings**.

2

Turn off auto-deploy if needed

If auto-deploy is enabled, disable it first. The working directory field is unavailable while auto-deploy is on.

3

Set the working directory

In **Basic settings** , enter the subfolder path, such as:
    
    
    crews/support_agent
    

4

Redeploy

Save the setting and redeploy the automation. The new working directory is used on the next deploy.

## 

​

Path Rules

The working directory must be a relative path inside the repository or ZIP root.

Rule| Example  
---|---  
Use a relative path| `crews/support_agent`  
Do not start with `/`| `/crews/support_agent` is invalid  
Do not use `.` or `..` path segments| `crews/../support_agent` is invalid  
Use only letters, numbers, dashes, underscores, dots, and forward slashes| `crews/support agent` is invalid  
Keep the path at 255 characters or fewer| Longer paths are rejected  
  
AMP trims leading and trailing whitespace, collapses repeated slashes, and removes trailing slashes. A blank value uses the repository root.

## 

​

Lock Files and UV Workspaces

The selected folder must contain the automation’s `pyproject.toml` and `src/` directory. A `uv.lock` or `poetry.lock` file can live either in the selected folder or at the repository root. This supports both common monorepo layouts:

  * Project lock file

  * Workspace lock file

    
    
    company-ai/
    `-- crews/
        `-- support_agent/
            |-- pyproject.toml
            |-- uv.lock
            `-- src/
                `-- support_agent/
                    `-- main.py
    
    
    
    company-ai/
    |-- uv.lock
    |-- packages/
    |   `-- shared_tools/
    `-- crews/
        `-- support_agent/
            |-- pyproject.toml
            `-- src/
                `-- support_agent/
                    `-- main.py
    

If your automation imports shared packages from elsewhere in the monorepo, declare those packages in `pyproject.toml` using UV workspace, path, or source configuration. AMP runs the automation from the selected folder, so shared code should be installed as a dependency instead of relying on the repository root being on the Python path.

## 

​

Troubleshooting

### 

​

Working Directory Not Found

Check that the path is relative to the repository or ZIP root. For ZIP uploads, the ZIP contents must include the working directory path exactly as entered.

### 

​

Missing pyproject.toml

The working directory should point to the Crew or Flow project folder, not just to a parent folder that contains several projects.

### 

​

Missing uv.lock or poetry.lock

Commit a lock file either in the selected project folder or in the repository root. For UV workspaces, keeping `uv.lock` at the workspace root is supported.

### 

​

Auto-Deploy Is Unavailable

Auto-deploy is disabled while a working directory is set. Use manual redeploys or trigger redeployments from CI/CD with the AMP API instead.

## Deploy to AMP

Continue with the deployment guide after choosing your monorepo working directory.

Was this page helpful?

YesNo

[Deploy to AMPPrevious](/en/enterprise/guides/deploy-to-amp)[Private Package RegistriesNext](/en/enterprise/guides/private-package-registry)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)