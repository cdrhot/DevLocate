# 👥 DevLocate

A complete FastAPI web application for finding K nearest people near you using OpenStreetMap (OSM) and Haversine distance calculations.

## Features

- 🗺️ **Interactive Map**: Real-time user location visualization using Leaflet.js and OpenStreetMap tiles
- 📍 **Nearby People Discovery**: Find K nearest users to your current location
- 📏 **Distance Calculation**: Accurate distance calculations using Haversine formula
- 📱 **Geolocation Support**: Automatic location detection via browser GPS or manual coordinate entry
- 🎨 **Responsive UI**: Clean, modern interface that works on desktop and mobile
- ⚡ **Fast API**: FastAPI backend with asynchronous request handling
- � **User Database**: 15 sample users across the NYC area for demonstration

## Project Structure

```
myproject/
├── app/
│   ├── main.py                   # FastAPI entry point
│   ├── routes/
│   │   └── map_routes.py         # API endpoints for user discovery
│   ├── services/
│   │   └── user_service.py       # User discovery logic
│   ├── data/
│   │   └── users_db.py           # Sample user database
│   ├── templates/
│   │   └── index.html            # Frontend HTML
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         # Styling
│   │   └── js/
│   │       └── map.js            # Frontend JavaScript
│   └── utils/
│       └── helpers.py            # Utility functions (distance calculation, validation)
├── requirements.txt              # Python dependencies
└── README.md                      # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd myproject
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Server

Start the FastAPI development server with hot reload:

```bash
uvicorn app.main:app --reload
```

The application will be available at:
- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Server

For production deployment:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Usage

1. **Open the web application**:
   - Navigate to http://localhost:8000 in your browser

2. **Enter coordinates**:
   - **Origin Latitude**: Starting point latitude
   - **Origin Longitude**: Starting point longitude
   - **Destination Latitude**: End point latitude
   - **Destination Longitude**: End point longitude

3. **Click "Find Route"**:
   - The map will display the route with markers
   - Distance (km) and duration (minutes) will be shown
   - Map will automatically zoom to fit the route

### Example Coordinates

- **New York Central**: Lat: 40.7128, Lon: -74.0060
- **New York Times Square**: Lat: 40.7580, Lon: -73.9855
- **London Big Ben**: Lat: 51.4975, Lon: -0.1245

## API Endpoints

### Get Route

```
GET /api/osm/route?origin_lat=40.7128&origin_lon=-74.0060&destination_lat=40.7614&destination_lon=-73.9776
```

**Parameters**:
- `origin_lat` (float): Origin latitude (-90 to 90)
- `origin_lon` (float): Origin longitude (-180 to 180)
- `destination_lat` (float): Destination latitude (-90 to 90)
- `destination_lon` (float): Destination longitude (-180 to 180)

**Response**:
```json
{
  "distance_km": 5.23,
  "duration_minutes": 12,
  "geometry": {
    "type": "LineString",
    "coordinates": [[lon, lat], ...]
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

### Health Check

```
GET /health
```

Response:
```json
{
  "status": "ok",
  "message": "OSM Route Finder is running"
}
```

### API Info

```
GET /api/info
```

## Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI web server
- **Requests**: HTTP library for external API calls
- **Jinja2**: Template engine

### Frontend
- **Leaflet.js**: Interactive map library
- **OpenStreetMap**: Free map tiles
- **HTML5**: Markup
- **CSS3**: Styling
- **Vanilla JavaScript**: Frontend logic

### External Services
- **OSRM (Open Source Routing Machine)**: Route calculation
  - API: http://router.project-osrm.org/route/v1/driving/

## File Descriptions

### Backend Files

- **main.py**: FastAPI application setup, routes mounting, static file serving
- **map_routes.py**: API endpoint for route calculation
- **osm_service.py**: OSRM API integration and coordinate validation
- **helpers.py**: Utility functions for distance/duration conversion

### Frontend Files

- **index.html**: Main HTML structure with form and map container
- **style.css**: Responsive styling for sidebar and map
- **map.js**: Leaflet map initialization, route display, API communication

## Features Explained

### Route Finding
1. User enters origin and destination coordinates
2. Frontend sends request to `/api/osm/route` endpoint
3. Backend queries OSRM API for optimal route
4. Route geometry is returned as GeoJSON
5. Frontend displays route on map with markers

### Map Visualization
- Green circle: Origin point
- Red circle: Destination point
- Blue line: Route path
- Auto-fit to route bounds

### Error Handling
- Input validation for coordinates
- OSRM API error handling
- Network timeout management
- User-friendly error messages

## Customization

### Change Default Coordinates
Edit the `value` attributes in `app/templates/index.html`:
```html
<input value="40.7128" ...>  <!-- Origin Lat -->
<input value="-74.0060" ...> <!-- Origin Lon -->
```

### Change Map Style
OSRM provides multiple routing profiles:
- `driving` (default)
- `walking`
- `cycling`

Modify in `app/services/osm_service.py`:
```python
OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"
```

### Add More Routes
Create new route functions in `app/routes/map_routes.py`

## Troubleshooting

### OSRM API Unavailable
- The public OSRM service may be temporarily down
- Consider using a private OSRM instance
- Modify `OSRM_BASE_URL` in `osm_service.py`

### Map Not Loading
- Check browser console for JavaScript errors
- Ensure Leaflet CDN is accessible
- Verify static files are properly served

### Port Already in Use
Use a different port:
```bash
uvicorn app.main:app --port 8001 --reload
```

## Performance

- **Route Calculation**: ~200-500ms (depends on distance and OSRM server)
- **Map Rendering**: <100ms for typical routes
- **Frontend Load**: <1s (with CDN resources)

## Security Considerations

- CORS enabled for all origins (configure for production)
- Input validation on coordinates
- Error messages don't expose sensitive information
- No database or authentication required for this version

## Future Enhancements

- Multiple waypoint support
- Alternative route suggestions
- Real-time traffic data
- Reverse geocoding (address lookup)
- Route optimization algorithms
- User authentication
- Database for saved routes
- Mobile app integration

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Support

For issues or questions, refer to:
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Leaflet Documentation: https://leafletjs.com/
- OSRM Documentation: http://project-osrm.org/docs/v5.5.1/api/

## Contributing

Feel free to fork, modify, and improve this project!

---

**Created**: 2025
**Version**: 1.0.0
