import heapq
from typing import Dict, List, Tuple, Optional
from .graph import CityGraph

class RoutingService:
    def __init__(self):
        self.graph = CityGraph.get_graph()
    
    def calculate_route(self, start: str, end: str) -> Tuple[List[str], float, int]:
        if not CityGraph.node_exists(start):
            raise ValueError(f"Start location '{start}' not found")
        if not CityGraph.node_exists(end):
            raise ValueError(f"End location '{end}' not found")
        
        distances, previous, nodes_visited = self._dijkstra(start)
        
        if distances[end] == float('inf'):
            raise ValueError(f"No route from '{start}' to '{end}'")
        
        path = self._reconstruct_path(previous, start, end)
        return path, distances[end], nodes_visited
    
    def _dijkstra(self, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]], int]:
        distances = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}
        distances[start] = 0
        
        pq = [(0, start)]
        visited = set()
        nodes_visited = 0
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            nodes_visited += 1
            
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in self.graph[current_node].items():
                new_distance = current_distance + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
        
        return distances, previous, nodes_visited
    
    def _reconstruct_path(self, previous: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        return path
    
    def get_graph_info(self) -> Tuple[List[str], int, int]:
        nodes = CityGraph.get_nodes()
        return nodes, len(nodes), CityGraph.get_edge_count()
