# GeoVista — Location Intelligence & Site Readiness Platform

<p align="center">
  <img src="https://img.shields.io/badge/Release-v2.0.0-0ea5e9?style=for-the-badge&logo=compass&logoColor=white" alt="Version 2.0" />
  <img src="https://img.shields.io/badge/Python-3.11-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-18.3-61dafb?style=for-the-badge&logo=react&logoColor=black" alt="React 18" />
  <img src="https://img.shields.io/badge/TypeScript-5.4-3178c6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/MapLibre_GL-3.6-3b82f6?style=for-the-badge&logo=maplibre&logoColor=white" alt="MapLibre GL" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

---

## 📌 Executive Overview

**GeoVista** is an AI-assisted geospatial location intelligence and site readiness analytics platform purpose-built for multi-criteria infrastructure site selection across Gujarat, India.

By synthesizing multi-layer geospatial data—census demographics across all 33 Gujarat districts, arterial logistics networks, commercial point-of-interest (POI) clusters, municipal land-use parcels, flood hazard zones, and renewable resource maps—GeoVista enables urban planners, infrastructure funds, and commercial developers to evaluate candidate locations in milliseconds.

---

## 🌟 Key Capabilities

### 1. Differentiated Multi-Criteria Decision Analysis (MCDA)
Unlike generic GIS tools that score every facility using identical criteria, GeoVista provides **6 distinct, research-backed spatial rule engines**:
- **EV Fast-Charging Stations**: Income-weighted EV adoption density, dwell-time anchors (malls, tech parks, highway fuel stops), and strict arterial proximity thresholds.
- **Retail & Commercial High-Street**: Positive footfall catchment (50,000+ population reach within a 2 km trade area), commercial zoning enforcement, and co-tenancy clustering.
- **Industrial Warehouse & Logistics**: Inverted demographic scoring (penalizes high-cost congested urban centers; rewards scalable peripheral parcels), multi-modal highway corridor access, and elevated flood risk penalties ($1.5\times$ multiplier).
- **5G Telecom Towers**: Subscriber density coverage demand, municipal rooftop/greenfield zoning compliance, and SRTM DEM elevation line-of-sight propagation heuristics.
- **Utility-Scale Solar PV**: Inverted settlement buffer ($>4\text{ km}$ buffer from dense habitations), Global Horizontal Irradiance (GHI) estimation ($5.0 - 6.4\text{ kWh/m}^2/\text{day}$), and non-agricultural wasteland prioritization.
- **Wind Turbines**: Habitation buffer compliance (Gujarat High Court $500\text{ m}+$ exclusion), logistics turning radius evaluation, and NIWE 120m hub-height wind speed modeling ($4.0 - 8.4\text{ m/s}$).

### 2. Advanced Spatial Algorithms
- **Getis-Ord $G_i^*$ Hotspot Detection**: Identifies statistically significant spatial clusters of high/low values with $90\%$, $95\%$, and $99\%$ confidence intervals ($z$-scores and $p$-values).
- **DBSCAN Density-Based Clustering**: Detects spatial competitor agglomerations and co-tenancy hubs while filtering out geographic noise.
- **Uber H3 Hexagonal Binning**: Multi-resolution spatial aggregation across H3 resolutions 4 through 9 for uniform territory analysis.
- **Multi-Modal Isochrones**: 5, 10, 15, and 30-minute travel-time envelopes for driving, cycling, and walking with zero-latency fallback geometry.
- **VORTEX Wind Resource Surface**: Real-time continuous 120m wind speed surface across Gujarat with interactive coastal corridor benchmarks.
- **Hard Limiting Constraints**: Instant zero-score disqualification for sites intersecting rivers, lakes, canals, or protected wetlands.

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                            │
│  React 18  •  TypeScript  •  Vite  •  MapLibre GL JS  •  TailwindCSS    │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────┐  │
│  │   MapWorkspace   │  │  ScoreBreakdown  │  │  Isochrone & Catchment│  │
│  │  (MapLibre GL)   │  │  (Radar Charts)  │  │   (Travel Contours)   │  │
│  └──────────────────┘  └──────────────────┘  └───────────────────────┘  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────┐  │
│  │  DrawROI Toolbar │  │ WindCorridors HUD│  │ CompareMatrix Modal   │  │
│  │  (Snipping Tool) │  │ (VORTEX Atlas)   │  │ (Multi-Site Ranking)  │  │
│  └──────────────────┘  └──────────────────┘  └───────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ HTTP REST / JSON (Port 8000)
┌────────────────────────────────────▼────────────────────────────────────┐
│                           APPLICATION GATEWAY                           │
│  FastAPI (Python 3.11)  •  Uvicorn  •  Pydantic v2  •  OpenAPI 3.1      │
│                                                                         │
│  /api/score         /api/compare       /api/hotspots    /api/clusters   │
│  /api/isochrones    /api/catchment     /api/wind/atlas  /api/search     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                         ANALYTIC COMPUTE ENGINES                        │
│                                                                         │
│  ┌─────────────────────────┐  ┌──────────────────────────────────────┐  │
│  │  SiteReadinessScorer    │  │  Spatial Statistics Engine           │  │
│  │  • 6 Archetype Profiles │  │  • Getis-Ord Gi* (libpysal/esda)     │  │
│  │  • Gaussian Decay       │  │  • DBSCAN Clustering (scikit-learn)  │  │
│  │  • Limiting Constraints │  │  • Uber H3 Hex Binning (h3-py)       │  │
│  └─────────────────────────┘  └──────────────────────────────────────┘  │
│  ┌─────────────────────────┐  ┌──────────────────────────────────────┐  │
│  │  Wind & Solar Modeling  │  │  Accessibility Engine                │  │
│  │  • NIWE 120m Wind Atlas │  │  • Isochrone Generation              │  │
│  │  • GHI Solar Irradiance │  │  • Demographic Catchment Aggregation │  │
│  └─────────────────────────┘  └──────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                           GEOSPATIAL DATA STORE                         │
│                                                                         │
│   demographics.geojson        poi.geojson          landuse.geojson      │
│   transportation.geojson      environment.geojson  water_bodies.geojson │
│   gujarat_boundary.geojson    gazetteer.json (0ms offline search)       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Archetype Rule Matrix

| Archetype | Primary Factor | Demographic Polarity | Road Buffer Threshold | Environmental / Flood Rules |
| :--- | :--- | :--- | :--- | :--- |
| **EV Charging** | Transportation ($35\%$) | **Positive** (Income-weighted) | $\le 1.5\text{ km}$ (Highway corridor) | Standard flood & water exclusion |
| **Retail Store** | Demographics ($35\%$) | **Positive** ($50\text{k}+$ catchment) | $\le 2.0\text{ km}$ (Pedestrian/vehicle) | Commercial zoning strictly enforced |
| **Warehouse** | Transportation ($40\%$) | **Inverted** (Penalizes urban core) | $\le 8.0\text{ km}$ (Freight arterial) | $1.5\times$ flood inventory penalty multiplier |
| **Telecom Tower** | Demographics ($30\%$) | **Positive** (Subscriber reach) | $\le 15.0\text{ km}$ (Maintenance road) | Elevation LoS heuristic ($0.8\times$ flood impact) |
| **Solar Farm** | Solar GHI ($40\%$) | **Inverted** ($>4\text{ km}$ rural buffer) | $\le 12.0\text{ km}$ (Grid evacuation) | GHI model ($5.0 - 6.4\text{ kWh/m}^2/\text{day}$) |
| **Wind Turbine** | Wind Resource ($35\%$) | **Inverted** (Habitation buffer) | $\le 15.0\text{ km}$ (Heavy haul access) | NIWE 120m speed model ($4.0 - 8.4\text{ m/s}$) |

---

## ⚡ API Specification

Interactive Swagger UI documentation is available at `http://localhost:8000/docs`.

| Method | Endpoint | Description | Key Parameters |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/score` | Compute composite readiness score (0–100) & grade | `lat`, `lng`, `site_type`, `weights` |
| `POST` | `/api/score/breakdown` | Comprehensive 5-layer score & factor contributions | `lat`, `lng`, `site_type`, `weights` |
| `POST` | `/api/compare` | Rank & compare candidate locations side-by-side | `sites: [{lat, lng, label}]`, `site_type` |
| `GET` | `/api/hotspots` | Getis-Ord $G_i^*$ spatial hot/cold spot analysis | `layer`, `distance_threshold` |
| `GET` | `/api/clusters` | DBSCAN density-based POI cluster geometries | `eps_meters`, `min_samples` |
| `GET` | `/api/h3` | Uber H3 hexagonal aggregation grid | `resolution` (4–9), `metric` |
| `GET` | `/api/isochrones` | Multi-modal travel-time accessibility polygon | `lat`, `lng`, `minutes`, `mode` |
| `POST` | `/api/catchment` | Progressive population reach within travel bands | `lat`, `lng`, `minutes: [5, 10, 15, 30]` |
| `GET` | `/api/wind/atlas` | Continuous 120m wind speed surface GeoJSON | None |
| `GET` | `/api/wind/prime-spots` | High-yield renewable wind corridor benchmarks | None |
| `GET` | `/api/search/autocomplete` | Gujarat geocoding with 0ms gazetteer + OSM Photon | `q`, `limit` |
| `POST` | `/api/report/export` | Generate comprehensive executive dossier | `site_data`, `format: ["json", "csv", "geojson"]` |
| `GET` | `/api/report/schema` | JSON Schema specification for audit dossiers | None |
| `GET` | `/api/health` | Service uptime and system health verification | None |

---

## 🚀 Quick Start

### Prerequisites
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) (recommended)
- *Alternatively:* Node.js 18+ and Python 3.10+

### Option A: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/MokshUpadhyay194/GeoSpatial_Site_BitNBuild.git
cd GeoSpatial_Site_BitNBuild/project

# Build and start all services
docker compose up --build
```

Services will be live at:
- **Frontend Workspace**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`

---

### Option B: Local Bare-Metal Setup

```bash
# 1. Start the FastAPI Backend
cd project/backend
python -m venv venv
# Windows: venv\Scripts\activate | Unix: source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 2. In a second terminal, start the React Frontend
cd project/frontend
npm install
npm run dev
```

---

## 📁 Repository Structure

```
project/
├── backend/
│   ├── main.py                       # FastAPI application entry & global error handlers
│   ├── config.py                     # Environment variables & runtime constants
│   ├── scoring/
│   │   ├── engine.py                 # Core evaluation engine & archetype dispatchers
│   │   ├── weights.py                # Specialized archetype weight profiles
│   │   ├── constraints.py            # Water-body disqualification & road thresholds
│   │   └── decay.py                  # Gaussian and inverse distance attenuation functions
│   ├── spatial/
│   │   ├── hotspot.py                # Getis-Ord Gi* hot/cold spot implementation
│   │   ├── clustering.py             # DBSCAN spatial point clustering
│   │   ├── h3_binning.py             # Uber H3 hexagonal aggregation
│   │   └── wind_resource.py          # NIWE 120m hub-height wind atlas interpolation
│   ├── accessibility/
│   │   ├── isochrone.py              # Travel-time contour geometry generator
│   │   └── catchment.py              # Multi-tier population & competitor reach aggregator
│   ├── utils/
│   │   ├── geo_helpers.py            # Haversine distance & ray-casting point-in-polygon
│   │   └── validators.py             # Pydantic request models & parameter validation
│   └── api/
│       ├── routes_score.py           # Site readiness scoring & factor breakdowns
│       ├── routes_compare.py         # Multi-site comparison & matrix ranking
│       ├── routes_hotspot.py         # Hotspot statistical endpoints
│       ├── routes_isochrone.py       # Travel contour & catchment endpoints
│       ├── routes_wind.py            # Wind atlas surface & prime corridor benchmarks
│       ├── routes_search.py          # Hybrid gazetteer + Photon geocoding
│       └── routes_report.py          # Executive dossier exports (JSON, GeoJSON, CSV)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MapView.tsx           # MapLibre GL WebGL map & layer management
│   │   │   ├── Header.tsx            # GeoVista navigation & archetype selector
│   │   │   ├── SearchBar.tsx         # Real-time search with keyboard navigation
│   │   │   ├── ScorePanel.tsx        # Animated readiness score counter & grade badge
│   │   │   ├── BreakdownChart.tsx    # Recharts radar & linear factor breakdowns
│   │   │   ├── ComparePanel.tsx      # Multi-candidate comparison matrix
│   │   │   ├── IsochronePanel.tsx    # Catchment KPI metrics & travel-mode controls
│   │   │   ├── DrawToolbar.tsx       # Snipping tool (freeform polygon & rectangle ROI)
│   │   │   ├── WindPrimeSpotsBar.tsx # Pulsing prime wind corridor selector
│   │   │   └── WindLegend.tsx        # VORTEX wind speed color ramp HUD
│   │   ├── hooks/
│   │   │   ├── useSpatialAnalytics.ts# H3, DBSCAN, and Gi* data fetching
│   │   │   ├── useIsochrone.ts       # 0ms synchronous isochrone render hook
│   │   │   └── useWindAtlas.ts       # Continuous wind surface layer hook
│   │   └── routes/
│   │       ├── MapWorkspace.tsx      # Primary intelligence workspace layout
│   │       ├── Compare.tsx           # Full-page candidate comparison
│   │       └── Reports.tsx           # Executive dossier viewer & PDF export
│   ├── vite.config.ts                # Vite dev server configuration & API proxies
│   └── tailwind.config.js            # Custom design tokens & dark mode color palettes
│
├── data/                             # Curated Gujarat GeoJSON feature collections
│   ├── demographics.geojson          # Population density nodes & income indicators
│   ├── poi.geojson                   # Commercial anchors, fuel hubs, and competitors
│   ├── landuse.geojson               # Municipal zoning parcels
│   ├── transportation.geojson        # Arterial logistics highways & transport lines
│   ├── water_bodies.geojson          # Disqualification water bodies (rivers, lakes, wetlands)
│   └── environment.geojson           # Flood risk polygons
│
├── docker/
│   ├── backend.Dockerfile            # Python 3.11 slim container
│   └── frontend.Dockerfile           # Node.js alpine multi-stage build
└── docker-compose.yml                # Coordinated multi-container orchestration
```

---

## 👥 Engineering Team

| Contributor | Area of Ownership |
| :--- | :--- |
| **Moksh [M]** | Core Evaluation Architecture, Scoring Dispatcher, Comparison APIs, ScorePanel UI |
| **Daksh [D]** | MapLibre GL Implementation, Spatial Algorithms (DBSCAN, Gi*, H3), DrawToolbar, Docker DevOps |
| **Maharshi [R]** | Data Engineering, Isochrone Catchment Models, Executive Dossier Generation, Swagger Specifications |

---

## 📄 License

Internal Hackathon Project — **BitNBuild 2026**. Distributed under the [MIT License](LICENSE).
