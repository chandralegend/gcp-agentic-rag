from __future__ import annotations

from typing import Any, List

from google.genai import types
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from google.adk.tools.tool_context import ToolContext
from vertexai.preview import rag
from ..config import agent_config


class RagEngineQueryTool(BaseTool):
    """Tool to query a Vertex AI RAG Engine corpus."""

    def __init__(self, rag_corpus: str, *, name: str = "query_rag_engine", description: str = "Query documents from Vertex AI RAG Engine") -> None:
        super().__init__(name=name, description=description)
        self.rag_corpus = rag_corpus

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
        response = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=self.rag_corpus)],
            similarity_top_k=5,
        )
        results: List[dict[str, str]] = []
        for ctx in response.contexts:
            results.append({
                "title": ctx.title,
                "content": ctx.chunk.content,
                "source_uri": ctx.source_uri,
            })
        return results


ask_vertex_ai_rag_engine = VertexAiRagRetrieval(
    name="retrieve_rag_documentation",
    description="Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,",
    rag_resources=[rag.RagResource(rag_corpus=agent_config.rag_corpus)],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

rag_engine_tool = RagEngineQueryTool(
    rag_corpus=agent_config.rag_corpus or "default_rag_corpus",
    name="rag_engine_query_tool",
    description="Tool to query a Vertex AI RAG Engine corpus for relevant documents."
)

__all__ = [
    "ask_vertex_ai_rag_engine",
    "rag_engine_tool",
]