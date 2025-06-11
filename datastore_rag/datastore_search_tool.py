"""ADK tool wrapping DiscoveryDatastoreSearcher."""
from __future__ import annotations

from typing import Any, List, Optional, Tuple

from google.genai import types
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from .searcher import DiscoveryDatastoreSearcher


class DatastoreSearchTool(BaseTool):
    """Tool to query a Discovery Engine backed Datastore."""

    def __init__(self, searcher: DiscoveryDatastoreSearcher, *, name: str = "datastore_search", description: str = "Search indexed datastore documents") -> None:
        super().__init__(name=name, description=description)
        self.searcher = searcher

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "query": types.Schema(type=types.Type.STRING, description="User search query"),
                },
                required=["query"],
            ),
        )

    async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
        query = args["query"]
        results = self.searcher(query)
        return results
