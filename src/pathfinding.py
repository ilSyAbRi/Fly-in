import heapq
from graph import Graph
from models import Zone, Connection
from typing import List, Dict, Any, Tuple



# f = g + h + t


class PathFinding:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.min_dis: Dict[Zone, int] = self.find_heuristic(self.graph)
        self.occupied_zones: Dict[int, Dict[Zone, int]] = {}
        self.occupied_edges: Dict[int, Dict[str, int]] = {}
        self.start_hub = graph.start_hub
        self.end_hub = graph.end_hub
        self.nb_drones: int = graph.nb_drones

    def find_path(self):
        stack: List[Tuple[float , int , int , str, Zone, Any]] = []
        heapq.heappush(stack, (self.min_dis[self.start_hub],
                               0,
                               0,
                               self.start_hub.name,
                               self.start_hub,
                               None
                       ))
        while stack:
            current_tuple = heapq.heappop(stack)
            f_score, turn_count , priority_check, zone_name, zone_obj, parent = current_tuple

            # if we have found the end
            if zone_obj == self.end_hub:
                path: List[Tuple[Zone, int]] = []
                trace = current_tuple
                while trace is not None:
                    _ ,turn, _, _, zone, parent = trace
                    path.append((zone, turn))
                    trace = parent
                path.reverse()
                return path


            # if we can wait
            if self._can_occupy_zone(zone_obj, turn_count + 1):
               wait_tuple = (f_score + 1, turn_count + 1, zone_name, priority_check,zone_obj, current_tuple)
               heapq.heappush(stack, wait_tuple)

            # make a choice
            neighbors = self.graph.get_neighbors(zone_name)
            for neighbor, connection, cost in neighbors:
                zone_ok = self._can_occupy_zone(neighbor, turn_count + cost)
                conn_ok = self._can_occupy_edge(connection, turn_count + cost)

                # f = g + h + t
                # g = cost of zone
                # t = turn count
                # h = cost to end
                if zone_ok and conn_ok:
                    priority_check = 0 if neighbor.zone_type == "priority" else 1
                    new_f = (turn_count + cost) + self.min_dis[neighbor] + 0.1
                    heapq.heappush(stack, (new_f, turn_count + cost, priority_check ,neighbor.name, neighbor, current_tuple))

        return []

    def _can_occupy_zone(self,zone, turn: int):

        if(
                turn not in self.occupied_zones
                or zone not in self.occupied_zones[turn]
                or zone.name == self.graph.start_hub.name
                or zone.name == self.graph.end_hub.name
        ):
            return True

        return zone.max_drones < self.occupied_zones[turn][zone]


    def _can_occupy_edge(self, conn: Connection, turn: int):
        conn_str = self._format_connection(conn)
        if (
                turn not in self.occupied_edges
                or conn_str not in self.occupied_edges[turn]
        ):
            return True
        return conn.max_link_capacity < self.occupied_edges[turn][conn_str]

    @staticmethod
    def _format_connection(conn: Connection) -> str:
        con_a: Zone = conn.zone_a
        con_b: Zone = conn.zone_b
        return (f"{min(con_a.name, con_b.name)} .. {max(con_a.name, con_b.name)}")



    @staticmethod
    def find_heuristic(graph: Graph) -> Dict[Zone, int]:
        pq = []
        end: Zone = graph.end_hub
        distances: Dict[Zone, int] = {end: 0}
        heapq.heappush(pq, [0, end.name, end])

        while pq:
            current_cost , current_name, current_obj = heapq.heappop(pq)

            neighbors =  graph.get_neighbors(current_name)

            if current_cost > distances[current_obj]:
                continue

            for zone, connection, cost_to_b in neighbors:
                new_cost = current_cost + cost_to_b

                if zone not in distances or new_cost < distances[zone]:
                    distances[zone] = new_cost
                    heapq.heappush(pq, (new_cost, zone.name, zone))
        return distances

    def plan_every_path(self) -> List[List[Tuple[Zone, int]]]:
        all_plans: List[List[Tuple[Zone, int]]] = []

        for _ in range(self.nb_drones):
            path = self.find_path()
            all_plans.append(path)


            previous_step = None

            for zone , turn in path:
                # if we just started
                if previous_step is None:
                    previous_step = zone

                # wait
                elif previous_step == zone:
                    previous_step = zone
                else:
                    connect = self.graph.get_connections(zone, previous_step)
                    if connect is not None:
                        con_str = self._format_connection(connect)

                        if turn not in self.occupied_edges:
                            self.occupied_edges[turn] = {}
                        if con_str not in self.occupied_edges[turn]:
                            self.occupied_edges[turn][con_str] = 1
                        else:
                            self.occupied_edges[turn][con_str] += 1

                # if the turn not saved
                if turn not in self.occupied_zones:
                    self.occupied_zones[turn] = {}
                # if the zone first appearance in that turn
                if zone not in self.occupied_zones[turn]:
                    self.occupied_zones[turn][zone] = 1
                else:
                    self.occupied_zones[turn][zone] += 1

        return all_plans