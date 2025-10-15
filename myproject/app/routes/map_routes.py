"""API routes for user discovery and directions."""

from fastapi import APIRouter, Query, HTTPException
from app.services.osm_service import OSMService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/api/osm/route")
async def get_route(
    origin_lat: float = Query(..., description="Origin latitude"),
    origin_lon: float = Query(..., description="Origin longitude"),
    destination_lat: float = Query(..., description="Destination latitude"),
    destination_lon: float = Query(..., description="Destination longitude")
):
    """
    Get route information between two points.
    
    Parameters:
    - origin_lat: Origin latitude
    - origin_lon: Origin longitude
    - destination_lat: Destination latitude
    - destination_lon: Destination longitude
    
    Returns:
    - JSON with distance (km), duration (minutes), and route geometry
    """
    
    # Fetch route from OSM service
    result = OSMService.get_route(
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon
    )
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to fetch route")
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/api/users/nearby")
async def get_nearby_users(
    latitude: float = Query(..., description="Current user latitude"),
    longitude: float = Query(..., description="Current user longitude"),
    k: int = Query(5, description="Number of nearest users to return (default: 5)")
):
    """
    Get K nearest users to current location.
    
    Parameters:
    - latitude: Current user latitude
    - longitude: Current user longitude
    - k: Number of nearest users to return (default: 5)
    
    Returns:
    - JSON with list of nearby users sorted by distance
    """
    
    # Fetch nearby users from service
    result = UserService.get_nearby_users(latitude, longitude, k)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to fetch nearby users")
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/api/users/all")
async def get_all_users():
    """
    Get all users in the system.
    
    Returns:
    - JSON with list of all users
    """
    
    result = UserService.get_all_users()
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
