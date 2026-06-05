# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy project configuration
COPY pyproject.toml .

# Install dependencies (this creates a cached layer)
RUN uv pip install --system "mcp[cli]>=1.0" crewai crewai-tools chromadb pydantic pyyaml python-dotenv

# Copy source code
COPY src/ /app/src/

# Environment variables
ENV CREWAI_MCP_TRANSPORT=sse
ENV CREWAI_MCP_HOST=0.0.0.0
ENV CREWAI_MCP_PORT=8808
ENV CREWAI_DOCS_PATH=/app/docs
ENV CREWAI_WORKSPACE=/app/workspace
ENV CREWAI_KNOWLEDGE_DB=/app/knowledge_db

# Create directories
RUN mkdir -p /app/docs /app/workspace /app/knowledge_db

# Ensure Python path includes our source
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Expose port for SSE / Streamable HTTP
EXPOSE 8808

# Start the MCP server using the python module approach
CMD ["python", "-m", "crewai_mcp.server"]
