.PHONY: run deploy rag-engine

run:
	poetry run python scripts/run_agent.py

deploy:
	poetry run python scripts/deploy.py

rag-engine:
	poetry run python scripts/create_rag_engine.py
