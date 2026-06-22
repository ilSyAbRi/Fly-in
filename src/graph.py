class Graph:
    def __init__(self, connections: list):
        self.links: dict[str,list[str]] = {}
 
        for connection in connections:
            self.links.setdefault(connection.name_a, []).append(connection.name_b)
            self.links.setdefault(connection.name_b, []).append(connection.name_a)


        print()
        for key, val in self.links.items():
            print(key, val)

