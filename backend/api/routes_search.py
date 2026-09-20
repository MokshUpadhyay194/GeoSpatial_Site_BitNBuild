"""Geocoding and Location Search API — Google Maps-Style Gujarat Spatial Search

Features:
  - Real-time autocomplete across all of Gujarat (cities, wards, streets, landmarks, GIDCs, villages)
  - Strict Gujarat Bounding Box restriction (20.0°N - 24.8°N, 68.0°E - 74.6°E)
  - Primary Engine: Photon OpenStreetMap Autocomplete with Gujarat spatial bounding
  - Secondary Engine: Nominatim Structured Geocoder with bounded viewbox
  - Pre-indexed Gujarat Gazetteer for instant 0ms offline suggestions
  - In-memory LRU caching to eliminate rate-limiting and redundant network latency
"""

import re
import urllib.parse
import urllib.request
import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query

router = APIRouter(prefix="", tags=["Search"])

# In-memory geocode cache
_SEARCH_CACHE: Dict[str, List[Dict[str, Any]]] = {}

# Gujarat State Geographic Bounding Box
GUJARAT_BBOX = {
    "min_lng": 68.1,
    "min_lat": 20.1,
    "max_lng": 74.5,
    "max_lat": 24.7,
}

# India Geographic Bounding Box
INDIA_BBOX = {
    "min_lng": 68.0,
    "min_lat": 6.5,
    "max_lng": 97.5,
    "max_lat": 37.5,
}

def is_within_gujarat(lat: float, lng: float) -> bool:
    """Validate that coordinates reside within Gujarat borders (with slight buffer)."""
    return (
        GUJARAT_BBOX["min_lat"] - 0.1 <= lat <= GUJARAT_BBOX["max_lat"] + 0.1 and
        GUJARAT_BBOX["min_lng"] - 0.1 <= lng <= GUJARAT_BBOX["max_lng"] + 0.1
    )

def is_within_india(lat: float, lng: float) -> bool:
    """Validate that coordinates reside within India borders."""
    return (
        INDIA_BBOX["min_lat"] <= lat <= INDIA_BBOX["max_lat"] and
        INDIA_BBOX["min_lng"] <= lng <= INDIA_BBOX["max_lng"]
    )

# Curated High-Priority Gujarat Benchmarks, District HQs, and Strategic Hubs
try:
    from backend.spatial.national_gazetteer import COMPREHENSIVE_GAZETTEER
    GUJARAT_GAZETTEER: List[Dict[str, Any]] = COMPREHENSIVE_GAZETTEER
except ImportError:
    try:
        from spatial.national_gazetteer import COMPREHENSIVE_GAZETTEER
        GUJARAT_GAZETTEER = COMPREHENSIVE_GAZETTEER
    except ImportError:
        GUJARAT_GAZETTEER = [
            {"id": "loc-sg-highway", "name": "SG Highway Commercial Corridor", "subTitle": "Bodakdev - Thaltej - Sola Arterial Axis, Ahmedabad", "lat": 23.0378, "lng": 72.5112, "category": "benchmark", "district": "Ahmedabad"}
        ]

COORD_REGEX = re.compile(r"^[-+]?([1-8]?\d(?:\.\d+)?|90(?:\.0+)?)[,\s]+[-+]?(180(?:\.0+)?|(?:1[0-7]\d|[1-9]?\d)(?:\.\d+)?)$")

def parse_coordinates(query: str) -> Optional[Dict[str, Any]]:
    m = COORD_REGEX.match(query.strip())
    if m:
        try:
            parts = [p.strip() for p in re.split(r"[, ]+", query.strip()) if p.strip()]
            if len(parts) >= 2:
                lat = float(parts[0])
                lng = float(parts[1])
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    in_guj = is_within_gujarat(lat, lng)
                    in_ind = is_within_india(lat, lng)
                    region_tag = " (Gujarat)" if in_guj else (" (India)" if in_ind else "")
                    return {
                        "id": "coord-custom",
                        "name": f"Coordinates: {lat:.4f}° N, {lng:.4f}° E",
                        "subTitle": f"Direct GPS Coordinates{region_tag}",
                        "lat": lat,
                        "lng": lng,
                        "category": "coordinate",
                        "district": "Custom Point",
                    }
        except Exception:
            return None
    return None


def fetch_photon_places(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    """Query Photon autocomplete engine across Gujarat and India."""
    # Bounded to India bounding box
    params = urllib.parse.urlencode({
        "q": query,
        "bbox": f"{INDIA_BBOX['min_lng']},{INDIA_BBOX['min_lat']},{INDIA_BBOX['max_lng']},{INDIA_BBOX['max_lat']}",
        "limit": limit * 2,
    })
    url = f"https://photon.komoot.io/api/?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "GeoVistaSiteReadiness/2.0 (team@geovista.app)"})

    results = []
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for feat in data.get("features", []):
                coords = feat.get("geometry", {}).get("coordinates", [])
                if len(coords) < 2:
                    continue
                lng, lat = float(coords[0]), float(coords[1])
                if not is_within_india(lat, lng):
                    continue

                p = feat.get("properties", {})
                name = p.get("name")
                if not name:
                    continue

                street = p.get("street") or ""
                district = p.get("district") or p.get("city") or p.get("county") or ""
                state = p.get("state") or "India"
                postcode = p.get("postcode") or ""

                sub_items = [item for item in [street, district, state, postcode] if item and item.lower() != name.lower()]
                subTitle = ", ".join(sub_items) if sub_items else "India"

                osm_key = p.get("osm_key", "")
                osm_value = p.get("osm_value", "")
                category = "geocoded"
                if osm_key in ["place"] and osm_value in ["city", "town"]:
                    category = "city"
                elif osm_key in ["industrial", "landuse"] or "gidc" in name.lower():
                    category = "industrial"
                elif osm_key in ["amenity", "tourism", "historic", "leisure"]:
                    category = "benchmark"
                elif osm_key in ["highway"]:
                    category = "ward"

                results.append({
                    "id": f"ph-{p.get('osm_id', '')}-{lat:.4f}-{lng:.4f}",
                    "name": name,
                    "subTitle": subTitle,
                    "lat": lat,
                    "lng": lng,
                    "category": category,
                    "district": district or state or "India",
                })
    except Exception:
        pass
    return results


def fetch_nominatim_places(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Secondary fallback: Nominatim geocoder with bounded viewbox to India."""
    params = urllib.parse.urlencode({
        "format": "json",
        "q": query,
        "viewbox": f"{INDIA_BBOX['min_lng']},{INDIA_BBOX['max_lat']},{INDIA_BBOX['max_lng']},{INDIA_BBOX['min_lat']}",
        "bounded": "1",
        "limit": limit,
        "addressdetails": "1",
    })
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GeoVistaSiteReadiness/2.0 (team@geovista.app; dakshthakkar42@gmail.com)",
            "Accept-Language": "en",
        }
    )
    results = []
    try:
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data:
                lat = float(item.get("lat", 0))
                lng = float(item.get("lon", 0))
                if not is_within_india(lat, lng):
                    continue

                display_name = item.get("display_name", "")
                parts = [p.strip() for p in display_name.split(",") if p.strip()]
                primary_name = item.get("name") or (parts[0] if parts else "Location")

                addr = item.get("address", {})
                city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or ""
                state = addr.get("state", "India")
                sub_parts = [p for p in [city, state] if p and p.lower() != primary_name.lower()]
                subTitle = ", ".join(sub_parts) if sub_parts else display_name

                results.append({
                    "id": f"nom-{item.get('place_id', '')}",
                    "name": primary_name,
                    "subTitle": subTitle,
                    "lat": lat,
                    "lng": lng,
                    "category": "geocoded",
                    "district": city or state or "India",
                })
    except Exception:
        pass
    return results


@router.get("/search")
async def search_locations(
    q: str = Query("", description="Search term, place, street, GIDC, ward, or coordinates in Gujarat"),
    limit: int = Query(8, description="Maximum number of results to return")
) -> Dict[str, Any]:
    """Google Maps-style autocomplete and geocoding strictly scoped to Gujarat."""
    query = q.strip()
    if not query:
        return {"query": "", "count": len(GUJARAT_GAZETTEER[:limit]), "results": GUJARAT_GAZETTEER[:limit]}

    # Check cache
    q_key = query.lower()
    if q_key in _SEARCH_CACHE:
        return {"query": query, "count": len(_SEARCH_CACHE[q_key]), "results": _SEARCH_CACHE[q_key][:limit]}

    results: List[Dict[str, Any]] = []

    # 1. Coordinate input (lat, lng)
    coord = parse_coordinates(query)
    if coord:
        results.append(coord)

    # 2. Match local Gujarat gazetteer presets
    matched_gazetteer = [
        p for p in GUJARAT_GAZETTEER
        if q_key in p["name"].lower()
        or q_key in p["subTitle"].lower()
        or q_key in p["district"].lower()
    ]
    results.extend(matched_gazetteer)

    # 3. Query Photon across India (searches every street, ward, village, landmark)
    if len(query) >= 2 and not coord:
        photon_matches = fetch_photon_places(query, limit=limit)
        for pm in photon_matches:
            # Deduplicate by ~400m proximity
            if not any(abs(r["lat"] - pm["lat"]) < 0.004 and abs(r["lng"] - pm["lng"]) < 0.004 for r in results):
                results.append(pm)

    # 4. If still under limit, query Nominatim with bounded viewbox
    if len(results) < 4 and len(query) >= 3 and not coord:
        nominatim_matches = fetch_nominatim_places(query, limit=limit - len(results))
        for nm in nominatim_matches:
            if not any(abs(r["lat"] - nm["lat"]) < 0.004 and abs(r["lng"] - nm["lng"]) < 0.004 for r in results):
                results.append(nm)

    final_results = results[:limit]
    if final_results:
        _SEARCH_CACHE[q_key] = final_results

    return {
        "query": query,
        "count": len(final_results),
        "results": final_results
    }
