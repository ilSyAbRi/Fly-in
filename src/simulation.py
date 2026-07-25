
from graph import Graph
from pathfinding import PathFinding
from parser import Parser

class Simulation:
    def __init__(self, graph: Graph, pathfinding: PathFinding, parser: Parser) -> None:
        self.graph = graph
        self.path = pathfinding.routing
        self.start = pathfinding.start_node
        self.end = pathfinding.end_hub
        self.nb_drones = parser.nb_drones
        self.drones = {}
        for id_drones in range(1, self.nb_drones + 1):
            self.drones[id_drones] = self.start

    def get_next_position(self, drone_id: int) -> None:
        current_position = self.drones[drone_id]
        possible_moves = self.path[current_position]

        return possible_moves[0]

    def simulation_turn(self):
        pass

    def all_drones_finished(self) -> bool:
        return all(position == self.end for position in self.drones.values())

    def count_drones_in_zone(self, zone_name):
        count = 0
        for position in self.drones.values():
            if zone_name == position:
                count += 1
        return count

    def dispatcher(self) -> None:
        print(self.path)
        turn = 0
        while self.all_drones_finished() is False:
            turn += 1
            self.simulation_turn()
            print(turn)
            print(self.drones)