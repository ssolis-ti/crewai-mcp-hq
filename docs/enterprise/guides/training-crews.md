# Source: https://docs.crewai.com/en/enterprise/guides/training-crews

How-To Guides

# Training Crews


Train your deployed crews directly from the CrewAI AMP platform to improve agent performance over time


Training lets you improve crew performance by running iterative training sessions directly from the **Training** tab in CrewAI AMP. The platform uses **auto-train mode** — it handles the iterative process automatically, unlike CLI training which requires interactive human feedback per iteration. After training completes, CrewAI evaluates agent outputs and consolidates feedback into actionable suggestions for each agent. These suggestions are then applied to future crew runs to improve output quality.

For details on how CrewAI training works under the hood, see the [Training Concepts](/en/concepts/training) page.

## 

​

Prerequisites

## Active deployment

You need a CrewAI AMP account with an active deployment in **Ready** status (Crew type).

## Run permission

Your account must have run permission for the deployment you want to train.

## 

​

How to train a crew

1

Open the Training tab

Navigate to **Deployments** , click your deployment, then select the **Training** tab.

2

Enter a training name

Provide a **Training Name** — this becomes the `.pkl` filename used to store training results. For example, “Expert Mode Training” produces `expert_mode_training.pkl`.

3

Fill in the crew inputs

Enter the crew’s input fields. These are the same inputs you’d provide for a normal kickoff — they’re dynamically loaded based on your crew’s configuration.

4

Start training

Click **Train Crew**. The button changes to “Training…” with a spinner while the process runs.Behind the scenes:

  * A training record is created for your deployment
  * The platform calls the deployment’s auto-train endpoint
  * The crew runs its iterations automatically — no manual feedback required

5

Monitor progress

The **Current Training Status** panel displays:

  * **Status** — Current state of the training run
  * **Nº Iterations** — Number of training iterations configured
  * **Filename** — The `.pkl` file being generated
  * **Started At** — When training began
  * **Training Inputs** — The inputs you provided

## 

​

Understanding training results

Once training completes, you’ll see per-agent result cards with the following information:

  * **Agent Role** — The name/role of the agent in your crew
  * **Final Quality** — A score from 0 to 10 evaluating the agent’s output quality
  * **Final Summary** — A summary of the agent’s performance during training
  * **Suggestions** — Actionable recommendations for improving the agent’s behavior

### 

​

Editing suggestions

You can refine the suggestions for any agent:

1

Click Edit

On any agent’s result card, click the **Edit** button next to the suggestions.

2

Modify suggestions

Update the suggestions text to better reflect the improvements you want.

3

Save changes

Click **Save**. The edited suggestions sync back to the deployment and are used in all future runs.

## 

​

Using trained data

To apply training results to your crew:

  1. Note the **Training Filename** (the `.pkl` file) from your completed training session.
  2. Specify this filename in your deployment’s kickoff or run configuration.
  3. The crew automatically loads the training file and applies the stored suggestions to each agent.

This means agents benefit from the feedback generated during training on every subsequent run.

## 

​

Previous trainings

The bottom of the Training tab displays a **history of all past training sessions** for the deployment. Use this to review previous training runs, compare results, or select a different training file to use.

## 

​

Error handling

If a training run fails, the status panel shows an error state along with a message describing what went wrong. Common causes of training failures:

  * **Deployment runtime not updated** — Ensure your deployment is running the latest version
  * **Crew execution errors** — Issues within the crew’s task logic or agent configuration
  * **Network issues** — Connectivity problems between the platform and the deployment

## 

​

Limitations

Keep these constraints in mind when planning your training workflow:

  * **One active training at a time** per deployment — wait for the current run to finish before starting another
  * **Auto-train mode only** — the platform does not support interactive per-iteration feedback like the CLI does
  * **Training data is deployment-specific** — training results are tied to the specific deployment instance and version

## 

​

Related resources

## Training Concepts

Learn how CrewAI training works under the hood.

## Kickoff Crew

Run your deployed crew from the AMP platform.

## Deploy to AMP

Get your crew deployed and ready for training.

Was this page helpful?

YesNo

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)