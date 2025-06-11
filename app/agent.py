"""Example ADK agent using DatastoreSearchTool."""

from dotenv import load_dotenv
from google.adk.agents import Agent

from .config import agent_config
# from .tools.datastore_tool import datastore_search_tool as search_tool
from .tools.ragengine_tool import ask_vertex_ai_rag_engine as search_tool
# from .tools.ragengine_tool import rag_engine_tool as search_tool
from .utils.prompts import get_prompt

load_dotenv()

root_agent = Agent(
    model=agent_config.model,
    name=agent_config.name,
    instruction=get_prompt(agent_config.agent_prompt_id),
    tools=[search_tool],
)

__all__ = ["root_agent"]
