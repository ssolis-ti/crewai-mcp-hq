# Source: https://docs.crewai.com/en/api-reference/introduction

Getting Started

# Introduction


Complete reference for the CrewAI AMP REST API


# 

​

CrewAI AMP API

Welcome to the CrewAI AMP API reference. This API allows you to programmatically interact with your deployed crews, enabling integration with your applications, workflows, and services.

## 

​

Quick Start

1

Get Your API Credentials

Navigate to your crew’s detail page in the CrewAI AMP dashboard and copy your Bearer Token from the Status tab.

2

Discover Required Inputs

Use the `GET /inputs` endpoint to see what parameters your crew expects.

3

Start a Crew Execution

Call `POST /kickoff` with your inputs to start the crew execution and receive a `kickoff_id`.

4

Monitor Progress

Use `GET /status/{kickoff_id}` to check execution status and retrieve results.

## 

​

Authentication

All API requests require authentication using a Bearer token. Include your token in the `Authorization` header:
    
    
    curl -H "Authorization: Bearer YOUR_CREW_TOKEN" \
      https://your-crew-url.crewai.com/inputs
    

### 

​

Token Types

Token Type| Scope| Use Case  
---|---|---  
**Bearer Token**|  Organization-level access| Full crew operations, ideal for server-to-server integration  
**User Bearer Token**|  User-scoped access| Limited permissions, suitable for user-specific operations  
  
You can find both token types in the Status tab of your crew’s detail page in the CrewAI AMP dashboard.

## 

​

Base URL

Each deployed crew has its own unique API endpoint:
    
    
    https://your-crew-name.crewai.com
    

Replace `your-crew-name` with your actual crew’s URL from the dashboard.

## 

​

Typical Workflow

  1. **Discovery** : Call `GET /inputs` to understand what your crew needs
  2. **Execution** : Submit inputs via `POST /kickoff` to start processing
  3. **Monitoring** : Poll `GET /status/{kickoff_id}` until completion
  4. **Results** : Extract the final output from the completed response

## 

​

Error Handling

The API uses standard HTTP status codes:

Code| Meaning  
---|---  
`200`| Success  
`400`| Bad Request - Invalid input format  
`401`| Unauthorized - Invalid bearer token  
`404`| Not Found - Resource doesn’t exist  
`422`| Validation Error - Missing required inputs  
`500`| Server Error - Contact support  
  
## 

​

Interactive Testing

**Why no “Send” button?** Since each CrewAI AMP user has their own unique crew URL, we use **reference mode** instead of an interactive playground to avoid confusion. This shows you exactly what the requests should look like without non-functional send buttons.

Each endpoint page shows you:

  * ✅ **Exact request format** with all parameters
  * ✅ **Response examples** for success and error cases
  * ✅ **Code samples** in multiple languages (cURL, Python, JavaScript, etc.)
  * ✅ **Authentication examples** with proper Bearer token format

### 

​

**To Test Your Actual API:**

## Copy cURL Examples

Copy the cURL examples and replace the URL + token with your real values

## Use Postman/Insomnia

Import the examples into your preferred API testing tool

**Example workflow:**

  1. **Copy this cURL example** from any endpoint page
  2. **Replace`your-actual-crew-name.crewai.com`** with your real crew URL
  3. **Replace the Bearer token** with your real token from the dashboard
  4. **Run the request** in your terminal or API client

## 

​

Need Help?

## Enterprise Support

Get help with API integration and troubleshooting

## Enterprise Dashboard

Manage your crews and view execution logs

Was this page helpful?

YesNo

[GET /inputsNext](/en/api-reference/inputs)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)