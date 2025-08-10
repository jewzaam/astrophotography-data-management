# Environment Setup Targets
# ========================

.PHONY: venv uv pip-install pip-install-dev clean deps check-deps

venv: ## Create Python virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		printf "$(GREEN)✅ Virtual environment created$(RESET)\n"; \
	fi

uv: venv ## Install uv package manager
	@if [ ! -f "$(VENV_DIR)/bin/uv" ]; then \
		$(PYTHON) -m ensurepip --upgrade; \
		$(PYTHON) -m pip install uv; \
		printf "$(GREEN)✅ uv installed$(RESET)\n"; \
	fi

deps: uv ## Install production dependencies
	@if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then \
		$(UV) pip install --upgrade pip >/dev/null; \
		$(UV) pip install -r requirements.txt; \
		printf "$(GREEN)✅ Production dependencies installed$(RESET)\n"; \
	else \
		printf "$(YELLOW)No production dependencies to install$(RESET)\n"; \
	fi

pip-install-dev: uv deps ## Install development dependencies in venv
	@if [ -f "requirements-dev.txt" ]; then \
		$(UV) pip install -r requirements-dev.txt; \
		printf "$(GREEN)✅ Development dependencies installed$(RESET)\n"; \
	else \
		printf "$(YELLOW)No development dependencies file found$(RESET)\n"; \
	fi

check-deps: ## Check for missing system dependencies
	@command -v python3 >/dev/null 2>&1 || { echo "❌ python3 is required but not installed"; exit 1; }
	@command -v sqlite3 >/dev/null 2>&1 || { echo "⚠️  sqlite3 not found, may be needed for database operations"; }
	@printf "$(GREEN)✅ System dependencies check completed$(RESET)\n"

clean: ## Remove temporary and backup files
	# Python caches
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	# Python virtual environment
	@rm -rf $(VENV_DIR) 2>/dev/null || true
	# Build and distribution artifacts
	@rm -rf dist build *.egg-info/ 2>/dev/null || true
	# Testing artifacts
	@rm -rf .pytest_cache .coverage htmlcov .tox 2>/dev/null || true
	# Linting caches
	@rm -rf .ruff_cache .mypy_cache 2>/dev/null || true
	# Local development artifacts
	@rm -rf local scratch logs 2>/dev/null || true
	@echo "✅ Cleanup completed"