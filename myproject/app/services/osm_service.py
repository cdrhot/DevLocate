"""Service module for OpenStreetMap and OSRM integration."""

import requests
from typing import Dict, Any, Optional
from app.utils.helpers import format_distance, format_duration, validate_coordinates


class OSMService:
    """Service class to interact with OpenStreetMap and OSRM APIs."""
    
    OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"
    
    @staticmethod
    def get_route(
        origin_lat: float,
        origin_lon: float,
        destination_lat: float,
        destination_lon: float
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch route information from OSRM API.
        
        Args:
            origin_lat (float): Origin latitude
            origin_lon (float): Origin longitude
            destination_lat (float): Destination latitude
            destination_lon (float): Destination longitude
            
        Returns:
            Dict: Route information with distance, duration, and geometry
            None: If request fails
        """
        
        # Validate coordinates
        if not validate_coordinates(origin_lat, origin_lon):
            return {"error": "Invalid origin coordinates"}
        if not validate_coordinates(destination_lat, destination_lon):
            return {"error": "Invalid destination coordinates"}
        
        try:
            # Build OSRM API URL
            url = (
                f"{OSMService.OSRM_BASE_URL}/"
                f"{origin_lon},{origin_lat};"
                f"{destination_lon},{destination_lat}"
                "?overview=full&geometries=geojson"
            )
            
            # Make request with timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if request was successful
            if data.get("code") != "Ok":
                return {"error": f"OSRM API error: {data.get('code')}"}
            
            # Extract route information
            if not data.get("routes"):
                return {"error": "No route found"}
            
            route = data["routes"][0]
            
            return {
                "distance_km": format_distance(route["distance"]),
                "duration_minutes": format_duration(route["duration"]),
                "geometry": route["geometry"],
                "origin": {
                    "lat": origin_lat,
                    "lon": origin_lon
                },
                "destination": {
                    "lat": destination_lat,
                    "lon": destination_lon
                }
            }
            
        except requests.exceptions.Timeout:
            return {"error": "Request timeout - OSRM service unavailable"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
