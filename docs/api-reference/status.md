# Source: https://docs.crewai.com/en/api-reference/status

Getting Started

# GET /status/{kickoff_id}


Get execution status


GET

https://your-actual-crew-name.crewai.comhttps://my-travel-crew.crewai.comhttps://content-creation-crew.crewai.comhttps://research-assistant-crew.crewai.com

/

status

/

{kickoff_id}

Try it

Get Execution Status

cURL
    
    
    curl --request GET \
      --url https://your-actual-crew-name.crewai.com/status/{kickoff_id} \
      --header 'Authorization: Bearer <token>'

200

running
    
    
    {
      "status": "running",
      "current_task": "research_task",
      "progress": {
        "completed_tasks": 1,
        "total_tasks": 3
      }
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

#### Path Parameters

​

kickoff_id

string<uuid>

required

The kickoff ID returned from the /kickoff endpoint

Example:

`"abcd1234-5678-90ef-ghij-klmnopqrstuv"`

#### Response

200

application/json

Successfully retrieved execution status

  * Option 1

  * Option 2

  * Option 3

​

status

enum<string>

Available options:

`running`

Example:

`"running"`

​

current_task

string

Name of the currently executing task

Example:

`"research_task"`

​

progress

object

Show child attributes

Was this page helpful?

YesNo

[POST /resumePrevious](/en/api-reference/resume)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)