import heapq

class PathFinding():
    def __init__(self, graph):
        self.graph = graph
        self.start_node = next(iter(self.graph.start_hub.keys()))
        self.end_hub = next(iter(self.graph.end_hub.keys()))
        self.dispatcher()

    def build_routing_table(self, dist):
        routing = {}

        for current_node in self.graph.adj:
            routing[current_node] = []
            neighbors = self.graph.get_neighbors(current_node)
            smallest = float("inf")
            for neighbor, connection, edge_cost in neighbors:
                total_cost = dist[neighbor.name] + edge_cost
                if total_cost < smallest:
                    smallest = total_cost
            for neighbor, connection, edge_cost in neighbors:
                total_cost = dist[neighbor.name] + edge_cost
                if total_cost == smallest:
                    routing[current_node].append(neighbor)
        for key , values in routing.items():
            print(key)
            for val in values:
                print(val.name)
            print()

    def djikstra(self):
        dist = {}
        visited = set()
        dist = {key: float("inf") for key in self.graph.adj.keys()}
        dist[self.end_hub] = 0
        pq = []
        heapq.heappush(pq, (0, self.end_hub))
        while pq:
            current_cost, current_node = heapq.heappop(pq)
            if current_node in visited:
                continue

            visited.add(current_node)

            neighbors = self.graph.get_neighbors(current_node)
            for neighbor in neighbors:
                neighbor_node, connection, cost = neighbor
                new_cost = dist[current_node] + cost
                if new_cost < dist[neighbor_node.name]:
                    dist[neighbor_node.name] = new_cost
                    heapq.heappush(pq,(new_cost, neighbor_node.name))
                elif new_cost == dist[neighbor_node.name]:
                    dist[neighbor_node.name] = new_cost
                    heapq.heappush(pq,(new_cost, neighbor_node.name))
        
        return dist

    def dispatcher(self):
        dist = self.djikstra()
        self.build_routing_table(dist)
