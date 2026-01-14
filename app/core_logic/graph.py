"""
Graph Data Structure with Dijkstra Algorithm
For Path of Least Risk calculation in Livestock Disease Surveillance Network
Member 1: Algorithmic Lead
"""

from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import heapq


class Graph:
    """
    Weighted undirected graph for modeling disease transmission routes.
    
    Vertices represent locations (cattle hubs), edges represent routes,
    weights represent risk levels (higher weight = higher risk).
    
    Time Complexity:
    - add_edge: O(1)
    - dijkstra: O((V + E) log V) where V = vertices, E = edges
    """
    
    def __init__(self):
        """Initialize an empty graph."""
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.vertices: set = set()
    
    def add_vertex(self, vertex: str):
        """Add a vertex to the graph. O(1)"""
        self.vertices.add(vertex)
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, u: str, v: str, weight: float):
        """
        Add an undirected edge between vertices u and v with given weight.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Risk weight (higher = more risky)
        
        Time Complexity: O(1)
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))
    
    def update_edge_weight(self, u: str, v: str, weight: float):
        """
        Update the weight of an existing edge (used when outbreak increases risk).
        
        Args:
            u: First vertex
            v: Second vertex
            weight: New risk weight
        
        Time Complexity: O(degree(u) + degree(v))
        """
        # Remove old edges
        self.adjacency_list[u] = [(neighbor, w) for neighbor, w in self.adjacency_list[u] if neighbor != v]
        self.adjacency_list[v] = [(neighbor, w) for neighbor, w in self.adjacency_list[v] if neighbor != u]
        
        # Add new edges with updated weight
        self.add_edge(u, v, weight)
    
    def get_neighbors(self, vertex: str) -> List[Tuple[str, float]]:
        """
        Get all neighbors of a vertex with their edge weights.
        
        Time Complexity: O(degree(vertex))
        """
        return self.adjacency_list.get(vertex, [])
    
    def get_all_vertices(self) -> List[str]:
        """Get all vertices in the graph. O(V)"""
        return list(self.vertices)
    
    def get_all_edges(self) -> List[Tuple[str, str, float]]:
        """
        Get all edges in the graph.
        
        Returns:
            List of tuples (u, v, weight)
        
        Time Complexity: O(V + E)
        """
        edges = []
        visited_pairs = set()
        
        for u in self.adjacency_list:
            for v, weight in self.adjacency_list[u]:
                # Avoid duplicate edges (since graph is undirected)
                pair = tuple(sorted([u, v]))
                if pair not in visited_pairs:
                    edges.append((u, v, weight))
                    visited_pairs.add(pair)
        
        return edges


def dijkstra(graph: Graph, start: str, end: Optional[str] = None) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Dijkstra's algorithm to find shortest path (path of least risk).
    
    Args:
        graph: Graph instance
        start: Starting vertex
        end: Optional destination vertex (if None, finds paths to all vertices)
    
    Returns:
        Tuple of (distances, previous_vertices)
        - distances: Dict mapping vertex to shortest distance from start
        - previous_vertices: Dict mapping vertex to previous vertex in shortest path
    
    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    
    Note: In this context, "shortest" means "least risky" (minimum weight sum).
    """
    if start not in graph.vertices:
        raise ValueError(f"Start vertex '{start}' not in graph")
    
    # Initialize distances: all vertices start with infinite distance
    distances: Dict[str, float] = {v: float('inf') for v in graph.vertices}
    distances[start] = 0.0
    
    # Previous vertex in shortest path
    previous: Dict[str, Optional[str]] = {v: None for v in graph.vertices}
    
    # Priority queue: (distance, vertex)
    pq: List[Tuple[float, str]] = [(0.0, start)]
    visited: set = set()
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        # Skip if already visited
        if current_vertex in visited:
            continue
        
        visited.add(current_vertex)
        
        # Early termination if we found the destination
        if end and current_vertex == end:
            break
        
        # Explore neighbors
        for neighbor, weight in graph.get_neighbors(current_vertex):
            if neighbor in visited:
                continue
            
            # Calculate new distance
            new_dist = current_dist + weight
            
            # Update if we found a shorter path
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_vertex
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances, previous


def reconstruct_path(previous: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """
    Reconstruct the shortest path from start to end using previous vertices.
    
    Args:
        previous: Dictionary mapping vertex to previous vertex
        start: Starting vertex
        end: Destination vertex
    
    Returns:
        List of vertices representing the path from start to end
        Returns empty list if no path exists
    
    Time Complexity: O(V)
    """
    if end not in previous or previous[end] is None and end != start:
        return []  # No path exists
    
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = previous[current]
        if current == start:
            path.append(start)
            break
    
    path.reverse()
    return path if path[0] == start else []


if __name__ == "__main__":
    # Example usage
    g = Graph()
    
    # Add cattle hubs as vertices
    g.add_edge("Ngaoundéré", "Maroua", 5.0)
    g.add_edge("Ngaoundéré", "Bamenda", 8.0)
    g.add_edge("Maroua", "Bamenda", 12.0)
    
    # Find shortest path from Ngaoundéré to Bamenda
    distances, previous = dijkstra(g, "Ngaoundéré", "Bamenda")
    path = reconstruct_path(previous, "Ngaoundéré", "Bamenda")
    
    print(f"Shortest distance: {distances['Bamenda']}")
    print(f"Path: {' -> '.join(path)}")
