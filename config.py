from pydantic_settings import BaseSettings

class AgentConfig(BaseSettings):
    # Agent configuration settings
    ...

class DeploymentConfig(BaseSettings):
    # Deployment configuration settings
    ...

agent_config = AgentConfig()
deployment_config = DeploymentConfig()

__all__ = ["agent_config", "deployment_config"]