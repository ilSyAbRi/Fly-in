from models import Drone, Zone
from graph import Graph
from parser import Parser
from typing import List, Tuple

class Engine():
    def __init__(self, parser : Parser, paths: List[List[Tuple[Zone, int]]], graph : Graph):
        self.nb_drones = parser.nb_drones
        self.graph = graph
        self.drones: List[Drone] = [Drone(f"D{i}", path) for i , path in enumerate(paths, start=1)]

        self.current_turn = 1
        self.last_turn = max(turn for drone in self.drones for _, turn in drone.path)
        self.start_engine()

    def _get_step_for_turn(self, drone, target_turn):
        for zone , turn in drone.path:
            if turn == target_turn:
                return zone
        return None

    def start_engine(self):
        while self.current_turn <= self.last_turn:
            self.execute_turn()
            self.current_turn += 1
        print(f"\n#Simulation ends in {self.last_turn} turn")

    def _move_drones(self):
        moves = []
        for drone in self.drones:
            next_step = self._get_step_for_turn(drone,self.current_turn)
            if next_step and not self._is_waiting(drone):
                moves.append((drone.name, next_step, None))
            else:
                connection = self._get_connection_for_turn(drone)

                if connection is not None:
                    prev_zone, next_zone = connection
                    moves.append((drone.name, prev_zone, next_zone))
        return moves

    def execute_turn(self):
        moves = self._move_drones()
        output = self._build_turn_output(moves)
        if output:
            print(output)

    def _build_turn_output(self, moves):
        output = []
        for drone_name, first_zone, second_zone in moves:
            if second_zone == None:
                movement = f"{drone_name}-{first_zone.name}"
                output.append(movement)
            else:
                movement = f"{drone_name}-{first_zone.name}-{second_zone.name}"
                output.append(movement)

        return " ".join(output)

    def _is_waiting(self, drone):
        current_step = self._get_step_for_turn(drone, self.current_turn)
        prev_step = self._get_step_for_turn(drone, self.current_turn -1)

        # One of the turns has no exact zone entry.
        if current_step is None or prev_step is None:
            return False

        return current_step == prev_step

    def _get_connection_for_turn(self, drone):
        for i in range(len(drone.path) - 1):
            prev_zone, prev_turn = drone.path[i]
            next_zone, next_turn = drone.path[i + 1]

            if (
                    next_zone.zone_type == "restricted"
                    and prev_turn < self.current_turn < next_turn
            ):
                return (prev_zone, next_zone)
        return None
