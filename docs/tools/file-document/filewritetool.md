# Source: https://docs.crewai.com/en/tools/file-document/filewritetool

File & Document

# File Write


The `FileWriterTool` is designed to write content to files.


# 

​

`FileWriterTool`

## 

​

Description

The `FileWriterTool` is a component of the crewai_tools package, designed to simplify the process of writing content to files with cross-platform compatibility (Windows, Linux, macOS). It is particularly useful in scenarios such as generating reports, saving logs, creating configuration files, and more. This tool handles path differences across operating systems, supports UTF-8 encoding, and automatically creates directories if they don’t exist, making it easier to organize your output reliably across different platforms.

## 

​

Installation

Install the crewai_tools package to use the `FileWriterTool` in your projects:
    
    
    pip install 'crewai[tools]'
    

## 

​

Example

To get started with the `FileWriterTool`:

Code
    
    
    from crewai_tools import FileWriterTool
    
    # Initialize the tool
    file_writer_tool = FileWriterTool()
    
    # Write content to a file in a specified directory
    result = file_writer_tool._run('example.txt', 'This is a test content.', 'test_directory')
    print(result)
    

## 

​

Arguments

  * `filename`: The name of the file you want to create or overwrite.
  * `content`: The content to write into the file.
  * `directory` (optional): The path to the directory where the file will be created. Defaults to the current directory (`.`). If the directory does not exist, it will be created.

## 

​

Conclusion

By integrating the `FileWriterTool` into your crews, the agents can reliably write content to files across different operating systems. This tool is essential for tasks that require saving output data, creating structured file systems, and handling cross-platform file operations. It’s particularly recommended for Windows users who may encounter file writing issues with standard Python file operations. By adhering to the setup and usage guidelines provided, incorporating this tool into projects is straightforward and ensures consistent file writing behavior across all platforms.

Was this page helpful?

YesNo

[File ReadPrevious](/en/tools/file-document/filereadtool)[PDF RAG SearchNext](/en/tools/file-document/pdfsearchtool)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)