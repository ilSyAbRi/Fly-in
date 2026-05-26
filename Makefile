GREEN=\033[1;38;5;156m
PURPLE=\033[1;38;5;171m
YELLOW=\033[1;38;5;11m
BLUE=\033[38;5;111m
CYAN=\033[1;36m
GREY=\033[38;5;243m
RESET=\033[0m

MAP ?= maps/easy/01_linear_path.txt
SRC = src

help:
	@echo "\n$(PURPLE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(GREEN)        FLY-IN PROJECT HELP$(RESET)"
	@echo "$(PURPLE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "\n\n"

	
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)            make install$(RESET)"
	@echo "--------------------"
	@echo "$(BLUE)WHY:$(RESET)"
	@echo "  You need a separate safe Python environment for this project."
	@echo ""
	@echo "$(BLUE)WHAT IT DOES:$(RESET)"
	@echo "  $(CYAN)-$(RESET) Creates a virtual environment (venv)"
	@echo "  $(CYAN)-$(RESET) Updates pip in that venv (not system pip)"
	@echo "  $(CYAN)-$(RESET) Installs flake8 (code checker)"
	@echo "  $(CYAN)-$(RESET) Installs mypy (type checker)"
	@echo "  $(CYAN)-$(RESET) Installs rich (improves Python terminal output)"
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
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

	@echo "\n\n\n\n"

	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)            make run$(RESET)"
	@echo "--------------------"
	@echo "$(BLUE)WHY:$(RESET)"
	@echo "  Runs the drone simulation on a selected map file."
	@echo ""
	@echo "$(BLUE)WHAT IT DOES:$(RESET)"
	@echo "  $(CYAN)-$(RESET) Starts the main program (main.py)"
	@echo "  $(CYAN)-$(RESET) Passes the map file to the parser"
	@echo "  $(CYAN)-$(RESET) Launches full simulation flow"
	@echo ""
	@echo "$(BLUE)HOW TO USE:$(RESET)"
	@echo "  Run: $(GREEN)make run$(RESET)"
	@echo "  Or:  $(GREEN)make run MAP=maps/hard/01_maze_nightmare.txt$(RESET)"
	@echo ""
	@echo "$(BLUE)DEFAULT BEHAVIOR:$(RESET)"
	@echo "  Uses: $(CYAN)$(MAP)$(RESET)"
	@echo ""
	@echo "$(BLUE)WHEN TO USE:$(RESET)"
	@echo "  - When testing your project quickly"
	@echo "  - When switching between maps"
	@echo ""
	@echo "$(GREEN)✔ Result: simulation starts and prints drone movements$(RESET)"
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

	@echo "\n\n\n\n"

	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)            make clean$(RESET)"
	@echo "--------------------"
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
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

	@echo "\n\n\n\n"

	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)              make lint$(RESET)"
	@echo "--------------------"
	@echo "$(BLUE)WHAT IT DOES:$(RESET)"
	@echo "  It checks your Python code before running it."
	@echo ""
	@echo "$(BLUE)TOOLS USED:$(RESET)"
	@echo "  - flake8 → checks code style (format, spacing, errors)"
	@echo "  - mypy   → checks types (int, str, etc.)"
	@echo ""
	@echo "$(BLUE)WHY IT IS IMPORTANT:$(RESET)"
	@echo "  - Finds bugs early"
	@echo "  - Keeps code clean and readable"
	@echo "  - Required for project validation"
	@echo ""
	@echo "$(BLUE)WHAT HAPPENS WHEN YOU RUN IT:$(RESET)"
	@echo "  1. flake8 scans all .py files"
	@echo "  2. mypy checks type safety in src folder"
	@echo "  3. It prints errors if something is wrong"
	@echo ""
	@echo "$(BLUE)HOW TO USE:$(RESET)"
	@echo "  Run: $(GREEN)make lint$(RESET)"
	@echo ""
	@echo "$(BLUE)WHEN TO USE:$(RESET)"
	@echo "  - Before commit"
	@echo "  - Before submit"
	@echo "  - After writing new code"
	@echo ""
	@echo "$(GREEN)✔ Result: your code is checked for errors and style issues$(RESET)"
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

	@echo "\n\n\n\n"

	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)              make debug$(RESET)"
	@echo "--------------------"
	@echo "$(BLUE)WHAT IT DOES:$(RESET)"
	@echo "  Runs your program in debug mode using Python debugger (pdb)."
	@echo ""
	@echo "$(BLUE)WHAT IS pdb:$(RESET)"
	@echo "  It lets you pause your program and check what is happening step by step."
	@echo ""
	@echo "$(BLUE)WHY IT IS USEFUL:$(RESET)"
	@echo "  - Helps find bugs"
	@echo "  - Shows values of variables"
	@echo "  - Lets you control execution line by line"
	@echo ""
	@echo "$(BLUE)WHAT HAPPENS WHEN YOU RUN IT:$(RESET)"
	@echo "  1. Program starts with pdb debugger"
	@echo "  2. Execution stops at first line"
	@echo "  3. You can step through code manually"
	@echo ""
	@echo "$(BLUE)HOW TO USE:$(RESET)"
	@echo "  Run:$(GREEN) make debug$(RESET)"
	@echo ""
	@echo "$(BLUE)WHEN TO USE:$(RESET)"
	@echo "  - When program crashes"
	@echo "  - When output is wrong"
	@echo "  - When you want to understand logic step by step"
	@echo ""
	@echo "$(GREEN)✔ Result: interactive debugging session starts$(RESET)"
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

	@echo "\n\n\n\n"

	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@echo "$(YELLOW)              Virtual environment (venv)$(RESET)"
	@echo "--------------------"
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
	@echo "$(GREY)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"

	@echo "\n\n\n\n"

	@echo "$(GREY)YO━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━YO━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(YELLOW)YO$(RESET)"
	@echo "$(GREEN)TIP:$(RESET)\nStep 1: Always run $(YELLOW)make install$(RESET).\nStep 2: activate the virtual environment (venv)."
	@echo "$(GREY)BY━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━BY━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(YELLOW)BY$(RESET)"

run:
	@echo "$(PURPLE)🚀 Starting Fly-in simulation...$(RESET)"
	@echo "$(CYAN)📄 Map: $(MAP) $(RESET)"
	@echo "-----------------------------------"
	@python3 src/main.py $(MAP)
	@echo "-----------------------------------"
	@echo "$(GREEN)✅ Simulation finished$(RESET)"


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


lint:
	@echo "$(CYAN)🧪 Running code quality checks...$(RESET)"
	@echo "$(GREY)-----------------------------------$(RESET)"
	flake8 $(SRC)
	@echo "$(GREY)-----------------------------------$(RESET)"
	@echo "$(CYAN)📌 Running mypy type checks...$(RESET)"
	mypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "$(GREY)-----------------------------------$(RESET)"
	@echo "$(GREEN)✅ Lint finished$(RESET)"


debug:
	@echo "$(PURPLE)🐛 Starting debug mode (pdb)...$(RESET)"
	@echo "$(BLUE)📄 Map: $(MAP)$(RESET)"
	@echo "$(GREY)-----------------------------------$(RESET)"
	@python3 -m pdb src/main.py $(MAP)
	@echo "$(GREY)-----------------------------------$(RESET)"
	@echo "$(GREEN)✅ Debug session ended$(RESET)"


install:
	@echo "$(PURPLE)Creating virtual environment...$(RESET)"
	@python3 -m venv venv

	@echo "$(PURPLE)Upgrading pip inside venv...$(RESET)"
	@venv/bin/python3 -m pip install --upgrade pip

	@echo "$(PURPLE)Installing dependencies in venv...$(RESET)"
	@venv/bin/pip install flake8 mypy rich

	@echo "$(GREEN)✔ Environment ready (venv + tools installed)$(RESET)"


.PHONY: run clean lint debug install help
