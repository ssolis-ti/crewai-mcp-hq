# Source: https://docs.crewai.com/en/enterprise/guides/microsoft-teams-trigger

Triggers

# Microsoft Teams Trigger


Kick off crews from Microsoft Teams chat activity


## 

​

Overview

Use the Microsoft Teams trigger to start automations whenever a new chat is created. Common patterns include summarizing inbound requests, routing urgent messages to support teams, or creating follow-up tasks in other systems.

Confirm Microsoft Teams is connected under **Tools & Integrations** and enabled in the **Triggers** tab for your deployment.

## 

​

Enabling the Microsoft Teams Trigger

  1. Open your deployment in CrewAI AMP
  2. Go to the **Triggers** tab
  3. Locate **Microsoft Teams** and switch the toggle to enable

![Enable or disable triggers with toggle](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/msteams-trigger.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=21eced4a8a635d17e32dccbeaf4ac217)

## 

​

Example: Summarize a new chat thread
    
    
    from teams_chat_created_crew import MicrosoftTeamsChatTrigger
    
    crew = MicrosoftTeamsChatTrigger().crew()
    result = crew.kickoff({
        "crewai_trigger_payload": teams_payload,
    })
    print(result.raw)
    

The crew parses thread metadata (subject, created time, roster) and generates an action plan for the receiving team.

## 

​

Testing Locally

Test your Microsoft Teams trigger integration locally using the CrewAI CLI:
    
    
    # View all available triggers
    crewai triggers list
    
    # Simulate a Microsoft Teams trigger with realistic payload
    crewai triggers run microsoft_teams/teams_message_created
    

The `crewai triggers run` command will execute your crew with a complete Teams payload, allowing you to test your parsing logic before deployment.

Use `crewai triggers run microsoft_teams/teams_message_created` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.

## 

​

Troubleshooting

  * Ensure the Teams connection is active; it must be refreshed if the tenant revokes permissions
  * Test locally with `crewai triggers run microsoft_teams/teams_message_created` to see the exact payload structure
  * Confirm the webhook subscription in Microsoft 365 is still valid if payloads stop arriving
  * Review execution logs for payload shape mismatches—Graph notifications may omit fields when a chat is private or restricted
  * Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

Was this page helpful?

YesNo

[OneDrive TriggerPrevious](/en/enterprise/guides/onedrive-trigger)[Slack TriggerNext](/en/enterprise/guides/slack-trigger)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)