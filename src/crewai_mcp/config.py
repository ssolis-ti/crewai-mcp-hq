"""
Centralized configuration for the CrewAI MCP Server.

Loads settings from environment variables (with .env support) and provides
typed access to all configuration values used across the server.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env from project root if present
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)


@dataclass(frozen=True)
class ServerConfig:
    """MCP transport & network configuration."""

    transport: str = "stdio"
    host: str = "0.0.0.0"
    port: int = 8808

    @classmethod
    def from_env(cls) -> "ServerConfig":
        return cls(
            transport=os.getenv("CREWAI_MCP_TRANSPORT", "stdio").lower(),
            host=os.getenv("CREWAI_MCP_HOST", "0.0.0.0"),
            port=int(os.getenv("CREWAI_MCP_PORT", "8808")),
        )


@dataclass(frozen=True)
class PathsConfig:
    """Filesystem paths used by the server."""

    docs_path: Path = field(default_factory=lambda: Path("./docs"))
    workspace: Path = field(default_factory=lambda: Path("./workspace"))
    knowledge_db: Path = field(default_factory=lambda: Path("./knowledge_db"))

    @classmethod
    def from_env(cls) -> "PathsConfig":
        base = Path(__file__).resolve().parent.parent.parent
        return cls(
            docs_path=Path(os.getenv("CREWAI_DOCS_PATH", str(base / "docs"))).resolve(),
            workspace=Path(os.getenv("CREWAI_WORKSPACE", str(base / "workspace"))).resolve(),
            knowledge_db=Path(os.getenv("CREWAI_KNOWLEDGE_DB", str(base / "knowledge_db"))).resolve(),
        )


@dataclass(frozen=True)
class LLMConfig:
    """Default LLM & embedding model settings."""

    default_llm: str = "openai/gpt-4o"
    embedder_provider: str = "openai"
    embedder_model: str = "text-embedding-3-small"
    embedder_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls(
            default_llm=os.getenv("CREWAI_DEFAULT_LLM", "openai/gpt-4o"),
            embedder_provider=os.getenv("CREWAI_EMBEDDER_PROVIDER", "openai"),
            embedder_model=os.getenv("CREWAI_EMBEDDER_MODEL", "text-embedding-3-small"),
            embedder_url=os.getenv("CREWAI_EMBEDDER_URL"),
        )

    def to_embedder_config(self) -> dict:
        """Return the embedder dict in the format CrewAI/ChromaDB expects."""
        cfg: dict = {"model": self.embedder_model}
        if self.embedder_url:
            cfg["url"] = self.embedder_url
        return {"provider": self.embedder_provider, "config": cfg}


@dataclass(frozen=True)
class AppConfig:
    """Root configuration aggregating all sub-configs."""

    server: ServerConfig = field(default_factory=ServerConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            server=ServerConfig.from_env(),
            paths=PathsConfig.from_env(),
            llm=LLMConfig.from_env(),
        )


# Singleton – import this wherever configuration is needed
config = AppConfig.from_env()
