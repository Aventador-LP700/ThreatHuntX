.DEFAULT_GOAL := help
.PHONY: help demo up down doctor test reset-demo
help:
	@printf '%s\n' 'make up          Build and start the lab' 'make doctor      Check local prerequisites' 'make test        Run Python tests with locked dependencies' 'make reset-demo  Reset this lab database' 'make down        Stop this project' 'make demo        Start the guided lab'
demo: up
up:
	./scripts/setup.sh
doctor:
	./scripts/setup.sh doctor
test:
	uv run --locked pytest
reset-demo:
	./scripts/setup.sh reset
down:
	./scripts/setup.sh down

.PHONY: showcase
showcase:
	npm --prefix frontend run build -- --mode showcase --outDir ../public-demo/dist --emptyOutDir
	PYTHONPATH=backend uv run --locked python -m scripts.build_showcase public-demo/dist
