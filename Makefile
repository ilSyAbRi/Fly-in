
GREEN=\033[1;38;5;156m
PURPLE=\033[1;38;5;171m
RESET=\033[0m

clean:
	@echo "$(PURPLE)Cleaning project...$(RESET)"

	@# find syntax: find [path] [conditions] [actions]
	@find . -type d \
		\( \
		-name "__pycache__" \
		-o -name ".pytest_cache" \
		-o -name ".mypy_cache" \
		\) \
		-exec rm -rf {} +
	
	@find . -type f \
		-name "*.pyc" \
		-delete

	@echo "$(GREEN)✔ Clean done: removed pycache, pytest, and mypy caches$(RESET)"
