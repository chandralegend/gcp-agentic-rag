import logging
import os

import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
from dotenv import set_key

from ..agent import rag_agent
from ..config import deployment_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

vertexai.init(
    project=deployment_config.project,
    location=deployment_config.location,
    staging_bucket=deployment_config.staging_bucket,
)

logger.info("Deploying agent to Vertex AI Agent Engine...")
app = AdkApp(agent=rag_agent, enable_tracing=True)
remote_app = agent_engines.create(
    app,
    requirements=[
        "google-cloud-aiplatform[adk,agent-engines]==1.97.0",
        "google-adk",
        "python-dotenv",
    ],
    extra_packages=["./datastore_rag"],
)
logger.info("Deployed agent to Vertex AI Agent Engine successfully, resource name: %s", remote_app.resource_name)
set_key(ENV_FILE_PATH, "AGENT_ENGINE_ID", remote_app.resource_name)
print(f"Agent Engine resource name: {remote_app.resource_name}")

