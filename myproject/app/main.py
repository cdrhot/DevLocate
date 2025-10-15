"""
FastAPI Main Application
Serves frontend and API endpoints for finding K nearest people
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Import routes
from app.routes.map_routes import router as map_router

# Create FastAPI app
app = FastAPI(
    title="DevLocate",
    description="FastAPI application for finding K nearest people near you using OpenStreetMap",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static files
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routes
app.include_router(map_router)


@app.get("/")
async def root():
    """
    Serve the main HTML page
    """
    templates_dir = BASE_DIR / "templates"
    index_path = templates_dir / "index.html"
    
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    else:
        return {"error": "index.html not found"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "OSM Route Finder is running"}


@app.get("/api/info")
async def api_info():
    """
    API information endpoint
    """
    return {
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


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
