import sys

# import simulation
from parser import Parser, StandardParserError, CustomParserError
from graph import Graph
from rich.traceback import install
from rich import print, markdown
from pathfinding import PathFinding
# from simulation import Simulation

install()

DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main() -> None:

    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    parse = Parser(file_path)
    parse.dispatcher()
    graph = Graph(parse)
    brain =  PathFinding(graph)
    print(brain.plan_every_path())

    
if __name__ == "__main__":

    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    # remember to use Exception
