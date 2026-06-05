# Source: https://docs.crewai.com/en/api-reference/kickoff

Getting Started

# POST /kickoff


Start a crew execution


POST

https://your-actual-crew-name.crewai.comhttps://my-travel-crew.crewai.comhttps://content-creation-crew.crewai.comhttps://research-assistant-crew.crewai.com

/

kickoff

Try it

cURL

travel_planning
    
    
    curl --request POST \
      --url https://your-actual-crew-name.crewai.com/kickoff \
      --header 'Authorization: Bearer <token>' \
      --header 'Content-Type: application/json' \
      --data '
    {
      "inputs": {
        "budget": "1000 USD",
        "interests": "games, tech, ai, relaxing hikes, amazing food",
        "duration": "7 days",
        "age": "35"
      },
      "meta": {
        "requestId": "travel-req-123",
        "source": "web-app"
      }
    }
    '

200

400

401

422

500
    
    
    {
      "kickoff_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv"
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

inputs

object

required

Key-value pairs of all required inputs for your crew

Show child attributes

Example:
    
    
    {  
      "budget": "1000 USD",  
      "interests": "games, tech, ai, relaxing hikes, amazing food",  
      "duration": "7 days",  
      "age": "35"  
    }

​

meta

object

Additional metadata to pass to the crew

Example:
    
    
    {  
      "requestId": "user-request-12345",  
      "source": "mobile-app"  
    }

​

taskWebhookUrl

string<uri>

Callback URL executed after each task completion

Example:

`"https://your-server.com/webhooks/task"`

​

stepWebhookUrl

string<uri>

Callback URL executed after each agent thought/action

Example:

`"https://your-server.com/webhooks/step"`

​

crewWebhookUrl

string<uri>

Callback URL executed when the crew execution completes

Example:

`"https://your-server.com/webhooks/crew"`

#### Response

200

application/json

Crew execution started successfully

​

kickoff_id

string<uuid>

Unique identifier for tracking this execution

Example:

`"abcd1234-5678-90ef-ghij-klmnopqrstuv"`

Was this page helpful?

YesNo

[GET /inputsPrevious](/en/api-reference/inputs)[POST /resumeNext](/en/api-reference/resume)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)