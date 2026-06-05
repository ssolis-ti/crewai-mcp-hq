# Source: https://docs.crewai.com/en/concepts/files

## On this page

  * Overview
  * File Types
  * File Sources
    * From Path
    * From URL
    * From Bytes
  * Using Files
    * With Crews
    * With Tasks
    * With Flows
    * With Standalone Agents
  * File Precedence
  * Provider Support
  * How Files Are Sent
    * Provider Transmission Methods
  * File Handling Modes
  * Provider Constraints
    * OpenAI
    * Anthropic
    * Google Gemini
    * AWS Bedrock
  * Referencing Files in Prompts

Core Concepts

# Files


Pass images, PDFs, audio, video, and text files to your agents for multimodal processing.


## 

​

Overview

CrewAI supports native multimodal file inputs, allowing you to pass images, PDFs, audio, video, and text files directly to your agents. Files are automatically formatted for each LLM provider’s API requirements.

File support requires the optional `crewai-files` package. Install it with:
    
    
    uv add 'crewai[file-processing]'
    

The file processing API is currently in early access.

## 

​

File Types

CrewAI supports five specific file types plus a generic `File` class that auto-detects the type:

Type| Class| Use Cases  
---|---|---  
**Image**| `ImageFile`| Photos, screenshots, diagrams, charts  
**PDF**| `PDFFile`| Documents, reports, papers  
**Audio**| `AudioFile`| Voice recordings, podcasts, meetings  
**Video**| `VideoFile`| Screen recordings, presentations  
**Text**| `TextFile`| Code files, logs, data files  
**Generic**| `File`| Auto-detect type from content  
      
    
    from crewai_files import File, ImageFile, PDFFile, AudioFile, VideoFile, TextFile
    
    image = ImageFile(source="screenshot.png")
    pdf = PDFFile(source="report.pdf")
    audio = AudioFile(source="meeting.mp3")
    video = VideoFile(source="demo.mp4")
    text = TextFile(source="data.csv")
    
    file = File(source="document.pdf")
    

## 

​

File Sources

The `source` parameter accepts multiple input types and auto-detects the appropriate handler:

### 

​

From Path
    
    
    from crewai_files import ImageFile
    
    image = ImageFile(source="./images/chart.png")
    

### 

​

From URL
    
    
    from crewai_files import ImageFile
    
    image = ImageFile(source="https://example.com/image.png")
    

### 

​

From Bytes
    
    
    from crewai_files import ImageFile, FileBytes
    
    image_bytes = download_image_from_api()
    image = ImageFile(source=FileBytes(data=image_bytes, filename="downloaded.png"))
    image = ImageFile(source=image_bytes)
    

## 

​

Using Files

Files can be passed at multiple levels, with more specific levels taking precedence.

### 

​

With Crews

Pass files when kicking off a crew:
    
    
    from crewai import Crew
    from crewai_files import ImageFile
    
    crew = Crew(agents=[analyst], tasks=[analysis_task])
    
    result = crew.kickoff(
        inputs={"topic": "Q4 Sales"},
        input_files={
            "chart": ImageFile(source="sales_chart.png"),
            "report": PDFFile(source="quarterly_report.pdf"),
        }
    )
    

### 

​

With Tasks

Attach files to specific tasks:
    
    
    from crewai import Task
    from crewai_files import ImageFile
    
    task = Task(
        description="Analyze the sales chart and identify trends in {chart}",
        expected_output="A summary of key trends",
        input_files={
            "chart": ImageFile(source="sales_chart.png"),
        }
    )
    

### 

​

With Flows

Pass files to flows, which automatically inherit to crews:
    
    
    from crewai.flow.flow import Flow, start
    from crewai_files import ImageFile
    
    class AnalysisFlow(Flow):
        @start()
        def analyze(self):
            return self.analysis_crew.kickoff()
    
    flow = AnalysisFlow()
    result = flow.kickoff(
        input_files={"image": ImageFile(source="data.png")}
    )
    

### 

​

With Standalone Agents

Pass files directly to agent kickoff:
    
    
    from crewai import Agent
    from crewai_files import ImageFile
    
    agent = Agent(
        role="Image Analyst",
        goal="Analyze images",
        backstory="Expert at visual analysis",
        llm="gpt-4o",
    )
    
    result = agent.kickoff(
        messages="What's in this image?",
        input_files={"photo": ImageFile(source="photo.jpg")},
    )
    

## 

​

File Precedence

When files are passed at multiple levels, more specific levels override broader ones:
    
    
    Flow input_files < Crew input_files < Task input_files
    

For example, if both Flow and Task define a file named `"chart"`, the Task’s version is used.

## 

​

Provider Support

Different providers support different file types. CrewAI automatically formats files for each provider’s API.

Provider| Image| PDF| Audio| Video| Text  
---|---|---|---|---|---  
**OpenAI** (completions API)| ✓| | | |   
**OpenAI** (responses API)| ✓| ✓| ✓| |   
**Anthropic** (claude-3.x)| ✓| ✓| | |   
**Google Gemini** (gemini-1.5, 2.0, 2.5)| ✓| ✓| ✓| ✓| ✓  
**AWS Bedrock** (claude-3)| ✓| ✓| | |   
**Azure OpenAI** (gpt-4o)| ✓| | ✓| |   
  
Google Gemini models support all file types including video (up to 1 hour, 2GB). Use Gemini when you need to process video content.

If you pass a file type that the provider doesn’t support (e.g., video to OpenAI), you’ll receive an `UnsupportedFileTypeError`. Choose your provider based on the file types you need to process.

## 

​

How Files Are Sent

CrewAI automatically chooses the optimal method to send files to each provider:

Method| Description| Used When  
---|---|---  
**Inline Base64**|  File embedded directly in the request| Small files (< 5MB typically)  
**File Upload API**|  File uploaded separately, referenced by ID| Large files that exceed threshold  
**URL Reference**|  Direct URL passed to the model| File source is already a URL  
  
### 

​

Provider Transmission Methods

Provider| Inline Base64| File Upload API| URL References  
---|---|---|---  
**OpenAI**|  ✓| ✓ (> 5 MB)| ✓  
**Anthropic**|  ✓| ✓ (> 5 MB)| ✓  
**Google Gemini**|  ✓| ✓ (> 20 MB)| ✓  
**AWS Bedrock**|  ✓| | ✓ (S3 URIs)  
**Azure OpenAI**|  ✓| | ✓  
  
You don’t need to manage this yourself. CrewAI automatically uses the most efficient method based on file size and provider capabilities. Providers without file upload APIs use inline base64 for all files.

## 

​

File Handling Modes

Control how files are processed when they exceed provider limits:
    
    
    from crewai_files import ImageFile, PDFFile
    
    image = ImageFile(source="large.png", mode="strict")
    image = ImageFile(source="large.png", mode="auto")
    image = ImageFile(source="large.png", mode="warn")
    pdf = PDFFile(source="large.pdf", mode="chunk")
    

## 

​

Provider Constraints

Each provider has specific limits for file sizes and dimensions:

### 

​

OpenAI

  * **Images** : Max 20 MB, up to 10 images per request
  * **PDFs** : Max 32 MB, up to 100 pages
  * **Audio** : Max 25 MB, up to 25 minutes

### 

​

Anthropic

  * **Images** : Max 5 MB, max 8000x8000 pixels, up to 100 images
  * **PDFs** : Max 32 MB, up to 100 pages

### 

​

Google Gemini

  * **Images** : Max 100 MB
  * **PDFs** : Max 50 MB
  * **Audio** : Max 100 MB, up to 9.5 hours
  * **Video** : Max 2 GB, up to 1 hour

### 

​

AWS Bedrock

  * **Images** : Max 4.5 MB, max 8000x8000 pixels
  * **PDFs** : Max 3.75 MB, up to 100 pages

## 

​

Referencing Files in Prompts

Use the file’s key name in your task descriptions to reference files:
    
    
    task = Task(
        description="""
        Analyze the provided materials:
        1. Review the chart in {sales_chart}
        2. Cross-reference with data in {quarterly_report}
        3. Summarize key findings
        """,
        expected_output="Analysis summary with key insights",
        input_files={
            "sales_chart": ImageFile(source="chart.png"),
            "quarterly_report": PDFFile(source="report.pdf"),
        }
    )
    

Was this page helpful?

YesNo

[LLMsPrevious](/en/concepts/llms)[ProcessesNext](/en/concepts/processes)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)