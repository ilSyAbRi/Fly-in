
class PathFinding():
    def __init__(self, graph):
        self.graph = graph
        self.start_node = next(iter(self.graph.start_hub.keys()))
        self.end_hub = next(iter(self.graph.end_hub.keys()))
        self.dispatcher()
    def djikstra(self, start: str, goal: str):
        dist = {}
        parent = {}
        visited = set()
        dist = {key: float("inf") for key in self.graph.adj.keys()}
        dist[self.start_node] = 0
        current = self.start_node
        com_cost = 0
        for key, cost in dist.items():

            if dist[current] > dist[key]:
                current = key
        neighbors = self.graph.get_neighbors(current)
        for neighbor in neighbors:
            neighbor_zone, connection, cost = neighbor

            new_cost = dist[current] + cost

    def dispatcher(self):
        self.djikstra(self.start_node, self.end_hub)