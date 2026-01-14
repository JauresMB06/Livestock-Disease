"""
Path of Least Risk Logic
Connects Graph and Union-Find for outbreak cluster detection and route recalculation
Member 1 & Member 2: Integration
"""

from typing import Dict, List, Tuple, Optional
from app.core_logic.graph import Graph, dijkstra, reconstruct_path
from app.core_logic.union_find import UnionFind
from app.gps_coordinates import get_all_hubs


class PathOfLeastRisk:
    """
    Manages disease outbreak clusters and calculates paths of least risk.
    
    When an outbreak occurs:
    1. Union-Find detects clusters (connected outbreaks)
    2. Graph edge weights increase based on outbreak severity
    3. Dijkstra recalculates safest routes
    """
    
    def __init__(self):
        """Initialize Path of Least Risk system."""
        self.graph = Graph()
        self.clusters = UnionFind()
        self.outbreaks: Dict[str, Dict] = {}  # location -> outbreak data
        self.base_weights: Dict[Tuple[str, str], float] = {}  # Store original weights
    
    def initialize_network(self, locations: List[str], routes: List[Tuple[str, str, float]]):
        """
        Initialize the network with locations and routes.
        
        Args:
            locations: List of location names
            routes: List of (from, to, base_weight) tuples
        """
        # Initialize Union-Find with all locations
        for location in locations:
            self.clusters.make_set(location)
        
        # Initialize graph with base routes
        for from_loc, to_loc, weight in routes:
            self.graph.add_edge(from_loc, to_loc, weight)
            # Store base weights
            edge_key = tuple(sorted([from_loc, to_loc]))
            self.base_weights[edge_key] = weight
    
    def report_outbreak(self, location: str, severity: int, disease: str, 
                       connected_locations: Optional[List[str]] = None):
        """
        Report an outbreak and update the network.
        
        Args:
            location: Location of outbreak
            severity: Severity level (1-5)
            disease: Disease name
            connected_locations: Locations to connect in cluster (if transmission suspected)
        """
        # Store outbreak data
        self.outbreaks[location] = {
            'severity': severity,
            'disease': disease,
            'location': location
        }
        
        # Connect locations in Union-Find if transmission suspected
        if connected_locations:
            for connected_loc in connected_locations:
                if connected_loc in self.clusters.parent:
                    self.clusters.union(location, connected_loc)
        
        # Increase edge weights based on severity
        # Higher severity = higher risk weight multiplier
        risk_multiplier = 1.0 + (severity * 0.5)  # 1.5x to 3.5x base weight
        
        # Update all edges connected to this location
        neighbors = self.graph.get_neighbors(location)
        for neighbor, current_weight in neighbors:
            edge_key = tuple(sorted([location, neighbor]))
            base_weight = self.base_weights.get(edge_key, current_weight)
            new_weight = base_weight * risk_multiplier
            
            self.graph.update_edge_weight(location, neighbor, new_weight)
    
    def get_clusters(self) -> Dict[str, List[str]]:
        """
        Get all outbreak clusters.
        
        Returns:
            Dictionary mapping cluster root to list of locations
        """
        return self.clusters.get_all_clusters()
    
    def get_cluster_for_location(self, location: str) -> List[str]:
        """
        Get all locations in the same cluster as the given location.
        
        Args:
            location: Location to check
        
        Returns:
            List of locations in the same cluster
        """
        clusters = self.get_clusters()
        root = self.clusters.find(location)
        return clusters.get(root, [location])
    
    def calculate_safest_route(self, start: str, end: str) -> Tuple[List[str], float]:
        """
        Calculate the safest route (path of least risk) between two locations.
        
        Args:
            start: Starting location
            end: Destination location
        
        Returns:
            Tuple of (path, total_risk)
        """
        if start not in self.graph.vertices or end not in self.graph.vertices:
            return [], float('inf')
        
        distances, previous = dijkstra(self.graph, start, end)
        path = reconstruct_path(previous, start, end)
        total_risk = distances.get(end, float('inf'))
        
        return path, total_risk
    
    def get_all_safest_routes(self, start: str) -> Dict[str, Tuple[List[str], float]]:
        """
        Get safest routes from start location to all other locations.
        
        Args:
            start: Starting location
        
        Returns:
            Dictionary mapping destination to (path, total_risk)
        """
        if start not in self.graph.vertices:
            return {}
        
        distances, previous = dijkstra(self.graph, start)
        
        routes = {}
        for destination in self.graph.vertices:
            if destination != start:
                path = reconstruct_path(previous, start, destination)
                total_risk = distances.get(destination, float('inf'))
                routes[destination] = (path, total_risk)
        
        return routes
    
    def get_outbreak_locations(self) -> List[str]:
        """Get all locations with active outbreaks."""
        return list(self.outbreaks.keys())
    
    def get_outbreak_info(self, location: str) -> Optional[Dict]:
        """Get outbreak information for a location."""
        return self.outbreaks.get(location)


def initialize_cameroon_network() -> PathOfLeastRisk:
    """
    Initialize the network with Cameroonian cattle hubs.
    
    Returns:
        Initialized PathOfLeastRisk system
    """
    hubs = get_all_hubs()
    locations = list(hubs.keys())
    
    # Define routes between hubs with base weights (distance-based)
    # Weights represent base risk (lower = safer)
    routes = [
        ("Ngaoundéré", "Maroua", 5.0),      # Base risk weight
        ("Ngaoundéré", "Bamenda", 8.0),
        ("Maroua", "Bamenda", 12.0),
    ]
    
    system = PathOfLeastRisk()
    system.initialize_network(locations, routes)
    
    return system


if __name__ == "__main__":
    # Example usage
    system = initialize_cameroon_network()
    
    # Report an outbreak
    print("Reporting outbreak at Ngaoundéré...")
    system.report_outbreak("Ngaoundéré", severity=3, disease="Anthrax")
    
    # Calculate safest route
    path, risk = system.calculate_safest_route("Maroua", "Bamenda")
    print(f"\nSafest route from Maroua to Bamenda:")
    print(f"  Path: {' -> '.join(path)}")
    print(f"  Total Risk: {risk}")
    
    # Get clusters
    clusters = system.get_clusters()
    print(f"\nOutbreak clusters: {clusters}")
