
GREEN=\033[1;38;5;156m
PURPLE=\033[1;38;5;171m
YELLOW=\033[1;33m
BLUE=\033[1;34m
CYAN=\033[1;36m
RESET=\033[0m

help:
	@echo "$(PURPLE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(GREEN)        FLY-IN PROJECT HELP$(RESET)"
	@echo "$(PURPLE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo ""

	@echo "$(YELLOW)make install$(RESET)"
	@echo "$(BLUE)WHY:$(RESET)"
	@echo "  You need a separate safe Python environment for this project."
	@echo ""
	@echo "$(BLUE)WHAT IT DOES:$(RESET)"
	@echo "  $(CYAN)-$(RESET) Creates a virtual environment (venv)"
	@echo "  $(CYAN)-$(RESET) Installs flake8 (code checker)"
	@echo "  $(CYAN)-$(RESET) Installs mypy (type checker)"
	@echo "  $(CYAN)-$(RESET) Keeps everything isolated from system Python"
	@echo ""
	@echo "$(BLUE)HOW TO USE:$(RESET)"
	@echo "  Run: $(GREEN)make install$(RESET)"
	@echo ""
	@echo "$(BLUE)WHEN TO USE:$(RESET)"
	@echo "  - First time you clone the project"
	@echo "  - After deleting venv"
	@echo ""
	@echo "$(GREEN)✔ Result: clean isolated Python environment$(RESET)"
	@echo ""

	@echo "$(YELLOW)make clean$(RESET)"
	@echo "$(BLUE)WHY:$(RESET)"
	@echo "  Python creates temporary files that are not needed."
	@echo ""
	@echo "$(BLUE)WHAT IT DOES:$(RESET)"
	@echo "  $(CYAN)-$(RESET) Removes __pycache__ folders"
	@echo "  $(CYAN)-$(RESET) Removes *.pyc files"
	@echo "  $(CYAN)-$(RESET) Removes .pytest_cache"
	@echo "  $(CYAN)-$(RESET) Removes .mypy_cache"
	@echo ""
	@echo "$(BLUE)HOW TO USE:$(RESET)"
	@echo "  Run: $(GREEN)make clean$(RESET)"
	@echo ""
	@echo "$(BLUE)WHEN TO USE:$(RESET)"
	@echo "  - Before submitting project"
	@echo "  - When project feels messy or slow"
	@echo ""
	@echo "$(GREEN)✔ Result: clean project state$(RESET)"
	@echo ""

	@echo "$(YELLOW)Virtual environment (venv)$(RESET)"
	@echo "$(BLUE)WHY:$(RESET)"
	@echo "  Different projects need different libraries."
	@echo ""
	@echo "$(BLUE)WHAT IT IS:$(RESET)"
	@echo "  A separate Python space for this project only."
	@echo ""
	@echo "$(BLUE)HOW TO USE:$(RESET)"
	@echo "  Activate: $(CYAN)source venv/bin/activate$(RESET)"
	@echo "  Deactivate: $(CYAN)deactivate$(RESET)"
	@echo ""
	@echo "$(BLUE)WHEN TO USE:$(RESET)"
	@echo "  - Activate before working on project"
	@echo "  - Always use it when coding or testing"
	@echo ""

	@echo "$(PURPLE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(GREEN)TIP:$(RESET) Always run $(YELLOW)make install$(RESET) first"
	@echo "$(PURPLE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

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

install:
	@echo "$(PURPLE)Creating virtual environment...$(RESET)"
	@python3 -m venv venv

	@echo "$(PURPLE)Upgrading pip inside venv...$(RESET)"
	@venv/bin/python3 -m pip install --upgrade pip

	@echo "$(PURPLE)Installing dependencies in venv...$(RESET)"
	@venv/bin/pip install flake8 mypy

	@echo "$(GREEN)✔ Environment ready (venv + tools installed)$(RESET)"
