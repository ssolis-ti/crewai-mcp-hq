# Source: https://docs.crewai.com/en/tools/ai-ml/overview

AI & Machine Learning

# Overview


Leverage AI services, generate images, process vision, and build intelligent systems


These tools integrate with AI and machine learning services to enhance your agents with advanced capabilities like image generation, vision processing, and intelligent code execution.

## 

​

**Available Tools**

## DALL-E Tool

Generate AI images using OpenAI’s DALL-E model.

## Vision Tool

Process and analyze images with computer vision capabilities.

## AI Mind Tool

Advanced AI reasoning and decision-making capabilities.

## LlamaIndex Tool

Build knowledge bases and retrieval systems with LlamaIndex.

## LangChain Tool

Integrate with LangChain for complex AI workflows.

## RAG Tool

Implement Retrieval-Augmented Generation systems.

## Code Interpreter Tool

Execute Python code and perform data analysis.

## 

​

**Common Use Cases**

  * **Content Generation** : Create images, text, and multimedia content
  * **Data Analysis** : Execute code and analyze complex datasets
  * **Knowledge Systems** : Build RAG systems and intelligent databases
  * **Computer Vision** : Process and understand visual content
  * **AI Safety** : Implement content moderation and safety checks

    
    
    from crewai_tools import DallETool, VisionTool, CodeInterpreterTool
    
    # Create AI tools
    image_generator = DallETool()
    vision_processor = VisionTool()
    code_executor = CodeInterpreterTool()
    
    # Add to your agent
    agent = Agent(
        role="AI Specialist",
        tools=[image_generator, vision_processor, code_executor],
        goal="Create and analyze content using AI capabilities"
    )
    

Was this page helpful?

YesNo

[SingleStore Search ToolPrevious](/en/tools/database-data/singlestoresearchtool)[DALL-E ToolNext](/en/tools/ai-ml/dalletool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)