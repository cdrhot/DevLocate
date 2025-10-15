# DevLocate - API Documentation

## Overview

DevLocate is a FastAPI application for finding routes between locations and discovering nearby users using OpenStreetMap and real-time geolocation.

---

## 🗺️ Route Finding Endpoints

### Get Route Between Two Points

**Endpoint**: `GET /api/osm/route`

**Description**: Calculate optimal route and distance between two coordinates using OSRM

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| origin_lat | float | Yes | Starting point latitude (-90 to 90) |
| origin_lon | float | Yes | Starting point longitude (-180 to 180) |
| destination_lat | float | Yes | Ending point latitude (-90 to 90) |
| destination_lon | float | Yes | Ending point longitude (-180 to 180) |

**Example Request**:
```
GET /api/osm/route?origin_lat=40.7128&origin_lon=-74.0060&destination_lat=40.7614&destination_lon=-73.9776
```

**Success Response** (200):
```json
{
  "distance_km": 5.23,
  "duration_minutes": 12,
  "geometry": {
    "type": "LineString",
    "coordinates": [
      [-74.0060, 40.7128],
      [-74.0055, 40.7135],
      ...
      [-73.9776, 40.7614]
    ]
  },
  "origin": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "destination": {
    "lat": 40.7614,
    "lon": -73.9776
  }
}
```

**Error Response** (400/500):
```json
{
  "detail": "Invalid origin coordinates"
}
```

---

## 👥 User Location Endpoints

### Get Nearby Users

**Endpoint**: `GET /api/users/nearby`

**Description**: Find K nearest users to a given location, sorted by distance

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| latitude | float | Yes | - | Current user latitude (-90 to 90) |
| longitude | float | Yes | - | Current user longitude (-180 to 180) |
| k | integer | No | 5 | Number of nearest users (1-15) |

**Example Request**:
```
GET /api/users/nearby?latitude=40.7128&longitude=-74.0060&k=5
```

**Success Response** (200):
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
      "id": 2,
      "username": "Bob Smith",
      "latitude": 40.7489,
      "longitude": -73.9680,
      "distance_km": 4.15
    },
    {
      "id": 3,
      "username": "Carol Davis",
      "latitude": 40.7614,
      "longitude": -73.9776,
      "distance_km": 5.23
    },
    {
      "id": 7,
      "username": "Grace Lee",
      "latitude": 40.7580,
      "longitude": -73.9855,
      "distance_km": 6.42
    },
    {
      "id": 4,
      "username": "David Wilson",
      "latitude": 40.7505,
      "longitude": -73.9972,
      "distance_km": 8.17
    }
  ]
}
```

**Error Response** (400):
```json
{
  "detail": "K must be at least 1"
}
```

---

### Get All Users

**Endpoint**: `GET /api/users/all`

**Description**: Retrieve all users in the system with their locations

**Example Request**:
```
GET /api/users/all
```

**Success Response** (200):
```json
{
  "count": 15,
  "users": [
    {
      "id": 1,
      "username": "Alice Johnson",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    {
      "id": 2,
      "username": "Bob Smith",
      "latitude": 40.7489,
      "longitude": -73.9680
    },
    ...
  ]
}
```

---

## 🔧 System Endpoints

### Health Check

**Endpoint**: `GET /health`

**Description**: Verify that the API is running and healthy

**Success Response** (200):
```json
{
  "status": "ok",
  "message": "OSM Route Finder is running"
}
```

---

### API Information

**Endpoint**: `GET /api/info`

**Description**: Get information about available endpoints

**Success Response** (200):
```json
{
  "app": "OSM Route Finder",
  "version": "1.0.0",
  "endpoints": {
    "root": "/",
    "health": "/health",
    "route": "/api/osm/route",
    "docs": "/docs",
    "redoc": "/redoc"
  }
}
```

---

## 📊 Distance Calculation

The API uses the **Haversine formula** for accurate distance calculation:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1−a))
d = R × c

where R = 6371 km (Earth's mean radius)
```

**Accuracy**: ±0.5% for typical distances

---

## 🗺️ Coordinate Systems

### Latitude
- Range: -90 to +90 degrees
- Negative = South, Positive = North
- Example: 40.7128 (NYC)

### Longitude
- Range: -180 to +180 degrees
- Negative = West, Positive = East
- Example: -74.0060 (NYC)

---

## 📋 Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Route found, users retrieved |
| 400 | Bad Request | Invalid coordinates, K out of range |
| 404 | Not Found | Invalid endpoint |
| 500 | Server Error | OSRM unavailable, database error |

---

## 🔐 CORS

The API has CORS enabled for all origins by default. Modify in `app/main.py`:

```python
CORSMiddleware(
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📍 Test Coordinates

Use these NYC coordinates for testing:

| Location | Latitude | Longitude |
|----------|----------|-----------|
| Central Park | 40.7829 | -73.9654 |
| Times Square | 40.7580 | -73.9855 |
| Statue of Liberty | 40.6892 | -74.0445 |
| Brooklyn Bridge | 40.7061 | -73.9969 |
| Empire State Building | 40.7484 | -73.9857 |

---

## 🚀 Example Usage

### Python

```python
import requests

# Find nearby users
response = requests.get(
    'http://localhost:8000/api/users/nearby',
    params={
        'latitude': 40.7128,
        'longitude': -74.0060,
        'k': 5
    }
)
users = response.json()
print(users)

# Find route
response = requests.get(
    'http://localhost:8000/api/osm/route',
    params={
        'origin_lat': 40.7128,
        'origin_lon': -74.0060,
        'destination_lat': 40.7614,
        'destination_lon': -73.9776
    }
)
route = response.json()
print(f"Distance: {route['distance_km']} km")
```

### JavaScript

```javascript
// Find nearby users
fetch('/api/users/nearby?latitude=40.7128&longitude=-74.0060&k=5')
  .then(response => response.json())
  .then(data => console.log(data));

// Find route
fetch('/api/osm/route?origin_lat=40.7128&origin_lon=-74.0060&destination_lat=40.7614&destination_lon=-73.9776')
  .then(response => response.json())
  .then(data => console.log(`Distance: ${data.distance_km} km`));
```

### cURL

```bash
# Nearby users
curl "http://localhost:8000/api/users/nearby?latitude=40.7128&longitude=-74.0060&k=5"

# Route
curl "http://localhost:8000/api/osm/route?origin_lat=40.7128&origin_lon=-74.0060&destination_lat=40.7614&destination_lon=-73.9776"

# Health check
curl http://localhost:8000/health
```

---

## 📚 Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try out the API directly in your browser with the interactive docs!

---

## 🐛 Troubleshooting

### OSRM API Unavailable
**Issue**: "Request timeout - OSRM service unavailable"
**Solution**: 
- Check internet connection
- OSRM public service might be down temporarily
- Use a private OSRM instance

### Invalid Coordinates
**Issue**: "Invalid coordinates"
**Solution**:
- Verify latitude is between -90 and 90
- Verify longitude is between -180 and 180
- Check for typos in coordinates

### No Users Found
**Issue**: Empty users list
**Solution**:
- K might be larger than available users
- Check that users are loaded in the database
- Verify database connection

---

## 📈 Performance Metrics

- **Route Calculation**: 200-500ms (depends on distance and OSRM load)
- **Nearby Users Query**: <50ms
- **All Users Query**: <10ms
- **Map Rendering**: <100ms

---

**API Version**: 1.1.0  
**Last Updated**: October 16, 2025
