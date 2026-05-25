import sys
from parser import Parser
from rich import print


DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main() -> None:
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    parser = Parser(file_path)
    content = parser.load_raw_input()
    print(content)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(f"[red]{e}[/red]")
    # remember to use Exception
