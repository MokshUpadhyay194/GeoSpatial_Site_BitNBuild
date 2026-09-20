"""National Spatial Model and Settlement Hierarchy for All-India & All-Gujarat.

Provides continuous, high-fidelity spatial estimations for:
  - Multi-scale settlement demographics (all 33 Gujarat districts + pan-India metros & hubs)
  - National Highway & State Highway network distances
  - Commercial POI & economic activity intensity
  - Regional landuse and industrial zoning (GIDCs, MIDCs, KIADBs, Logistics, Wastelands)
  - Environmental hazards (floodplains, CRZ coastal zones, river deltas, seismic belts)
  - Solar Global Horizontal Irradiance (GHI) across India
"""

import math
from typing import Dict, Any, Tuple, List, Optional

try:
    from backend.utils.geo_helpers import haversine_distance
    from backend.scoring.decay import gaussian, inverse_distance
except ImportError:
    from utils.geo_helpers import haversine_distance
    from scoring.decay import gaussian, inverse_distance


# ─────────────────────────────────────────────────────────────────────────────
# 1. SETTLEMENT HIERARCHY — ALL 33 GUJARAT DISTRICTS + PAN-INDIA HUBS
# ─────────────────────────────────────────────────────────────────────────────

ALL_SETTLEMENTS: List[Dict[str, Any]] = [
    # ── GUJARAT: ALL 33 DISTRICTS & STRATEGIC HUBS ───────────────────────────
    {"name": "Ahmedabad", "state": "Gujarat", "district": "Ahmedabad", "lat": 23.0225, "lng": 72.5714, "pop": 8500000, "density": 18500, "tier": 1, "income": "high", "radius_km": 25},
    {"name": "Surat", "state": "Gujarat", "district": "Surat", "lat": 21.1702, "lng": 72.8311, "pop": 6500000, "density": 16000, "tier": 1, "income": "high", "radius_km": 20},
    {"name": "Vadodara", "state": "Gujarat", "district": "Vadodara", "lat": 22.3072, "lng": 73.1812, "pop": 2300000, "density": 9500, "tier": 2, "income": "high", "radius_km": 16},
    {"name": "Rajkot", "state": "Gujarat", "district": "Rajkot", "lat": 22.3039, "lng": 70.8022, "pop": 1900000, "density": 8500, "tier": 2, "income": "medium", "radius_km": 15},
    {"name": "Gandhinagar", "state": "Gujarat", "district": "Gandhinagar", "lat": 23.2156, "lng": 72.6369, "pop": 450000, "density": 4500, "tier": 2, "income": "high", "radius_km": 12},
    {"name": "Bhavnagar", "state": "Gujarat", "district": "Bhavnagar", "lat": 21.7645, "lng": 72.1519, "pop": 750000, "density": 5500, "tier": 3, "income": "medium", "radius_km": 12},
    {"name": "Jamnagar", "state": "Gujarat", "district": "Jamnagar", "lat": 22.4707, "lng": 70.0577, "pop": 700000, "density": 5000, "tier": 3, "income": "medium", "radius_km": 12},
    {"name": "Junagadh", "state": "Gujarat", "district": "Junagadh", "lat": 21.5222, "lng": 70.4579, "pop": 420000, "density": 4000, "tier": 3, "income": "medium", "radius_km": 10},
    {"name": "Anand", "state": "Gujarat", "district": "Anand", "lat": 22.5645, "lng": 72.9289, "pop": 380000, "density": 3800, "tier": 3, "income": "medium", "radius_km": 10},
    {"name": "Bharuch", "state": "Gujarat", "district": "Bharuch", "lat": 21.7051, "lng": 72.9959, "pop": 420000, "density": 3900, "tier": 3, "income": "medium", "radius_km": 10},
    {"name": "Mehsana", "state": "Gujarat", "district": "Mehsana", "lat": 23.5880, "lng": 72.3693, "pop": 340000, "density": 3400, "tier": 3, "income": "medium", "radius_km": 10},
    {"name": "Godhra", "state": "Gujarat", "district": "Panchmahal", "lat": 22.7753, "lng": 73.6149, "pop": 290000, "density": 2800, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Halol", "state": "Gujarat", "district": "Panchmahal", "lat": 22.4985, "lng": 73.4735, "pop": 140000, "density": 2400, "tier": 4, "income": "medium", "radius_km": 8},
    {"name": "Dahod", "state": "Gujarat", "district": "Dahod", "lat": 22.8362, "lng": 74.2552, "pop": 260000, "density": 2400, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Palanpur", "state": "Gujarat", "district": "Banaskantha", "lat": 24.1724, "lng": 72.4344, "pop": 270000, "density": 2600, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Patan", "state": "Gujarat", "district": "Patan", "lat": 23.8500, "lng": 72.1300, "pop": 230000, "density": 2200, "tier": 3, "income": "medium", "radius_km": 8},
    {"name": "Himatnagar", "state": "Gujarat", "district": "Sabarkantha", "lat": 23.5979, "lng": 73.0725, "pop": 220000, "density": 2300, "tier": 3, "income": "medium", "radius_km": 8},
    {"name": "Modasa", "state": "Gujarat", "district": "Aravalli", "lat": 23.4633, "lng": 73.2984, "pop": 160000, "density": 1900, "tier": 4, "income": "medium", "radius_km": 8},
    {"name": "Nadiad", "state": "Gujarat", "district": "Kheda", "lat": 22.6916, "lng": 72.8634, "pop": 310000, "density": 3100, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Lunawada", "state": "Gujarat", "district": "Mahisagar", "lat": 23.1325, "lng": 73.6175, "pop": 140000, "density": 1600, "tier": 4, "income": "medium", "radius_km": 7},
    {"name": "Chhota Udepur", "state": "Gujarat", "district": "Chhota Udepur", "lat": 22.3082, "lng": 74.0135, "pop": 120000, "density": 1400, "tier": 4, "income": "low", "radius_km": 7},
    {"name": "Surendranagar", "state": "Gujarat", "district": "Surendranagar", "lat": 22.7274, "lng": 71.6372, "pop": 290000, "density": 2800, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Morbi", "state": "Gujarat", "district": "Morbi", "lat": 22.8120, "lng": 70.8380, "pop": 370000, "density": 3600, "tier": 3, "income": "high", "radius_km": 11},
    {"name": "Botad", "state": "Gujarat", "district": "Botad", "lat": 22.1704, "lng": 71.6664, "pop": 190000, "density": 2000, "tier": 4, "income": "medium", "radius_km": 8},
    {"name": "Amreli", "state": "Gujarat", "district": "Amreli", "lat": 21.6032, "lng": 71.2221, "pop": 210000, "density": 2100, "tier": 3, "income": "medium", "radius_km": 8},
    {"name": "Porbandar", "state": "Gujarat", "district": "Porbandar", "lat": 21.6417, "lng": 69.6093, "pop": 270000, "density": 2600, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Veraval", "state": "Gujarat", "district": "Gir Somnath", "lat": 20.9077, "lng": 70.3678, "pop": 250000, "density": 2500, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Dwarka", "state": "Gujarat", "district": "Devbhumi Dwarka", "lat": 22.2394, "lng": 68.9678, "pop": 150000, "density": 1700, "tier": 4, "income": "medium", "radius_km": 8},
    {"name": "Bhuj", "state": "Gujarat", "district": "Kutch", "lat": 23.2420, "lng": 69.6669, "pop": 280000, "density": 2500, "tier": 3, "income": "medium", "radius_km": 10},
    {"name": "Gandhidham", "state": "Gujarat", "district": "Kutch", "lat": 23.0753, "lng": 70.1337, "pop": 340000, "density": 3400, "tier": 3, "income": "high", "radius_km": 10},
    {"name": "Mundra", "state": "Gujarat", "district": "Kutch", "lat": 22.8394, "lng": 69.7214, "pop": 170000, "density": 2200, "tier": 4, "income": "high", "radius_km": 9},
    {"name": "Valsad", "state": "Gujarat", "district": "Valsad", "lat": 20.6100, "lng": 72.9300, "pop": 260000, "density": 2700, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Vapi", "state": "Gujarat", "district": "Valsad", "lat": 20.3893, "lng": 72.9106, "pop": 310000, "density": 3900, "tier": 3, "income": "high", "radius_km": 10},
    {"name": "Navsari", "state": "Gujarat", "district": "Navsari", "lat": 20.9467, "lng": 72.9520, "pop": 330000, "density": 3300, "tier": 3, "income": "medium", "radius_km": 9},
    {"name": "Vyara", "state": "Gujarat", "district": "Tapi", "lat": 21.1120, "lng": 73.4020, "pop": 130000, "density": 1500, "tier": 4, "income": "low", "radius_km": 7},
    {"name": "Rajpipla", "state": "Gujarat", "district": "Narmada", "lat": 21.8719, "lng": 73.5024, "pop": 140000, "density": 1600, "tier": 4, "income": "medium", "radius_km": 8},
    {"name": "Ahwa", "state": "Gujarat", "district": "Dang", "lat": 20.7580, "lng": 73.6840, "pop": 85000, "density": 950, "tier": 4, "income": "low", "radius_km": 6},

    # ── PAN-INDIA: MAJOR METROPOLITAN & REGIONAL CLUSTERS ────────────────────
    {"name": "Mumbai", "state": "Maharashtra", "district": "Mumbai", "lat": 19.0760, "lng": 72.8777, "pop": 21000000, "density": 26000, "tier": 1, "income": "high", "radius_km": 30},
    {"name": "Delhi-NCR", "state": "Delhi", "district": "New Delhi", "lat": 28.6139, "lng": 77.2090, "pop": 30000000, "density": 23000, "tier": 1, "income": "high", "radius_km": 35},
    {"name": "Bengaluru", "state": "Karnataka", "district": "Bengaluru Urban", "lat": 12.9716, "lng": 77.5946, "pop": 13000000, "density": 14500, "tier": 1, "income": "high", "radius_km": 25},
    {"name": "Hyderabad", "state": "Telangana", "district": "Hyderabad", "lat": 17.3850, "lng": 78.4867, "pop": 10500000, "density": 12500, "tier": 1, "income": "high", "radius_km": 25},
    {"name": "Chennai", "state": "Tamil Nadu", "district": "Chennai", "lat": 13.0827, "lng": 80.2707, "pop": 11500000, "density": 15500, "tier": 1, "income": "high", "radius_km": 24},
    {"name": "Kolkata", "state": "West Bengal", "district": "Kolkata", "lat": 22.5726, "lng": 88.3639, "pop": 15000000, "density": 24000, "tier": 1, "income": "medium", "radius_km": 26},
    {"name": "Pune", "state": "Maharashtra", "district": "Pune", "lat": 18.5204, "lng": 73.8567, "pop": 7200000, "density": 10500, "tier": 2, "income": "high", "radius_km": 20},
    {"name": "Jaipur", "state": "Rajasthan", "district": "Jaipur", "lat": 26.9124, "lng": 75.7873, "pop": 4100000, "density": 6800, "tier": 2, "income": "medium", "radius_km": 18},
    {"name": "Lucknow", "state": "Uttar Pradesh", "district": "Lucknow", "lat": 26.8467, "lng": 80.9462, "pop": 3900000, "density": 6200, "tier": 2, "income": "medium", "radius_km": 18},
    {"name": "Chandigarh", "state": "Chandigarh", "district": "Chandigarh", "lat": 30.7333, "lng": 76.7794, "pop": 1500000, "density": 9500, "tier": 2, "income": "high", "radius_km": 14},
    {"name": "Indore", "state": "Madhya Pradesh", "district": "Indore", "lat": 22.7196, "lng": 75.8577, "pop": 3300000, "density": 6400, "tier": 2, "income": "medium", "radius_km": 16},
    {"name": "Bhopal", "state": "Madhya Pradesh", "district": "Bhopal", "lat": 23.2599, "lng": 77.4126, "pop": 2500000, "density": 4800, "tier": 2, "income": "medium", "radius_km": 15},
    {"name": "Nagpur", "state": "Maharashtra", "district": "Nagpur", "lat": 21.1458, "lng": 79.0882, "pop": 2900000, "density": 5400, "tier": 2, "income": "medium", "radius_km": 16},
    {"name": "Patna", "state": "Bihar", "district": "Patna", "lat": 25.5941, "lng": 85.1376, "pop": 2700000, "density": 7800, "tier": 2, "income": "medium", "radius_km": 15},
    {"name": "Bhubaneswar", "state": "Odisha", "district": "Khordha", "lat": 20.2961, "lng": 85.8245, "pop": 1400000, "density": 4600, "tier": 2, "income": "medium", "radius_km": 14},
    {"name": "Visakhapatnam", "state": "Andhra Pradesh", "district": "Visakhapatnam", "lat": 17.6868, "lng": 83.2185, "pop": 2400000, "density": 5200, "tier": 2, "income": "medium", "radius_km": 15},
    {"name": "Coimbatore", "state": "Tamil Nadu", "district": "Coimbatore", "lat": 11.0168, "lng": 76.9558, "pop": 2300000, "density": 5000, "tier": 2, "income": "high", "radius_km": 15},
    {"name": "Kochi", "state": "Kerala", "district": "Ernakulam", "lat": 9.9312, "lng": 76.2673, "pop": 2400000, "density": 5800, "tier": 2, "income": "high", "radius_km": 15},
    {"name": "Guwahati", "state": "Assam", "district": "Kamrup Metropolitan", "lat": 26.1445, "lng": 91.7362, "pop": 1400000, "density": 4200, "tier": 2, "income": "medium", "radius_km": 14},
    {"name": "Varanasi", "state": "Uttar Pradesh", "district": "Varanasi", "lat": 25.3176, "lng": 82.9739, "pop": 1800000, "density": 6000, "tier": 3, "income": "medium", "radius_km": 14},
    {"name": "Agra", "state": "Uttar Pradesh", "district": "Agra", "lat": 27.1767, "lng": 78.0081, "pop": 2200000, "density": 5700, "tier": 3, "income": "medium", "radius_km": 14},
    {"name": "Ludhiana", "state": "Punjab", "district": "Ludhiana", "lat": 30.9010, "lng": 75.8573, "pop": 2000000, "density": 5900, "tier": 2, "income": "high", "radius_km": 15},
    {"name": "Amritsar", "state": "Punjab", "district": "Amritsar", "lat": 31.6340, "lng": 74.8723, "pop": 1400000, "density": 5100, "tier": 3, "income": "medium", "radius_km": 13},
    {"name": "Nashik", "state": "Maharashtra", "district": "Nashik", "lat": 19.9975, "lng": 73.7898, "pop": 2000000, "density": 5000, "tier": 2, "income": "medium", "radius_km": 14},
    {"name": "Jodhpur", "state": "Rajasthan", "district": "Jodhpur", "lat": 26.2389, "lng": 73.0243, "pop": 1650000, "density": 4500, "tier": 3, "income": "medium", "radius_km": 13},
    {"name": "Udaipur", "state": "Rajasthan", "district": "Udaipur", "lat": 24.5854, "lng": 73.7125, "pop": 700000, "density": 3400, "tier": 3, "income": "medium", "radius_km": 12},
    {"name": "Raipur", "state": "Chhattisgarh", "district": "Raipur", "lat": 21.2514, "lng": 81.6296, "pop": 1600000, "density": 4400, "tier": 2, "income": "medium", "radius_km": 14},
    {"name": "Jamshedpur", "state": "Jharkhand", "district": "East Singhbhum", "lat": 22.8046, "lng": 86.2029, "pop": 1650000, "density": 4700, "tier": 3, "income": "high", "radius_km": 13},
    {"name": "Ranchi", "state": "Jharkhand", "district": "Ranchi", "lat": 23.3441, "lng": 85.3096, "pop": 1550000, "density": 4500, "tier": 2, "income": "medium", "radius_km": 13},
    {"name": "Dehradun", "state": "Uttarakhand", "district": "Dehradun", "lat": 30.3165, "lng": 78.0322, "pop": 1000000, "density": 3600, "tier": 3, "income": "medium", "radius_km": 12},
    {"name": "Srinagar", "state": "Jammu & Kashmir", "district": "Srinagar", "lat": 34.0837, "lng": 74.7973, "pop": 1450000, "density": 4000, "tier": 3, "income": "medium", "radius_km": 13},
    {"name": "Panaji", "state": "Goa", "district": "North Goa", "lat": 15.4909, "lng": 73.8278, "pop": 270000, "density": 3200, "tier": 3, "income": "high", "radius_km": 10},
    {"name": "Madurai", "state": "Tamil Nadu", "district": "Madurai", "lat": 9.9252, "lng": 78.1198, "pop": 1700000, "density": 5400, "tier": 3, "income": "medium", "radius_km": 13},
    {"name": "Thiruvananthapuram", "state": "Kerala", "district": "Thiruvananthapuram", "lat": 8.5241, "lng": 76.9366, "pop": 1900000, "density": 5300, "tier": 2, "income": "high", "radius_km": 14},
    {"name": "Vijayawada", "state": "Andhra Pradesh", "district": "NTR", "lat": 16.5062, "lng": 80.6480, "pop": 1800000, "density": 5600, "tier": 2, "income": "medium", "radius_km": 14},
    {"name": "Gwalior", "state": "Madhya Pradesh", "district": "Gwalior", "lat": 26.2183, "lng": 78.1828, "pop": 1400000, "density": 4400, "tier": 3, "income": "medium", "radius_km": 13},
    {"name": "Jabalpur", "state": "Madhya Pradesh", "district": "Jabalpur", "lat": 23.1815, "lng": 79.9864, "pop": 1550000, "density": 4600, "tier": 3, "income": "medium", "radius_km": 13},
    {"name": "Kota", "state": "Rajasthan", "district": "Kota", "lat": 25.2138, "lng": 75.8648, "pop": 1300000, "density": 4300, "tier": 3, "income": "medium", "radius_km": 13},
]


# ─────────────────────────────────────────────────────────────────────────────
# 2. NATIONAL & STATE HIGHWAY NETWORK GEOMETRY (Multi-Point Corridors)
# ─────────────────────────────────────────────────────────────────────────────

NATIONAL_HIGHWAY_CORRIDORS = [
    # NH-48 (Western Golden Quadrilateral & Southern Corridor)
    {
        "name": "NH-48 Golden Corridor",
        "class": "expressway",
        "points": [
            (28.614, 77.209), (28.459, 77.026), (27.897, 76.271), (26.912, 75.787),
            (26.449, 74.639), (24.585, 73.712), (23.850, 72.950), (23.022, 72.571),
            (22.691, 72.863), (22.307, 73.181), (21.705, 72.995), (21.170, 72.831),
            (20.946, 72.952), (20.610, 72.930), (20.389, 72.910), (19.076, 72.877),
            (18.520, 73.856), (16.852, 74.581), (15.849, 74.497), (15.364, 75.124),
            (14.464, 75.921), (13.340, 77.100), (12.971, 77.594), (12.916, 79.132),
            (13.082, 80.270)
        ]
    },
    # NH-44 (North-South Grand Corridor)
    {
        "name": "NH-44 North-South Corridor",
        "class": "expressway",
        "points": [
            (34.083, 74.797), (32.726, 74.857), (31.634, 74.872), (30.901, 75.857),
            (29.390, 76.963), (28.614, 77.209), (27.176, 78.008), (26.218, 78.182),
            (25.448, 78.568), (24.180, 78.740), (21.145, 79.088), (19.664, 78.532),
            (17.385, 78.486), (15.828, 78.037), (14.681, 77.600), (12.971, 77.594),
            (11.664, 78.146), (9.925, 78.119), (8.256, 77.545)
        ]
    },
    # NH-27 (East-West Porbandar to Silchar Corridor)
    {
        "name": "NH-27 East-West Arterial Corridor",
        "class": "national_highway",
        "points": [
            (21.641, 69.609), (21.750, 70.250), (22.303, 70.802), (22.820, 70.830),
            (23.250, 70.600), (23.480, 71.050), (23.830, 71.600), (24.172, 72.434),
            (24.585, 73.712), (24.888, 74.626), (25.213, 75.864), (25.448, 78.568),
            (26.449, 80.331), (26.846, 80.946), (26.760, 83.373), (26.120, 85.360),
            (25.770, 87.470), (26.727, 88.395), (26.144, 91.736)
        ]
    },
    # NH-16 (Eastern Coast Corridor / Chennai-Kolkata)
    {
        "name": "NH-16 Eastern Coastal Corridor",
        "class": "expressway",
        "points": [
            (13.082, 80.270), (14.442, 79.986), (15.505, 80.049), (16.306, 80.436),
            (16.506, 80.648), (17.000, 81.804), (17.686, 83.218), (18.294, 83.893),
            (19.314, 84.794), (20.296, 85.824), (20.462, 85.882), (21.493, 86.933),
            (22.330, 87.323), (22.572, 88.363)
        ]
    },
    # NH-19 (Delhi-Kolkata Grand Trunk Arterial)
    {
        "name": "NH-19 Grand Trunk Highway",
        "class": "expressway",
        "points": [
            (28.614, 77.209), (27.492, 77.673), (27.176, 78.008), (26.775, 79.027),
            (26.449, 80.331), (25.929, 80.812), (25.435, 81.846), (25.317, 82.973),
            (24.953, 84.015), (24.795, 85.000), (23.795, 86.430), (23.688, 86.966),
            (23.520, 87.311), (22.572, 88.363)
        ]
    },
    # NE-1 & Delhi-Mumbai Expressway Corridor
    {
        "name": "NE-1 & Delhi-Mumbai Expressway",
        "class": "expressway",
        "points": [
            (28.614, 77.209), (28.250, 77.050), (26.900, 76.500), (25.800, 76.200),
            (24.500, 75.500), (23.500, 74.900), (22.836, 74.255), (22.775, 73.614),
            (22.498, 73.473), (22.307, 73.181), (21.705, 72.995), (21.170, 72.831),
            (20.389, 72.910), (19.076, 72.877)
        ]
    },
    # Gujarat State Corridors & Coastal Highways (SH-1, SH-41, Saurashtra Ring)
    {
        "name": "Saurashtra & Kutch Coastal Highway Link",
        "class": "state_highway",
        "points": [
            (23.242, 69.666), (22.833, 69.355), (22.239, 68.967), (21.641, 69.609),
            (20.907, 70.367), (21.090, 71.770), (21.764, 72.151), (22.247, 72.190),
            (23.022, 72.571)
        ]
    },
    {
        "name": "North Gujarat Highway (SH-41)",
        "class": "state_highway",
        "points": [
            (23.022, 72.571), (23.215, 72.636), (23.588, 72.369), (23.850, 72.130),
            (24.172, 72.434)
        ]
    },
    {
        "name": "Eastern Tribal & Mineral Corridor (NH-56)",
        "class": "state_highway",
        "points": [
            (24.172, 72.434), (23.597, 73.072), (23.463, 73.298), (23.132, 73.617),
            (22.775, 73.614), (22.308, 74.013), (21.871, 73.502), (21.112, 73.402),
            (20.758, 73.684), (20.389, 72.910)
        ]
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# 3. SPATIAL HELPER FUNCTIONS FOR ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def _dist_to_segment(p_lat: float, p_lng: float, a_lat: float, a_lng: float, b_lat: float, b_lng: float) -> float:
    """Distance from point to a line segment in meters using projected flat approximation."""
    cos_lat = math.cos(math.radians(p_lat))
    scale_y = 111132.92
    scale_x = 111412.84 * cos_lat

    px, py = 0.0, 0.0
    ax = (a_lng - p_lng) * scale_x
    ay = (a_lat - p_lat) * scale_y
    bx = (b_lng - p_lng) * scale_x
    by = (b_lat - p_lat) * scale_y

    dx = bx - ax
    dy = by - ay
    seg_len_sq = dx * dx + dy * dy

    if seg_len_sq < 1.0:
        return math.sqrt(ax * ax + ay * ay)

    # Project point onto segment
    t = max(0.0, min(1.0, (-(ax * dx + ay * dy)) / seg_len_sq))
    proj_x = ax + t * dx
    proj_y = ay + t * dy

    return math.sqrt(proj_x * proj_x + proj_y * proj_y)


def get_hierarchical_settlement(lat: float, lng: float) -> Tuple[Dict[str, Any], float]:
    """Find the nearest settlement and return its record and distance in meters."""
    closest = None
    min_dist_m = float("inf")

    for s in ALL_SETTLEMENTS:
        d_m = haversine_distance(lat, lng, s["lat"], s["lng"], unit="m")
        if d_m < min_dist_m:
            min_dist_m = d_m
            closest = s

    if closest is None:
        closest = ALL_SETTLEMENTS[0]
        min_dist_m = 50000.0

    return closest, min_dist_m


def get_hierarchical_transport(lat: float, lng: float) -> Tuple[float, str]:
    """Find distance in meters to the nearest National or State Highway corridor."""
    min_dist_m = float("inf")
    closest_name = "Regional Road Network"

    for corridor in NATIONAL_HIGHWAY_CORRIDORS:
        pts = corridor["points"]
        for i in range(len(pts) - 1):
            a_lat, a_lng = pts[i]
            b_lat, b_lng = pts[i + 1]
            d_m = _dist_to_segment(lat, lng, a_lat, a_lng, b_lat, b_lng)
            if d_m < min_dist_m:
                min_dist_m = d_m
                closest_name = corridor["name"]

    return min_dist_m, closest_name


def get_hierarchical_demographics_score(lat: float, lng: float) -> Tuple[float, str, int, str]:
    """Calculate realistic demographic score across all 33 Gujarat districts and all of India."""
    settlement, dist_m = get_hierarchical_settlement(lat, lng)
    radius_m = settlement["radius_km"] * 1000.0

    # Gaussian decay centered around settlement core
    decay = gaussian(dist_m, sigma=max(radius_m * 0.75, 4000.0))

    # Population scaling
    norm_pop = min(settlement["pop"] / 2000000.0, 1.0)
    density_factor = min(settlement["density"] / 12000.0, 1.0)

    # Core vs Suburban vs Rural gradient
    urban_influence = (norm_pop * 0.5 + density_factor * 0.5) * decay

    # Base density depending on Indian region (Gangetic plain vs Desert vs Coastal vs Plateau)
    if 24.5 <= lat <= 28.5 and 80.0 <= lng <= 88.0:
        rural_base = 45.0  # High-density Gangetic plain (UP/Bihar)
    elif 20.0 <= lat <= 24.8 and 68.0 <= lng <= 74.5:
        rural_base = 38.0  # Gujarat agricultural/semi-arid baseline
    elif 11.0 <= lat <= 15.0:
        rural_base = 42.0  # Southern peninsular baseline
    elif 25.0 <= lat <= 28.5 and 69.5 <= lng <= 73.5:
        rural_base = 24.0  # Thar desert sparse rural
    elif lat >= 23.5 and lng <= 70.5:
        rural_base = 26.0  # Kutch arid sparse rural
    else:
        rural_base = 35.0  # National rural baseline

    score = rural_base + (urban_influence * (96.0 - rural_base))
    score = round(max(22.0, min(score, 98.0)), 1)

    # Effective local population in catchment
    est_catchment_pop = int(max(400, settlement["pop"] * decay * 0.25))

    if dist_m <= radius_m * 0.35:
        label = f"Urban Core — {settlement['name']} ({settlement['district']})"
    elif dist_m <= radius_m:
        label = f"Suburban Growth Belt — {settlement['name']} ({dist_m / 1000:.1f}km)"
    elif dist_m <= radius_m * 2.2:
        label = f"Perimeter Hinterland — {settlement['name']} Transit Influence"
    else:
        label = f"Rural Agricultural Basin ({settlement['district']} District)"

    return score, label, est_catchment_pop, settlement["income"]


def get_hierarchical_transport_score(lat: float, lng: float) -> Tuple[float, str]:
    """Calculate distance-decay transportation accessibility score across India."""
    dist_m, corridor_name = get_hierarchical_transport(lat, lng)

    # Decays from 98 near expressways/highways down to ~35 for distant rural roads
    if dist_m <= 1000:
        score = 94.0 + min((1000 - dist_m) / 1000.0 * 4.0, 4.0)
        label = f"Direct Highway Frontage (< 1km to {corridor_name})"
    elif dist_m <= 4000:
        score = 80.0 + (4000 - dist_m) / 3000.0 * 14.0
        label = f"High Arterial Connectivity ({dist_m / 1000:.1f}km to {corridor_name})"
    elif dist_m <= 12000:
        score = 60.0 + (12000 - dist_m) / 8000.0 * 20.0
        label = f"Regional Highway Link ({dist_m / 1000:.1f}km to {corridor_name})"
    elif dist_m <= 25000:
        score = 42.0 + (25000 - dist_m) / 13000.0 * 18.0
        label = f"Secondary Feeder Access ({dist_m / 1000:.1f}km to {corridor_name})"
    else:
        score = max(28.0, 42.0 - (dist_m - 25000) / 25000.0 * 14.0)
        label = f"Remote Feeder Route (> 25km to {corridor_name})"

    return round(score, 1), label


def get_hierarchical_poi_score(lat: float, lng: float) -> Tuple[float, str]:
    """Calculate commercial POI and retail density across India."""
    settlement, dist_m = get_hierarchical_settlement(lat, lng)
    trans_dist_m, _ = get_hierarchical_transport(lat, lng)
    radius_m = settlement["radius_km"] * 1000.0

    # Urban core footfall intensity
    urban_decay = gaussian(dist_m, sigma=radius_m * 0.6)
    # Highway frontage commercial nodes (dhabas, petrol bunks, plazas)
    hwy_decay = gaussian(trans_dist_m, sigma=1800.0)

    tier_mult = {1: 1.0, 2: 0.85, 3: 0.70, 4: 0.55}.get(settlement["tier"], 0.6)
    density_val = (urban_decay * 0.7 + hwy_decay * 0.3) * tier_mult

    score = 28.0 + min(density_val * 68.0, 68.0)
    score = round(min(max(score, 25.0), 98.0), 1)

    if score >= 80:
        label = f"Dense Commercial Cluster — {settlement['name']} Central"
    elif score >= 60:
        label = f"Active Retail & Service Precinct — {settlement['name']}"
    elif score >= 42:
        label = f"Highway Commercial / Secondary Market Node"
    else:
        label = "Dispersed Local Convenience Nodes"

    return score, label


def get_hierarchical_landuse_score(lat: float, lng: float, site_type: str = "ev_charging") -> Tuple[float, str]:
    """Classify and score land use compatibility for any location in India."""
    settlement, dist_m = get_hierarchical_settlement(lat, lng)
    trans_dist_m, _ = get_hierarchical_transport(lat, lng)
    radius_m = settlement["radius_km"] * 1000.0

    # Determine predominant geographic land character
    is_core = dist_m <= radius_m * 0.4
    is_suburban = radius_m * 0.4 < dist_m <= radius_m * 1.1
    is_hwy_corridor = trans_dist_m <= 2500.0

    # Arid / wasteland regions (Kutch, Western Rajasthan)
    is_wasteland = (lat >= 23.3 and lng <= 70.8) or (lat >= 25.5 and lng <= 72.5)

    if is_wasteland:
        zone = "Revenue Wasteland / Open Scrub"
        ev_score = 35.0
        retail_score = 25.0
        warehouse_score = 65.0
        solar_score = 96.0
        wind_score = 94.0
        telecom_score = 65.0
    elif is_hwy_corridor and is_suburban:
        zone = "Industrial & Logistics Corridor"
        ev_score = 82.0
        retail_score = 68.0
        warehouse_score = 96.0
        solar_score = 72.0
        wind_score = 70.0
        telecom_score = 80.0
    elif is_core:
        zone = "Urban Mixed Commercial"
        ev_score = 92.0
        retail_score = 95.0
        warehouse_score = 42.0
        solar_score = 25.0
        wind_score = 20.0
        telecom_score = 88.0
    elif is_suburban:
        zone = "Suburban Residential & Developing Mixed"
        ev_score = 75.0
        retail_score = 78.0
        warehouse_score = 72.0
        solar_score = 55.0
        wind_score = 50.0
        telecom_score = 82.0
    else:
        zone = "Agricultural & Rural Alluvial Plain"
        ev_score = 45.0
        retail_score = 40.0
        warehouse_score = 68.0
        solar_score = 85.0
        wind_score = 80.0
        telecom_score = 62.0

    type_scores = {
        "ev_charging": ev_score,
        "retail": retail_score,
        "warehouse": warehouse_score,
        "solar": solar_score,
        "windmill": wind_score,
        "renewables": max(solar_score, wind_score),
        "telecom": telecom_score,
    }
    score = type_scores.get(site_type, ev_score)
    return round(score, 1), f"Zoning: {zone}"


def get_hierarchical_environment_score(lat: float, lng: float) -> Tuple[float, str]:
    """Evaluate environmental risk factors across India (floodplains, CRZ coastlines, seismic)."""
    # 1. Coastal Regulation Zone (CRZ) — within ~1.5km of Arabian Sea, Bay of Bengal, or Gulfs
    is_coastal = False
    coastal_label = ""
    # Gulf of Kutch / Khambhat
    if (22.2 <= lat <= 23.1 and 69.0 <= lng <= 70.5) or (21.0 <= lat <= 22.2 and 72.0 <= lng <= 72.9):
        is_coastal = True
        coastal_label = "Coastal Regulation Zone / Marine Tidal Area"
    # West coast (Mumbai, Konkan, Malabar)
    elif (8.0 <= lat <= 20.5 and 72.5 <= lng <= 76.5) and abs(lng - (72.8 + (lat - 19.0) * -0.05)) < 0.15:
        is_coastal = True
        coastal_label = "Arabian Sea Coastal Buffer Zone"
    # East coast (Coromandel, Odisha, Bengal)
    elif (10.0 <= lat <= 22.0 and 79.5 <= lng <= 88.5) and abs(lng - (80.2 + (lat - 13.0) * 0.7)) < 0.20:
        is_coastal = True
        coastal_label = "Bay of Bengal Coastal Buffer Zone"

    if is_coastal:
        return 45.0, coastal_label

    # 2. Major River Floodplain Basins
    # Narmada River basin (~21.65 - 21.95 N, 72.8 - 75.0 E)
    if 21.65 <= lat <= 21.95 and 72.8 <= lng <= 75.0:
        return 55.0, "Narmada River Alluvial Basin / Seasonal Floodplain"
    # Tapi River basin (~21.05 - 21.35 N, 72.7 - 73.8 E)
    elif 21.05 <= lat <= 21.35 and 72.7 <= lng <= 73.8:
        return 58.0, "Tapi River Floodplain Zone"
    # Sabarmati basin (~22.75 - 23.35 N, 72.5 - 72.75 E)
    elif 22.75 <= lat <= 23.35 and 72.50 <= lng <= 72.75:
        return 65.0, "Sabarmati Watershed Plain"
    # Yamuna / Ganges Gangetic plain (~25.0 - 28.5 N, 77.0 - 86.0 E)
    elif 25.0 <= lat <= 28.5 and 77.0 <= lng <= 86.0 and (abs(lat - (28.6 - (lng - 77.2) * 0.35)) < 0.25):
        return 52.0, "Indo-Gangetic Riparian Basin / Monsoonal Drainage"
    # Rann of Kutch Salt Flat Hazard
    elif 23.6 <= lat <= 24.6 and 68.5 <= lng <= 71.5:
        return 40.0, "Rann Saline Inundation & Seasonal Salt Marsh"

    # 3. Stable Inland Terrain
    return 92.0, "Low Environmental Risk Zone (Stable Inundation Free)"


def get_national_solar_ghi(lat: float, lng: float) -> Tuple[float, str, Dict[str, Any]]:
    """Calibrated Global Horizontal Irradiance (GHI) across all Indian climatic zones."""
    if lat >= 24.5 and lng <= 73.0:
        # Thar Desert (Rajasthan) & Kutch/North Gujarat (Patan, Banaskantha) — Prime Solar
        ghi = 5.9 + (lat - 24.5) * 0.08 - abs(lng - 71.0) * 0.05
    elif 12.0 <= lat <= 20.0 and 74.5 <= lng <= 79.0:
        # Deccan Plateau (Karnataka, Telangana, Maharashtra, AP) — High Solar
        ghi = 5.4 + (20.0 - lat) * 0.03 - abs(lng - 76.5) * 0.04
    elif lat <= 12.0:
        # Southern Peninsular / Coastal (moderate cloud attenuation)
        ghi = 5.1 - (12.0 - lat) * 0.08
    elif lat >= 25.0 and lng >= 77.0:
        # Indo-Gangetic & Eastern Plains (winter haze / monsoonal cloud cover)
        ghi = 5.0 - (lat - 25.0) * 0.06 - (lng - 77.0) * 0.03
    else:
        # Central India / Gujarat Mainland
        ghi = 5.3 + (lat - 21.0) * 0.12 - abs(lng - 72.0) * 0.06

    ghi = round(max(4.1, min(ghi, 6.4)), 2)
    score = round(max(28.0, min((ghi - 4.0) / (6.4 - 4.0) * 70.0 + 28.0, 98.0)), 1)

    if ghi >= 5.8:
        label = f"Prime Solar Belt (GHI: {ghi} kWh/m²/day)"
    elif ghi >= 5.3:
        label = f"High Solar Irradiance (GHI: {ghi} kWh/m²/day)"
    elif ghi >= 4.8:
        label = f"Moderate Solar Potential (GHI: {ghi} kWh/m²/day)"
    else:
        label = f"Sub-optimal Solar Zone (GHI: {ghi} kWh/m²/day)"

    return score, label, {
        "ghi_kwh_m2_day": ghi,
        "annual_generation_mwh_mwp": round(ghi * 365 * 0.78, 0),
        "capacity_utilization_factor_pct": round((ghi / 24.0) * 0.78 * 100, 1)
    }
