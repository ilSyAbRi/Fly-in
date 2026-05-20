import sys
from parser import Parser, PersonalError


DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    parser = Parser(file_path)
    content = parser.load_raw_input()
    print(content)


if __name__ == "__main__":
    try:
        main()
    except PersonalError as e:
        print(e)
        sys.exit(1)
