from typing import Any

from google.genai import types
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from ..utils.discover_datastore_searcher import (
    DiscoveryDatastoreSearcher,
    DiscoveryDatastoreSearcherConfig,
)
from ..config import agent_config


class DatastoreSearchTool(BaseTool):
    """Tool to query a Discovery Engine backed Datastore."""

    def __init__(
        self,
        searcher: DiscoveryDatastoreSearcher,
        *,
        name: str = "datastore_search",
        description: str = "Search indexed datastore documents",
    ) -> None:
        super().__init__(name=name, description=description)
        self.searcher = searcher

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "query": types.Schema(
                        type=types.Type.STRING, description="User search query"
                    ),
                },
                required=["query"],
            ),
        )

    async def run_async(
        self, *, args: dict[str, Any], tool_context: ToolContext
    ) -> Any:
        query = args["query"]
        results = self.searcher(query)
        return results


config = DiscoveryDatastoreSearcherConfig(
    project_id=agent_config.project_id,
    location=agent_config.location,
    data_store_id=agent_config.datastore_id,
    datastore_kind=agent_config.datastore_kind,
)

searcher = DiscoveryDatastoreSearcher(config=config)

datastore_search_tool = DatastoreSearchTool(
    searcher=searcher,
    name="search_datastore",
    description="Search documents from datastore",
)

__all__ = ["datastore_search_tool"]