# Source: https://docs.crewai.com/en/enterprise/guides/google-drive-trigger

Triggers

# Google Drive Trigger


Respond to Google Drive file events with automated crews


## 

​

Overview

Trigger your automations when files are created, updated, or removed in Google Drive. Typical workflows include summarizing newly uploaded content, enforcing sharing policies, or notifying owners when critical files change.

Connect Google Drive in **Tools & Integrations** and confirm the trigger is enabled for the automation you want to monitor.

## 

​

Enabling the Google Drive Trigger

  1. Open your deployment in CrewAI AMP
  2. Go to the **Triggers** tab
  3. Locate **Google Drive** and switch the toggle to enable

![Enable or disable triggers with toggle](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/gdrive-trigger.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=caef65990821bbc38454b46ca8f7bc46)

## 

​

Example: Summarize file activity

The drive example crews parse the payload to extract file metadata, evaluate permissions, and publish a summary.
    
    
    from drive_file_crew import GoogleDriveFileTrigger
    
    crew = GoogleDriveFileTrigger().crew()
    crew.kickoff({
        "crewai_trigger_payload": drive_payload,
    })
    

## 

​

Testing Locally

Test your Google Drive trigger integration locally using the CrewAI CLI:
    
    
    # View all available triggers
    crewai triggers list
    
    # Simulate a Google Drive trigger with realistic payload
    crewai triggers run google_drive/file_changed
    

The `crewai triggers run` command will execute your crew with a complete Drive payload, allowing you to test your parsing logic before deployment.

Use `crewai triggers run google_drive/file_changed` (not `crewai run`) to simulate trigger execution during development. After deployment, your crew will automatically receive the trigger payload.

## 

​

Monitoring Executions

Track history and performance of triggered runs with the **Executions** list in the deployment dashboard.

![List of executions triggered by automation](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/list-executions.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=be7efd03eb810139e42a10815402158d)

## 

​

Troubleshooting

  * Verify Google Drive is connected and the trigger toggle is enabled
  * Test locally with `crewai triggers run google_drive/file_changed` to see the exact payload structure
  * If a payload is missing permission data, ensure the connected account has access to the file or folder
  * The trigger sends file IDs only; use the Drive API if you need to fetch binary content during the crew run
  * Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution

Was this page helpful?

YesNo

[Google Calendar TriggerPrevious](/en/enterprise/guides/google-calendar-trigger)[Outlook TriggerNext](/en/enterprise/guides/outlook-trigger)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)