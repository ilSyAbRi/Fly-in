import sys
from parser import Parser, StandardParserError, CustomParserError
from graph import Graph
from rich.traceback import install

install()

DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main() -> None:

    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    parse = Parser(file_path)

    parse.dispatcher()

    for key, value in parse.hubs.items():
        print(key, value.name, value.x, value.y)
    for key, value in parse.start_hub.items():
        print(key, vars(value))
    for key, value in parse.end_hub.items():
        print(key, vars(value))

    for connection in parse.connections:
        print(connection.name_a, connection.name_b,
              connection.max_link_capacity)
    graph = Graph(parse.connections)
    print(graph.links)


if __name__ == "__main__":

    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    # remember to use Exception
