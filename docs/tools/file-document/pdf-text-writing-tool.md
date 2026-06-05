# Source: https://docs.crewai.com/en/tools/file-document/pdf-text-writing-tool

File & Document

# PDF Text Writing Tool


The `PDFTextWritingTool` writes text to specific positions in a PDF, supporting custom fonts.


# 

​

`PDFTextWritingTool`

## 

​

Description

Write text at precise coordinates on a PDF page, optionally embedding a custom TrueType font.

## 

​

Parameters

### 

​

Run Parameters

  * `pdf_path` (str, required): Path to the input PDF.
  * `text` (str, required): Text to add.
  * `position` (tuple[int, int], required): `(x, y)` coordinates.
  * `font_size` (int, default `12`)
  * `font_color` (str, default `"0 0 0 rg"`)
  * `font_name` (str, default `"F1"`)
  * `font_file` (str, optional): Path to `.ttf` file.
  * `page_number` (int, default `0`)

## 

​

Example

Code
    
    
    from crewai import Agent, Task, Crew
    from crewai_tools import PDFTextWritingTool
    
    tool = PDFTextWritingTool()
    
    agent = Agent(
        role="PDF Editor",
        goal="Annotate PDFs",
        backstory="Documentation specialist",
        tools=[tool],
        verbose=True,
    )
    
    task = Task(
        description="Write 'CONFIDENTIAL' at (72, 720) on page 1 of ./sample.pdf",
        expected_output="Confirmation message",
        agent=agent,
    )
    
    crew = Crew(
        agents=[agent], 
        tasks=[task],
        verbose=True,
    )
    
    result = crew.kickoff()
    

### 

​

Direct usage

Code
    
    
    from crewai_tools import PDFTextWritingTool
    
    PDFTextWritingTool().run(
      pdf_path="./input.pdf",
      text="CONFIDENTIAL",
      position=(72, 720),
      font_size=18,
      page_number=0,
    )
    

## 

​

Tips

  * Coordinate origin is the bottom‑left corner.
  * If using a custom font (`font_file`), ensure it is a valid `.ttf`.

Was this page helpful?

YesNo

[OCR ToolPrevious](/en/tools/file-document/ocrtool)[OverviewNext](/en/tools/web-scraping/overview)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)