# Source: https://docs.crewai.com/en/enterprise/features/agent-control-plane/monitoring

Agent Control Plane

# Watch your Automations


Watch fleet health, LLM consumption, and per-automation behavior from the Automations tab.


**ACP (Beta) Docs Navigation**

  * [Overview](/en/enterprise/features/agent-control-plane/overview)
  * **Monitoring** _(you are here)_
  * [Rules](/en/enterprise/features/agent-control-plane/rules)

## 

​

Overview

The **Automations** tab is the read-only operations view of the [Agent Control Plane](/en/enterprise/features/agent-control-plane/overview). It combines two metric cards, an interactive sankey, and two sub-tables — **Automations** and **Consumption** — that you can search, filter, and sort.

![Agent Control Plane overview](https://mintcdn.com/crewai/HY7Xvrzh3OdVk_2O/images/enterprise/acp-overview-automations-sankey.png?fit=max&auto=format&n=HY7Xvrzh3OdVk_2O&q=85&s=e2648e1d5841f113a9fafab8f10a34ab)

All charts and tables respect the **Last 24 hours / Last Week / Last 30 days** selector at the top right. Deltas compare the selected window against the previous one of the same length.

Rows only show data for deployments on **crewAI v1.13 or higher** — older deployments appear in the _“We’ve detected N other automations that we can’t display”_ banner under the sankey and contribute zero metrics until they’re updated and re-deployed. See [Overview — Requirements](/en/enterprise/features/agent-control-plane/overview#requirements).

## 

​

Dashboard

The header of the page has two metric cards and an interactive sankey. Clicking either card switches the sankey between two modes:

  * **Health mode** — `Total Automations → status buckets (Critical / Warning / Healthy)`. Click a bucket to filter the Automations table to just those deployments.
  * **Consumption mode** — `Model Providers → Automations → Total Cost`. Click a provider to filter the Consumption table to that provider.

Card| What it shows  
---|---  
**Automations**| `active` automations (and total count), total `errors` in the window, currently `active executions` (and total in the window), with a delta vs the previous period.  
**Consumption**|  Total `cost` and `tokens used`, with a cost delta vs the previous period.  
  
![Overview with consumption sankey](https://mintcdn.com/crewai/HY7Xvrzh3OdVk_2O/images/enterprise/acp-overview-consumption-sankey.png?fit=max&auto=format&n=HY7Xvrzh3OdVk_2O&q=85&s=f9df1214919a385ab426742b4a5315d9)

## 

​

Automations table

The **Automations** sub-tab is the per-deployment breakdown of fleet health. Each row is one deployed crew or flow.

![Automations table with health status breakdown](https://mintcdn.com/crewai/HY7Xvrzh3OdVk_2O/images/enterprise/acp-automations-table.png?fit=max&auto=format&n=HY7Xvrzh3OdVk_2O&q=85&s=900866a0051e59b8e6948d2cad01d977)

Column| What it shows  
---|---  
**Automation**|  Deployment name and any tags assigned to it (e.g. `production`, `financial`).  
**Last execution**|  Time since the most recent run.  
**Health Status Breakdown**|  Stacked bar of `Critical` / `Warning` / `Healthy` percentages for executions in the window.  
**Executions with Errors**|  Total failed executions in the window.  
**PII detection applied**| `Yes` if a per-deployment PII config or a matching [PII rule](/en/enterprise/features/agent-control-plane/rules) is active.  
**Executions**|  Total executions in the window.  
**Last updated**|  When the deployment was last re-deployed.  
**Crew Version**|  The `crewai` version reported by the deployment. An info icon next to versions below `1.13` flags rows that can’t contribute metrics.  
  
Search by name, filter by `Status` (`Healthy` / `Warning` / `Critical`), and sort by any column header. Click a deployment name to open the **Automation panel** (see below).

## 

​

Consumption table

The **Consumption** sub-tab is the per-deployment breakdown of LLM spend and token usage.

![Consumption table broken down by LLM provider](https://mintcdn.com/crewai/HY7Xvrzh3OdVk_2O/images/enterprise/acp-consumption-table.png?fit=max&auto=format&n=HY7Xvrzh3OdVk_2O&q=85&s=4bbd46bbe7360c7edf1eca351d055443)

Column| What it shows  
---|---  
**Automation**|  Deployment name.  
**Last execution**|  Time since the most recent run.  
**Tokens used**|  One row per LLM provider used by this automation, with the delta vs the previous period.  
**Cost**|  Cost per LLM provider, with the delta vs the previous period.  
**Total cost**|  Sum across all providers, with the delta.  
**Executions**|  Total executions in the window.  
**Last updated**|  When the deployment was last re-deployed.  
**Crew Version**|  The `crewai` version reported by the deployment.  
  
Filter by **LLM provider** and sort by `Cost`, `Executions`, or `Last run`.

**Empty cells (`—` or `$0.00`) usually mean the deployment is below crewAI v1.13.** In the screenshot above, _Automation F_ (`1.7.0`) and _Automation I_ (`1.12.2`) show blanks for tokens and cost — their executions still run, but they don’t emit the provider-level telemetry that powers this table. Update and re-deploy these crews to start collecting consumption data.

## 

​

Related

## Agent Control Plane — Overview

What ACP is, requirements, plan tiers, and RBAC.

## Agent Control Plane — Rules

Apply organization-wide PII Redaction rules across many automations.

## Traces

Drill into a single execution to see agent reasoning, tool calls, and token usage.

## Deploy to AMP

Deploy a crew on a crewAI version that supports the Agent Control Plane.

## Need Help?

Contact our support team for help interpreting metrics in the Agent Control Plane.

Was this page helpful?

YesNo

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)