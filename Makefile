.PHONY: dev help

help: ## Show this help
	@echo "Available commands:"
	@echo "  dev    - Run the development server locally using functions-framework with environment variables"

.DEFAULT_GOAL := help

dev:
	uv run --env-file .env functions-framework --target=main --port=9001

deploy:
	gcloud functions deploy tr-webhook \
	  --runtime python311 \
	  --trigger-http \
	  --entry-point main \
	  --allow-unauthenticated \
	  --memory 512MB \
	  --timeout 60s \
	  --region us-central1