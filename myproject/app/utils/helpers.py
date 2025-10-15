"""Helper functions for the application."""

import math


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula.
    
    Args:
        lat1, lon1: First coordinate (latitude, longitude)
        lat2, lon2: Second coordinate (latitude, longitude)
        
    Returns:
        float: Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return round(R * c, 2)


def format_distance(distance_m):
    """
    Convert distance in meters to kilometers.
    
    Args:
        distance_m (float): Distance in meters
        
    Returns:
        float: Distance in kilometers
    """
    return round(distance_m / 1000, 2)


def format_duration(duration_s):
    """
    Convert duration in seconds to minutes.
    
    Args:
        duration_s (float): Duration in seconds
        
    Returns:
        int: Duration in minutes
    """
    return round(duration_s / 60)


def validate_coordinates(lat, lon):
    """
    Validate latitude and longitude.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        bool: True if valid, False otherwise
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180
