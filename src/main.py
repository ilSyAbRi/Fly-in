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
    for _, val in parse.start_hub.items():
        print(val.name, val.x, val.y, val.zone_type, val.max_drones, val.color)
    print()
    for _, val in parse.hubs.items():
        print(val.name, val.x, val.y, val.zone_type, val.max_drones, val.color)
    print()
    for _, val in parse.end_hub.items():
        print(val.name, val.x, val.y, val.zone_type, val.max_drones, val.color)

    graph = Graph(parse.connections)
    print("\n\n")
    print(graph.links)


if __name__ == "__main__":

    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    # remember to use Exception
