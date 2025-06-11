"""Example ADK agent using DatastoreSearchTool."""

from dotenv import load_dotenv
from google.adk.agents import Agent

from .config import agent_config
from .prompts import AGENT_INSTRUCTIONS
from .tools.datastore_tool import datastore_search_tool as search_tool
# from .tools.ragengine_tool import ask_vertex_ai_rag_engine as search_tool
# from .tools.ragengine_tool import rag_engine_tool as search_tool

load_dotenv()

rag_agent = Agent(
    model=agent_config.model,
    name=agent_config.name,
    instruction=AGENT_INSTRUCTIONS,
    tools=[search_tool],
)

__all__ = ["rag_agent"]
