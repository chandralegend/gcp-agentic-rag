from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel

_CONFIG_DIR = Path(__file__).resolve().parent / "config"


def _load_yaml(filename: str) -> Dict[str, Any]:
    path = _CONFIG_DIR / filename
    if path.exists():
        with path.open() as f:
            return yaml.safe_load(f) or {}
    return {}


class AgentConfig(BaseModel):
    """Configuration for the agent."""

    name: str = "rag_agent"
    model: str = "gemini-1.5-pro"
    project_id: str = ""
    location: str = "us-central1"
    datastore_id: str = ""
    datastore_kind: str = "Document"
    rag_corpus: str | None = None


class DeploymentConfig(BaseModel):
    """Configuration for deployment."""

    project: str = ""
    location: str = "us-central1"
    staging_bucket: str = ""


agent_config = AgentConfig(**_load_yaml("agent.yaml"))
deployment_config = DeploymentConfig(**_load_yaml("deployment.yaml"))

__all__ = ["agent_config", "deployment_config"]
