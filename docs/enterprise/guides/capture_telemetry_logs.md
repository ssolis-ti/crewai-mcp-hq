# Source: https://docs.crewai.com/en/enterprise/guides/capture_telemetry_logs

How-To Guides

# OpenTelemetry Export


Export traces and logs from your CrewAI AMP deployments to your own OpenTelemetry collector


CrewAI AMP can export OpenTelemetry **traces** and **logs** from your deployments directly to your own collector. This lets you monitor agent performance, track LLM calls, and debug issues using your existing observability stack. Telemetry data follows the [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) plus additional CrewAI-specific attributes.

## 

​

Prerequisites

## CrewAI AMP account

Your organization must have an active CrewAI AMP account.

## OpenTelemetry collector

You need an OpenTelemetry-compatible collector endpoint (e.g., your own OTel Collector, Datadog, Grafana, or any OTLP-compatible backend).

## 

​

Setting up a collector

  1. In CrewAI AMP, go to **Settings** > **OpenTelemetry Collectors**.
  2. Click **Add Collector**.
  3. Select an integration type — **OpenTelemetry Traces** or **OpenTelemetry Logs**.
  4. Configure the connection:
     * **Endpoint** — Your collector’s OTLP endpoint (e.g., `https://otel-collector.example.com:4317`).
     * **Service Name** — A name to identify this service in your observability platform.
     * **Custom Headers** _(optional)_ — Add authentication or routing headers as key-value pairs.
     * **Certificate** _(optional)_ — Provide a TLS certificate if your collector requires one.
  5. Click **Save**.

![OpenTelemetry Collector Configuration](https://mintcdn.com/crewai/Iusqhn1gyqMXVYO_/images/crewai-otel-collector-config.png?fit=max&auto=format&n=Iusqhn1gyqMXVYO_&q=85&s=a20c5089fc516d820142637c18cf9a5e)

You can add multiple collectors — for example, one for traces and another for logs, or send to different backends for different purposes.

Was this page helpful?

YesNo

[Enable Crew StudioPrevious](/en/enterprise/guides/enable-crew-studio)[Azure OpenAI SetupNext](/en/enterprise/guides/azure-openai-setup)

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)