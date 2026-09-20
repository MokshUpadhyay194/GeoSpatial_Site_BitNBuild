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
GUJARAT_GAZETTEER: List[Dict[str, Any]] = [
    # --- AHMEDABAD & GANDHINAGAR ---
    {
        "id": "loc-sg-highway",
        "name": "SG Highway Commercial Corridor",
        "subTitle": "Bodakdev - Thaltej - Sola Arterial Axis, Ahmedabad",
        "lat": 23.0378,
        "lng": 72.5112,
        "category": "benchmark",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-gift-city",
        "name": "GIFT City International FinTech Zone",
        "subTitle": "India's Flagship IFSC Smart City, Gandhinagar",
        "lat": 23.1601,
        "lng": 72.6841,
        "category": "benchmark",
        "district": "Gandhinagar",
    },
    {
        "id": "loc-gandhinagar-central",
        "name": "Gandhinagar Central (Sector 10-21)",
        "subTitle": "Capital Administrative & Secretariat Sector, Gandhinagar",
        "lat": 23.2156,
        "lng": 72.6369,
        "category": "city",
        "district": "Gandhinagar",
    },
    {
        "id": "loc-infocity",
        "name": "Infocity IT & Software Park",
        "subTitle": "Major IT/ITES Corridor & Innovation Hub, Gandhinagar",
        "lat": 23.1904,
        "lng": 72.6288,
        "category": "industrial",
        "district": "Gandhinagar",
    },
    {
        "id": "loc-sanand-gidc",
        "name": "Sanand GIDC Mega Automotive Corridor",
        "subTitle": "Heavy Industrial & Auto OEM Cluster, Ahmedabad Rural",
        "lat": 22.9868,
        "lng": 72.3814,
        "category": "benchmark",
        "district": "Ahmedabad Rural",
    },
    {
        "id": "loc-sbr",
        "name": "Sindhu Bhavan Road (SBR)",
        "subTitle": "High-Street Retail & Corporate Corridor, Ahmedabad",
        "lat": 23.0450,
        "lng": 72.4980,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-bodakdev",
        "name": "Bodakdev Urban Ward",
        "subTitle": "SG Highway & Judges Bungalow Precinct, Ahmedabad",
        "lat": 23.0373,
        "lng": 72.5074,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-prahladnagar",
        "name": "Prahlad Nagar Corporate Road",
        "subTitle": "Makarba - Vejalpur Commercial Zone, Ahmedabad",
        "lat": 23.0125,
        "lng": 72.5085,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-satellite",
        "name": "Satellite & Shivranjani",
        "subTitle": "Dense Mixed Commercial & Residential Hub, Ahmedabad",
        "lat": 23.0305,
        "lng": 72.5178,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-vastrapur",
        "name": "Vastrapur Lake & IIM Ahmedabad",
        "subTitle": "Institutional & Premium Retail District, Ahmedabad",
        "lat": 23.0350,
        "lng": 72.5293,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-navrangpura",
        "name": "Navrangpura Commercial District",
        "subTitle": "CG Road, Municipal Market & Law Garden, Ahmedabad",
        "lat": 23.0365,
        "lng": 72.5611,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-ashram-road",
        "name": "Ashram Road Financial Corridor",
        "subTitle": "Historic CBD & Sabarmati Riverfront, Ahmedabad",
        "lat": 23.0298,
        "lng": 72.5714,
        "category": "ward",
        "district": "Ahmedabad",
    },
    {
        "id": "loc-changodar",
        "name": "Changodar Industrial & Logistics Park",
        "subTitle": "Sarkhej-Bavla National Highway Freight Corridor",
        "lat": 22.9234,
        "lng": 72.4285,
        "category": "industrial",
        "district": "Ahmedabad Rural",
    },

    # --- VADODARA ---
    {
        "id": "loc-vadodara-central",
        "name": "Vadodara Central Business District",
        "subTitle": "Sayajigunj, Station Area & Alkapuri, Vadodara",
        "lat": 22.3072,
        "lng": 73.1812,
        "category": "city",
        "district": "Vadodara",
    },
    {
        "id": "loc-vadodara-alkapuri",
        "name": "Alkapuri Central Commercial Hub",
        "subTitle": "R.C. Dutt Road Premier Business District, Vadodara",
        "lat": 22.3106,
        "lng": 73.1812,
        "category": "benchmark",
        "district": "Vadodara",
    },
    {
        "id": "loc-vadodara-makarpura",
        "name": "Makarpura GIDC Industrial Estate",
        "subTitle": "Major Electrical & Heavy Engineering Hub, Vadodara",
        "lat": 22.2536,
        "lng": 73.1950,
        "category": "industrial",
        "district": "Vadodara",
    },
    {
        "id": "loc-vadodara-akota",
        "name": "Akota & Gotri Commercial Corridor",
        "subTitle": "West Vadodara High-Density Retail & Residential Axis",
        "lat": 22.3015,
        "lng": 73.1614,
        "category": "city",
        "district": "Vadodara",
    },

    # --- SURAT ---
    {
        "id": "loc-surat-central",
        "name": "Surat Central & Ring Road Textile Market",
        "subTitle": "Asia's Premier Textile & Fabric Trading Capital, Surat",
        "lat": 21.1959,
        "lng": 72.8302,
        "category": "city",
        "district": "Surat",
    },
    {
        "id": "loc-surat-vesu",
        "name": "Vesu Commercial & Luxury Retail Hub",
        "subTitle": "South Surat High-Density Premium Corridor, Surat",
        "lat": 21.1442,
        "lng": 72.7712,
        "category": "city",
        "district": "Surat",
    },
    {
        "id": "loc-surat-diamond-bourse",
        "name": "Surat Diamond Bourse (DREAM City)",
        "subTitle": "Khajod Global Gems & Jewelry Trading Capital, Surat",
        "lat": 21.1219,
        "lng": 72.7661,
        "category": "city",
        "district": "Surat",
    },
    {
        "id": "loc-surat-hazira",
        "name": "Hazira Port & Industrial Belt",
        "subTitle": "Deep-Water LNG, Steel & Heavy Petrochemical Terminal, Surat",
        "lat": 21.1158,
        "lng": 72.6482,
        "category": "industrial",
        "district": "Surat",
    },

    # --- RAJKOT ---
    {
        "id": "loc-rajkot-ringroad",
        "name": "150 Feet Ring Road Commercial Axis",
        "subTitle": "West Rajkot Retail, Hospitality & Healthcare Corridor, Rajkot",
        "lat": 22.2850,
        "lng": 70.7680,
        "category": "city",
        "district": "Rajkot",
    },
    {
        "id": "loc-rajkot-central",
        "name": "Rajkot Central & Yagnik Road",
        "subTitle": "Saurashtra Commercial & Financial Epicenter, Rajkot",
        "lat": 22.3039,
        "lng": 70.8022,
        "category": "city",
        "district": "Rajkot",
    },
    {
        "id": "loc-rajkot-aji",
        "name": "Aji GIDC & Shapar-Veraval Industrial Zone",
        "subTitle": "Engineering, Casting & Diesel Engine Capital, Rajkot",
        "lat": 22.2514,
        "lng": 70.8142,
        "category": "industrial",
        "district": "Rajkot",
    },

    # --- BHAVNAGAR ---
    {
        "id": "loc-bhavnagar-city",
        "name": "Bhavnagar Central & Waghawadi Road",
        "subTitle": "Commercial High-Street & Civic Center, Bhavnagar",
        "lat": 21.7645,
        "lng": 72.1519,
        "category": "city",
        "district": "Bhavnagar",
    },
    {
        "id": "loc-alang-shipyard",
        "name": "Alang Ship Recycling & Marine Yard",
        "subTitle": "World's Largest Ship Breaking & Steel Recovery Cluster, Bhavnagar",
        "lat": 21.4167,
        "lng": 72.1833,
        "category": "industrial",
        "district": "Bhavnagar",
    },

    # --- KUTCH ---
    {
        "id": "loc-mundra-port",
        "name": "Mundra Port & SEZ Logistics Hub",
        "subTitle": "Deep-Water Container Terminal & Freight Corridor, Kutch",
        "lat": 22.8394,
        "lng": 69.7214,
        "category": "benchmark",
        "district": "Kutch",
    },
    {
        "id": "loc-gandhidham-kandla",
        "name": "Gandhidham & Deendayal Port (Kandla)",
        "subTitle": "Major Dry Cargo Port, Timber & Logistics Node, Kutch",
        "lat": 23.0753,
        "lng": 70.1337,
        "category": "industrial",
        "district": "Kutch",
    },
    {
        "id": "loc-bhuj-city",
        "name": "Bhuj Central Heritage & Commercial Hub",
        "subTitle": "Kutch District Headquarters & Transport Node, Bhuj",
        "lat": 23.2420,
        "lng": 69.6669,
        "category": "city",
        "district": "Kutch",
    },

    # --- BHARUCH, ANAND, VAPI, MORBI, DHOLERA ---
    {
        "id": "loc-dahej-pcpir",
        "name": "Dahej PCPIR & Deep-Water Port Terminal",
        "subTitle": "Petrochemicals, Petroleum & Chemical Investment Zone, Bharuch",
        "lat": 21.7125,
        "lng": 72.5855,
        "category": "industrial",
        "district": "Bharuch",
    },
    {
        "id": "loc-ankleshwar-gidc",
        "name": "Ankleshwar GIDC Mega Chemical Estate",
        "subTitle": "Asia's Foremost Chemical & Pharmaceuticals Cluster, Bharuch",
        "lat": 21.6264,
        "lng": 73.0031,
        "category": "industrial",
        "district": "Bharuch",
    },
    {
        "id": "loc-anand-amul",
        "name": "Anand Agri & Amul Dairy Corridor",
        "subTitle": "India's Dairy Capital & Agro-Processing Zone, Anand",
        "lat": 22.5645,
        "lng": 72.9289,
        "category": "city",
        "district": "Anand",
    },
    {
        "id": "loc-vapi-gidc",
        "name": "Vapi Mega GIDC Industrial Estate",
        "subTitle": "Chemicals, Paper, Dyes & Packaging Hub, Valsad",
        "lat": 20.3893,
        "lng": 72.9106,
        "category": "industrial",
        "district": "Valsad",
    },
    {
        "id": "loc-morbi-ceramic",
        "name": "Morbi Ceramic Industrial Cluster",
        "subTitle": "National Ceramic Tile & Sanitaryware Capital, Morbi",
        "lat": 22.8120,
        "lng": 70.8380,
        "category": "industrial",
        "district": "Morbi",
    },
    {
        "id": "loc-dholera-sir",
        "name": "Dholera Special Investment Region (SIR)",
        "subTitle": "Greenfield Smart Industrial City & Semiconductor Node",
        "lat": 22.2472,
        "lng": 72.1908,
        "category": "industrial",
        "district": "Ahmedabad Rural",
    },

    # --- ALL 33 GUJARAT DISTRICT HEADQUARTERS & STRATEGIC HUBS ---
    {
        "id": "loc-godhra-city",
        "name": "Godhra Central & Station Road",
        "subTitle": "Panchmahal District Headquarters & Rail Junction",
        "lat": 22.7753,
        "lng": 73.6149,
        "category": "city",
        "district": "Panchmahal",
    },
    {
        "id": "loc-halol-gidc",
        "name": "Halol GIDC Industrial & Auto Hub",
        "subTitle": "Manufacturing & Automobile Corridor, Panchmahal",
        "lat": 22.4985,
        "lng": 73.4735,
        "category": "industrial",
        "district": "Panchmahal",
    },
    {
        "id": "loc-dahod-city",
        "name": "Dahod Smart City & Railway Loco Hub",
        "subTitle": "Dahod District Headquarters & Western Railway Engineering Works",
        "lat": 22.8362,
        "lng": 74.2552,
        "category": "city",
        "district": "Dahod",
    },
    {
        "id": "loc-palanpur-city",
        "name": "Palanpur Central & Diamond Processing Zone",
        "subTitle": "Banaskantha District Headquarters & Transport Node",
        "lat": 24.1724,
        "lng": 72.4344,
        "category": "city",
        "district": "Banaskantha",
    },
    {
        "id": "loc-patan-city",
        "name": "Patan Historical & Solar Power Corridor",
        "subTitle": "Patan District Headquarters & Charanka Solar Park Gateway",
        "lat": 23.8500,
        "lng": 72.1300,
        "category": "city",
        "district": "Patan",
    },
    {
        "id": "loc-himatnagar-city",
        "name": "Himatnagar Central & Ceramic Basin",
        "subTitle": "Sabarkantha District Headquarters & NH-48 Link",
        "lat": 23.5979,
        "lng": 73.0725,
        "category": "city",
        "district": "Sabarkantha",
    },
    {
        "id": "loc-modasa-city",
        "name": "Modasa Commercial & Logistics Center",
        "subTitle": "Aravalli District Headquarters & Eastern Transit Node",
        "lat": 23.4633,
        "lng": 73.2984,
        "category": "city",
        "district": "Aravalli",
    },
    {
        "id": "loc-nadiad-city",
        "name": "Nadiad Santram & Express Highway Junction",
        "subTitle": "Kheda District Headquarters & NE-1 Corridor",
        "lat": 22.6916,
        "lng": 72.8634,
        "category": "city",
        "district": "Kheda",
    },
    {
        "id": "loc-lunawada-city",
        "name": "Lunawada Central Hub",
        "subTitle": "Mahisagar District Headquarters & Kadana Dam Gateway",
        "lat": 23.1325,
        "lng": 73.6175,
        "category": "city",
        "district": "Mahisagar",
    },
    {
        "id": "loc-chhota-udepur",
        "name": "Chhota Udepur Mineral & Tribal Heritage Center",
        "subTitle": "Chhota Udepur District Headquarters & Dolomite Hub",
        "lat": 22.3082,
        "lng": 74.0135,
        "category": "city",
        "district": "Chhota Udepur",
    },
    {
        "id": "loc-surendranagar-city",
        "name": "Surendranagar - Wadhwan Twin Cities",
        "subTitle": "Surendranagar District Headquarters & Cotton Ginning Capital",
        "lat": 22.7274,
        "lng": 71.6372,
        "category": "city",
        "district": "Surendranagar",
    },
    {
        "id": "loc-botad-city",
        "name": "Botad Diamond & Agro Hub",
        "subTitle": "Botad District Headquarters & Saurashtra Rail Link",
        "lat": 22.1704,
        "lng": 71.6664,
        "category": "city",
        "district": "Botad",
    },
    {
        "id": "loc-amreli-city",
        "name": "Amreli Central & Agro Marketing Yard",
        "subTitle": "Amreli District Headquarters & Southern Saurashtra Node",
        "lat": 21.6032,
        "lng": 71.2221,
        "category": "city",
        "district": "Amreli",
    },
    {
        "id": "loc-junagadh-city",
        "name": "Junagadh Girnar Tourism & Commercial Center",
        "subTitle": "Junagadh District Headquarters & Gir Sanctuary Gateway",
        "lat": 21.5222,
        "lng": 70.4579,
        "category": "city",
        "district": "Junagadh",
    },
    {
        "id": "loc-porbandar-port",
        "name": "Porbandar Coastal Port & Mineral Hub",
        "subTitle": "Porbandar District Headquarters & All-Weather Sea Port",
        "lat": 21.6417,
        "lng": 69.6093,
        "category": "city",
        "district": "Porbandar",
    },
    {
        "id": "loc-veraval-somnath",
        "name": "Veraval Port & Somnath Coastal Corridor",
        "subTitle": "Gir Somnath District Headquarters & Seafood Processing Hub",
        "lat": 20.9077,
        "lng": 70.3678,
        "category": "city",
        "district": "Gir Somnath",
    },
    {
        "id": "loc-dwarka-city",
        "name": "Devbhumi Dwarka Pilgrimage & Wind Corridor",
        "subTitle": "Devbhumi Dwarka District Headquarters & High-Wind Belt",
        "lat": 22.2394,
        "lng": 68.9678,
        "category": "benchmark",
        "district": "Devbhumi Dwarka",
    },
    {
        "id": "loc-valsad-city",
        "name": "Valsad Central & Horticulture Gateway",
        "subTitle": "Valsad District Headquarters & Western Corridor Junction",
        "lat": 20.6100,
        "lng": 72.9300,
        "category": "city",
        "district": "Valsad",
    },
    {
        "id": "loc-navsari-city",
        "name": "Navsari Twin City Diamond & Sugar Hub",
        "subTitle": "Navsari District Headquarters & South Gujarat Silk Corridor",
        "lat": 20.9467,
        "lng": 72.9520,
        "category": "city",
        "district": "Navsari",
    },
    {
        "id": "loc-vyara-city",
        "name": "Vyara Central & Agro Forestry Center",
        "subTitle": "Tapi District Headquarters & Ukai Hydel Gateway",
        "lat": 21.1120,
        "lng": 73.4020,
        "category": "city",
        "district": "Tapi",
    },
    {
        "id": "loc-rajpipla-statue",
        "name": "Rajpipla & Statue of Unity Corridor",
        "subTitle": "Narmada District Headquarters & Global Tourism Zone (Kevadia)",
        "lat": 21.8719,
        "lng": 73.5024,
        "category": "benchmark",
        "district": "Narmada",
    },
    {
        "id": "loc-ahwa-dang",
        "name": "Ahwa Dang Forest & Eco-Tourism Center",
        "subTitle": "Dang District Headquarters & Saputara Hill Station Gateway",
        "lat": 20.7580,
        "lng": 73.6840,
        "category": "city",
        "district": "Dang",
    },

    # --- ALL-INDIA MAJOR METROS & STRATEGIC HUBS ---
    {
        "id": "loc-mumbai-bkc",
        "name": "Bandra Kurla Complex (BKC)",
        "subTitle": "India's Premier International Financial Center, Mumbai, Maharashtra",
        "lat": 19.0657,
        "lng": 72.8687,
        "category": "benchmark",
        "district": "Mumbai Suburban",
    },
    {
        "id": "loc-mumbai-nariman",
        "name": "Nariman Point Business District",
        "subTitle": "Historic Financial Capital & Marine Drive, Mumbai, Maharashtra",
        "lat": 18.9256,
        "lng": 72.8242,
        "category": "benchmark",
        "district": "Mumbai City",
    },
    {
        "id": "loc-delhi-cp",
        "name": "Connaught Place (CP)",
        "subTitle": "Central Business District & Heritage Radial Axis, New Delhi",
        "lat": 28.6315,
        "lng": 77.2167,
        "category": "benchmark",
        "district": "New Delhi",
    },
    {
        "id": "loc-gurugram-cybercity",
        "name": "DLF Cyber City & Golf Course Road",
        "subTitle": "Global Fortune 500 Tech & Corporate Corridor, Gurugram, Haryana",
        "lat": 28.4950,
        "lng": 77.0895,
        "category": "benchmark",
        "district": "Gurugram",
    },
    {
        "id": "loc-noida-sector62",
        "name": "Noida Sector 62 IT & Institutional Hub",
        "subTitle": "Software, Electronic Hardware & Media Corridor, Gautam Buddha Nagar, UP",
        "lat": 28.6280,
        "lng": 77.3649,
        "category": "industrial",
        "district": "Gautam Buddha Nagar",
    },
    {
        "id": "loc-bengaluru-whitefield",
        "name": "Whitefield International Tech Park (ITPB)",
        "subTitle": "India's Silicon Valley Flagship IT & R&D Hub, Bengaluru, Karnataka",
        "lat": 12.9863,
        "lng": 77.7370,
        "category": "benchmark",
        "district": "Bengaluru Urban",
    },
    {
        "id": "loc-bengaluru-electronic-city",
        "name": "Electronic City Phases 1 & 2",
        "subTitle": "Major Electronics, IT & Semiconductor Campus, Bengaluru, Karnataka",
        "lat": 12.8399,
        "lng": 77.6770,
        "category": "industrial",
        "district": "Bengaluru Urban",
    },
    {
        "id": "loc-hyderabad-hitec",
        "name": "HITEC City & Cyberabad",
        "subTitle": "Global Technology, Pharma & Biotech Center, Hyderabad, Telangana",
        "lat": 17.4435,
        "lng": 78.3772,
        "category": "benchmark",
        "district": "Hyderabad",
    },
    {
        "id": "loc-chennai-omr",
        "name": "Old Mahabalipuram Road (OMR) IT Expressway",
        "subTitle": "Tamil Nadu Software & Hardware Corridor, Chennai, Tamil Nadu",
        "lat": 12.9165,
        "lng": 80.2280,
        "category": "benchmark",
        "district": "Chennai",
    },
    {
        "id": "loc-pune-hinjawadi",
        "name": "Hinjawadi Rajiv Gandhi Infotech Park",
        "subTitle": "Automotive Engineering, SaaS & IT Hub, Pune, Maharashtra",
        "lat": 18.5913,
        "lng": 73.7389,
        "category": "industrial",
        "district": "Pune",
    },
    {
        "id": "loc-kolkata-saltlake",
        "name": "Salt Lake Sector V IT Hub",
        "subTitle": "Eastern India's Premier IT & Commercial Complex, Kolkata, West Bengal",
        "lat": 22.5802,
        "lng": 88.4312,
        "category": "benchmark",
        "district": "North 24 Parganas",
    },
    {
        "id": "loc-jaipur-mansarovar",
        "name": "Jaipur Central & Mansarovar Industrial Corridor",
        "subTitle": "Rajasthan Capital, Gems, Tourism & Logistics Hub, Jaipur, Rajasthan",
        "lat": 26.8688,
        "lng": 75.7600,
        "category": "city",
        "district": "Jaipur",
    },
    {
        "id": "loc-lucknow-gomtinagar",
        "name": "Gomti Nagar Extension & Shaheed Path",
        "subTitle": "Uttar Pradesh Capital Commercial Axis, Lucknow, Uttar Pradesh",
        "lat": 26.8500,
        "lng": 80.9900,
        "category": "city",
        "district": "Lucknow",
    },
    {
        "id": "loc-chandigarh-it-park",
        "name": "Rajiv Gandhi Chandigarh Technology Park",
        "subTitle": "Tricity IT & Engineering Hub, Chandigarh Union Territory",
        "lat": 30.7250,
        "lng": 76.8450,
        "category": "city",
        "district": "Chandigarh",
    },
    {
        "id": "loc-indore-super-corridor",
        "name": "Indore Super Corridor & IT SEZ",
        "subTitle": "Commercial Capital of Madhya Pradesh, Indore, MP",
        "lat": 22.7533,
        "lng": 75.8037,
        "category": "city",
        "district": "Indore",
    },
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


def fetch_photon_gujarat(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    """Query Photon autocomplete engine strictly bounded to Gujarat (bbox: 68.1, 20.1 to 74.5, 24.7)."""
    params = urllib.parse.urlencode({
        "q": query,
        "bbox": f"{GUJARAT_BBOX['min_lng']},{GUJARAT_BBOX['min_lat']},{GUJARAT_BBOX['max_lng']},{GUJARAT_BBOX['max_lat']}",
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
                if not is_within_gujarat(lat, lng):
                    continue

                p = feat.get("properties", {})
                name = p.get("name")
                if not name:
                    continue

                street = p.get("street") or ""
                district = p.get("district") or p.get("city") or p.get("county") or ""
                state = p.get("state") or "Gujarat"
                if state.lower() in ["maharashtra", "rajasthan", "madhya pradesh", "karnataka", "delhi"]:
                    continue
                postcode = p.get("postcode") or ""

                sub_items = [item for item in [street, district, state, postcode] if item and item.lower() != name.lower()]
                subTitle = ", ".join(sub_items) if sub_items else "Gujarat, India"

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
                    "district": district or "Gujarat",
                })
    except Exception:
        pass
    return results


def fetch_nominatim_gujarat(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Secondary fallback: Nominatim geocoder with bounded viewbox to Gujarat."""
    params = urllib.parse.urlencode({
        "format": "json",
        "q": query,
        "viewbox": f"{GUJARAT_BBOX['min_lng']},{GUJARAT_BBOX['max_lat']},{GUJARAT_BBOX['max_lng']},{GUJARAT_BBOX['min_lat']}",
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
                if not is_within_gujarat(lat, lng):
                    continue

                display_name = item.get("display_name", "")
                parts = [p.strip() for p in display_name.split(",") if p.strip()]
                primary_name = item.get("name") or (parts[0] if parts else "Location")

                addr = item.get("address", {})
                city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or ""
                state = addr.get("state", "Gujarat")
                sub_parts = [p for p in [city, state] if p and p.lower() != primary_name.lower()]
                subTitle = ", ".join(sub_parts) if sub_parts else display_name

                results.append({
                    "id": f"nom-{item.get('place_id', '')}",
                    "name": primary_name,
                    "subTitle": subTitle,
                    "lat": lat,
                    "lng": lng,
                    "category": "geocoded",
                    "district": city or state or "Gujarat",
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

    # 3. Query Photon with strict Gujarat bounding box (searches every street, ward, village, landmark)
    if len(query) >= 2 and not coord:
        photon_matches = fetch_photon_gujarat(query, limit=limit)
        for pm in photon_matches:
            # Deduplicate by ~400m proximity
            if not any(abs(r["lat"] - pm["lat"]) < 0.004 and abs(r["lng"] - pm["lng"]) < 0.004 for r in results):
                results.append(pm)

    # 4. If still under limit, query Nominatim with bounded viewbox
    if len(results) < 4 and len(query) >= 3 and not coord:
        nominatim_matches = fetch_nominatim_gujarat(query, limit=limit - len(results))
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
