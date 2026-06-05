# Source: https://docs.crewai.com/en/tools/file-document/ocrtool

File & Document

# OCR Tool


The `OCRTool` extracts text from local images or image URLs using an LLM with vision.


# 

​

`OCRTool`

## 

​

Description

Extract text from images (local path or URL). Uses a vision‑capable LLM via CrewAI’s LLM interface.

## 

​

Installation

No extra install beyond `crewai-tools`. Ensure your selected LLM supports vision.

## 

​

Parameters

### 

​

Run Parameters

  * `image_path_url` (str, required): Local image path or HTTP(S) URL.

## 

​

Examples

### 

​

Direct usage

Code
    
    
    from crewai_tools import OCRTool
    
    print(OCRTool().run(image_path_url="/tmp/receipt.png"))
    

### 

​

With an agent

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import OCRTool
    
    ocr = OCRTool()
    
    agent = Agent(
        role="OCR", 
        goal="Extract text", 
        tools=[ocr],
    )
    
    task = Task(
        description="Extract text from https://example.com/invoice.jpg", 
        expected_output="All detected text in plain text",
        agent=agent,
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    

## 

​

Notes

  * Ensure the selected LLM supports image inputs.
  * For large images, consider downscaling to reduce token usage.
  * You can pass a specific LLM instance to the tool (e.g., `LLM(model="gpt-4o")`) if needed, matching the README guidance.

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import OCRTool
    
    tool = OCRTool()
    
    agent = Agent(
        role="OCR Specialist",
        goal="Extract text from images",
        backstory="Vision‑enabled analyst",
        tools=[tool],
        verbose=True,
    )
    
    task = Task(
        description="Extract text from https://example.com/receipt.png",
        expected_output="All detected text in plain text",
        agent=agent,
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    

Was this page helpful?

YesNo

[Directory ReadPrevious](/en/tools/file-document/directoryreadtool)[PDF Text Writing ToolNext](/en/tools/file-document/pdf-text-writing-tool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)