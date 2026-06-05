# Source: https://docs.crewai.com/en/enterprise/guides/kickoff-crew

How-To Guides

# Kickoff Crew


Kickoff a Crew on CrewAI AMP


## 

​

Overview

Once you’ve deployed your crew to the CrewAI AMP platform, you can kickoff executions through the web interface or the API. This guide covers both approaches.

## 

​

Method 1: Using the Web Interface

### 

​

Step 1: Navigate to Your Deployed Crew

  1. Log in to [CrewAI AMP](https://app.crewai.com)
  2. Click on the crew name from your projects list
  3. You’ll be taken to the crew’s detail page

![Crew Dashboard](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew-dashboard.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=6dfd552914d3ed5ec24abb1ba606ff7d)

### 

​

Step 2: Initiate Execution

From your crew’s detail page, you have two options to kickoff an execution:

#### 

​

Option A: Quick Kickoff

  1. Click the `Kickoff` link in the Test Endpoints section
  2. Enter the required input parameters for your crew in the JSON editor
  3. Click the `Send Request` button

![Kickoff Endpoint](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-endpoint.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=39603fac859ca2a602c51c585c2a4861)

#### 

​

Option B: Using the Visual Interface

  1. Click the `Run` tab in the crew detail page
  2. Enter the required inputs in the form fields
  3. Click the `Run Crew` button

![Run Crew](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/run-crew.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=87b09919c9210c7ca8fb0b0952d99005)

### 

​

Step 3: Monitor Execution Progress

After initiating the execution:

  1. You’ll receive a response containing a `kickoff_id` \- **copy this ID**
  2. This ID is essential for tracking your execution

![Copy Task ID](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/copy-task-id.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=f5d6e458d4773fb94590d7accdde8499)

### 

​

Step 4: Check Execution Status

To monitor the progress of your execution:

  1. Click the “Status” endpoint in the Test Endpoints section
  2. Paste the `kickoff_id` into the designated field
  3. Click the “Get Status” button

![Get Status](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/get-status.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=f8c8f553fd5797fab5fbec2993f5d745)

The status response will show:

  * Current execution state (`running`, `completed`, etc.)
  * Details about which tasks are in progress
  * Any outputs produced so far

### 

​

Step 5: View Final Results

Once execution is complete:

  1. The status will change to `completed`
  2. You can view the full execution results and outputs
  3. For a more detailed view, check the `Executions` tab in the crew detail page

## 

​

Method 2: Using the API

You can also kickoff crews programmatically using the CrewAI AMP REST API.

### 

​

Authentication

All API requests require a bearer token for authentication:
    
    
    curl -H "Authorization: Bearer YOUR_CREW_TOKEN" https://your-crew-url.crewai.com
    

Your bearer token is available on the Status tab of your crew’s detail page.

### 

​

Checking Crew Health

Before executing operations, you can verify that your crew is running properly:
    
    
    curl -H "Authorization: Bearer YOUR_CREW_TOKEN" https://your-crew-url.crewai.com
    

A successful response will return a message indicating the crew is operational:
    
    
    Healthy%
    

### 

​

Step 1: Retrieve Required Inputs

First, determine what inputs your crew requires:
    
    
    curl -X GET \
      -H "Authorization: Bearer YOUR_CREW_TOKEN" \
      https://your-crew-url.crewai.com/inputs
    

The response will be a JSON object containing an array of required input parameters, for example:
    
    
    { "inputs": ["topic", "current_year"] }
    

This example shows that this particular crew requires two inputs: `topic` and `current_year`.

### 

​

Step 2: Kickoff Execution

Initiate execution by providing the required inputs:
    
    
    curl -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_CREW_TOKEN" \
      -d '{"inputs": {"topic": "AI Agent Frameworks", "current_year": "2025"}}' \
      https://your-crew-url.crewai.com/kickoff
    

The response will include a `kickoff_id` that you’ll need for tracking:
    
    
    { "kickoff_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv" }
    

### 

​

Step 3: Check Execution Status

Monitor the execution progress using the kickoff_id:
    
    
    curl -X GET \
      -H "Authorization: Bearer YOUR_CREW_TOKEN" \
      https://your-crew-url.crewai.com/status/abcd1234-5678-90ef-ghij-klmnopqrstuv
    

## 

​

Handling Executions

### 

​

Long-Running Executions

For executions that may take a long time:

  1. Consider implementing a polling mechanism to check status periodically
  2. Use webhooks (if available) for notification when execution completes
  3. Implement error handling for potential timeouts

### 

​

Execution Context

The execution context includes:

  * Inputs provided at kickoff
  * Environment variables configured during deployment
  * Any state maintained between tasks

### 

​

Debugging Failed Executions

If an execution fails:

  1. Check the “Executions” tab for detailed logs
  2. Review the “Traces” tab for step-by-step execution details
  3. Look for LLM responses and tool usage in the trace details

## Need Help?

Contact our support team for assistance with execution issues or questions about the Enterprise platform.

Was this page helpful?

YesNo

[Private Package RegistriesPrevious](/en/enterprise/guides/private-package-registry)[Update CrewNext](/en/enterprise/guides/update-crew)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)