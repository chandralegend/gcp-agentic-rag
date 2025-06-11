import os
import json
import asyncio
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService

from src.config import deployment_config


def pretty_print_event(event: dict) -> None:
    if "content" not in event:
        print(f"[{event.get('author', 'unknown')}]: {event}")
        return
    author = event.get("author", "unknown")
    parts = event["content"].get("parts", [])
    for part in parts:
        if "text" in part:
            text = part["text"]
            if len(text) > 200:
                text = text[:197] + "..."
            print(f"[{author}]: {text}")
        elif "functionCall" in part:
            func_call = part["functionCall"]
            args = json.dumps(func_call.get("args", {}))
            if len(args) > 100:
                args = args[:97] + "..."
            print(f"[{author}]: Function call {func_call.get('name', '')} {args}")
        elif "functionResponse" in part:
            func_response = part["functionResponse"]
            response = json.dumps(func_response.get("response", {}))
            if len(response) > 100:
                response = response[:97] + "..."
            print(f"[{author}]: Function response {func_response.get('name', '')} {response}")


def main() -> None:
    load_dotenv()
    vertexai.init(project=deployment_config.project, location=deployment_config.location)
    session_service = VertexAiSessionService(project=deployment_config.project, location=deployment_config.location)
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")
    if not agent_engine_id:
        raise RuntimeError("AGENT_ENGINE_ID not set. Deploy the agent first.")

    session = asyncio.run(session_service.create_session(app_name=agent_engine_id, user_id="local-user"))
    agent_engine = agent_engines.get(agent_engine_id)

    while True:
        query = input("\n[user]: ")
        if not query:
            break
        for event in agent_engine.stream_query(user_id="local-user", session_id=session.id, message=query):
            pretty_print_event(event)


if __name__ == "__main__":
    main()

