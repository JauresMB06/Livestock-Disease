"""
Web Dashboard API Routes
Connects to Segment Tree for range queries
Member 2: Full-Stack Developer
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.core_logic.segment_tree import SegmentTree
from pydantic import BaseModel

router = APIRouter()

# In-memory storage for dashboard data
# In production, this would be connected to a database
_dashboard_data: List[float] = []
_segment_tree: Optional[SegmentTree] = None


def get_segment_tree() -> SegmentTree:
    """Get or create the Segment Tree for dashboard queries."""
    global _segment_tree, _dashboard_data
    
    if _segment_tree is None:
        # Initialize with empty data (can be loaded from database)
        _dashboard_data = [0.0] * 30  # 30 time periods (e.g., days/weeks)
        _segment_tree = SegmentTree(_dashboard_data, operation="sum")
    
    return _segment_tree


def update_dashboard_data(index: int, value: float):
    """Update dashboard data and segment tree."""
    global _dashboard_data, _segment_tree
    
    if _segment_tree is None:
        get_segment_tree()
    
    if 0 <= index < len(_dashboard_data):
        _dashboard_data[index] = value
        # Rebuild segment tree with updated data
        _segment_tree = SegmentTree(_dashboard_data, operation="sum")


class RangeQueryRequest(BaseModel):
    start_index: int
    end_index: int
    operation: str = "sum"  # "sum", "min", "max"


class DataPoint(BaseModel):
    index: int
    value: float


@router.get("/stats/range")
def query_range(start: int, end: int, operation: str = "sum"):
    """
    Query range statistics using Segment Tree.
    
    Args:
        start: Start index (0-indexed)
        end: End index (0-indexed, inclusive)
        operation: Operation type ("sum", "min", "max")
    """
    try:
        st = get_segment_tree()
        
        # Create appropriate segment tree if operation differs
        if operation != "sum":
            st = SegmentTree(_dashboard_data, operation=operation)
        
        result = st.query_range(start, end)
        
        return {
            "start": start,
            "end": end,
            "operation": operation,
            "result": result,
            "range_size": end - start + 1
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stats/range")
def query_range_post(request: RangeQueryRequest):
    """Query range statistics using POST method."""
    return query_range(request.start_index, request.end_index, request.operation)


@router.post("/data/update")
def update_data_point(data: DataPoint):
    """Update a single data point."""
    try:
        update_dashboard_data(data.index, data.value)
        return {
            "status": "updated",
            "index": data.index,
            "value": data.value
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/data/update-range")
def update_data_range(start: int, end: int, value: float):
    """Update a range of data points (add value to each)."""
    try:
        st = get_segment_tree()
        st.update_range(start, end, value)
        
        # Update underlying data array
        for i in range(start, end + 1):
            if 0 <= i < len(_dashboard_data):
                _dashboard_data[i] += value
        
        return {
            "status": "updated",
            "start": start,
            "end": end,
            "value_added": value
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/data/all")
def get_all_data():
    """Get all dashboard data."""
    return {
        "data": _dashboard_data,
        "length": len(_dashboard_data)
    }


@router.get("/stats/summary")
def get_summary():
    """Get summary statistics using Segment Tree."""
    st_sum = get_segment_tree()
    st_min = SegmentTree(_dashboard_data, operation="min")
    st_max = SegmentTree(_dashboard_data, operation="max")
    
    n = len(_dashboard_data)
    if n == 0:
        return {
            "total": 0,
            "min": 0,
            "max": 0,
            "average": 0
        }
    
    total = st_sum.query_range(0, n - 1)
    min_val = st_min.query_range(0, n - 1)
    max_val = st_max.query_range(0, n - 1)
    avg = total / n if n > 0 else 0
    
    return {
        "total": total,
        "min": min_val if min_val != float('inf') else 0,
        "max": max_val if max_val != float('-inf') else 0,
        "average": avg,
        "data_points": n
    }
