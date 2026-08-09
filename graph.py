
from typing import Dict, List, Tuple

from models import Connection, Zone
from parser import Parser


class Graph:
    """Store zones, connections, and movement costs."""

    def __init__(self, parse: Parser) -> None:
        """Initialize the graph from parsed map data.

        Args:
            parse: Parsed map data containing hubs, connections,
                and drone information.

        Returns:
            None.
        """
        self.start_hub: Zone = next(iter(parse.start_hub.values()))
        self.end_hub: Zone = next(iter(parse.end_hub.values()))
        self.hubs: Dict[str, Zone] = parse.hubs
        self.adj: Dict[str, List[Tuple[Zone, Connection, int]]] = {
            zone.name: [] for zone in self.hubs.values()
        }
        self.nb_drones: int = parse.nb_drones

        self._build_graph(parse)

    def _build_graph(self, parse: Parser) -> None:
        """Build the adjacency list from parsed connections.

        Args:
            parse: Parsed map data containing the connections.

        Returns:
            None.
        """
        for con in parse.connections:
            zone_a = con.zone_a
            zone_b = con.zone_b

            if zone_a.zone_type != "blocked":
                self.adj[zone_b.name].append(
                    (zone_a, con, self.get_cost(zone_a))
                )

            if zone_b.zone_type != "blocked":
                self.adj[zone_a.name].append(
                    (zone_b, con, self.get_cost(zone_b))
                )

    def get_cost(self, zone: Zone) -> int:
        """Get the movement cost for a zone.

        Args:
            zone: Zone whose movement cost should be returned.

        Returns:
            The movement cost of the zone.
        """
        if zone.zone_type == "restricted":
            return 2

        if zone.zone_type == "normal" or zone.zone_type == "priority":
            return 1

        return 0

    def get_connections(
        self,
        zone_a: Zone,
        zone_b: Zone,
    ) -> Connection | None:
        """Get the connection between two zones.

        Args:
            zone_a: First zone.
            zone_b: Second zone.

        Returns:
            The connection between the zones, or None if no
            connection exists.
        """
        neighbors = self.get_neighbors(zone_a.name)

        for zone, connections, _ in neighbors:
            if zone.name == zone_b.name:
                return connections

        return None

    def get_neighbors(
        self,
        name: str,
    ) -> List[Tuple[Zone, Connection, int]]:
        """Get all neighboring zones for a zone.

        Args:
            name: Name of the zone.

        Returns:
            A list containing neighboring zones, connections,
            and movement costs.
        """
        return self.adj.get(name, [])
