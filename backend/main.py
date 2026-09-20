"""FastAPI Main Application Entry Point.

Owner: Moksh [M]
Role: Core Infra & Integration Point
"""

import sys
from pathlib import Path

# Ensure backend directory is in sys.path for versatile startup
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
for p in [str(BACKEND_DIR), str(PROJECT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException

try:
    from backend.config import APP_TITLE, APP_VERSION, ALLOWED_ORIGINS
    from backend.api.routes_layers import router as layers_router
    from backend.api.routes_score import router as score_router
except ImportError:
    from config import APP_TITLE, APP_VERSION, ALLOWED_ORIGINS
    from api.routes_layers import router as layers_router
    from api.routes_score import router as score_router

OPENAPI_TAGS = [
    {"name": "Health", "description": "Service heartbeat and diagnostic telemetry."},
    {"name": "Scoring", "description": "Composite MCDA site readiness evaluation across 6 industry archetypes (EV, Retail, Warehouse, Telecom, Solar, Wind)."},
    {"name": "Comparison", "description": "Multi-candidate side-by-side benchmark comparison and ranking matrix."},
    {"name": "Layers", "description": "GeoJSON spatial layer catalogue and registry for Gujarat."},
    {"name": "Spatial", "description": "Getis-Ord Gi* hotspots, DBSCAN POI clustering, and Uber H3 hexagonal binning."},
    {"name": "Accessibility", "description": "Multi-modal travel-time isochrones and demographic/competitor catchment envelopes."},
    {"name": "Reports", "description": "Comprehensive site readiness dossier generation and schema export."},
    {"name": "Search", "description": "Gujarat place autocompletion and GPS geocoding."},
    {"name": "Wind Resource", "description": "Gujarat NIWE/VORTEX 120m wind atlas telemetry and prime corridor analytics."},
]

app = FastAPI(
    title="GeoVista — GeoSpatial Site Readiness Analyzer",
    version=APP_VERSION,
    description=(
        "## AI-Powered GeoSpatial Site Readiness Platform for Gujarat, India\n\n"
        "GeoVista delivers real-time multicriteria decision analysis (MCDA), spatial clustering, "
        "travel-time accessibility catchments, and specialized energy/infrastructure models "
        "across Gujarat's industrial, commercial, and renewable corridors.\n\n"
        "### Key Capabilities\n"
        "- **6 Differentiated Archetypes**: EV Fast-Charging, Retail, Industrial Warehouse, 5G Telecom, Solar Utility, and Wind Turbine.\n"
        "- **Advanced Spatial Algorithms**: Getis-Ord Gi* hotspot analysis, DBSCAN density clustering, and Uber H3 hexagonal aggregation.\n"
        "- **Accessibility Envelopes**: Isochrone travel contours and demographic population reach across progressive time horizons.\n"
        "- **Dossier Generation**: Exportable and printable executive audit reports with GeoJSON geometries and CSV tables."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=OPENAPI_TAGS,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.exceptions import RequestValidationError, HTTPException as FastAPIHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

# Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters provided.",
                "details": exc.errors(),
            }
        },
    )

@app.exception_handler(FastAPIHTTPException)
async def fastapi_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
            }
        },
    )

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
            }
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred while processing the geospatial query.",
                "details": str(exc),
            }
        },
    )

# Core Phase 1 Routers
app.include_router(layers_router, prefix="/api")
app.include_router(score_router, prefix="/api")

# Conditionally mount future sprint routers as teammates complete them
try:
    from backend.api.routes_hotspot import router as hotspot_router
    app.include_router(hotspot_router, prefix="/api", tags=["Spatial"])
except ImportError:
    try:
        from api.routes_hotspot import router as hotspot_router
        app.include_router(hotspot_router, prefix="/api", tags=["Spatial"])
    except ImportError:
        pass

try:
    from backend.api.routes_isochrone import router as isochrone_router
    app.include_router(isochrone_router, prefix="/api", tags=["Accessibility"])
except ImportError:
    try:
        from api.routes_isochrone import router as isochrone_router
        app.include_router(isochrone_router, prefix="/api", tags=["Accessibility"])
    except ImportError:
        pass

try:
    from backend.api.routes_report import router as report_router
    app.include_router(report_router, prefix="/api", tags=["Reports"])
except ImportError:
    try:
        from api.routes_report import router as report_router
        app.include_router(report_router, prefix="/api", tags=["Reports"])
    except ImportError:
        pass

try:
    from backend.api.routes_compare import router as compare_router
    app.include_router(compare_router, prefix="/api", tags=["Comparison"])
except ImportError:
    pass

try:
    from backend.api.routes_search import router as search_router
    app.include_router(search_router, prefix="/api", tags=["Search"])
except ImportError:
    try:
        from api.routes_search import router as search_router
        app.include_router(search_router, prefix="/api", tags=["Search"])
    except ImportError:
        pass

try:
    from backend.api.routes_wind import router as wind_router
    app.include_router(wind_router, prefix="/api", tags=["Wind Resource"])
except ImportError:
    try:
        from api.routes_wind import router as wind_router
        app.include_router(wind_router, prefix="/api", tags=["Wind Resource"])
    except ImportError:
        pass



@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint for container orchestrators and status monitoring."""
    return {
        "status": "ok",
        "data": {
            "version": APP_VERSION,
            "status": "healthy",
            "service": "GeoSpatial Site Readiness Analyzer Backend"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
