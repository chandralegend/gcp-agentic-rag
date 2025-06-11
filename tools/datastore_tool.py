import os

from typing import Any

from google.genai import types
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from ..utils.discover_datastore_searcher import (
    DiscoveryDatastoreSearcher,
    DiscoveryDatastoreSearcherConfig,
)


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
    project_id=os.environ.get("GCP_PROJECT", ""),
    location=os.environ.get("GCP_LOCATION", "us-central1"),
    data_store_id=os.environ.get("DATASTORE_ID", ""),
    datastore_kind=os.environ.get("DATASTORE_KIND", "Document"),
)

searcher = DiscoveryDatastoreSearcher(config=config)

datastore_search_tool = DatastoreSearchTool(
    searcher=searcher,
    name="search_datastore",
    description="Search documents from datastore",
)

__all__ = ["datastore_search_tool"]