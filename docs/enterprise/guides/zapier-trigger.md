# Source: https://docs.crewai.com/en/enterprise/guides/zapier-trigger

Triggers

# Zapier Trigger


Trigger CrewAI crews from Zapier workflows to automate cross-app workflows


This guide will walk you through the process of setting up Zapier triggers for CrewAI AMP, allowing you to automate workflows between CrewAI AMP and other applications.

## 

​

Prerequisites

  * A CrewAI AMP account
  * A Zapier account
  * A Slack account (for this specific example)

## 

​

Step-by-Step Setup

1

Set Up the Slack Trigger

  * In Zapier, create a new Zap.

![Zapier 1](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-1.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=d7602ce90ddcd4f0365fd821f4ff1ff2)

2

Choose Slack as your trigger app

![Zapier 2](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-2.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e5cdc5705b87b4e06178fa12fb5ef64b)

  * Select `New Pushed Message` as the Trigger Event.
  * Connect your Slack account if you haven’t already.

3

Configure the CrewAI AMP Action

  * Add a new action step to your Zap.
  * Choose CrewAI+ as your action app and Kickoff as the Action Event

![Zapier 5](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-3.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e52e2404a73623df30d125873bd8ff42)

4

Connect your CrewAI AMP account

  * Connect your CrewAI AMP account.
  * Select the appropriate Crew for your workflow.

![Zapier 6](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-4.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=13aac37fdb67ee1c9f841a602ac3abf5)

  * Configure the inputs for the Crew using the data from the Slack message.

5

Format the CrewAI AMP Output

  * Add another action step to format the text output from CrewAI AMP.
  * Use Zapier’s formatting tools to convert the Markdown output to HTML.

![Zapier 8](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-5.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e772b4803dfffe4de12d9a7ea21484ce)

![Zapier 9](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-6.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=9fa4a34d5c511b6bb76f276348928699)

6

Send the Output via Email

  * Add a final action step to send the formatted output via email.
  * Choose your preferred email service (e.g., Gmail, Outlook).
  * Configure the email details, including recipient, subject, and body.
  * Insert the formatted CrewAI AMP output into the email body.

![Zapier 7](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-7.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=f3d2a0c67b29888cfdc5b0d81ba5c29b)

7

Kick Off the crew from Slack

  * Enter the text in your Slack channel

![Zapier 10](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-7b.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=916dbdffd171dc52c40ebc74cc39a38f)

  * Select the 3 ellipsis button and then chose Push to Zapier

![Zapier 11](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-8.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=a6a6e2fd0b0b239af4c17ae1f34ad720)

8

Select the crew and then Push to Kick Off

![Zapier 12](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/enterprise/zapier-9.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=eda865381d7121d38025c2b13abeccdf)

## 

​

Tips for Success

  * Ensure that your CrewAI AMP inputs are correctly mapped from the Slack message.
  * Test your Zap thoroughly before turning it on to catch any potential issues.
  * Consider adding error handling steps to manage potential failures in the workflow.

By following these steps, you’ll have successfully set up Zapier triggers for CrewAI AMP, allowing for automated workflows triggered by Slack messages and resulting in email notifications with CrewAI AMP output.

Was this page helpful?

YesNo

[Salesforce TriggerPrevious](/en/enterprise/guides/salesforce-trigger)[Build CrewNext](/en/enterprise/guides/build-crew)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)