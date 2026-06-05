# Source: https://docs.crewai.com/en/enterprise/features/agent-control-plane/overview

## On this page

  * Overview
  * Requirements
  * What you can do here
  * Related

Agent Control Plane

# Agent Control Plane Overview


Single operations hub for live automations — fleet health, LLM consumption, and organization-wide policies in one place.


**ACP (Beta) Docs Navigation**

  * **Overview** _(you are here)_
  * [Monitoring](/en/enterprise/features/agent-control-plane/monitoring)
  * [Rules](/en/enterprise/features/agent-control-plane/rules)

## 

​

Overview

The **Agent Control Plane** (ACP) is the operations hub for everything you have running on CrewAI AMP. It is a single screen — split into **Automations** and **Rules** tabs — that lets your team:

  * Monitor the **health** of every live automation (crew or flow), with `Critical` / `Warning` / `Healthy` breakdowns and execution counts.
  * Track **LLM consumption** — tokens and cost — per automation, per provider, and per model, with a delta vs the previous period.
  * Drill into any single automation or model provider for time-series charts and per-provider breakdowns.
  * Apply organization-wide **Rules** (today: PII Redaction) across many automations at once instead of editing each deployment individually.

![Agent Control Plane overview](https://mintcdn.com/crewai/HY7Xvrzh3OdVk_2O/images/enterprise/acp-overview-automations-sankey.png?fit=max&auto=format&n=HY7Xvrzh3OdVk_2O&q=85&s=e2648e1d5841f113a9fafab8f10a34ab)

The Agent Control Plane is currently labeled **Beta** in CrewAI Platform.

The two tabs answer two different questions:

  * **Automations** — _“How is my fleet behaving right now, and what is it costing me?”_ See [Monitoring](/en/enterprise/features/agent-control-plane/monitoring).
  * **Rules** — _“How do I enforce a policy (e.g. PII redaction) across many deployments without re-deploying each one?”_ See [Rules](/en/enterprise/features/agent-control-plane/rules).

## 

​

Requirements

**crewAI v1.13 or higher** is required for an automation to populate any data on this page — health, executions, errors, tokens, and cost all flow through telemetry that lit up in `crewai==1.13`. Older deployments appear in the _“We’ve detected N other automations that we can’t display”_ banner and contribute zero rows until they are updated and re-deployed.

**Enterprise Plan or Ultra Plan** is required to create or edit [Rules](/en/enterprise/features/agent-control-plane/rules). Lower-tier organizations can open the Rules tab and view existing rules, but the editor renders read-only with an “Enterprise” lock pill and the alert _“PII Redaction rules require an Enterprise plan.”_ Monitoring (the Automations tab) is available on all plans where the feature is enabled.

  * The **Agent Control Plane** feature must be enabled for your organization. If you don’t see it in the sidebar, ask your account owner to request enablement.
  * Inside ACP, [RBAC](/en/enterprise/features/rbac) governs access: `read` to view the dashboard and rules, `manage` to create, edit, toggle, or delete rules.
  * All charts and tables can be scoped to the **Last 24 hours** , **Last Week** , or **Last 30 days** using the time selector at the top right. Deltas (`↑ 8 vs yesterday`, `↓ $20.57 vs yesterday`, etc.) compare the selected window against the previous one of the same length.

## 

​

What you can do here

## Monitoring

Watch fleet health and LLM spend with metric cards, an interactive sankey, per-automation tables, and drill-down side panels for any automation or provider.

## Rules

Apply organization-wide PII Redaction policies scoped by tools and tags. Changes take effect on the next execution — no re-deploy required.

## 

​

Related

## Traces

Drill into a single execution to see agent reasoning, tool calls, and token usage.

## RBAC

Manage who can read the Agent Control Plane and who can edit rules.

## PII Redaction for Traces

Entity catalog and per-deployment PII configuration referenced by Rules.

## Deploy to AMP

Deploy a crew on a crewAI version that supports the Agent Control Plane.

## Need Help?

Contact our support team for help interpreting metrics or designing rules.

Was this page helpful?

YesNo

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)