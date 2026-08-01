from models import Drone, Zone
from graph import Graph
from parser import Parser
from typing import List, Tuple


class Engine():
    def __init__(self, parser : Parser, paths: List[List[Tuple[Zone, int]]], graph : Graph):
        self.nb_drones = parser.nb_drones
        self.graph = graph
        self.end_hub = graph.end_hub
        self.drones: List[Drone] = [Drone(f"D0{i}", path) for i , path in enumerate(paths, start=1)]

        i = 0
        for drone in self.drones:

            print(drone.name)
            print(drone.path[i])
            i = i + 1
    def start_engine(self):
        pass

    def execute_turn(self):
        """Print the successful moves after moving"""
        pass

    def _move_drones(self):
        """It should move the drones and also make the output ready"""
        pass

    def is_finished(self, drone_name):
        #return all(True for drone in self.drones if drone.path == self.end_hub else False)
        pass

    def dispatcher(self):
        pass