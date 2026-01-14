# Big-O Complexity Analysis
## Livestock Disease Surveillance Network - Data Structures

Member 1: Algorithmic Lead

---

## 1. Graph Data Structure

### Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `add_vertex(v)` | O(1) | O(1) | Adding a single vertex |
| `add_edge(u, v, w)` | O(1) | O(1) | Adding an edge (amortized) |
| `update_edge_weight(u, v, w)` | O(degree(u) + degree(v)) | O(1) | Worst case: O(V) if fully connected |
| `get_neighbors(v)` | O(degree(v)) | O(degree(v)) | Returns all neighbors |
| `get_all_vertices()` | O(V) | O(V) | V = number of vertices |
| `get_all_edges()` | O(V + E) | O(V + E) | E = number of edges |

### Dijkstra's Algorithm

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `dijkstra(graph, start, end)` | O((V + E) log V) | O(V) | Using binary heap |
| `reconstruct_path(prev, start, end)` | O(V) | O(V) | Worst case path length |

**Analysis:**
- Uses binary heap (priority queue) for efficient extraction of minimum distance vertex
- Each vertex is extracted once: O(V log V)
- Each edge is relaxed once: O(E log V)
- Total: O((V + E) log V)
- For sparse graphs (E ≈ V): O(V log V)
- For dense graphs (E ≈ V²): O(V² log V)

---

## 2. Union-Find (Disjoint Set Union)

### Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `make_set(x)` | O(1) | O(1) | Initialize singleton set |
| `find(x)` | O(α(n)) amortized | O(α(n)) amortized | α = inverse Ackermann function |
| `union(x, y)` | O(α(n)) amortized | O(1) | With path compression & union by rank |
| `connected(x, y)` | O(α(n)) amortized | O(1) | Uses find operation |
| `get_cluster_size(x)` | O(α(n)) amortized | O(1) | Uses find operation |
| `get_all_clusters()` | O(n · α(n)) | O(n) | n = number of elements |
| `get_cluster_count()` | O(n · α(n)) | O(n) | Uses get_all_clusters |

**Analysis:**
- Uses path compression: makes parent point directly to root
- Uses union by rank: attaches smaller tree under larger tree
- α(n) is the inverse Ackermann function, effectively constant for practical purposes
- For n ≤ 2^65536, α(n) ≤ 5
- Amortized complexity is nearly constant in practice

---

## 3. Priority Queue (Min Heap)

### Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `push(alert)` | O(log n) | O(1) | Insert into heap |
| `pop()` | O(log n) | O(1) | Extract minimum |
| `peek()` | O(1) | O(1) | View minimum without removal |
| `is_empty()` | O(1) | O(1) | Check if empty |
| `get_size()` | O(1) | O(1) | Get number of elements |
| `get_all_alerts()` | O(n log n) | O(n) | Creates sorted copy |
| `clear()` | O(1) | O(1) | Clear all elements |

**Analysis:**
- Implemented using binary heap (array-based)
- Height of heap: O(log n)
- Insert/delete operations maintain heap property: O(log n)
- Peek operation is O(1) since minimum is always at root
- Space: O(n) for storing n elements

---

## 4. Segment Tree with Lazy Propagation

### Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `build(data)` | O(n) | O(n) | Construct tree from array |
| `query_range(l, r)` | O(log n) | O(log n) | Query range [l, r] |
| `update_range(l, r, val)` | O(log n) | O(log n) | Update range with lazy propagation |
| `update_point(i, val)` | O(log n) | O(log n) | Update single point |

**Analysis:**
- Tree size: O(n) - uses 2n space for n elements
- Height: O(log n)
- Query: Traverses at most 2 log n nodes
- Update with lazy propagation: Updates are deferred until query time
- Lazy propagation reduces update complexity from O(n) to O(log n) for range updates
- Supports operations: sum, min, max

**Lazy Propagation Benefits:**
- Without lazy: Range update would be O(n log n)
- With lazy: Range update is O(log n)
- Lazy values are pushed down only when needed (during queries)

---

## 5. Trie (Clinical Signs)

### Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `insert(sign, disease)` | O(m) | O(m) | m = length of sign |
| `search(prefix)` | O(m + k) | O(k) | m = prefix length, k = results |
| `contains(sign)` | O(m) | O(1) | m = length of sign |
| `get_diseases(sign)` | O(m) | O(d) | d = number of diseases |

**Analysis:**
- Insert: O(m) where m is the length of the clinical sign string
- Search: O(m) to navigate to prefix node + O(k) to collect all matching signs
- Space: O(ALPHABET_SIZE × N × M) where N = number of signs, M = average length
- Efficient for prefix matching and autocomplete
- Better than linear search O(n) for large dictionaries

---

## Overall System Complexity

### Path of Least Risk Calculation
1. Update Graph edges based on outbreaks: O(E) worst case
2. Run Dijkstra: O((V + E) log V)
3. **Total: O((V + E) log V)**

### Cluster Detection
1. Union-Find operations: O(n · α(n)) ≈ O(n) in practice
2. **Total: O(n)** where n = number of outbreak locations

### Range Queries (Dashboard)
1. Segment Tree query: O(log n)
2. **Total: O(log n)** per query

### Alert Processing
1. Insert alert: O(log n)
2. Extract highest priority: O(log n)
3. **Total: O(log n)** per alert operation

### Autocomplete (CLI)
1. Trie search: O(m + k) where m = prefix length, k = results
2. **Total: O(m + k)** - very efficient for real-time suggestions

---

## Space Complexity Summary

| Data Structure | Space Complexity |
|---------------|------------------|
| Graph | O(V + E) |
| Union-Find | O(n) |
| Priority Queue | O(n) |
| Segment Tree | O(n) |
| Trie | O(ALPHABET_SIZE × N × M) |

**Total System Space:** O(V + E + n) where:
- V = number of locations (vertices)
- E = number of routes (edges)
- n = number of alerts/time periods

---

## References

[1] Project Requirements Document
[2] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms (3rd ed.). MIT Press.
