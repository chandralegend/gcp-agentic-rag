# gcp-agentic-rag

This repository provides a small boilerplate for building a Retrieval Augmented Generation (RAG) agent using the Vertex AI Agent Development Kit (ADK) and Vertex AI RAG Engine.

Configuration is managed through YAML files located in the `config/` directory. These files define agent behaviour, deployment settings and prompt text so the project can be easily customised without modifying the code.

## Configuration

- **config/agent.yaml** – parameters for the agent such as model name, datastore details and the RAG corpus id.
- **config/deployment.yaml** – project, location and staging bucket used when deploying the agent.
- **config/prompts.yaml** – prompt text. The `agent_instructions` entry is loaded and used when creating the agent.

## Usage

Install dependencies (using Poetry or pip) and adjust the YAML files to match your environment.

Common tasks are available through the `Makefile`:

```bash
make run        # run the deployed agent in the terminal
make deploy     # deploy the agent to Vertex AI Agent Engine
make rag-engine # create a RAG Engine corpus from local markdown files
```

The deployment script writes the created agent engine id to `.env`. Ensure this file contains your Vertex project credentials before running the make commands.

## Structure

- `agent.py` – builds the ADK agent using configuration and prompts from YAML.
- `tools/` – tools used by the agent. They read configuration from `config/agent.yaml`.
- `scripts/` – helper scripts to deploy the agent, run it and create a RAG Engine corpus.

This template can be extended to suit different projects by editing the YAML files and adding additional tools or prompts.
