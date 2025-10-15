# DevLocate - Nearby Users Feature

## ✨ New Features Added

### 1. **Fake User Database with Locations**
   - **File**: `app/data/users_db.py`
   - **Content**: 15 fake users with usernames and lat/long coordinates
   - **Coverage**: All users in NYC area for realistic demo

### 2. **Nearby Users Finding**
   - **Service**: `app/services/user_service.py`
   - **Features**:
     - Calculate distances using Haversine formula
     - Find K nearest users to current location
     - Sort users by distance
     - Return user info with distances

### 3. **Distance Calculation**
   - **Helper**: Enhanced `app/utils/helpers.py` 
   - **Function**: `calculate_distance()` - Haversine formula implementation
   - **Accuracy**: Distance in kilometers with 2 decimal precision

### 4. **Backend API Endpoints**
   - **File**: `app/routes/map_routes.py`
   - **Endpoints**:
     - `GET /api/users/nearby?latitude=40.7128&longitude=-74.0060&k=5`
       - Find K nearest users to coordinates
     - `GET /api/users/all`
       - Get all users in system

### 5. **Frontend Enhancements**
   - **Tabs Interface**: Routes vs. Nearby Users tabs
   - **Geolocation Support**: 
     - "Use My Location" button with browser permission
     - Falls back to manual coordinate entry
   - **Nearby Users Form**:
     - Current latitude input
     - Current longitude input
     - K parameter input (number of users to show)
   - **User List Display**:
     - Shows ranked list of nearest users
     - Displays username, distance, and coordinates
     - Color-coded for visual distinction

### 6. **Map Visualization**
   - **User Markers**: Colored circle markers for each nearby user
   - **Auto-zoom**: Map automatically fits all user markers
   - **Popup Info**: Click markers to see user details
   - **Multiple colors**: Different colors for each user

## 📱 How to Use

### Finding Nearby Users

**Option 1: Using Geolocation**
1. Click on **"Nearby Users"** tab
2. Click **"📍 Use My Location"** button
3. Grant browser permission
4. Your current latitude/longitude will auto-fill
5. Set K value (number of users)
6. Click **"Find Nearby Users"**

**Option 2: Manual Entry**
1. Click on **"Nearby Users"** tab
2. Enter your latitude
3. Enter your longitude
4. Set K value (number of users)
5. Click **"Find Nearby Users"**

**Result**: 
- Map shows nearby users with colored markers
- Sidebar shows list of K nearest users ranked by distance
- Each user shows: name, distance (km), and coordinates

## 🏗️ Project Structure Update

```
myproject/
├── app/
│   ├── data/
│   │   ├── __init__.py
│   │   └── users_db.py              # ✨ Fake user data
│   ├── services/
│   │   ├── osm_service.py
│   │   └── user_service.py          # ✨ Nearby users logic
│   ├── routes/
│   │   └── map_routes.py            # ✨ Updated with user endpoints
│   ├── templates/
│   │   └── index.html               # ✨ Updated UI with tabs
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # ✨ Tab and user list styles
│   │   └── js/
│   │       └── map.js               # ✨ User marker rendering
│   └── utils/
│       └── helpers.py               # ✨ Distance calculation
```

## 🔧 Technical Details

### User Service Methods

```python
# Get K nearest users
UserService.get_nearby_users(
    current_lat: float,
    current_lon: float,
    k: int = 5
)

# Get all users
UserService.get_all_users()
```

### Distance Formula

Uses the **Haversine formula**:
```
d = 2 * R * asin(sqrt(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)))
```
Where R = 6371 km (Earth's radius)

### Sample API Response

```json
{
  "current_location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "count": 5,
  "users": [
    {
      "id": 1,
      "username": "Alice Johnson",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "distance_km": 0.0
    },
    {
      "id": 7,
      "username": "Grace Lee",
      "latitude": 40.7580,
      "longitude": -73.9855,
      "distance_km": 6.42
    }
    // ... more users
  ]
}
```

## 🎨 Frontend Features

### Tab Switching
- Switch between "Routes" and "Nearby Users" tabs
- Each tab maintains its own form state
- Clean tab UI with active state indication

### Geolocation Integration
- Browser's native geolocation API
- Handles permission requests gracefully
- Falls back to manual entry if permission denied
- Auto-populates coordinates on success

### User List UI
- Ranked display (#1, #2, etc.)
- Color-coded distance badges
- Hover effects for interactivity
- Scrollable list for many users

### Map Integration
- User markers with distinct colors
- Auto-fit zoom to show all users
- Click markers for user information
- Separate from route display

## 📊 Fake Users Data

15 pre-populated users in NYC area:
- Alice Johnson, Bob Smith, Carol Davis
- David Wilson, Emma Brown, Frank Miller
- Grace Lee, Henry Taylor, Ivy Martinez
- Jack Thompson, Kate Anderson, Leo Clark
- Mia Rodriguez, Noah Garcia, Olivia Martinez

All coordinates within NYC bounds for realistic demo.

## 🚀 Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Navigate to http://localhost:8000
```

## ✅ What's Been Tested

- ✅ Route finding (existing feature maintained)
- ✅ Nearby users calculation
- ✅ Distance formula accuracy
- ✅ Tab switching
- ✅ Form validation
- ✅ Error handling
- ✅ Map rendering with user markers
- ✅ User list display

## 🎯 Next Steps (Optional Enhancements)

1. **Database Integration**: Replace fake data with real database
2. **User Authentication**: Add user login system
3. **Real Location Saving**: Store user locations dynamically
4. **Search Filters**: Filter users by distance range
5. **Profile Pages**: Click users to see profiles
6. **Messaging**: Direct messaging between users
7. **User Analytics**: Show user activity on map
8. **Custom Markers**: Upload user profile pictures for markers

---

**Version**: 1.1.0  
**Last Updated**: October 16, 2025
