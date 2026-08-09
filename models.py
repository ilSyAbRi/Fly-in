
from typing import List, Tuple


class Zone:
    """Represent a zone in the drone network."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str,
        color: str,
        max_drones: int,
    ) -> None:
        """Initialize a zone.

        Args:
            name: Name of the zone.
            x: Horizontal position of the zone.
            y: Vertical position of the zone.
            zone_type: Type of the zone.
            color: Display color of the zone.
            max_drones: Maximum number of drones allowed in the zone.

        Returns:
            None.
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones


class Connection:
    """Represent a connection between two zones."""

    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int,
    ) -> None:
        """Initialize a connection.

        Args:
            zone_a: First zone of the connection.
            zone_b: Second zone of the connection.
            max_link_capacity: Maximum number of drones allowed
                on the connection.

        Returns:
            None.
        """
        self.zone_a: Zone = zone_a
        self.zone_b: Zone = zone_b
        self.max_link_capacity = max_link_capacity


class Drone:
    """Represent a drone and its planned path."""

    def __init__(
        self,
        name: str,
        path: List[Tuple[Zone, int]],
    ) -> None:
        """Initialize a drone.

        Args:
            name: Name of the drone.
            path: Planned path containing zone and turn pairs.

        Returns:
            None.
        """
        self.name = name
        self.path = path
