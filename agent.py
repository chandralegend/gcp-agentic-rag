"""Example ADK agent using DatastoreSearchTool."""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

from .prompts import AGENT_INSTRUCTIONS
from .tools.datastore_tool import datastore_search_tool as search_tool
# from .tools.ragengine_tool import ask_vertex_ai_rag_engine as search_tool
# from .tools.ragengine_tool import rag_engine_tool as search_tool

load_dotenv()

rag_agent = Agent(
    model="gemini-2.0-pro",  # default model
    name="datastore_rag_agent",
    instruction=AGENT_INSTRUCTIONS,
    tools=[search_tool],
)
