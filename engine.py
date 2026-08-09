from typing import List, Tuple

from graph import Graph
from models import Drone, Zone
from parser import Parser


class Engine:
    """Manage drone movement and simulation turns."""

    def __init__(
        self,
        parser: Parser,
        paths: List[List[Tuple[Zone, int]]],
        graph: Graph,
    ) -> None:
        """Initialize the simulation engine.

        Args:
            parser: Parsed simulation data.
            paths: Planned paths for all drones.
            graph: Graph containing zones and connections.

        Returns:
            None.
        """
        self.nb_drones = parser.nb_drones
        self.graph = graph
        self.drones: List[Drone] = [
            Drone(f"D{i}", path)
            for i, path in enumerate(paths, start=1)
        ]

        self.current_turn = 1
        self.last_turn = max(
            turn
            for drone in self.drones
            for _, turn in drone.path
        )
        self.start_engine()

    def _get_step_for_turn(
        self,
        drone: Drone,
        target_turn: int,
    ) -> Zone | None:
        """Get the drone's zone at a specific turn.

        Args:
            drone: Drone whose path should be checked.
            target_turn: Turn to search for.

        Returns:
            The zone occupied by the drone at the requested turn,
            or None if no exact zone entry exists.
        """
        for zone, turn in drone.path:
            if turn == target_turn:
                return zone
        return None

    def start_engine(self) -> None:
        """Run the simulation until the final turn.

        Returns:
            None.
        """
        while self.current_turn <= self.last_turn:
            self.execute_turn()
            self.current_turn += 1

    def _move_drones(
        self,
    ) -> List[Tuple[str, Zone, Zone | None]]:
        """Determine drone movements for the current turn.

        Returns:
            A list containing each drone name, its current zone,
            and an optional destination zone for restricted travel.
        """
        moves: List[Tuple[str, Zone, Zone | None]] = []

        for drone in self.drones:
            next_step = self._get_step_for_turn(
                drone,
                self.current_turn,
            )

            if next_step and not self._is_waiting(drone):
                moves.append((drone.name, next_step, None))
            else:
                connection = self._get_connection_for_turn(drone)

                if connection is not None:
                    prev_zone, next_zone = connection
                    moves.append(
                        (drone.name, prev_zone, next_zone)
                    )

        return moves

    def execute_turn(self) -> None:
        """Execute and print the current simulation turn.

        Returns:
            None.
        """
        moves = self._move_drones()
        output = self._build_turn_output(moves)

        if output:
            print(output)

    def _build_turn_output(
        self,
        moves: List[Tuple[str, Zone, Zone | None]],
    ) -> str:
        """Build the formatted output for a simulation turn.

        Args:
            moves: Drone movements for the current turn.

        Returns:
            A formatted string containing all drone movements.
        """
        output: List[str] = []

        for drone_name, first_zone, second_zone in moves:
            if second_zone is None:
                movement = f"{drone_name}-{first_zone.name}"
                output.append(movement)
            else:
                movement = (
                    f"{drone_name}-{first_zone.name}-"
                    f"{second_zone.name}"
                )
                output.append(movement)

        return " ".join(output)

    def _is_waiting(self, drone: Drone) -> bool:
        """Check whether a drone waits during the current turn.

        Args:
            drone: Drone to check.

        Returns:
            True if the drone remains in the same zone,
            otherwise False.
        """
        current_step = self._get_step_for_turn(
            drone,
            self.current_turn,
        )
        prev_step = self._get_step_for_turn(
            drone,
            self.current_turn - 1,
        )

        # One of the turns has no exact zone entry.
        if current_step is None or prev_step is None:
            return False

        return current_step == prev_step

    def _get_connection_for_turn(
        self,
        drone: Drone,
    ) -> Tuple[Zone, Zone] | None:
        """Get a restricted connection used during the current turn.

        Args:
            drone: Drone whose path should be checked.

        Returns:
            The previous and next zones of the active connection,
            or None if the drone is not traveling through one.
        """
        for i in range(len(drone.path) - 1):
            prev_zone, prev_turn = drone.path[i]
            next_zone, next_turn = drone.path[i + 1]

            if (
                next_zone.zone_type == "restricted"
                and prev_turn < self.current_turn < next_turn
            ):
                return (prev_zone, next_zone)

        return None