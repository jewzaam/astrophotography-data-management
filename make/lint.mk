# Linting & Quality Targets
# =========================

.PHONY: lint

lint: pip-install-dev ## Run all code quality checks (linting, formatting, type checking)
	@if [ -n "$$(find . -name '*.py' -not -path './.venv/*' -not -path './.*' 2>/dev/null)" ]; then \
		ruff check .; \
		ruff format --check .; \
		mypy --ignore-missing-imports .; \
		printf "$(GREEN)✅ All code quality checks passed$(RESET)\n"; \
	else \
		printf "$(YELLOW)No Python files found to check$(RESET)\n"; \
	fi