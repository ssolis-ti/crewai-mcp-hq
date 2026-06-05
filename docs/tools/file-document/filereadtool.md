# Source: https://docs.crewai.com/en/tools/file-document/filereadtool

File & Document

# File Read


The `FileReadTool` is designed to read files from the local file system.


## 

​

Overview

We are still working on improving tools, so there might be unexpected behavior or changes in the future.

The FileReadTool conceptually represents a suite of functionalities within the crewai_tools package aimed at facilitating file reading and content retrieval. This suite includes tools for processing batch text files, reading runtime configuration files, and importing data for analytics. It supports a variety of text-based file formats such as `.txt`, `.csv`, `.json`, and more. Depending on the file type, the suite offers specialized functionality, such as converting JSON content into a Python dictionary for ease of use.

## 

​

Installation

To utilize the functionalities previously attributed to the FileReadTool, install the crewai_tools package:
    
    
    pip install 'crewai[tools]'
    

## 

​

Usage Example

To get started with the FileReadTool:

Code
    
    
    from crewai_tools import FileReadTool
    
    # Initialize the tool to read any files the agents knows or lean the path for
    file_read_tool = FileReadTool()
    
    # OR
    
    # Initialize the tool with a specific file path, so the agent can only read the content of the specified file
    file_read_tool = FileReadTool(file_path='path/to/your/file.txt')
    

## 

​

Arguments

  * `file_path`: The path to the file you want to read. It accepts both absolute and relative paths. Ensure the file exists and you have the necessary permissions to access it.

Was this page helpful?

YesNo

[OverviewPrevious](/en/tools/file-document/overview)[File WriteNext](/en/tools/file-document/filewritetool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)