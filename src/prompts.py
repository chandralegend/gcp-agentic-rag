"""Load prompts from YAML configuration."""

from pathlib import Path
import yaml

_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

with (_CONFIG_DIR / "prompts.yaml").open() as f:
    _PROMPTS = yaml.safe_load(f) or {}

AGENT_INSTRUCTIONS: str = _PROMPTS.get("agent_instructions", "")

__all__ = ["AGENT_INSTRUCTIONS"]
