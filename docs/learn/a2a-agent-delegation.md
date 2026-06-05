# Source: https://docs.crewai.com/en/learn/a2a-agent-delegation

Learn

# Agent-to-Agent (A2A) Protocol


Agents delegate tasks to remote A2A agents and/or operate as A2A-compliant server agents.


## 

​

A2A Agent Delegation

Deploying A2A agents to production? See [A2A on AMP](/en/enterprise/features/a2a) for distributed state, enterprise authentication, gRPC transport, and horizontal scaling.

CrewAI treats [A2A protocol](https://a2a-protocol.org/latest/) as a first-class delegation primitive, enabling agents to delegate tasks, request information, and collaborate with remote agents, as well as act as A2A-compliant server agents. In client mode, agents autonomously choose between local execution and remote delegation based on task requirements.

## 

​

How It Works

When an agent is configured with A2A capabilities:

  1. The Agent analyzes each task
  2. It decides to either:
     * Handle the task directly using its own capabilities
     * Delegate to a remote A2A agent for specialized handling
  3. If delegating, the agent communicates with the remote A2A agent through the protocol
  4. Results are returned to the CrewAI workflow

A2A delegation requires the `a2a-sdk` package. Install with: `uv add 'crewai[a2a]'` or `pip install 'crewai[a2a]'`

## 

​

Basic Configuration

`crewai.a2a.config.A2AConfig` is deprecated and will be removed in v2.0.0. Use `A2AClientConfig` for connecting to remote agents and/or `A2AServerConfig` for exposing agents as servers.

Configure an agent for A2A delegation by setting the `a2a` parameter:

Code
    
    
    from crewai import Agent, Crew, Task
    from crewai.a2a import A2AClientConfig
    
    agent = Agent(
        role="Research Coordinator",
        goal="Coordinate research tasks efficiently",
        backstory="Expert at delegating to specialized research agents",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://example.com/.well-known/agent-card.json",
            timeout=120,
            max_turns=10
        )
    )
    
    task = Task(
        description="Research the latest developments in quantum computing",
        expected_output="A comprehensive research report",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    

## 

​

Client Configuration Options

The `A2AClientConfig` class accepts the following parameters:

​

endpoint

str

required

The A2A agent endpoint URL (typically points to `.well-known/agent-card.json`)

​

auth

AuthScheme

default:"None"

Authentication scheme for the A2A agent. Supports Bearer tokens, OAuth2, API keys, and HTTP authentication.

​

timeout

int

default:"120"

Request timeout in seconds

​

max_turns

int

default:"10"

Maximum number of conversation turns with the A2A agent

​

response_model

type[BaseModel]

default:"None"

Optional Pydantic model for requesting structured output from an A2A agent. A2A protocol does not enforce this, so an A2A agent does not need to honor this request.

​

fail_fast

bool

default:"True"

Whether to raise an error immediately if agent connection fails. When `False`, the agent continues with available agents and informs the LLM about unavailable ones.

​

trust_remote_completion_status

bool

default:"False"

When `True`, returns the A2A agent’s result directly when it signals completion. When `False`, allows the server agent to review the result and potentially continue the conversation.

​

updates

UpdateConfig

default:"StreamingConfig()"

Update mechanism for receiving task status. Options: `StreamingConfig`, `PollingConfig`, or `PushNotificationConfig`.

​

accepted_output_modes

list[str]

default:"[\"application/json\"]"

Media types the client can accept in responses.

​

extensions

list[str]

default:"[]"

A2A protocol extension URIs the client supports.

​

client_extensions

list[A2AExtension]

default:"[]"

Client-side processing hooks for tool injection, prompt augmentation, and response modification.

​

transport

ClientTransportConfig

default:"ClientTransportConfig()"

Transport configuration including preferred transport, supported transports for negotiation, and protocol-specific settings (gRPC message sizes, keepalive, etc.).

​

transport_protocol

Literal['JSONRPC', 'GRPC', 'HTTP+JSON']

default:"None"

**Deprecated** : Use `transport=ClientTransportConfig(preferred=...)` instead.

​

supported_transports

list[str]

default:"None"

**Deprecated** : Use `transport=ClientTransportConfig(supported=...)` instead.

## 

​

Authentication

For A2A agents that require authentication, use one of the provided auth schemes:

  * Bearer Token

  * API Key

  * OAuth2

  * HTTP Basic

bearer_token_auth.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.auth import BearerTokenAuth
    
    agent = Agent(
        role="Secure Coordinator",
        goal="Coordinate tasks with secured agents",
        backstory="Manages secure agent communications",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://secure-agent.example.com/.well-known/agent-card.json",
            auth=BearerTokenAuth(token="your-bearer-token"),
            timeout=120
        )
    )
    

api_key_auth.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.auth import APIKeyAuth
    
    agent = Agent(
        role="API Coordinator",
        goal="Coordinate with API-based agents",
        backstory="Manages API-authenticated communications",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://api-agent.example.com/.well-known/agent-card.json",
            auth=APIKeyAuth(
                api_key="your-api-key",
                location="header",  # or "query" or "cookie"
                name="X-API-Key"
            ),
            timeout=120
        )
    )
    

oauth2_auth.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.auth import OAuth2ClientCredentials
    
    agent = Agent(
        role="OAuth Coordinator",
        goal="Coordinate with OAuth-secured agents",
        backstory="Manages OAuth-authenticated communications",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://oauth-agent.example.com/.well-known/agent-card.json",
            auth=OAuth2ClientCredentials(
                token_url="https://auth.example.com/oauth/token",
                client_id="your-client-id",
                client_secret="your-client-secret",
                scopes=["read", "write"]
            ),
            timeout=120
        )
    )
    

http_basic_auth.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.auth import HTTPBasicAuth
    
    agent = Agent(
        role="Basic Auth Coordinator",
        goal="Coordinate with basic auth agents",
        backstory="Manages basic authentication communications",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://basic-agent.example.com/.well-known/agent-card.json",
            auth=HTTPBasicAuth(
                username="your-username",
                password="your-password"
            ),
            timeout=120
        )
    )
    

## 

​

Multiple A2A Agents

Configure multiple A2A agents for delegation by passing a list:

Code
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.auth import BearerTokenAuth
    
    agent = Agent(
        role="Multi-Agent Coordinator",
        goal="Coordinate with multiple specialized agents",
        backstory="Expert at delegating to the right specialist",
        llm="gpt-4o",
        a2a=[
            A2AClientConfig(
                endpoint="https://research.example.com/.well-known/agent-card.json",
                timeout=120
            ),
            A2AClientConfig(
                endpoint="https://data.example.com/.well-known/agent-card.json",
                auth=BearerTokenAuth(token="data-token"),
                timeout=90
            )
        ]
    )
    

The LLM will automatically choose which A2A agent to delegate to based on the task requirements.

## 

​

Error Handling

Control how agent connection failures are handled using the `fail_fast` parameter:

Code
    
    
    from crewai.a2a import A2AClientConfig
    
    # Fail immediately on connection errors (default)
    agent = Agent(
        role="Research Coordinator",
        goal="Coordinate research tasks",
        backstory="Expert at delegation",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://research.example.com/.well-known/agent-card.json",
            fail_fast=True
        )
    )
    
    # Continue with available agents
    agent = Agent(
        role="Multi-Agent Coordinator",
        goal="Coordinate with multiple agents",
        backstory="Expert at working with available resources",
        llm="gpt-4o",
        a2a=[
            A2AClientConfig(
                endpoint="https://primary.example.com/.well-known/agent-card.json",
                fail_fast=False
            ),
            A2AClientConfig(
                endpoint="https://backup.example.com/.well-known/agent-card.json",
                fail_fast=False
            )
        ]
    )
    

When `fail_fast=False`:

  * If some agents fail, the LLM is informed which agents are unavailable and can delegate to working agents
  * If all agents fail, the LLM receives a notice about unavailable agents and handles the task directly
  * Connection errors are captured and included in the context for better decision-making

## 

​

Update Mechanisms

Control how your agent receives task status updates from remote A2A agents:

  * Streaming (Default)

  * Polling

  * Push Notifications

streaming_config.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.updates import StreamingConfig
    
    agent = Agent(
        role="Research Coordinator",
        goal="Coordinate research tasks",
        backstory="Expert at delegation",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://research.example.com/.well-known/agent-card.json",
            updates=StreamingConfig()
        )
    )
    

polling_config.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.updates import PollingConfig
    
    agent = Agent(
        role="Research Coordinator",
        goal="Coordinate research tasks",
        backstory="Expert at delegation",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://research.example.com/.well-known/agent-card.json",
            updates=PollingConfig(
                interval=2.0,
                timeout=300.0,
                max_polls=100
            )
        )
    )
    

push_notifications_config.py
    
    
    from crewai.a2a import A2AClientConfig
    from crewai.a2a.updates import PushNotificationConfig
    
    agent = Agent(
        role="Research Coordinator",
        goal="Coordinate research tasks",
        backstory="Expert at delegation",
        llm="gpt-4o",
        a2a=A2AClientConfig(
            endpoint="https://research.example.com/.well-known/agent-card.json",
            updates=PushNotificationConfig(
                url="{base_url}/a2a/callback",
                token="your-validation-token",
                timeout=300.0
            )
        )
    )
    

## 

​

Exposing Agents as A2A Servers

You can expose your CrewAI agents as A2A-compliant servers, allowing other A2A clients to delegate tasks to them.

### 

​

Server Configuration

Add an `A2AServerConfig` to your agent to enable server capabilities:

a2a_server_agent.py
    
    
    from crewai import Agent
    from crewai.a2a import A2AServerConfig
    
    agent = Agent(
        role="Data Analyst",
        goal="Analyze datasets and provide insights",
        backstory="Expert data scientist with statistical analysis skills",
        llm="gpt-4o",
        a2a=A2AServerConfig(url="https://your-server.com")
    )
    

### 

​

Server Configuration Options

​

name

str

default:"None"

Human-readable name for the agent. Defaults to the agent’s role if not provided.

​

description

str

default:"None"

Human-readable description. Defaults to the agent’s goal and backstory if not provided.

​

version

str

default:"1.0.0"

Version string for the agent card.

​

skills

list[AgentSkill]

default:"[]"

List of agent skills. Auto-generated from agent tools if not provided.

​

capabilities

AgentCapabilities

Declaration of optional capabilities supported by the agent.

​

default_input_modes

list[str]

default:"[\"text/plain\", \"application/json\"]"

Supported input MIME types.

​

default_output_modes

list[str]

default:"[\"text/plain\", \"application/json\"]"

Supported output MIME types.

​

url

str

default:"None"

Preferred endpoint URL. If set, overrides the URL passed to `to_agent_card()`.

​

protocol_version

str

default:"0.3.0"

A2A protocol version this agent supports.

​

provider

AgentProvider

default:"None"

Information about the agent’s service provider.

​

documentation_url

str

default:"None"

URL to the agent’s documentation.

​

icon_url

str

default:"None"

URL to an icon for the agent.

​

additional_interfaces

list[AgentInterface]

default:"[]"

Additional supported interfaces (transport and URL combinations).

​

security

list[dict[str, list[str]]]

default:"[]"

Security requirement objects for all agent interactions.

​

security_schemes

dict[str, SecurityScheme]

default:"{}"

Security schemes available to authorize requests.

​

supports_authenticated_extended_card

bool

default:"False"

Whether agent provides extended card to authenticated users.

​

extended_skills

list[AgentSkill]

default:"[]"

Additional skills visible only to authenticated users in the extended agent card.

​

signing_config

AgentCardSigningConfig

default:"None"

Configuration for signing the AgentCard with JWS. Supports RS256, ES256, PS256, and related algorithms.

​

server_extensions

list[ServerExtension]

default:"[]"

Server-side A2A protocol extensions with `on_request`/`on_response` hooks that modify agent behavior.

​

push_notifications

ServerPushNotificationConfig

default:"None"

Configuration for outgoing push notifications, including HMAC-SHA256 signing secret.

​

transport

ServerTransportConfig

default:"ServerTransportConfig()"

Transport configuration including preferred transport, gRPC server settings, JSON-RPC paths, and HTTP+JSON settings.

​

auth

ServerAuthScheme

default:"None"

Authentication scheme for incoming A2A requests. Defaults to `SimpleTokenAuth` using the `AUTH_TOKEN` environment variable.

​

preferred_transport

Literal['JSONRPC', 'GRPC', 'HTTP+JSON']

default:"None"

**Deprecated** : Use `transport=ServerTransportConfig(preferred=...)` instead.

​

signatures

list[AgentCardSignature]

default:"None"

**Deprecated** : Use `signing_config=AgentCardSigningConfig(...)` instead.

### 

​

Combined Client and Server

An agent can act as both client and server by providing both configurations:

Code
    
    
    from crewai import Agent
    from crewai.a2a import A2AClientConfig, A2AServerConfig
    
    agent = Agent(
        role="Research Coordinator",
        goal="Coordinate research and serve analysis requests",
        backstory="Expert at delegation and analysis",
        llm="gpt-4o",
        a2a=[
            A2AClientConfig(
                endpoint="https://specialist.example.com/.well-known/agent-card.json",
                timeout=120
            ),
            A2AServerConfig(url="https://your-server.com")
        ]
    )
    

### 

​

File Inputs and Structured Output

A2A supports passing files and requesting structured output in both directions. **Client side** : When delegating to a remote A2A agent, files from the task’s `input_files` are sent as `FilePart`s in the outgoing message. If `response_model` is set on the `A2AClientConfig`, the Pydantic model’s JSON schema is embedded in the message metadata, requesting structured output from the remote agent. **Server side** : Incoming `FilePart`s are extracted and passed to the agent’s task as `input_files`. If the client included a JSON schema, the server creates a response model from it and applies it to the task. When the agent returns structured data, the response is sent back as a `DataPart` rather than plain text.

## 

​

Best Practices

## Set Appropriate Timeouts

Configure timeouts based on expected A2A agent response times. Longer-running tasks may need higher timeout values.

## Limit Conversation Turns

Use `max_turns` to prevent excessive back-and-forth. The agent will automatically conclude conversations before hitting the limit.

## Use Resilient Error Handling

Set `fail_fast=False` for production environments with multiple agents to gracefully handle connection failures and maintain workflow continuity.

## Secure Your Credentials

Store authentication tokens and credentials as environment variables, not in code.

## Monitor Delegation Decisions

Use verbose mode to observe when the LLM chooses to delegate versus handle tasks directly.

## 

​

Supported Authentication Methods

  * **Bearer Token** \- Simple token-based authentication
  * **OAuth2 Client Credentials** \- OAuth2 flow for machine-to-machine communication
  * **OAuth2 Authorization Code** \- OAuth2 flow requiring user authorization
  * **API Key** \- Key-based authentication (header, query param, or cookie)
  * **HTTP Basic** \- Username/password authentication
  * **HTTP Digest** \- Digest authentication (requires `httpx-auth` package)

## 

​

Learn More

For more information about the A2A protocol and reference implementations:

  * [A2A Protocol Documentation](https://a2a-protocol.org)
  * [A2A Sample Implementations](https://github.com/a2aproject/a2a-samples)
  * [A2A Python SDK](https://github.com/a2aproject/a2a-python)

Was this page helpful?

YesNo

⌘I

[website](https://crewai.com)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[reddit](https://www.reddit.com/r/crewAIInc)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=crewai)