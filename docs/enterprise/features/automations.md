# Source: https://docs.crewai.com/en/enterprise/features/automations

Build

# Automations


Manage, deploy, and monitor your live crews (automations) in one place.


## 

​

Overview

Automations is the live operations hub for your deployed crews. Use it to deploy from GitHub or a ZIP file, manage environment variables, re‑deploy when needed, and monitor the status of each automation.

![Automations Overview](https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/automations-overview.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=a7d0655da82c70b0ca152715cb8253f4)

## 

​

Deployment Methods

### 

​

Deploy from GitHub

Use this for version‑controlled projects and continuous deployment.

1

Connect GitHub

Click **Configure GitHub** and authorize access.

2

Select Repository & Branch

Choose the **Repository** and **Branch** you want to deploy from.

3

Enable Auto‑deploy (optional)

Turn on **Automatically deploy new commits** to ship updates on every push.

4

Add Environment Variables

Add secrets individually or use **Bulk View** for multiple variables.

5

Deploy

Click **Deploy** to create your live automation.

![GitHub Deployment](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/deploy-from-github.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=4fb72dc68799d5a0c35e2e74f1a7cc6c)

### 

​

Deploy from ZIP

Ship quickly without Git—upload a compressed package of your project.

1

Choose File

Select the ZIP archive from your computer.

2

Add Environment Variables

Provide any required variables or keys.

3

Deploy

Click **Deploy** to create your live automation.

![ZIP Deployment](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/deploy-from-zip.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=8cea74868a553d34b0aa182ad5489099)

## 

​

Automations Dashboard

The table lists all live automations with key details:

  * **CREW** : Automation name
  * **STATUS** : Online / Failed / In Progress
  * **URL** : Endpoint for kickoff/status
  * **TOKEN** : Automation token
  * **ACTIONS** : Re‑deploy, delete, and more

Use the top‑right controls to filter and search:

  * Search by name
  * Filter by **Status**
  * Filter by **Source** (GitHub / Studio / ZIP)

Once deployed, you can view the automation details and have the **Options** dropdown menu to `chat with this crew`, `Export React Component` and `Export as MCP`.

![Automations Table](https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/automations-table.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=f7fb571e8473f5cb7940c3e3bb34f95c)

## 

​

Best Practices

  * Prefer GitHub deployments for version control and CI/CD
  * Use re‑deploy to roll forward after code or config updates or set it to auto-deploy on every push

## 

​

Related

## Deploy a Crew

Deploy a Crew from GitHub or ZIP file.

## Automation Triggers

Trigger automations via webhooks or API.

## Webhook Automation

Stream real-time events and updates to your systems.

Was this page helpful?

YesNo

[CrewAI AMPPrevious](/en/enterprise/introduction)[Crew StudioNext](/en/enterprise/features/crew-studio)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)