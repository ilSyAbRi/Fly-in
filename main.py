"""Run the Fly-in drone simulation."""

import sys

import arcade
from rich.traceback import install

from display import Display
from engine import Engine
from graph import Graph
from parser import CustomParserError, Parser, StandardParserError
from pathfinding import PathFinding


install()

DEFAULT_PATH = "maps/easy/01_linear_path.txt"


def main() -> None:
    """Run the drone simulation.

    Parses the input map, builds the graph, calculates paths for all
    drones, creates the graphical display, and starts the Arcade event
    loop.

    Returns:
        None.
    """
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    parse = Parser(file_path)
    parse.dispatcher()

    graph = Graph(parse)
    brain = PathFinding(graph)

    Display(
        graph,
        Engine(parse, brain.plan_every_path(), graph).drones,
    )

    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except (StandardParserError, CustomParserError) as e:
        print(f"\033[31m{e}\033[0m")
    except Exception as e:
        print(f"\033[31m{e}\033[0m")
