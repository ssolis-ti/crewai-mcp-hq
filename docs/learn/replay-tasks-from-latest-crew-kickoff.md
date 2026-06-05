# Source: https://docs.crewai.com/en/learn/replay-tasks-from-latest-crew-kickoff

Learn

# Replay Tasks from Latest Crew Kickoff


Replay tasks from the latest crew.kickoff(…)


## 

​

Introduction

CrewAI provides the ability to replay from a task specified from the latest crew kickoff. This feature is particularly useful when you’ve finished a kickoff and may want to retry certain tasks or don’t need to refetch data over and your agents already have the context saved from the kickoff execution so you just need to replay the tasks you want to.

You must run `crew.kickoff()` before you can replay a task. Currently, only the latest kickoff is supported, so if you use `kickoff_for_each`, it will only allow you to replay from the most recent crew run.

Here’s an example of how to replay from a task:

### 

​

Replaying from Specific Task Using the CLI

To use the replay feature, follow these steps:

1

Open your terminal or command prompt.

2

Navigate to the directory where your CrewAI project is located.

3

Run the following commands:

To view the latest kickoff task_ids use:
    
    
    crewai log-tasks-outputs
    

Once you have your `task_id` to replay, use:
    
    
    crewai replay -t <task_id>
    

Ensure `crewai` is installed and configured correctly in your development environment.

### 

​

Replaying from a Task Programmatically

To replay from a task programmatically, use the following steps:

1

Specify the `task_id` and input parameters for the replay process.

Specify the `task_id` and input parameters for the replay process.

2

Execute the replay command within a try-except block to handle potential errors.

Execute the replay command within a try-except block to handle potential errors.

Code
    
    
      def replay():
      """
      Replay the crew execution from a specific task.
      """
      task_id = '<task_id>'
      inputs = {"topic": "CrewAI Training"}  # This is optional; you can pass in the inputs you want to replay; otherwise, it uses the previous kickoff's inputs.
      try:
          YourCrewName_Crew().crew().replay(task_id=task_id, inputs=inputs)
    
      except subprocess.CalledProcessError as e:
          raise Exception(f"An error occurred while replaying the crew: {e}")
    
      except Exception as e:
          raise Exception(f"An unexpected error occurred: {e}")
    

## 

​

Conclusion

With the above enhancements and detailed functionality, replaying specific tasks in CrewAI has been made more efficient and robust. Ensure you follow the commands and steps precisely to make the most of these features.

Was this page helpful?

YesNo

[Using Multimodal AgentsPrevious](/en/learn/multimodal-agents)[Sequential ProcessesNext](/en/learn/sequential-process)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)