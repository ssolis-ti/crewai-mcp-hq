# Source: https://docs.crewai.com/en/api-reference/inputs

Getting Started

# GET /inputs


Get required inputs for your crew


GET

https://your-actual-crew-name.crewai.comhttps://my-travel-crew.crewai.comhttps://content-creation-crew.crewai.comhttps://research-assistant-crew.crewai.com

/

inputs

Try it

Get Required Inputs

cURL
    
    
    curl --request GET \
      --url https://your-actual-crew-name.crewai.com/inputs \
      --header 'Authorization: Bearer <token>'

200

travel_crew
    
    
    {
      "inputs": [
        "budget",
        "interests",
        "duration",
        "age"
      ]
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

#### Response

200

application/json

Successfully retrieved required inputs

​

inputs

string[]

Array of required input parameter names

Example:
    
    
    ["budget", "interests", "duration", "age"]

Was this page helpful?

YesNo

[IntroductionPrevious](/en/api-reference/introduction)[POST /kickoffNext](/en/api-reference/kickoff)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)