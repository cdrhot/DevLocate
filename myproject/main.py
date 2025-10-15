"""
DevLocate - Find K nearest people near you
Simple FastAPI application with OpenStreetMap integration
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import math
from pathlib import Path
from typing import Dict, Any, Optional

# ============================================================================
# USER DATABASE
# ============================================================================

FAKE_USERS = [
    {"id": 1, "username": "Alice Johnson", "latitude": 40.7128, "longitude": -74.0060},
    {"id": 2, "username": "Bob Smith", "latitude": 40.7282, "longitude": -74.0076},
    {"id": 3, "username": "Carol Davis", "latitude": 40.7505, "longitude": -73.9972},
    {"id": 4, "username": "David Wilson", "latitude": 40.7549, "longitude": -73.9965},
    {"id": 5, "username": "Emma Brown", "latitude": 40.7614, "longitude": -73.9776},
    {"id": 6, "username": "Frank Miller", "latitude": 40.7489, "longitude": -73.9680},
    {"id": 7, "username": "Grace Lee", "latitude": 40.7580, "longitude": -73.9855},
    {"id": 8, "username": "Henry Taylor", "latitude": 40.7489, "longitude": -73.9680},
    {"id": 9, "username": "Ivy Martinez", "latitude": 40.7614, "longitude": -73.9776},
    {"id": 10, "username": "Jack Thompson", "latitude": 40.7282, "longitude": -74.0076},
    {"id": 11, "username": "Kate Anderson", "latitude": 40.7505, "longitude": -73.9972},
    {"id": 12, "username": "Leo Clark", "latitude": 40.7549, "longitude": -73.9965},
    {"id": 13, "username": "Mia Rodriguez", "latitude": 40.7614, "longitude": -73.9776},
    {"id": 14, "username": "Noah Garcia", "latitude": 40.7489, "longitude": -73.9680},
    {"id": 15, "username": "Olivia Martinez", "latitude": 40.7580, "longitude": -73.9855},
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula."""
    R = 6371  # Earth's radius in km
    dLat = (lat2 - lat1) * math.pi / 180
    dLon = (lon2 - lon1) * math.pi / 180
    a = (math.sin(dLat / 2) ** 2 + 
         math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * 
         math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate if coordinates are within valid ranges."""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def get_nearby_users(latitude: float, longitude: float, k: int = 5) -> Dict[str, Any]:
    """Get K nearest users to current location."""
    if not validate_coordinates(latitude, longitude):
        return {"error": "Invalid coordinates"}
    
    if k < 1 or k > 15:
        return {"error": "K must be between 1 and 15"}
    
    # Calculate distances for all users
    users_with_distance = []
    for user in FAKE_USERS:
        distance = calculate_distance(latitude, longitude, user["latitude"], user["longitude"])
        users_with_distance.append({
            "id": user["id"],
            "username": user["username"],
            "latitude": user["latitude"],
            "longitude": user["longitude"],
            "distance_km": round(distance, 2)
        })
    
    # Sort by distance and get top K
    users_with_distance.sort(key=lambda x: x["distance_km"])
    nearby_users = users_with_distance[:k]
    
    return {
        "current_location": {"latitude": latitude, "longitude": longitude},
        "count": len(nearby_users),
        "users": nearby_users
    }


def get_route(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float) -> Optional[Dict[str, Any]]:
    """Get route information from OSRM API."""
    if not validate_coordinates(origin_lat, origin_lon):
        return {"error": "Invalid origin coordinates"}
    if not validate_coordinates(dest_lat, dest_lon):
        return {"error": "Invalid destination coordinates"}
    
    try:
        # Call OSRM API
        url = (f"http://router.project-osrm.org/route/v1/driving/"
               f"{origin_lon},{origin_lat};"
               f"{dest_lon},{dest_lat}"
               "?overview=full&geometries=geojson")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return {"error": "Failed to fetch route"}
        
        data = response.json()
        
        if "routes" not in data or len(data["routes"]) == 0:
            return {"error": "No route found"}
        
        route = data["routes"][0]
        distance_km = round(route["distance"] / 1000, 2)
        duration_minutes = round(route["duration"] / 60, 0)
        
        return {
            "origin": {"lat": origin_lat, "lon": origin_lon},
            "destination": {"lat": dest_lat, "lon": dest_lon},
            "distance_km": distance_km,
            "duration_minutes": int(duration_minutes),
            "geometry": route.get("geometry", {})
        }
    
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="DevLocate",
    description="Find K nearest people near you using OpenStreetMap",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Serve main HTML page."""
    templates_dir = BASE_DIR / "templates"
    index_path = templates_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"error": "index.html not found"}


@app.get("/api/osm/route")
async def get_route_endpoint(
    origin_lat: float = Query(...),
    origin_lon: float = Query(...),
    destination_lat: float = Query(...),
    destination_lon: float = Query(...)
):
    """Get route between two points."""
    result = get_route(origin_lat, origin_lon, destination_lat, destination_lon)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to fetch route")
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.get("/api/users/nearby")
async def get_nearby_users_endpoint(
    latitude: float = Query(...),
    longitude: float = Query(...),
    k: int = Query(5)
):
    """Get K nearest users to current location."""
    result = get_nearby_users(latitude, longitude, k)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.get("/api/users/all")
async def get_all_users_endpoint():
    """Get all users in system."""
    return {"users": FAKE_USERS}
