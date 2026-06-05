# Source: https://docs.crewai.com/en/enterprise/guides/react-component-export

How-To Guides

# React Component Export


Learn how to export and integrate CrewAI AMP React components into your applications


This guide explains how to export CrewAI AMP crews as React components and integrate them into your own applications.

## 

​

Exporting a React Component

1

Export the Component

Click on the ellipsis (three dots on the right of your deployed crew) and select the export option and save the file locally. We will be using `CrewLead.jsx` for our example.

![Export React Component](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/export-react-component.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e0c72184b57eeae414674023197fca1b)

## 

​

Setting Up Your React Environment

To run this React component locally, you’ll need to set up a React development environment and integrate this component into a React project.

1

Install Node.js

  * Download and install Node.js from the official website: <https://nodejs.org/>
  * Choose the LTS (Long Term Support) version for stability.

2

Create a new React project

  * Open Command Prompt or PowerShell
  * Navigate to the directory where you want to create your project
  * Run the following command to create a new React project:
        
        npx create-react-app my-crew-app
        

  * Change into the project directory:
        
        cd my-crew-app
        

3

Install necessary dependencies
    
    
    npm install react-dom
    

4

Create the CrewLead component

  * Move the downloaded file `CrewLead.jsx` into the `src` folder of your project,

5

Modify your App.js to use the CrewLead component

  * Open `src/App.js`
  * Replace its contents with something like this:

    
    
    import React from 'react';
    import CrewLead from './CrewLead';
    
    function App() {
        return (
            <div className="App">
                <CrewLead baseUrl="YOUR_API_BASE_URL" bearerToken="YOUR_BEARER_TOKEN" />
            </div>
        );
    }
    
    export default App;
    

  * Replace `YOUR_API_BASE_URL` and `YOUR_BEARER_TOKEN` with the actual values for your API.

6

Start the development server

  * In your project directory, run:
        
        npm start
        

  * This will start the development server, and your default web browser should open automatically to <http://localhost:3000>, where you’ll see your React app running.

## 

​

Customization

You can then customise the `CrewLead.jsx` to add color, title etc

![Customise React Component](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/customise-react-component.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=4673fd3ac9eedc1c83b777afb8cf09c9)

![Customise React Component](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/customise-react-component-2.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=714c15d129b3db4bd96cdc55e80916dd)

## 

​

Next Steps

  * Customize the component styling to match your application’s design
  * Add additional props for configuration
  * Integrate with your application’s state management
  * Add error handling and loading states

Was this page helpful?

YesNo

[Custom MCP ServersPrevious](/en/enterprise/guides/custom-mcp-server)[Team ManagementNext](/en/enterprise/guides/team-management)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)