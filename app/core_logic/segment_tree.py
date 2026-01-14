"""
Segment Tree with Lazy Propagation
For efficient range queries on disease outbreak data
Member 1: Algorithmic Lead
"""

from typing import List, Optional, Callable
from math import ceil, log2


class SegmentTree:
    """
    Segment Tree with Lazy Propagation for range queries and updates.
    
    Used for querying disease outbreak statistics over time ranges or location ranges.
    
    Time Complexity:
    - build: O(n)
    - query_range: O(log n)
    - update_range: O(log n) with lazy propagation
    - update_point: O(log n)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, data: List[float], operation: str = "sum"):
        """
        Initialize segment tree with data.
        
        Args:
            data: Initial array of values
            operation: Operation to perform ("sum", "min", "max")
        
        Time Complexity: O(n)
        """
        self.n = len(data)
        self.operation = operation
        
        # Determine operation function
        if operation == "sum":
            self.op = lambda a, b: a + b
            self.identity = 0.0
        elif operation == "min":
            self.op = lambda a, b: min(a, b)
            self.identity = float('inf')
        elif operation == "max":
            self.op = lambda a, b: max(a, b)
            self.identity = float('-inf')
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        # Calculate tree size (next power of 2)
        self.size = 2 ** (ceil(log2(self.n)) + 1) - 1
        
        # Segment tree array - need enough space
        tree_size = 4 * self.n  # Standard segment tree size
        self.tree: List[float] = [self.identity] * tree_size
        
        # Lazy propagation array
        self.lazy: List[float] = [0.0] * tree_size
        
        # Build the tree
        self._build(data, 0, 0, self.n - 1)
    
    def _build(self, data: List[float], node: int, start: int, end: int):
        """Build the segment tree from data recursively. O(n)"""
        if start == end:
            # Leaf node
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            # Build left subtree
            self._build(data, 2 * node + 1, start, mid)
            # Build right subtree
            self._build(data, 2 * node + 2, mid + 1, end)
            # Update current node
            self.tree[node] = self.op(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def _push_lazy(self, node: int, start: int, end: int):
        """
        Push lazy value to children.
        
        Args:
            node: Current node index
            start: Start of segment
            end: End of segment
        
        Time Complexity: O(1)
        """
        if self.lazy[node] != 0:
            # Apply lazy value to current node
            if self.operation == "sum":
                self.tree[node] += self.lazy[node] * (end - start + 1)
            elif self.operation == "min":
                self.tree[node] += self.lazy[node]
            elif self.operation == "max":
                self.tree[node] += self.lazy[node]
            
            # Push to children if not leaf
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            
            self.lazy[node] = 0
    
    def query_range(self, l: int, r: int) -> float:
        """
        Query range [l, r] (0-indexed, inclusive).
        
        Args:
            l: Left index
            r: Right index
        
        Returns:
            Result of operation over range
        
        Time Complexity: O(log n)
        """
        if l < 0 or r >= self.n or l > r:
            raise ValueError(f"Invalid range: [{l}, {r}]")
        
        return self._query_range(0, 0, self.n - 1, l, r)
    
    def _query_range(self, node: int, start: int, end: int, l: int, r: int) -> float:
        """Internal recursive query function."""
        # Push lazy value
        self._push_lazy(node, start, end)
        
        # No overlap
        if start > r or end < l:
            return self.identity
        
        # Complete overlap
        if l <= start and end <= r:
            return self.tree[node]
        
        # Partial overlap
        mid = (start + end) // 2
        left_result = self._query_range(2 * node + 1, start, mid, l, r)
        right_result = self._query_range(2 * node + 2, mid + 1, end, l, r)
        
        return self.op(left_result, right_result)
    
    def update_range(self, l: int, r: int, value: float):
        """
        Update range [l, r] by adding value (with lazy propagation).
        
        Args:
            l: Left index
            r: Right index
            value: Value to add
        
        Time Complexity: O(log n)
        """
        if l < 0 or r >= self.n or l > r:
            raise ValueError(f"Invalid range: [{l}, {r}]")
        
        self._update_range(0, 0, self.n - 1, l, r, value)
    
    def _update_range(self, node: int, start: int, end: int, l: int, r: int, value: float):
        """Internal recursive update function."""
        # Push lazy value
        self._push_lazy(node, start, end)
        
        # No overlap
        if start > r or end < l:
            return
        
        # Complete overlap
        if l <= start and end <= r:
            # Update lazy value
            self.lazy[node] += value
            self._push_lazy(node, start, end)
            return
        
        # Partial overlap
        mid = (start + end) // 2
        self._update_range(2 * node + 1, start, mid, l, r, value)
        self._update_range(2 * node + 2, mid + 1, end, l, r, value)
        
        # Update current node after children are updated
        self._push_lazy(2 * node + 1, start, mid)
        self._push_lazy(2 * node + 2, mid + 1, end)
        self.tree[node] = self.op(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def update_point(self, index: int, value: float):
        """
        Update a single point.
        
        Args:
            index: Index to update
            value: New value
        
        Time Complexity: O(log n)
        """
        current_value = self.query_range(index, index)
        self.update_range(index, index, value - current_value)


if __name__ == "__main__":
    # Example usage: Track disease cases over time periods
    # Data represents cases per week for 8 weeks
    cases_per_week = [5, 3, 8, 2, 6, 4, 7, 1]
    
    # Build segment tree for sum queries
    st = SegmentTree(cases_per_week, operation="sum")
    
    # Query total cases in weeks 2-5 (0-indexed: weeks 2, 3, 4, 5)
    total = st.query_range(2, 5)
    print(f"Total cases in weeks 2-5: {total}")
    
    # Update: Add 3 cases to weeks 3-6
    st.update_range(3, 6, 3)
    
    # Query again
    total_updated = st.query_range(2, 5)
    print(f"Total cases in weeks 2-5 after update: {total_updated}")
