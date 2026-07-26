from graph import Graph
from pathfinding import PathFinding
from parser import Parser


class Simulation:
    def __init__(
        self,
        graph: Graph,pathfinding: PathFinding,parser: Parser) -> None:

        self.graph = graph
        self.path = pathfinding.routing
        self.start = pathfinding.start_node
        self.end = pathfinding.end_hub
        self.nb_drones = parser.nb_drones
        self.drones = {}
        for drone_id in range(1, self.nb_drones + 1):
            self.drones[drone_id] = self.start

    def get_possible_positions(self,drone_id: int) -> list[str]:
        current_position = self.drones[drone_id]
        return self.path[current_position]

    def get_connection(self,current_position: str,next_position: str):

        neighbors = self.graph.get_neighbors(current_position)
        for zone, connection, cost in neighbors:
            if zone.name == next_position:
                return connection

        return None

    def count_drones_in_zone(self,zone_name: str) -> int:
        drones_count = 0
        for position in self.drones.values():
            if position == zone_name:
                drones_count += 1
        return drones_count

    def can_enter_zone(self,zone_name: str) -> bool:

        if zone_name == self.start:
            return True

        if zone_name == self.end:
            return True

        zone = self.graph.hubs[zone_name]

        drones_count = self.count_drones_in_zone(zone_name)

        if zone.zone_type == "restricted":
            return drones_count < 1
        return drones_count < zone.max_drones

    def get_next_position(self,drone_id: int):

        possible_positions = self.get_possible_positions(drone_id)

        for position in possible_positions:
            zone = self.graph.hubs[position]
            if zone.zone_type == "priority":
                if self.can_enter_zone(position):
                    return position

        for position in possible_positions:
            if self.can_enter_zone(position):
                return position
        return None

    def count_connection_usage(self,connection,connection_usage: dict) -> int:
        return connection_usage.get(connection,0)

    def can_use_connection(self,connection,connection_usage: dict) -> bool:

        if connection is None:
            return False
        current_usage = self.count_connection_usage(connection,connection_usage)

        return (current_usage < connection.max_link_capacity)

    def move_drone(self,drone_id: int,connection_usage: dict) -> None:
        if self.drones[drone_id] == self.end:
            return

        current_position = self.drones[drone_id]
        next_position = self.get_next_position(drone_id)
        if next_position is None:
            return

        connection = self.get_connection(current_position,next_position)
        if not self.can_use_connection(connection,connection_usage):
            return
        self.drones[drone_id] = next_position
        connection_usage[connection] = (connection_usage.get(connection,0) + 1)

    def simulation_turn(self) -> None:

        connection_usage = {}

        for drone_id in range(1,self.nb_drones + 1):
            self.move_drone(drone_id, connection_usage)

    def all_drones_finished(self) -> bool:
        return all(position == self.end for position in self.drones.values())

    def dispatcher(self) -> None:
        turn = 0
        while not self.all_drones_finished():
            turn += 1
            self.simulation_turn()
            print(f"Turn {turn}:")
            print(self.drones)