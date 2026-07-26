
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
        for drones_id in range(1, self.nb_drones + 1):
            self.drones[drones_id] = self.start

    def get_next_position(self, drone_id: int) -> str:
        current_position = self.drones[drone_id]
        possible_moves = self.path[current_position]

        return possible_moves[0]

    def get_connection(self, current_position: str, next_position: str):
        neighbors = self.graph.get_neighbors(current_position)

        for zone, connection, cost in neighbors:
            if zone.name == next_position:
                return connection

        return None

    def simulation_turn(self):
        for drone_id in range(1, self.nb_drones + 1):
            if self.drones[drone_id] == self.end:
                continue

            next_position = self.get_next_position(drone_id)

            if not self.can_enter_zone(next_position):
                continue

            if not self.can_use_connection(
                    self.drones[drone_id],
                    next_position
            ):
                continue

            self.drones[drone_id] = next_position

    def all_drones_finished(self) -> bool:
        return all(position == self.end for position in self.drones.values())

    def count_drones_in_zone(self, zone_name):
        drones_count = 0
        for position in self.drones.values():
            if zone_name == position:
                drones_count += 1
        return drones_count

    def can_enter_zone(self, zone_name: str) -> bool:
        if zone_name == self.start or zone_name == self.end:
            return True
        zone_ob = self.graph.hubs[zone_name]
        drones_count = self.count_drones_in_zone(zone_name)
        return drones_count < zone_ob.max_drones

    def dispatcher(self) -> None:
        turn = 0
        # while self.all_drones_finished() is False:
        turn += 1
        self.simulation_turn()
        print(turn)
        print(self.drones)