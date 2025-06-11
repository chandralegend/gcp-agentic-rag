"""Example ADK agent using DatastoreSearchTool."""
import os
from dotenv import load_dotenv
from google.adk.agents import Agent

from .prompts import base_instructions
from .searcher import DiscoveryDatastoreSearcher, DiscoveryDatastoreSearcherConfig
from .datastore_search_tool import DatastoreSearchTool

load_dotenv()

config = DiscoveryDatastoreSearcherConfig(
    project_id=os.environ.get("GCP_PROJECT", ""),
    location=os.environ.get("GCP_LOCATION", "us-central1"),
    data_store_id=os.environ.get("DATASTORE_ID", ""),
    datastore_kind=os.environ.get("DATASTORE_KIND", "Document"),
)
searcher = DiscoveryDatastoreSearcher(config=config)

search_tool = DatastoreSearchTool(searcher, name="search_datastore", description="Search documents from datastore")

rag_agent = Agent(
    model="gemini-2.0-pro",  # default model
    name="datastore_rag_agent",
    instruction=base_instructions(),
    tools=[search_tool],
)
