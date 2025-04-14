.PHONY: dev help

help: ## Show this help
	@echo "Available commands:"
	@echo "  dev    - Run the development server locally using functions-framework with environment variables"

.DEFAULT_GOAL := help

dev:
	uv run --env-file .env functions-framework --target=main --port=9000