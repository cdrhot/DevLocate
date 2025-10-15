"""Simple test script to verify the API is working"""
import sys
sys.path.insert(0, '.')

from app.data.users_db import get_all_users
from app.services.user_service import UserService

# Test get all users
all_users = get_all_users()
print(f"Total users: {len(all_users)}")
print(f"First user: {all_users[0]}")

# Test nearby users
result = UserService.get_nearby_users(40.7128, -74.0060, k=5)
print(f"\nNearby users result:")
print(result)

print("\n✅ All imports and functions working!")
