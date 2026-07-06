from parser import Parser
from models import Zone, Connection
from typing import Dict, List, Tuple

class  Graph:
    def __init__(self, parse):
        """Potato tomato"""
        self.adj: Dict[str: List[Tuple[Zone, Connection, int]]] = {
            zone.name: [] for zone in parse.hubs.values()}
        

        self._build_graph(parse)

    def _build_graph(self, parse: Parser):

        for con in parse.connections:
            zone_a = con.zone_a
            zone_b = con.zone_b

            if zone_a.zone_type != "blocked":
                self.adj[zone_b.name].append((zone_a, con, self.get_cost(zone_a)))
            if zone_b.zone_type != "blocked":
                self.adj[zone_a.name].append((zone_b, con, self.get_cost(zone_b)))

    def get_cost(self, zone: Zone) -> int:

        if zone.zone_type == "normal" or zone.zone_type == "priority":
            return 1
        if zone.zone_type == "restricted":
            return 2
        else:
            return 1

    def get_neighbors(self, name: str):

        return self.adj.get(name)
