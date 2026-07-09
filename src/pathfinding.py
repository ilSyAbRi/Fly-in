
import heapq

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
        pq = []

        while pq:
            heapq.heappush(pq, (0, self.start_node))
            current_cost, current_node = heapq.heappop(pq)
            neighbors = self.graph.get_neighbors(current_node)
            for neighbor in neighbors:
                neighbor_node, connection, cost = neighbor
                new_cost = dist[current_node] + cost
                if new_cost < dist[neighbor_node.name]:
                    dist[neighbor_node.name] = new_cost
                    parent[neighbor_node.name] = current_node
                    heapq.heappush(pq,(new_cost, neighbor_node))


    def dispatcher(self):
        self.djikstra(self.start_node, self.end_hub)
