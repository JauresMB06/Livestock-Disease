"""
Union-Find (Disjoint Set Union) Data Structure
For cluster detection in disease outbreaks
Member 1: Algorithmic Lead
"""

from typing import Dict, Optional


class UnionFind:
    """
    Union-Find data structure with path compression and union by rank.
    
    Used to detect clusters of disease outbreaks - locations with connected outbreaks
    are grouped together.
    
    Time Complexity:
    - find: O(α(n)) amortized (α is inverse Ackermann function, effectively constant)
    - union: O(α(n)) amortized
    - connected: O(α(n)) amortized
    
    Space Complexity: O(n) where n is number of elements
    """
    
    def __init__(self):
        """Initialize an empty Union-Find structure."""
        self.parent: Dict[str, str] = {}
        self.rank: Dict[str, int] = {}
        self.cluster_sizes: Dict[str, int] = {}
    
    def make_set(self, x: str):
        """
        Create a new set containing only element x.
        
        Args:
            x: Element to add
        
        Time Complexity: O(1)
        """
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.cluster_sizes[x] = 1
    
    def find(self, x: str) -> str:
        """
        Find the root of the set containing x (with path compression).
        
        Args:
            x: Element to find
        
        Returns:
            Root element of the set containing x
        
        Time Complexity: O(α(n)) amortized
        """
        if x not in self.parent:
            self.make_set(x)
        
        # Path compression: make parent point directly to root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        
        return self.parent[x]
    
    def union(self, x: str, y: str):
        """
        Union the sets containing x and y (with union by rank).
        
        Args:
            x: First element
            y: Second element
        
        Time Complexity: O(α(n)) amortized
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return  # Already in the same set
        
        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        
        # Update cluster size
        self.cluster_sizes[root_x] += self.cluster_sizes[root_y]
        del self.cluster_sizes[root_y]
        
        # Update rank
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
    
    def connected(self, x: str, y: str) -> bool:
        """
        Check if x and y are in the same set (cluster).
        
        Args:
            x: First element
            y: Second element
        
        Returns:
            True if x and y are in the same set, False otherwise
        
        Time Complexity: O(α(n)) amortized
        """
        return self.find(x) == self.find(y)
    
    def get_cluster_size(self, x: str) -> int:
        """
        Get the size of the cluster containing x.
        
        Args:
            x: Element
        
        Returns:
            Number of elements in the cluster
        
        Time Complexity: O(α(n)) amortized
        """
        root = self.find(x)
        return self.cluster_sizes.get(root, 0)
    
    def get_all_clusters(self) -> Dict[str, list]:
        """
        Get all clusters as a dictionary mapping root to list of elements.
        
        Returns:
            Dictionary mapping root to list of elements in that cluster
        
        Time Complexity: O(n * α(n))
        """
        clusters: Dict[str, list] = {}
        
        # Collect all elements
        all_elements = set(self.parent.keys())
        
        for element in all_elements:
            root = self.find(element)
            if root not in clusters:
                clusters[root] = []
            clusters[root].append(element)
        
        return clusters
    
    def get_cluster_count(self) -> int:
        """
        Get the number of distinct clusters.
        
        Returns:
            Number of clusters
        
        Time Complexity: O(n * α(n))
        """
        return len(self.get_all_clusters())


if __name__ == "__main__":
    # Example usage: Cluster detection for disease outbreaks
    uf = UnionFind()
    
    # Locations with outbreaks
    locations = ["Ngaoundéré", "Maroua", "Bamenda", "Garoua", "Douala"]
    
    for loc in locations:
        uf.make_set(loc)
    
    # Connect outbreaks (if they're geographically close or have transmission)
    uf.union("Ngaoundéré", "Maroua")  # Same region cluster
    uf.union("Bamenda", "Garoua")     # Another cluster
    
    print(f"Clusters: {uf.get_all_clusters()}")
    print(f"Number of clusters: {uf.get_cluster_count()}")
    print(f"Ngaoundéré and Maroua connected: {uf.connected('Ngaoundéré', 'Maroua')}")
    print(f"Ngaoundéré and Bamenda connected: {uf.connected('Ngaoundéré', 'Bamenda')}")
