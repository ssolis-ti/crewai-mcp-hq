# Source: https://docs.crewai.com/en/tools/cloud-storage/overview

Cloud & Storage

# Overview


Interact with cloud services, storage systems, and cloud-based AI platforms


These tools enable your agents to interact with cloud services, access cloud storage, and leverage cloud-based AI platforms for scalable operations.

## 

​

**Available Tools**

## S3 Reader Tool

Read files and data from Amazon S3 buckets.

## S3 Writer Tool

Write and upload files to Amazon S3 storage.

## Bedrock Invoke Agent

Invoke Amazon Bedrock agents for AI-powered tasks.

## Bedrock KB Retriever

Retrieve information from Amazon Bedrock knowledge bases.

## 

​

**Common Use Cases**

  * **File Storage** : Store and retrieve files from cloud storage systems
  * **Data Backup** : Backup important data to cloud storage
  * **AI Services** : Access cloud-based AI models and services
  * **Knowledge Retrieval** : Query cloud-hosted knowledge bases
  * **Scalable Operations** : Leverage cloud infrastructure for processing

    
    
    from crewai_tools import S3ReaderTool, S3WriterTool, BedrockInvokeAgentTool
    
    # Create cloud tools
    s3_reader = S3ReaderTool()
    s3_writer = S3WriterTool()
    bedrock_agent = BedrockInvokeAgentTool()
    
    # Add to your agent
    agent = Agent(
        role="Cloud Operations Specialist",
        tools=[s3_reader, s3_writer, bedrock_agent],
        goal="Manage cloud resources and AI services"
    )
    

Was this page helpful?

YesNo

[E2B Sandbox ToolsPrevious](/en/tools/ai-ml/e2bsandboxtools)[S3 Reader ToolNext](/en/tools/cloud-storage/s3readertool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)