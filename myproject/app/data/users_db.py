"""Fake user database with location data."""

# Fake user data with username and coordinates
FAKE_USERS = [
    {"id": 1, "username": "Alice Johnson", "latitude": 40.7128, "longitude": -74.0060},
    {"id": 2, "username": "Bob Smith", "latitude": 40.7489, "longitude": -73.9680},
    {"id": 3, "username": "Carol Davis", "latitude": 40.7614, "longitude": -73.9776},
    {"id": 4, "username": "David Wilson", "latitude": 40.7505, "longitude": -73.9972},
    {"id": 5, "username": "Emma Brown", "latitude": 40.7549, "longitude": -73.9840},
    {"id": 6, "username": "Frank Miller", "latitude": 40.7282, "longitude": -74.0076},
    {"id": 7, "username": "Grace Lee", "latitude": 40.7580, "longitude": -73.9855},
    {"id": 8, "username": "Henry Taylor", "latitude": 40.7549, "longitude": -73.9965},
    {"id": 9, "username": "Ivy Martinez", "latitude": 40.7614, "longitude": -74.0037},
    {"id": 10, "username": "Jack Thompson", "latitude": 40.7128, "longitude": -73.9352},
    {"id": 11, "username": "Kate Anderson", "latitude": 40.7489, "longitude": -73.9680},
    {"id": 12, "username": "Leo Clark", "latitude": 40.7505, "longitude": -73.9680},
    {"id": 13, "username": "Mia Rodriguez", "latitude": 40.7282, "longitude": -73.9965},
    {"id": 14, "username": "Noah Garcia", "latitude": 40.7549, "longitude": -73.9840},
    {"id": 15, "username": "Olivia Martinez", "latitude": 40.7614, "longitude": -73.9776},
]


def get_all_users():
    """Get all users from database."""
    return FAKE_USERS


def get_user_by_id(user_id):
    """Get a specific user by ID."""
    for user in FAKE_USERS:
        if user["id"] == user_id:
            return user
    return None
