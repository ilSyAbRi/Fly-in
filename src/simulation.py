from models import Drone, Zone
from graph import Graph
from parser import Parser
from typing import List, Tuple, Dict

class Engine():
    def __init__(self, parser : Parser, paths: List[List[Tuple[Zone, int]]], graph : Graph):
        self.nb_drones = parser.nb_drones
        self.graph = graph
        self.drones: List[Drone] = [Drone(f"D0{i}", path) for i , path in enumerate(paths, start=1)]

        self.current_turn = 0
        self.last_turn = max(turn for drone in self.drones for _, turn in drone.path)
        self.start_engine()

    def _get_step_for_turn(self, drone):
        for zone , turn in drone.path:
            if turn == self.current_turn:
                return zone
        return None

    def start_engine(self):
        while self.current_turn <= self.last_turn:
            self.execute_turn()
            self.current_turn += 1

    def _move_drones(self):
        moves = []
        for drone in self.drones:
            next_step = self._get_step_for_turn(drone)
            if next_step:
                moves.append((drone.name, next_step))
        return moves

    def execute_turn(self):
        moves = self._move_drones()
        print(self.current_turn)
        for drone_name , step in moves:
            print(drone_name, step.name)
