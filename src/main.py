import sys
from parser import Parser, StandardParserError, CustomParserError
from rich import print
from rich.traceback import install

install()

DEFAULT_PATH = "maps/easy/01_linear_path.txt"

def main() -> None:
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    parser = Parser(file_path)
    parser.dispatcher()

if __name__ == "__main__":
    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"[bold bright_red]{e}[/bold bright_red]")
    # remember to use Exception
