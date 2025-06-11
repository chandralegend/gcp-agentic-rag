"""Load prompts from YAML configuration."""

from pathlib import Path
import yaml

_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

with (_CONFIG_DIR / "prompts.yaml").open() as f:
    _PROMPTS = yaml.safe_load(f) or {}

def get_prompt(name: str) -> str:
    """Retrieve a prompt by name."""
    prompt = _PROMPTS.get(name)
    assert prompt, f"Prompt '{name}' not found in prompts.yaml"
    return prompt

__all__ = ["get_prompt"]
