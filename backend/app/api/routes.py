from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..core.service import RoutingService

router = APIRouter(prefix="/api/v1", tags=["routing"])
routing_service = RoutingService()

class RouteRequest(BaseModel):
    start: str
    end: str

class RouteResponse(BaseModel):
    path: List[str]
    total_distance: float
    nodes_visited: int

class GraphInfoResponse(BaseModel):
    nodes: List[str]
    node_count: int
    edge_count: int

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Smart Logistics Routing Engine"}

@router.post("/route", response_model=RouteResponse)
async def calculate_route(request: RouteRequest):
    """Calculate the shortest route between two locations using Dijkstra's algorithm"""
    try:
        path, distance, nodes_visited = routing_service.calculate_route(
            request.start, request.end
        )
        return RouteResponse(
            path=path,
            total_distance=distance,
            nodes_visited=nodes_visited
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/graph", response_model=GraphInfoResponse)
async def get_graph_info():
    """Get information about the logistics network graph"""
    try:
        nodes, node_count, edge_count = routing_service.get_graph_info()
        return GraphInfoResponse(
            nodes=sorted(nodes),
            node_count=node_count,
            edge_count=edge_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
