"""
Unit Tests for Data Structures
Tests for Graph, Trie, Segment Tree, Union-Find, and Priority Queue
Member 1: Algorithmic Lead
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core_logic.graph import Graph, dijkstra, reconstruct_path
from app.core_logic.segment_tree import SegmentTree
from app.core_logic.union_find import UnionFind
from app.core_logic.priority_queue import PriorityQueue, Alert, ZoonoticRisk
from app.trie_clinical_signs import ClinicalSignsTrie, build_clinical_signs_trie
from app.clinical_signs_dict import CLINICAL_SIGNS_DICT


class TestGraph(unittest.TestCase):
    """Test Graph data structure and Dijkstra algorithm."""
    
    def setUp(self):
        """Set up test graph."""
        self.graph = Graph()
        self.graph.add_edge("Ngaoundéré", "Maroua", 5.0)
        self.graph.add_edge("Ngaoundéré", "Bamenda", 8.0)
        self.graph.add_edge("Maroua", "Bamenda", 12.0)
    
    def test_add_edge(self):
        """Test adding edges."""
        self.assertEqual(len(self.graph.get_all_vertices()), 3)
        self.assertEqual(len(self.graph.get_all_edges()), 3)
    
    def test_dijkstra(self):
        """Test Dijkstra's algorithm."""
        distances, previous = dijkstra(self.graph, "Ngaoundéré")
        
        self.assertEqual(distances["Ngaoundéré"], 0.0)
        self.assertEqual(distances["Maroua"], 5.0)
        self.assertEqual(distances["Bamenda"], 8.0)  # Direct path shorter than via Maroua
    
    def test_path_reconstruction(self):
        """Test path reconstruction."""
        distances, previous = dijkstra(self.graph, "Ngaoundéré", "Bamenda")
        path = reconstruct_path(previous, "Ngaoundéré", "Bamenda")
        
        self.assertEqual(path[0], "Ngaoundéré")
        self.assertEqual(path[-1], "Bamenda")
    
    def test_update_edge_weight(self):
        """Test updating edge weights (for risk increase)."""
        self.graph.update_edge_weight("Ngaoundéré", "Maroua", 10.0)
        distances, _ = dijkstra(self.graph, "Ngaoundéré")
        
        self.assertEqual(distances["Maroua"], 10.0)


class TestUnionFind(unittest.TestCase):
    """Test Union-Find data structure."""
    
    def setUp(self):
        """Set up test Union-Find."""
        self.uf = UnionFind()
        for loc in ["A", "B", "C", "D"]:
            self.uf.make_set(loc)
    
    def test_make_set(self):
        """Test creating sets."""
        self.assertEqual(self.uf.find("A"), "A")
        self.assertEqual(self.uf.find("B"), "B")
    
    def test_union(self):
        """Test union operation."""
        self.uf.union("A", "B")
        self.assertTrue(self.uf.connected("A", "B"))
        self.assertFalse(self.uf.connected("A", "C"))
    
    def test_cluster_size(self):
        """Test cluster size calculation."""
        self.uf.union("A", "B")
        self.uf.union("C", "D")
        
        self.assertEqual(self.uf.get_cluster_size("A"), 2)
        self.assertEqual(self.uf.get_cluster_count(), 2)
    
    def test_all_clusters(self):
        """Test getting all clusters."""
        self.uf.union("A", "B")
        clusters = self.uf.get_all_clusters()
        
        self.assertEqual(len(clusters), 3)  # 2 clusters + 1 singleton


class TestPriorityQueue(unittest.TestCase):
    """Test Priority Queue."""
    
    def setUp(self):
        """Set up test priority queue."""
        self.pq = PriorityQueue()
    
    def test_push_pop(self):
        """Test push and pop operations."""
        self.pq.push(Alert("Anthrax", "Loc1", ZoonoticRisk.P1))
        self.pq.push(Alert("Mastitis", "Loc2", ZoonoticRisk.P4))
        
        alert = self.pq.pop()
        self.assertEqual(alert.disease, "Anthrax")  # P1 should come first
        self.assertEqual(alert.risk_level, ZoonoticRisk.P1)
    
    def test_priority_order(self):
        """Test that alerts are processed in priority order."""
        self.pq.push(Alert("Disease1", "Loc1", ZoonoticRisk.P4))
        self.pq.push(Alert("Disease2", "Loc2", ZoonoticRisk.P1))
        self.pq.push(Alert("Disease3", "Loc3", ZoonoticRisk.P2))
        
        alerts = []
        while not self.pq.is_empty():
            alerts.append(self.pq.pop())
        
        self.assertEqual(alerts[0].risk_level, ZoonoticRisk.P1)
        self.assertEqual(alerts[1].risk_level, ZoonoticRisk.P2)
        self.assertEqual(alerts[2].risk_level, ZoonoticRisk.P4)
    
    def test_is_empty(self):
        """Test empty check."""
        self.assertTrue(self.pq.is_empty())
        self.pq.push(Alert("Test", "Loc", ZoonoticRisk.P1))
        self.assertFalse(self.pq.is_empty())


class TestSegmentTree(unittest.TestCase):
    """Test Segment Tree with Lazy Propagation."""
    
    def test_sum_query(self):
        """Test sum queries."""
        data = [1, 2, 3, 4, 5]
        st = SegmentTree(data, operation="sum")
        
        self.assertEqual(st.query_range(0, 4), 15)
        self.assertEqual(st.query_range(0, 2), 6)
        self.assertEqual(st.query_range(2, 4), 12)
    
    def test_range_update(self):
        """Test range updates with lazy propagation."""
        data = [1, 2, 3, 4, 5]
        st = SegmentTree(data, operation="sum")
        
        # Original sum of [1,3]: 2+3+4 = 9
        original_sum = st.query_range(1, 3)
        self.assertEqual(original_sum, 9)
        
        st.update_range(1, 3, 2)  # Add 2 to indices 1-3
        # After update: (2+2)+(3+2)+(4+2) = 4+5+6 = 15
        self.assertEqual(st.query_range(1, 3), 15)
    
    def test_min_query(self):
        """Test min queries."""
        data = [5, 2, 8, 1, 9]
        st = SegmentTree(data, operation="min")
        
        self.assertEqual(st.query_range(0, 4), 1)
        self.assertEqual(st.query_range(0, 2), 2)
    
    def test_max_query(self):
        """Test max queries."""
        data = [5, 2, 8, 1, 9]
        st = SegmentTree(data, operation="max")
        
        self.assertEqual(st.query_range(0, 4), 9)
        self.assertEqual(st.query_range(0, 2), 8)


class TestTrie(unittest.TestCase):
    """Test Trie data structure."""
    
    def setUp(self):
        """Set up test Trie."""
        self.trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)
    
    def test_search(self):
        """Test Trie search."""
        results = self.trie.search("fever")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['clinical_sign'], "fever")
    
    def test_prefix_search(self):
        """Test prefix-based search."""
        results = self.trie.search("lam")
        self.assertGreater(len(results), 0)
        # All results should start with "lam"
        for result in results:
            self.assertTrue(result['clinical_sign'].startswith("lam"))
    
    def test_contains(self):
        """Test contains check."""
        self.assertTrue(self.trie.contains("fever"))
        self.assertTrue(self.trie.contains("lameness"))
        self.assertFalse(self.trie.contains("nonexistent"))
    
    def test_get_diseases(self):
        """Test getting diseases for a clinical sign."""
        diseases = self.trie.get_diseases("fever")
        self.assertGreater(len(diseases), 0)


if __name__ == '__main__':
    unittest.main()
