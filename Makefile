.PHONY: install run-local run-ray test test-local test-ray demo clean requirements dev-setup help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using Poetry
	@echo "Installing dependencies..."
	poetry install

run-local: ## Run services locally (separate ports)
	@echo "Starting local services..."
	poetry run python deployment/local_deploy.py

run-ray: ## Deploy services using Ray Serve
	@echo "Deploying with Ray Serve..."
	poetry run python deployment/ray_deploy.py

test: ## Test the services
	@echo "Running service tests..."
	poetry run python presentation/test_services.py

test-local: ## Test local services automatically
	@echo "Testing local services..."
	echo "1" | poetry run python presentation/test_services.py

test-ray: ## Test Ray services automatically
	@echo "Testing Ray services..."
	echo "2" | poetry run python presentation/test_services.py

demo: ## Run interactive demo
	@echo "Starting interactive demo..."
	poetry run python presentation/demo.py

clean: ## Clean up Ray and Python cache
	@echo "Cleaning up..."
	ray stop --force 2>/dev/null || true
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

dev-setup: install ## Complete development setup
	@echo "Development setup complete!"
	@echo "   Run 'make run-local' to start local services"
	@echo "   Run 'make run-ray' to deploy with Ray Serve"
	@echo "   Run 'make test' to test the services"
