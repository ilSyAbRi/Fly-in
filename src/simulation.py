from graph import Graph
from pathfinding import PathFinding
from parser import Parser


class Simulation:
    def __init__(
        self,
        graph: Graph,
        pathfinding: PathFinding,
        parser: Parser
    ) -> None:

        self.graph = graph
        self.path = pathfinding.routing
        self.start = pathfinding.start_node
        self.end = pathfinding.end_hub

        self.nb_drones = parser.nb_drones

        self.drones = {}

        for drone_id in range(1, self.nb_drones + 1):
            self.drones[drone_id] = self.start

    def get_possible_positions(
        self,
        drone_id: int
    ) -> list[str]:

        current_position = self.drones[drone_id]

        return self.path[current_position]

    def get_connection(
        self,
        current_position: str,
        next_position: str
    ):

        neighbors = self.graph.get_neighbors(
            current_position
        )

        for zone, connection, cost in neighbors:

            if zone.name == next_position:
                return connection

        return None

    def count_drones_in_zone(
        self,
        zone_name: str
    ) -> int:

        count = 0

        for position in self.drones.values():

            if position == zone_name:
                count += 1

        return count

    def can_enter_zone(
        self,
        zone_name: str,
        reserved_zones: dict
    ) -> bool:

        # Start and end have unlimited capacity
        if zone_name == self.start:
            return True

        if zone_name == self.end:
            return True

        zone = self.graph.hubs[zone_name]

        current_drones = self.count_drones_in_zone(
            zone_name
        )

        reserved_drones = reserved_zones.get(
            zone_name,
            0
        )

        # Restricted = maximum 1 drone
        if zone.zone_type == "restricted":

            return (
                current_drones + reserved_drones < 1
            )

        # Normal / priority
        return (
            current_drones + reserved_drones
            < zone.max_drones
        )

    def can_use_connection(
        self,
        connection,
        reserved_connections: dict
    ) -> bool:

        if connection is None:
            return False

        used = reserved_connections.get(
            connection,
            0
        )

        return (
            used < connection.max_link_capacity
        )

    def get_next_position(
        self,
        drone_id: int,
        reserved_zones: dict,
        reserved_connections: dict
    ):

        current_position = self.drones[drone_id]

        possible_positions = (
            self.get_possible_positions(drone_id)
        )

        # ---------------------------------
        # First: try priority zones
        # ---------------------------------

        for next_position in possible_positions:

            zone = self.graph.hubs[next_position]

            if zone.zone_type != "priority":
                continue

            if not self.can_enter_zone(
                next_position,
                reserved_zones
            ):
                continue

            connection = self.get_connection(
                current_position,
                next_position
            )

            if not self.can_use_connection(
                connection,
                reserved_connections
            ):
                continue

            return next_position

        # ---------------------------------
        # Second: try normal/restricted
        # ---------------------------------

        for next_position in possible_positions:

            zone = self.graph.hubs[next_position]

            if not self.can_enter_zone(
                next_position,
                reserved_zones
            ):
                continue

            connection = self.get_connection(
                current_position,
                next_position
            )

            if not self.can_use_connection(
                connection,
                reserved_connections
            ):
                continue

            return next_position

        # No available path
        return None

    def simulation_turn(self) -> dict:

        # Reservations for this turn
        reserved_zones = {}
        reserved_connections = {}

        # Final movements for this turn
        reservations = {}

        # ---------------------------------
        # Decide movements
        # ---------------------------------

        for drone_id in range(
            1,
            self.nb_drones + 1
        ):

            # Drone already finished
            if self.drones[drone_id] == self.end:
                continue

            next_position = self.get_next_position(
                drone_id,
                reserved_zones,
                reserved_connections
            )

            # No available path
            if next_position is None:
                continue

            current_position = self.drones[
                drone_id
            ]

            connection = self.get_connection(
                current_position,
                next_position
            )

            # Reserve zone
            reserved_zones[next_position] = (
                reserved_zones.get(
                    next_position,
                    0
                ) + 1
            )

            # Reserve connection
            reserved_connections[connection] = (
                reserved_connections.get(
                    connection,
                    0
                ) + 1
            )

            # Reserve drone movement
            reservations[drone_id] = next_position

        # ---------------------------------
        # Apply all movements
        # ---------------------------------

        for drone_id, next_position in (
            reservations.items()
        ):

            self.drones[drone_id] = next_position

        return reservations

    def all_drones_finished(self) -> bool:

        return all(
            position == self.end
            for position in self.drones.values()
        )

    def dispatcher(self) -> None:

        while not self.all_drones_finished():

            movements = self.simulation_turn()

            output = []

            for drone_id, position in (
                movements.items()
            ):

                output.append(
                    f"D{drone_id}-{position}"
                )

            print(" ".join(output))
