from parser import Parser
from models import Zone, Connection
from typing import Dict, List, Tuple

class  Graph:
    def __init__(self, parse):
        self.nodes = {}
        self.edges = []
        for val in parse.connections:
            print(val.zone_a.name, val.zone_b.name, val.max_link_capacity)
        self.adjacency: Dict[str: List[Tuple[Zone, Connection, int]]] = {
            zone.name: [] for zone in parse.hubs.values()}
        

        self._build_graph()




    def _build_graph(self):
        pass

