import heapq
from graph import Graph
from models import Zone, Connection
from typing import List, Dict

class PathFinding:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.min_dis: Dict[Zone, int] = self.find_heuristic(self.graph)
        print(self.min_dis)




    @staticmethod
    def find_heuristic(graph: Graph) -> Dict[Zone, int]:
        pq = []
        end: Zone = graph.end_hub
        distances: Dict[Zone, int] = {end: 0}
        heapq.heappush(pq, [0, end.name, end])

        while pq:
            current_cost , current_name, current_obj = heapq.heappop(pq)

            neighbors =  graph.get_neighbors(current_name)

            if current_cost > distances[current_obj]:
                continue

            for zone, connection, cost_to_b in neighbors:
                new_cost = current_cost + cost_to_b

                if zone not in distances or new_cost < distances[zone]:
                    distances[zone] = new_cost
                    heapq.heappush(pq, (new_cost, zone.name, zone))
        return distances