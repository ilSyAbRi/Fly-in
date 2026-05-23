import sys
from parser import Parser
from rich.traceback import install

DEFAULT_PATH = "maps/easy/01_linear_path.txt"


install()


def main() -> None:
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    parser = Parser(file_path)
    content = parser.load_raw_input()
    print(content)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(e)
    # remember to use Exception
