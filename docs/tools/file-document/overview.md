# Source: https://docs.crewai.com/en/tools/file-document/overview

File & Document

# Overview


Read, write, and search through various file formats with CrewAI’s document processing tools


These tools enable your agents to work with various file formats and document types. From reading PDFs to processing JSON data, these tools handle all your document processing needs.

## 

​

**Available Tools**

## File Read Tool

Read content from any file type including text, markdown, and more.

## File Write Tool

Write content to files, create new documents, and save processed data.

## PDF Search Tool

Search and extract text content from PDF documents efficiently.

## DOCX Search Tool

Search through Microsoft Word documents and extract relevant content.

## JSON Search Tool

Parse and search through JSON files with advanced query capabilities.

## CSV Search Tool

Process and search through CSV files, extract specific rows and columns.

## XML Search Tool

Parse XML files and search for specific elements and attributes.

## MDX Search Tool

Search through MDX files and extract content from documentation.

## TXT Search Tool

Search through plain text files with pattern matching capabilities.

## Directory Search Tool

Search for files and folders within directory structures.

## Directory Read Tool

Read and list directory contents, file structures, and metadata.

## OCR Tool

Extract text from images (local files or URLs) using a vision‑capable LLM.

## PDF Text Writing Tool

Write text at specific coordinates in PDFs, with optional custom fonts.

## 

​

**Common Use Cases**

  * **Document Processing** : Extract and analyze content from various file formats
  * **Data Import** : Read structured data from CSV, JSON, and XML files
  * **Content Search** : Find specific information within large document collections
  * **File Management** : Organize and manipulate files and directories
  * **Data Export** : Save processed results to various file formats

## 

​

**Quick Start Example**
    
    
    from crewai_tools import FileReadTool, PDFSearchTool, JSONSearchTool
    
    # Create tools
    file_reader = FileReadTool()
    pdf_searcher = PDFSearchTool()
    json_processor = JSONSearchTool()
    
    # Add to your agent
    agent = Agent(
        role="Document Analyst",
        tools=[file_reader, pdf_searcher, json_processor],
        goal="Process and analyze various document types"
    )
    

## 

​

**Tips for Document Processing**

  * **File Permissions** : Ensure your agent has proper read/write permissions
  * **Large Files** : Consider chunking for very large documents
  * **Format Support** : Check tool documentation for supported file formats
  * **Error Handling** : Implement proper error handling for corrupted or inaccessible files

Was this page helpful?

YesNo

[Tools OverviewPrevious](/en/tools/overview)[File ReadNext](/en/tools/file-document/filereadtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)