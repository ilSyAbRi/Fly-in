class Zone:

    def __init__(self, name: str, x: int, y: int,
                 zone_type: str,
                 color: str,
                 max_drones: int):
        """
            Represent a zone in the drone network.

            A zone stores its position, type, color,
            and maximum drone capacity.
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
    def extract_data(self):
        return {"name": self.name, "x": self.x, "y": self.y, "zone_type": self.zone_type, "max_drones": self.max_drones, "color": self.color}

class Connection:

    def __init__(self, zone_a: object, zone_b: object, max_link_capacity: int):
        """
        represent connection
        """
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
