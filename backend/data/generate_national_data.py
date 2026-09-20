"""Nationwide and All-Gujarat GeoJSON Data Layer Generator.

Generates calibrated, schema-compliant GeoJSON datasets for:
  - data/demographics.geojson
  - data/transportation.geojson
  - data/poi.geojson
  - data/landuse.geojson
  - data/environment.geojson
"""

import math
import random
import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.spatial.india_spatial import ALL_SETTLEMENTS, NATIONAL_HIGHWAY_CORRIDORS

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

random.seed(42)

def generate_national_demographics():
    features = []
    
    for s in ALL_SETTLEMENTS:
        c_lat, c_lng = s["lat"], s["lng"]
        radius = s["radius_km"]
        pop = s["pop"]
        density = s["density"]
        
        # 1. Core Centroid
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [round(c_lng, 5), round(c_lat, 5)]},
            "properties": {
                "name": f"{s['name']} Central Core",
                "population": int(pop * 0.12),
                "density_per_sq_km": round(density * 1.15, 1),
                "city": s["name"],
                "district": s["district"],
                "income_index": 0.85 if s["income"] == "high" else (0.65 if s["income"] == "medium" else 0.45),
                "value": round(0.85 + random.uniform(0, 0.12), 2),
            }
        })
        
        # 2. Distributed Sectors & Wards across the settlement radius
        points_count = 20 if s["tier"] == 1 else (14 if s["tier"] == 2 else 8)
        for i in range(points_count):
            angle = random.uniform(0, 2 * math.pi)
            dist_km = random.triangular(0.8, radius, radius * 0.4)
            p_lat = c_lat + dist_km * math.cos(angle) / 111.0
            p_lng = c_lng + dist_km * math.sin(angle) / (111.0 * math.cos(math.radians(c_lat)))
            
            factor = max(0.12, 1.0 - (dist_km / radius))
            sub_pop = int((pop / 150.0) * factor * random.uniform(0.75, 1.35))
            sub_density = round(max(350.0, density * factor * random.uniform(0.8, 1.2)), 1)
            
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(p_lng, 5), round(p_lat, 5)]},
                "properties": {
                    "name": f"{s['name']} Ward {i + 1}",
                    "population": max(500, sub_pop),
                    "density_per_sq_km": sub_density,
                    "city": s["name"],
                    "district": s["district"],
                    "income_index": round(0.45 + factor * 0.4, 2),
                    "value": round(max(0.15, min(1.0, factor * 0.85 + random.uniform(-0.08, 0.08))), 3),
                }
            })
            
    return {"type": "FeatureCollection", "features": features}


def generate_national_transportation():
    features = []
    
    # 1. Major National Corridors
    for c in NATIONAL_HIGHWAY_CORRIDORS:
        coords = [[round(lng, 5), round(lat, 5)] for lat, lng in c["points"]]
        speed = 120 if c["class"] == "expressway" else (100 if c["class"] == "national_highway" else 80)
        lanes = 6 if c["class"] == "expressway" else (4 if c["class"] == "national_highway" else 2)
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "name": c["name"],
                "road_type": "highway",
                "surface": "paved",
                "lanes": lanes,
                "speed_limit_kmh": speed
            }
        })
        
    # 2. Key Urban Ring Roads & Links
    urban_links = [
        {
            "name": "SG Highway Commercial Corridor, Ahmedabad",
            "coords": [[72.5112, 23.0378], [72.5150, 23.0800], [72.5300, 23.1300], [72.5500, 23.1800]],
            "lanes": 6,
            "speed": 80
        },
        {
            "name": "SP Ring Road (Ahmedabad Orbital Expressway)",
            "coords": [[72.4600, 23.0200], [72.4800, 23.1200], [72.6200, 23.1400], [72.6900, 23.0500], [72.6600, 22.9500], [72.5100, 22.9400], [72.4600, 23.0200]],
            "lanes": 4,
            "speed": 90
        },
        {
            "name": "Surat-Dumas Commercial Express Link",
            "coords": [[72.8311, 21.1702], [72.7800, 21.1400], [72.7200, 21.1000]],
            "lanes": 4,
            "speed": 70
        },
        {
            "name": "Eastern Freeway & Marine Drive, Mumbai",
            "coords": [[72.8242, 18.9256], [72.8450, 18.9600], [72.8687, 19.0657], [72.9300, 19.1600]],
            "lanes": 6,
            "speed": 80
        },
        {
            "name": "NICE Peripheral Ring Road, Bengaluru",
            "coords": [[77.4800, 12.8500], [77.5200, 12.9200], [77.5600, 13.0400], [77.6200, 13.0800]],
            "lanes": 6,
            "speed": 100
        },
        {
            "name": "Outer Ring Road (Nehru ORR), Hyderabad",
            "coords": [[78.3200, 17.4200], [78.4000, 17.5500], [78.5800, 17.4800], [78.5500, 17.3200], [78.3600, 17.3500], [78.3200, 17.4200]],
            "lanes": 8,
            "speed": 100
        }
    ]
    for ul in urban_links:
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": ul["coords"]},
            "properties": {
                "name": ul["name"],
                "road_type": "primary",
                "surface": "paved",
                "lanes": ul["lanes"],
                "speed_limit_kmh": ul["speed"]
            }
        })
        
    return {"type": "FeatureCollection", "features": features}


def generate_national_poi(total_count: int = 800):
    categories = ["retail", "restaurant", "ev_charging", "gas_station", "grocery", "bank", "hotel"]
    features = []
    
    for i in range(total_count):
        s = random.choice(ALL_SETTLEMENTS)
        c_lat, c_lng = s["lat"], s["lng"]
        radius = s["radius_km"] * 0.65
        
        angle = random.uniform(0, 2 * math.pi)
        dist_km = random.triangular(0.2, radius, 1.8)
        p_lat = c_lat + dist_km * math.cos(angle) / 111.0
        p_lng = c_lng + dist_km * math.sin(angle) / (111.0 * math.cos(math.radians(c_lat)))
        
        cat = random.choice(categories)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [round(p_lng, 5), round(p_lat, 5)]},
            "properties": {
                "name": f"{s['name']} {cat.replace('_', ' ').title()} #{i + 1}",
                "type": cat,
                "category": cat,
                "city": s["name"],
                "rating": round(random.uniform(3.4, 4.9), 1),
                "footfall": random.randint(300, 4800),
                "revenue_index": round(random.uniform(0.40, 0.96), 2),
                "value": round(random.uniform(0.25, 0.98), 3),
            }
        })
        
    return {"type": "FeatureCollection", "features": features}


def generate_national_landuse():
    zones = [
        # Ahmedabad
        {"name": "SG Highway Commercial Corridor", "type": "commercial", "coords": [[72.50, 23.02], [72.53, 23.02], [72.53, 23.08], [72.50, 23.08], [72.50, 23.02]], "far": 2.7},
        {"name": "Ashram Road Central Business District", "type": "commercial", "coords": [[72.56, 23.02], [72.59, 23.02], [72.59, 23.05], [72.56, 23.05], [72.56, 23.02]], "far": 3.0},
        {"name": "Sanand Industrial Cluster GIDC", "type": "industrial", "coords": [[72.35, 22.97], [72.42, 22.97], [72.42, 23.01], [72.35, 23.01], [72.35, 22.97]], "far": 1.5},
        {"name": "Naroda GIDC Manufacturing Area", "type": "industrial", "coords": [[72.65, 23.06], [72.70, 23.06], [72.70, 23.10], [72.65, 23.10], [72.65, 23.06]], "far": 1.4},
        {"name": "South Bopal Urban Residential Zone", "type": "residential", "coords": [[72.45, 22.99], [72.50, 22.99], [72.50, 23.03], [72.45, 23.03], [72.45, 22.99]], "far": 2.0},
        # Surat
        {"name": "Surat Ring Road Commercial Area", "type": "commercial", "coords": [[72.81, 21.16], [72.85, 21.16], [72.85, 21.20], [72.81, 21.20], [72.81, 21.16]], "far": 2.8},
        {"name": "Hazira Heavy Engineering & Port Zone", "type": "industrial", "coords": [[72.62, 21.10], [72.68, 21.10], [72.68, 21.15], [72.62, 21.15], [72.62, 21.10]], "far": 1.6},
        # Vadodara
        {"name": "Makarpura GIDC Industrial Corridor", "type": "industrial", "coords": [[73.17, 22.25], [73.22, 22.25], [73.22, 22.29], [73.17, 22.29], [73.17, 22.25]], "far": 1.6},
        # Halol / Panchmahal
        {"name": "Halol Automobile & Manufacturing GIDC", "type": "industrial", "coords": [[73.45, 22.48], [73.50, 22.48], [73.50, 22.52], [73.45, 22.52], [73.45, 22.48]], "far": 1.5},
        # Morbi
        {"name": "Morbi Ceramic Mega Industrial Zone", "type": "industrial", "coords": [[70.81, 22.79], [70.88, 22.79], [70.88, 22.84], [70.81, 22.84], [70.81, 22.79]], "far": 1.8},
        # Ankleshwar & Dahej
        {"name": "Ankleshwar Chemical & Pharma GIDC", "type": "industrial", "coords": [[72.98, 21.61], [73.04, 21.61], [73.04, 21.65], [72.98, 21.65], [72.98, 21.61]], "far": 1.6},
        {"name": "Dahej PCPIR Petrochemical Complex", "type": "industrial", "coords": [[72.55, 21.69], [72.62, 21.69], [72.62, 21.74], [72.55, 21.74], [72.55, 21.69]], "far": 1.7},
        # Vapi
        {"name": "Vapi GIDC Industrial Estate", "type": "industrial", "coords": [[72.89, 20.37], [72.94, 20.37], [72.94, 20.41], [72.89, 20.41], [72.89, 20.37]], "far": 1.6},
        # Kutch
        {"name": "Kutch Revenue Wasteland & Renewable Zone", "type": "wasteland", "coords": [[69.50, 23.60], [69.90, 23.60], [69.90, 23.90], [69.50, 23.90], [69.50, 23.60]], "far": 0.5},
        # Pan-India Major Commercial & Industrial Polygons
        {"name": "Bandra Kurla Complex (BKC), Mumbai", "type": "commercial", "coords": [[72.860, 19.060], [72.875, 19.060], [72.875, 19.072], [72.860, 19.072], [72.860, 19.060]], "far": 3.5},
        {"name": "DLF Cyber City, Gurugram", "type": "commercial", "coords": [[77.080, 28.490], [77.098, 28.490], [77.098, 28.502], [77.080, 28.502], [77.080, 28.490]], "far": 3.2},
        {"name": "Whitefield IT Park (ITPB), Bengaluru", "type": "commercial", "coords": [[77.725, 12.980], [77.745, 12.980], [77.745, 12.995], [77.725, 12.995], [77.725, 12.980]], "far": 2.8},
        {"name": "Hinjawadi Infotech SEZ, Pune", "type": "industrial", "coords": [[73.725, 18.585], [73.750, 18.585], [73.750, 18.600], [73.725, 18.600], [73.725, 18.585]], "far": 2.0},
        {"name": "HITEC City & Gachibowli, Hyderabad", "type": "commercial", "coords": [[78.365, 17.435], [78.388, 17.435], [78.388, 17.452], [78.365, 17.452], [78.365, 17.435]], "far": 3.0}
    ]
    
    features = []
    for z in zones:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [z["coords"]]},
            "properties": {
                "zone_name": z["name"],
                "zone_type": z["type"],
                "area_sq_km": round(random.uniform(2.5, 9.5), 2),
                "building_density": random.randint(90, 340),
                "max_floor_area_ratio": z["far"],
                "permitted": z["type"] in ["commercial", "mixed", "industrial"]
            }
        })
        
    return {"type": "FeatureCollection", "features": features}


def generate_national_environment():
    risks = [
        # Sabarmati River
        {
            "hazard": "Sabarmati River Lowland Spillover",
            "river": "Sabarmati",
            "risk": "high",
            "return_yrs": 25,
            "elev": 48.0,
            "coords": [[72.5700, 22.9800], [72.5850, 22.9800], [72.5900, 23.0400], [72.5750, 23.0400], [72.5700, 22.9800]]
        },
        # Gulf of Khambhat
        {
            "hazard": "Gulf of Khambhat Tidal Inundation Zone",
            "river": "Tidal/Coastal",
            "risk": "high",
            "return_yrs": 10,
            "elev": 8.5,
            "coords": [[72.30, 21.60], [72.70, 21.60], [72.80, 21.20], [72.40, 21.20], [72.30, 21.60]]
        },
        # Tapi River Delta
        {
            "hazard": "Tapi River Delta Inundation",
            "river": "Tapi",
            "risk": "medium",
            "return_yrs": 30,
            "elev": 14.0,
            "coords": [[72.74, 21.15], [72.80, 21.15], [72.82, 21.19], [72.76, 21.19], [72.74, 21.15]]
        },
        # Narmada River Basin
        {
            "hazard": "Narmada River Alluvial Floodplain Buffer",
            "river": "Narmada",
            "risk": "medium",
            "return_yrs": 35,
            "elev": 22.0,
            "coords": [[72.95, 21.72], [73.20, 21.72], [73.20, 21.80], [72.95, 21.80], [72.95, 21.72]]
        },
        # Rann of Kutch Salt Marsh
        {
            "hazard": "Great Rann Saline Tidal Inundation",
            "river": "Saline Wetland",
            "risk": "high",
            "return_yrs": 5,
            "elev": 4.0,
            "coords": [[69.00, 23.80], [70.50, 23.80], [70.50, 24.40], [69.00, 24.40], [69.00, 23.80]]
        },
        # Mumbai Coastal CRZ
        {
            "hazard": "Mumbai Coastal Regulation Zone & Mithi Basin",
            "river": "Arabian Sea / Mithi",
            "risk": "high",
            "return_yrs": 15,
            "elev": 6.0,
            "coords": [[72.810, 18.980], [72.850, 18.980], [72.850, 19.040], [72.810, 19.040], [72.810, 18.980]]
        },
        # Yamuna Floodplain (Delhi)
        {
            "hazard": "Yamuna River Riparian Floodplain (Delhi)",
            "river": "Yamuna",
            "risk": "medium",
            "return_yrs": 20,
            "elev": 208.0,
            "coords": [[77.240, 28.620], [77.270, 28.620], [77.270, 28.690], [77.240, 28.690], [77.240, 28.620]]
        }
    ]
    
    features = []
    for r in risks:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [r["coords"]]},
            "properties": {
                "hazard": r["hazard"],
                "risk_level": r["risk"],
                "flood_return_years": r["return_yrs"],
                "river": r["river"],
                "elevation_m": r["elev"],
                "is_exclusion": r["risk"] == "high"
            }
        })
        
    return {"type": "FeatureCollection", "features": features}


def build_and_save_all():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    layers = [
        ("demographics.geojson", generate_national_demographics()),
        ("transportation.geojson", generate_national_transportation()),
        ("poi.geojson", generate_national_poi(850)),
        ("landuse.geojson", generate_national_landuse()),
        ("environment.geojson", generate_national_environment()),
    ]
    
    for filename, fc in layers:
        out_path = DATA_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(fc, f, indent=2)
        print(f"Generated {filename}: {len(fc['features'])} features.")

if __name__ == "__main__":
    build_and_save_all()
