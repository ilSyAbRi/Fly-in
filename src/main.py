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
    for key, val in parse.start_hub.items():
        start_key = key
        print(val.name, val.x, val.y, val.zone_type, val.max_drones, val.color)
    print()
    for _, val in parse.hubs.items():
        print(_)
        print(val.name, val.x, val.y, val.zone_type, val.max_drones, val.color)
    print()
    for key, val in parse.end_hub.items():
        end_key = key
        print(val.name, val.x, val.y, val.zone_type, val.max_drones, val.color)
    print()
    print()
    for data in parse.connections:
        print(data.name_a, data.name_b, data.max_link_capacity)

    graph = Graph(parse.connections)
    # start_key = list(parse.start_hub.keys())[0]
    # end_key = list(parse.end_hub.keys())[0]
    print(start_key)
    print(end_key)
    print("\n\n\n")

    graph = Graph(parse.connections)
    print(graph.links[start_key])
    print(graph.links)
    print(graph.links[end_key])

if __name__ == "__main__":

    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    # remember to use Exception
