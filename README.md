# 👥 DevLocate

Find K nearest people near you using OpenStreetMap.

## Quick Start

### 1. Set Up Virtual Environment (Recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App

**With Virtual Environment**:
```bash
# Windows
.venv\Scripts\uvicorn main:app --reload --port 8000

# Linux/Mac
.venv/bin/uvicorn main:app --reload --port 8000
```

**Without Virtual Environment**:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Open Browser
```
http://localhost:8000
```

## How to Use

1. **Enter your coordinates** or click "📍 Use My Location"
2. **Set K value** (number of people to find, 1-15)
3. **Click "Find Nearby Users"**
4. **View results** on the map
5. **Click any user** to see the route to them

## Features

✅ Find K nearest people  
✅ Interactive map with Leaflet.js  
✅ Click users to see route  
✅ Geolocation support  
✅ Distance calculation (Haversine formula)  
✅ Beautiful responsive UI  
✅ OSRM routing integration  

## Project Structure

```
DevLocate/
├── main.py              # All backend logic
├── static/              # CSS and JavaScript
│   ├── css/style.css
│   └── js/map.js
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## Technologies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Leaflet.js** - Interactive maps
- **OpenStreetMap** - Map tiles
- **OSRM** - Routing
- **Haversine** - Distance calculation

## API Endpoints

- `GET /` - Main page
- `GET /api/users/nearby?latitude=X&longitude=Y&k=5` - Get K nearest users
- `GET /api/users/all` - Get all users
- `GET /api/osm/route?origin_lat=X&origin_lon=Y&destination_lat=X&destination_lon=Y` - Get route

## Demo Data

15 sample users in NYC area for testing.

## License

MIT License

That's it! Simple, clean, efficient. 🚀
