# Source: https://docs.crewai.com/en/enterprise/guides/outlook-trigger

Triggers

# Outlook Trigger


Launch automations from Outlook emails and calendar updates


## 

​

Overview

Automate responses when Outlook delivers a new message or when an event is removed from the calendar. Teams commonly route escalations, file tickets, or alert attendees of cancellations.

Connect Outlook in **Tools & Integrations** and ensure the trigger is enabled for your deployment.

## 

​

Enabling the Outlook Trigger

  1. Open your deployment in CrewAI AMP
  2. Go to the **Triggers** tab
  3. Locate **Outlook** and switch the toggle to enable

![Enable or disable triggers with toggle](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/outlook-trigger.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=f8a739ad0963ccddafeed60f21366628)

## 

​

Example: Summarize a new email
    
    
    from outlook_message_crew import OutlookMessageTrigger
    
    crew = OutlookMessageTrigger().crew()
    crew.kickoff({
        "crewai_trigger_payload": outlook_payload,
    })
    

The crew extracts sender details, subject, body preview, and attachments before generating a structured response.

## 

​

Testing Locally

Test your Outlook trigger integration locally using the CrewAI CLI:
    
    
    # View all available triggers
    crewai triggers list
    
    # Simulate an Outlook trigger with realistic payload
    crewai triggers run microsoft_outlook/email_received
    

The `crewai triggers run` command will execute your crew with a complete Outlook payload, allowing you to test your parsing logic before deployment.

Use `crewai triggers run microsoft_outlook/email_received` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.

## 

​

Troubleshooting

  * Verify the Outlook connector is still authorized; the subscription must be renewed periodically
  * Test locally with `crewai triggers run microsoft_outlook/email_received` to see the exact payload structure
  * If attachments are missing, confirm the webhook subscription includes the `includeResourceData` flag
  * Review execution logs when events fail to match—cancellation payloads lack attendee lists by design and the crew should account for that
  * Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

Was this page helpful?

YesNo

[Google Drive TriggerPrevious](/en/enterprise/guides/google-drive-trigger)[OneDrive TriggerNext](/en/enterprise/guides/onedrive-trigger)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)