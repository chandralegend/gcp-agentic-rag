.PHONY: run deploy rag-engine

run:
	python scripts/run_agent.py

deploy:
	python scripts/deploy.py

rag-engine:
	python scripts/create_rag_engine.py
