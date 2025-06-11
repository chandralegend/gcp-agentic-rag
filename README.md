# Vertex AI RAG Agent Template

This repository provides a small boilerplate for building a Retrieval Augmented Generation (RAG) agent using the Vertex AI Agent Development Kit (ADK) and Vertex AI RAG Engine.

Configuration is managed through YAML files located in the `config/` directory. These files define agent behaviour, deployment settings and prompt text so the project can be easily customised without modifying the code.

## Configuration

- **src/config/agent.yaml** – parameters for the agent such as model name, datastore details and the RAG corpus id.
- **src/config/deployment.yaml** – project, location and staging bucket used when deploying the agent.
- **src/config/prompts.yaml** – prompt text. The `default` entry is loaded and used when creating the agent.

## Usage

Install dependencies (using Poetry or pip) and adjust the YAML files to match your environment.

```bash
make install  # install dependencies
```

Common tasks are available through the `Makefile`:

```bash
make web        # start a web server to view the agent in the browser
make run        # run the deployed agent in the terminal
make deploy     # deploy the agent to Vertex AI Agent Engine
make rag-engine # create a RAG Engine corpus from local markdown files
python scripts/index_datastore.py --metadata-file metadata.json \ 
    # index markdown and metadata into Cloud Datastore
python scripts/index_rag_engine.py --metadata-file metadata.json \ 
    --corpus your-corpus-id  # upload files to an existing RAG corpus
```

The deployment script writes the created agent engine id to `.env`. Ensure this file contains your Vertex project credentials before running the make commands.

## Structure

- `agent.py` – builds the ADK agent using configuration and prompts from YAML.
- `tools/` – tools used by the agent. They read configuration from `config/agent.yaml`.
- `scripts/` – helper scripts to deploy the agent, run it and create a RAG Engine corpus.

This template can be extended to suit different projects by editing the YAML files and adding additional tools or prompts.
