class Graph:
    def __init__(self, connections: list) -> None:
        self.links: dict[str, list[str]] = {}
        for connection in connections:
            link_a = self.links.setdefault(connection.name_a, [])
            link_b = self.links.setdefault(connection.name_b, [])
            link_a.append(connection.name_b)
            link_b.append(connection.name_a)
