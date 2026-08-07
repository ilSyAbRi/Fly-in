from parser import Parser
from models import Zone, Connection
from typing import Dict, List, Tuple

class  Graph:
    def __init__(self, parse):
        """Potato tomato"""
        self.start_hub: Zone = next(iter(parse.start_hub.values()))
        self.end_hub: Zone = next(iter(parse.end_hub.values()))
        self.hubs: Dict[str, Zone] = parse.hubs
        self.adj: Dict[str: List[Tuple[Zone, Connection, int]]] = {
            zone.name: [] for zone in self.hubs.values()}
        self.nb_drones: int = parse.nb_drones
 

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
        if zone.zone_type == "restricted":
            return 2
        if zone.zone_type == "normal" or zone.zone_type == "priority":
            return 1
        return 0

    def get_connections(self, zone_a: Zone, zone_b: Zone) -> Connection | None:
        neighbors = self.get_neighbors(zone_a.name)

        for zone, connections, _ in neighbors:
            if zone.name == zone_b.name:
                return connections

        return None

    def get_neighbors(self, name: str) -> List[Tuple[Zone, Connection, int]]:

        return self.adj.get(name, [])
