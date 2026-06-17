import sys
from parser import Parser, StandardParserError, CustomParserError
from rich.traceback import install

install()

DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main() -> None:

    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    data = Parser(file_path)

    data.dispatcher()

    for zone in data.zones:
        print(zone.name, zone.x, zone.y,
              zone.zone_type, zone.color, zone.max_drones)
    for connection in data.connections:
        print(connection.name_a, connection.name_b,
              connection.max_link_capacity)


if __name__ == "__main__":

    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    # remember to use Exception
