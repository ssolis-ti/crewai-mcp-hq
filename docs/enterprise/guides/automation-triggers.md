# Source: https://docs.crewai.com/en/enterprise/guides/automation-triggers

Triggers

# Triggers Overview


Understand how CrewAI AMP triggers work, how to manage them, and where to find integration-specific playbooks


CrewAI AMP triggers connect your automations to real-time events across the tools your teams already use. Instead of polling systems or relying on manual kickoffs, triggers listen for changes—new emails, calendar updates, CRM status changes—and immediately launch the crew or flow you specify.

![Automation Triggers Overview](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew_connectors.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=c31a4b9031f0f517fdce3baa48471f58)

### 

​

Integration Playbooks

Deep-dive guides walk through setup and sample workflows for each integration:

## Gmail Trigger

[Enable crews when emails arrive or threads update.](/en/enterprise/guides/gmail-trigger)

## Google Calendar Trigger

[React to calendar events as they are created, updated, or cancelled.](/en/enterprise/guides/google-calendar-trigger)

## Google Drive Trigger

[Handle Drive file uploads, edits, and deletions.](/en/enterprise/guides/google-drive-trigger)

## Outlook Trigger

[Automate responses to new Outlook messages and calendar updates.](/en/enterprise/guides/outlook-trigger)

## OneDrive Trigger

[Audit file activity and sharing changes in OneDrive.](/en/enterprise/guides/onedrive-trigger)

## Microsoft Teams Trigger

[Kick off workflows when new Teams chats start.](/en/enterprise/guides/microsoft-teams-trigger)

## HubSpot Trigger

[Launch automations from HubSpot workflows and lifecycle events.](/en/enterprise/guides/hubspot-trigger)

## Salesforce Trigger

[Connect Salesforce processes to CrewAI for CRM automation.](/en/enterprise/guides/salesforce-trigger)

## Slack Trigger

[Start crews directly from Slack slash commands.](/en/enterprise/guides/slack-trigger)

## Zapier Trigger

[Bridge CrewAI with thousands of Zapier-supported apps.](/en/enterprise/guides/zapier-trigger)

## 

​

Trigger Capabilities

With triggers, you can:

  * **Respond to real-time events** \- Automatically execute workflows when specific conditions are met
  * **Integrate with external systems** \- Connect with platforms like Gmail, Outlook, OneDrive, JIRA, Slack, Stripe and more
  * **Scale your automation** \- Handle high-volume events without manual intervention
  * **Maintain context** \- Access trigger data within your crews and flows

## 

​

Managing Triggers

### 

​

Viewing Available Triggers

To access and manage your automation triggers:

  1. Navigate to your deployment in the CrewAI dashboard
  2. Click on the **Triggers** tab to view all available trigger integrations

![List of available automation triggers](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/list-available-triggers.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=5de0e753bcb9db2e7f2e126354741de8)

This view shows all the trigger integrations available for your deployment, along with their current connection status.

### 

​

Enabling and Disabling Triggers

Each trigger can be easily enabled or disabled using the toggle switch:

![Enable or disable triggers with toggle](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/trigger-selected.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=10b3ee6296f323168473593b64a1e4c8)

  * **Enabled (blue toggle)** : The trigger is active and will automatically execute your deployment when the specified events occur
  * **Disabled (gray toggle)** : The trigger is inactive and will not respond to events

Simply click the toggle to change the trigger state. Changes take effect immediately.

### 

​

Monitoring Trigger Executions

Track the performance and history of your triggered executions:

![List of executions triggered by automation](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/list-executions.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=be7efd03eb810139e42a10815402158d)

## 

​

Building Trigger-Driven Automations

Before building your automation, it’s helpful to understand the structure of trigger payloads that your crews and flows will receive.

### 

​

Trigger Setup Checklist

Before wiring a trigger into production, make sure you:

  * Connect the integration under **Tools & Integrations** and complete any OAuth or API key steps
  * Enable the trigger toggle on the deployment that should respond to events
  * Provide any required environment variables (API tokens, tenant IDs, shared secrets)
  * Create or update tasks that can parse the incoming payload within the first crew task or flow step
  * Decide whether to pass trigger context automatically using `allow_crewai_trigger_context`
  * Set up monitoring—webhook logs, CrewAI execution history, and optional external alerting

### 

​

Testing Triggers Locally with CLI

The CrewAI CLI provides powerful commands to help you develop and test trigger-driven automations without deploying to production.

#### 

​

List Available Triggers

View all available triggers for your connected integrations:
    
    
    crewai triggers list
    

This command displays all triggers available based on your connected integrations, showing:

  * Integration name and connection status
  * Available trigger types
  * Trigger names and descriptions

#### 

​

Simulate Trigger Execution

Test your crew with realistic trigger payloads before deployment:
    
    
    crewai triggers run <trigger_name>
    

For example:
    
    
    crewai triggers run microsoft_onedrive/file_changed
    

This command:

  * Executes your crew locally
  * Passes a complete, realistic trigger payload
  * Simulates exactly how your crew will be called in production

**Important Development Notes:**

  * Use `crewai triggers run <trigger>` to simulate trigger execution during development
  * Using `crewai run` will NOT simulate trigger calls and won’t pass the trigger payload
  * After deployment, your crew will be executed with the actual trigger payload
  * If your crew expects parameters that aren’t in the trigger payload, execution may fail

### 

​

Triggers with Crew

Your existing crew definitions work seamlessly with triggers, you just need to have a task to parse the received payload:
    
    
    @CrewBase
    class MyAutomatedCrew:
        @agent
        def researcher(self) -> Agent:
            return Agent(
                config=self.agents_config['researcher'],
            )
    
        @task
        def parse_trigger_payload(self) -> Task:
            return Task(
                config=self.tasks_config['parse_trigger_payload'],
                agent=self.researcher(),
            )
    
        @task
        def analyze_trigger_content(self) -> Task:
            return Task(
                config=self.tasks_config['analyze_trigger_data'],
                agent=self.researcher(),
            )
    

The crew will automatically receive and can access the trigger payload through the standard CrewAI context mechanisms.

Crew and Flow inputs can include `crewai_trigger_payload`. CrewAI automatically injects this payload: - Tasks: appended to the first task’s description by default (“Trigger Payload: ”) - Control via `allow_crewai_trigger_context`: set `True` to always inject, `False` to never inject - Flows: any `@start()` method that accepts a `crewai_trigger_payload` parameter will receive it

### 

​

Integration with Flows

For flows, you have more control over how trigger data is handled:

#### 

​

Accessing Trigger Payload

All `@start()` methods in your flows will accept an additional parameter called `crewai_trigger_payload`:
    
    
    from crewai.flow import Flow, start, listen
    
    class MyAutomatedFlow(Flow):
        @start()
        def handle_trigger(self, crewai_trigger_payload: dict = None):
            """
            This start method can receive trigger data
            """
            if crewai_trigger_payload:
                # Process the trigger data
                trigger_id = crewai_trigger_payload.get('id')
                event_data = crewai_trigger_payload.get('payload', {})
    
                # Store in flow state for use by other methods
                self.state.trigger_id = trigger_id
                self.state.trigger_type = event_data
    
                return event_data
    
            # Handle manual execution
            return None
    
        @listen(handle_trigger)
        def process_data(self, trigger_data):
            """
            Process the data from the trigger
            """
            # ... process the trigger
    

#### 

​

Triggering Crews from Flows

When kicking off a crew within a flow that was triggered, pass the trigger payload as it:
    
    
    @start()
    def delegate_to_crew(self, crewai_trigger_payload: dict = None):
        """
        Delegate processing to a specialized crew
        """
        crew = MySpecializedCrew()
    
        # Pass the trigger payload to the crew
        result = crew.crew().kickoff(
            inputs={
                'a_custom_parameter': "custom_value",
                'crewai_trigger_payload': crewai_trigger_payload
            },
        )
    
        return result
    

## 

​

Troubleshooting

**Trigger not firing:**

  * Verify the trigger is enabled in your deployment’s Triggers tab
  * Check integration connection status under Tools & Integrations
  * Ensure all required environment variables are properly configured

**Execution failures:**

  * Check the execution logs for error details
  * Use `crewai triggers run <trigger_name>` to test locally and see the exact payload structure
  * Verify your crew can handle the `crewai_trigger_payload` parameter
  * Ensure your crew doesn’t expect parameters that aren’t included in the trigger payload

**Development issues:**

  * Always test with `crewai triggers run <trigger>` before deploying to see the complete payload
  * Remember that `crewai run` does NOT simulate trigger calls—use `crewai triggers run` instead
  * Use `crewai triggers list` to verify which triggers are available for your connected integrations
  * After deployment, your crew will receive the actual trigger payload, so test thoroughly locally first

Automation triggers transform your CrewAI deployments into responsive, event-driven systems that can seamlessly integrate with your existing business processes and tools.

Was this page helpful?

YesNo

[Zendesk IntegrationPrevious](/en/enterprise/integrations/zendesk)[Gmail TriggerNext](/en/enterprise/guides/gmail-trigger)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)