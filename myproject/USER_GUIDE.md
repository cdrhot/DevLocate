# DevLocate - Complete Feature Guide

## 🎯 Features Overview

### 1. **Route Finding** (Routes Tab)
Find optimal routes between two locations using OpenStreetMap/OSRM.

**How to use:**
1. Click **"Routes"** tab
2. Enter origin coordinates (latitude, longitude)
3. Enter destination coordinates
4. Click **"Find Route"**
5. View:
   - Distance in kilometers
   - Travel time in minutes
   - Route visualization on the map (blue line)

---

### 2. **Find Nearby Users** (Nearby Users Tab)
Discover other users closest to your location.

**How to use:**

#### Option A: Using Browser Geolocation
1. Click **"Nearby Users"** tab
2. Click **"📍 Use My Location"** button
3. Grant location permission to browser
4. Your coordinates auto-populate
5. Set K value (how many users to show, 1-15)
6. Click **"Find Nearby Users"**

#### Option B: Manual Coordinate Entry
1. Click **"Nearby Users"** tab
2. Enter your latitude
3. Enter your longitude
4. Set K value (how many users to show, 1-15)
5. Click **"Find Nearby Users"**

---

### 3. **Show Directions to Users** ⭐ NEW FEATURE
Get directions and distances to any nearby user.

**How to use:**
1. Find nearby users (see above)
2. In the "Nearby Users" list, **click on any user**
3. The application will:
   - Fetch the route to that user
   - Display it on the map (blue line)
   - Show distance and travel time
   - Display a success message in green

**What you'll see:**
- ✅ Green success message: "✅ Route to [Username] - X km (Y min)"
- Blue line on map showing the path
- Route information panel with distance and duration

---

## 📍 Map Features

### Markers
- **Green circle**: Your current location (in route mode) or selected user location
- **Red circle**: Destination (in route mode)
- **Colored circles**: Other nearby users (each user has a unique color)

### Interactions
- **Click any marker**: Shows popup with user/location info
- **Map auto-fits**: Zooms to show all markers properly
- **Pan & Zoom**: Use mouse to navigate the map

---

## 🎨 UI Elements

### Tabs
- **Routes**: Find routes between locations
- **Nearby Users**: Find and navigate to nearby people

### Colors
- **Blue (#3498db)**: Primary routes and actions
- **Green (#27ae60)**: Success messages and nearby users
- **Red (#e74c3c)**: Errors
- **Gray (#95a5a6)**: Secondary buttons

### Interactive Elements
- **User items**: Hover shows more details, click to get directions
- **Buttons**: Highlight on hover, click to interact
- **Forms**: Input validation with helpful error messages

---

## 🗂️ Fake User Database

The application comes pre-loaded with 15 fictional users in NYC area:

1. Alice Johnson (40.7128, -74.0060)
2. Bob Smith (40.7489, -73.9680)
3. Carol Davis (40.7614, -73.9776)
4. David Wilson (40.7505, -73.9972)
5. Emma Brown (40.7549, -73.9840)
6. Frank Miller (40.7282, -74.0076)
7. Grace Lee (40.7580, -73.9855)
8. Henry Taylor (40.7549, -73.9965)
9. Ivy Martinez (40.7614, -74.0037)
10. Jack Thompson (40.7128, -73.9352)
11. Kate Anderson (40.7489, -73.9680)
12. Leo Clark (40.7505, -73.9680)
13. Mia Rodriguez (40.7282, -73.9965)
14. Noah Garcia (40.7549, -73.9840)
15. Olivia Martinez (40.7614, -73.9776)

---

## 📊 Example Workflows

### Workflow 1: Find a Route
1. Start: Click **Routes** tab
2. Enter: Origin (40.7128, -74.0060)
3. Enter: Destination (40.7614, -73.9776)
4. Result: Shows 5.23 km distance, 12 minutes duration, route on map

### Workflow 2: Find Nearby Users & Get Directions
1. Start: Click **Nearby Users** tab
2. Select: Enter coordinates (40.7128, -74.0060)
3. Set: K = 5
4. See: List of 5 nearest users
5. Click: On "Grace Lee" (6.42 km away)
6. Result: Route to Grace Lee displayed, "✅ Route to Grace Lee - 6.42 km (15 min)"

### Workflow 3: Use GPS Location
1. Start: Click **Nearby Users** tab
2. Click: "📍 Use My Location" button
3. Grant: Browser permission for location
4. Auto-fill: Your current coordinates
5. Set: K = 10
6. See: All 10 nearest users
7. Click: Any user to get directions

---

## ⚙️ API Endpoints

### Routes
- `GET /api/osm/route?origin_lat=40.7128&origin_lon=-74.0060&destination_lat=40.7614&destination_lon=-73.9776`

### Users
- `GET /api/users/nearby?latitude=40.7128&longitude=-74.0060&k=5`
- `GET /api/users/all`

### System
- `GET /health` - Health check
- `GET /api/info` - API information

---

## 🐛 Troubleshooting

### Nearby Users tab not showing content
- **Fix**: Make sure to enter coordinates and click "Find Nearby Users"
- **Check**: Console for errors (F12 > Console)

### Geolocation not working
- **Check**: Browser permissions (allow location access)
- **Note**: Only works on HTTPS or localhost
- **Fallback**: Use manual coordinate entry

### No users found nearby
- **Reason**: K might be larger than available users (max 15)
- **Fix**: Increase coordinate proximity or reduce K value

### Map not loading
- **Check**: Internet connection (needs to load OSM tiles)
- **Check**: Browser supports Leaflet (all modern browsers do)
- **Fix**: Refresh page

### Invalid coordinates error
- **Remember**: Latitude: -90 to 90, Longitude: -180 to 180
- **Example**: 40.7128, -74.0060 (NYC)

---

## 🔄 Data Flow

```
User Input
    ↓
Validation
    ↓
API Request
    ↓
Backend Processing
    ↓
Route/User Calculation
    ↓
JSON Response
    ↓
Display on Map
    ↓
Show Results
```

---

## 📱 Responsive Design

- **Desktop**: Full sidebar + large map
- **Tablet**: Stacked layout, touch-friendly
- **Mobile**: Adjusted font sizes, scrollable results

---

## 🎓 Learning Resources

- **Leaflet.js**: Interactive maps - https://leafletjs.com/
- **OpenStreetMap**: Free map data - https://www.openstreetmap.org/
- **OSRM**: Routing engine - https://project-osrm.org/
- **Haversine Formula**: Distance calculation - https://en.wikipedia.org/wiki/Haversine_formula

---

## 💡 Tips & Tricks

✨ **Pro Tips:**
1. Use K=1 to find the closest user
2. Use K=15 to see all nearby users
3. Click user markers on map for quick info
4. Browser geolocation only works on HTTPS or localhost
5. Zoom in/out on map for better visibility
6. Refresh page to clear previous selections

---

## 🚀 Version History

**v1.1.0 (Current)**
- ✨ NEW: Nearby users finding with fake database
- ✨ NEW: Click users to show directions
- ✨ NEW: Browser geolocation support
- ✨ NEW: Tab-based UI
- 🔧 Fixed: Leaflet CDN integrity hashes
- 🔧 Fixed: Exception handling

**v1.0.0 (Initial)**
- Route finding with OSRM
- Leaflet map visualization
- Distance and duration display

---

**Last Updated**: October 16, 2025  
**Built with**: FastAPI, Leaflet.js, OpenStreetMap, OSRM
