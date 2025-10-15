"""Service for finding nearby users."""

from typing import List, Dict, Any, Optional
from app.data.users_db import get_all_users
from app.utils.helpers import calculate_distance, validate_coordinates


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def get_nearby_users(
        current_lat: float,
        current_lon: float,
        k: int = 5
    ) -> Optional[Dict[str, Any]]:
        """
        Find K nearest users to current location.
        
        Args:
            current_lat (float): Current user latitude
            current_lon (float): Current user longitude
            k (int): Number of nearest users to return (default: 5)
            
        Returns:
            Dict: List of nearby users with distances
            None: If request fails
        """
        
        # Validate coordinates
        if not validate_coordinates(current_lat, current_lon):
            return {"error": "Invalid coordinates"}
        
        # Validate k parameter
        if k < 1:
            return {"error": "K must be at least 1"}
        
        try:
            # Get all users
            all_users = get_all_users()
            
            if not all_users:
                return {"error": "No users found"}
            
            # Calculate distances for each user
            users_with_distance = []
            for user in all_users:
                distance = calculate_distance(
                    current_lat,
                    current_lon,
                    user["latitude"],
                    user["longitude"]
                )
                users_with_distance.append({
                    "id": user["id"],
                    "username": user["username"],
                    "latitude": user["latitude"],
                    "longitude": user["longitude"],
                    "distance_km": distance
                })
            
            # Sort by distance and get top K
            nearby_users = sorted(
                users_with_distance,
                key=lambda x: x["distance_km"]
            )[:k]
            
            return {
                "current_location": {
                    "latitude": current_lat,
                    "longitude": current_lon
                },
                "count": len(nearby_users),
                "users": nearby_users
            }
            
        except Exception as e:
            return {"error": f"Error finding nearby users: {str(e)}"}
    
    @staticmethod
    def get_all_users() -> Dict[str, Any]:
        """
        Get all users in the system.
        
        Returns:
            Dict: List of all users
        """
        try:
            users = get_all_users()
            return {
                "count": len(users),
                "users": users
            }
        except Exception as e:
            return {"error": f"Error retrieving users: {str(e)}"}
