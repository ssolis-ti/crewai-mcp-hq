# Source: https://docs.crewai.com/en/api-reference/resume

Getting Started

# POST /resume


Resume crew execution with human feedback


POST

https://your-actual-crew-name.crewai.comhttps://my-travel-crew.crewai.comhttps://content-creation-crew.crewai.comhttps://research-assistant-crew.crewai.com

/

resume

Try it

cURL

approve_and_continue
    
    
    curl --request POST \
      --url https://your-actual-crew-name.crewai.com/resume \
      --header 'Authorization: Bearer <token>' \
      --header 'Content-Type: application/json' \
      --data '
    {
      "execution_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
      "task_id": "research_task",
      "human_feedback": "Excellent research! Proceed to the next task.",
      "is_approve": true,
      "taskWebhookUrl": "https://api.example.com/webhooks/task",
      "stepWebhookUrl": "https://api.example.com/webhooks/step",
      "crewWebhookUrl": "https://api.example.com/webhooks/crew"
    }
    '

200

resumed
    
    
    {
      "status": "resumed",
      "message": "Execution resumed successfully"
    }

#### Authorizations

​

Authorization

string

header

required

📋 Reference Documentation \- _The tokens shown in examples are placeholders for reference only._

Use your actual Bearer Token or User Bearer Token from the CrewAI AMP dashboard for real API calls.

Bearer Token: Organization-level access for full crew operations User Bearer Token: User-scoped access with limited permissions

#### Body

application/json

​

execution_id

string<uuid>

required

The unique identifier for the crew execution (from kickoff)

Example:

`"abcd1234-5678-90ef-ghij-klmnopqrstuv"`

​

task_id

string

required

The ID of the task that requires human feedback

Example:

`"research_task"`

​

human_feedback

string

required

Your feedback on the task output. This will be incorporated as additional context for subsequent task executions.

Example:

`"Great research! Please add more details about recent developments in the field."`

​

is_approve

boolean

required

Whether you approve the task output: true = positive feedback (continue), false = negative feedback (retry task)

Example:

`true`

​

taskWebhookUrl

string<uri>

Callback URL executed after each task completion. MUST be provided to continue receiving task notifications.

Example:

`"https://your-server.com/webhooks/task"`

​

stepWebhookUrl

string<uri>

Callback URL executed after each agent thought/action. MUST be provided to continue receiving step notifications.

Example:

`"https://your-server.com/webhooks/step"`

​

crewWebhookUrl

string<uri>

Callback URL executed when the crew execution completes. MUST be provided to receive completion notification.

Example:

`"https://your-server.com/webhooks/crew"`

#### Response

200

application/json

Execution resumed successfully

​

status

enum<string>

Status of the resumed execution

Available options:

`resumed`,

`retrying`,

`completed`

Example:

`"resumed"`

​

message

string

Human-readable message about the resume operation

Example:

`"Execution resumed successfully"`

Was this page helpful?

YesNo

[POST /kickoffPrevious](/en/api-reference/kickoff)[GET /status/{kickoff_id}Next](/en/api-reference/status)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)