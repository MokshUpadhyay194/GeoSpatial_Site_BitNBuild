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
    from backend.spatial.national_gazetteer import COMPREHENSIVE_GAZETTEER
except ImportError:
    from utils.geo_helpers import haversine_distance
    from scoring.decay import gaussian, inverse_distance
    try:
        from spatial.national_gazetteer import COMPREHENSIVE_GAZETTEER
    except ImportError:
        COMPREHENSIVE_GAZETTEER = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. SETTLEMENT HIERARCHY — ALL 33 GUJARAT DISTRICTS + PAN-INDIA HUBS
# ─────────────────────────────────────────────────────────────────────────────

# Known city populations and demographics (calibrated with Census & Municipal data)
KNOWN_POPS: Dict[str, Tuple[int, int, int, str, int]] = {
    'Ahmedabad': (8500000, 18500, 1, 'high', 25),
    'Surat': (6500000, 16000, 1, 'high', 20),
    'Vadodara': (2300000, 9500, 2, 'high', 16),
    'Rajkot': (1900000, 8500, 2, 'medium', 15),
    'Gandhinagar': (450000, 4500, 2, 'high', 12),
    'Bhavnagar': (750000, 5500, 3, 'medium', 12),
    'Jamnagar': (700000, 5000, 3, 'medium', 12),
    'Junagadh': (420000, 4000, 3, 'medium', 10),
    'Anand': (380000, 3800, 3, 'medium', 10),
    'Bharuch': (420000, 3900, 3, 'medium', 10),
    'Mehsana': (340000, 3400, 3, 'medium', 10),
    'Godhra': (290000, 2800, 3, 'medium', 9),
    'Halol': (140000, 2400, 4, 'medium', 8),
    'Dahod': (260000, 2400, 3, 'medium', 9),
    'Palanpur': (270000, 2600, 3, 'medium', 9),
    'Patan': (230000, 2200, 3, 'medium', 8),
    'Himatnagar': (220000, 2300, 3, 'medium', 8),
    'Modasa': (160000, 1900, 4, 'medium', 8),
    'Nadiad': (310000, 3100, 3, 'medium', 9),
    'Lunawada': (140000, 1600, 4, 'medium', 7),
    'Chhota Udepur': (120000, 1400, 4, 'low', 7),
    'Surendranagar': (290000, 2800, 3, 'medium', 9),
    'Morbi': (370000, 3600, 3, 'high', 11),
    'Botad': (190000, 2000, 4, 'medium', 8),
    'Amreli': (210000, 2100, 3, 'medium', 8),
    'Porbandar': (270000, 2600, 3, 'medium', 9),
    'Veraval': (250000, 2500, 3, 'medium', 9),
    'Dwarka': (150000, 1700, 4, 'medium', 8),
    'Bhuj': (280000, 2500, 3, 'medium', 10),
    'Gandhidham': (340000, 3400, 3, 'high', 10),
    'Mundra': (170000, 2200, 4, 'high', 9),
    'Valsad': (260000, 2700, 3, 'medium', 9),
    'Vapi': (310000, 3900, 3, 'high', 10),
    'Navsari': (330000, 3300, 3, 'medium', 9),
    'Vyara': (130000, 1500, 4, 'low', 7),
    'Rajpipla': (140000, 1600, 4, 'medium', 8),
    'Ahwa': (85000, 950, 4, 'low', 6),
}

PAN_INDIA_HUBS: List[Dict[str, Any]] = [
    # Maharashtra
    {'name': 'Mumbai CBD', 'state': 'Maharashtra', 'district': 'Mumbai', 'lat': 18.9256, 'lng': 72.8242, 'pop': 21000000, 'density': 26000, 'tier': 1, 'income': 'high', 'radius_km': 28, 'category': 'benchmark'},
    {'name': 'Bandra Kurla Complex (BKC)', 'state': 'Maharashtra', 'district': 'Mumbai Suburban', 'lat': 19.0667, 'lng': 72.8687, 'pop': 850000, 'density': 22000, 'tier': 1, 'income': 'high', 'radius_km': 10, 'category': 'benchmark'},
    {'name': 'Pune Central', 'state': 'Maharashtra', 'district': 'Pune', 'lat': 18.5204, 'lng': 73.8567, 'pop': 7200000, 'density': 10500, 'tier': 2, 'income': 'high', 'radius_km': 20, 'category': 'city'},
    {'name': 'Hinjawadi IT Corridor, Pune', 'state': 'Maharashtra', 'district': 'Pune', 'lat': 18.5913, 'lng': 73.7389, 'pop': 420000, 'density': 8500, 'tier': 2, 'income': 'high', 'radius_km': 10, 'category': 'industrial'},
    {'name': 'Nagpur', 'state': 'Maharashtra', 'district': 'Nagpur', 'lat': 21.1458, 'lng': 79.0882, 'pop': 2900000, 'density': 5400, 'tier': 2, 'income': 'medium', 'radius_km': 16, 'category': 'city'},
    {'name': 'Nashik', 'state': 'Maharashtra', 'district': 'Nashik', 'lat': 19.9975, 'lng': 73.7898, 'pop': 2000000, 'density': 5000, 'tier': 2, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Chhatrapati Sambhajinagar', 'state': 'Maharashtra', 'district': 'Aurangabad', 'lat': 19.8762, 'lng': 75.3433, 'pop': 1500000, 'density': 5400, 'tier': 3, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Kolhapur', 'state': 'Maharashtra', 'district': 'Kolhapur', 'lat': 16.7050, 'lng': 74.2433, 'pop': 750000, 'density': 4200, 'tier': 3, 'income': 'high', 'radius_km': 12, 'category': 'city'},
    {'name': 'Solapur', 'state': 'Maharashtra', 'district': 'Solapur', 'lat': 17.6599, 'lng': 75.9064, 'pop': 1050000, 'density': 4800, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    # Delhi-NCR
    {'name': 'Connaught Place & New Delhi', 'state': 'Delhi', 'district': 'New Delhi', 'lat': 28.6315, 'lng': 77.2167, 'pop': 30000000, 'density': 23000, 'tier': 1, 'income': 'high', 'radius_km': 30, 'category': 'benchmark'},
    {'name': 'DLF Cyber City & Gurugram', 'state': 'Haryana', 'district': 'Gurugram', 'lat': 28.4950, 'lng': 77.0890, 'pop': 1600000, 'density': 12000, 'tier': 1, 'income': 'high', 'radius_km': 14, 'category': 'benchmark'},
    {'name': 'Noida Sector 62 IT Hub', 'state': 'Uttar Pradesh', 'district': 'Gautam Buddha Nagar', 'lat': 28.6280, 'lng': 77.3680, 'pop': 1200000, 'density': 11000, 'tier': 2, 'income': 'high', 'radius_km': 12, 'category': 'benchmark'},
    # Karnataka
    {'name': 'Bengaluru Central (MG Road)', 'state': 'Karnataka', 'district': 'Bengaluru Urban', 'lat': 12.9716, 'lng': 77.5946, 'pop': 13000000, 'density': 14500, 'tier': 1, 'income': 'high', 'radius_km': 25, 'category': 'city'},
    {'name': 'Whitefield IT Corridor, Bengaluru', 'state': 'Karnataka', 'district': 'Bengaluru Urban', 'lat': 12.9698, 'lng': 77.7500, 'pop': 650000, 'density': 11500, 'tier': 1, 'income': 'high', 'radius_km': 10, 'category': 'benchmark'},
    {'name': 'Mysuru', 'state': 'Karnataka', 'district': 'Mysuru', 'lat': 12.2958, 'lng': 76.6394, 'pop': 1200000, 'density': 4600, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Hubballi-Dharwad', 'state': 'Karnataka', 'district': 'Dharwad', 'lat': 15.3647, 'lng': 75.1240, 'pop': 1150000, 'density': 4400, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Mangaluru Port & City', 'state': 'Karnataka', 'district': 'Dakshina Kannada', 'lat': 12.9141, 'lng': 74.8560, 'pop': 800000, 'density': 4200, 'tier': 3, 'income': 'high', 'radius_km': 12, 'category': 'city'},
    # Telangana & Andhra Pradesh
    {'name': 'Hyderabad CBD', 'state': 'Telangana', 'district': 'Hyderabad', 'lat': 17.3850, 'lng': 78.4867, 'pop': 10500000, 'density': 12500, 'tier': 1, 'income': 'high', 'radius_km': 25, 'category': 'city'},
    {'name': 'HITEC City & Gachibowli, Hyderabad', 'state': 'Telangana', 'district': 'Hyderabad', 'lat': 17.4435, 'lng': 78.3772, 'pop': 750000, 'density': 13000, 'tier': 1, 'income': 'high', 'radius_km': 12, 'category': 'benchmark'},
    {'name': 'Visakhapatnam', 'state': 'Andhra Pradesh', 'district': 'Visakhapatnam', 'lat': 17.6868, 'lng': 83.2185, 'pop': 2400000, 'density': 5200, 'tier': 2, 'income': 'medium', 'radius_km': 15, 'category': 'city'},
    {'name': 'Vijayawada', 'state': 'Andhra Pradesh', 'district': 'NTR', 'lat': 16.5062, 'lng': 80.6480, 'pop': 1800000, 'density': 5600, 'tier': 2, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Guntur', 'state': 'Andhra Pradesh', 'district': 'Guntur', 'lat': 16.3067, 'lng': 80.4365, 'pop': 900000, 'density': 4700, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Tirupati', 'state': 'Andhra Pradesh', 'district': 'Tirupati', 'lat': 13.6288, 'lng': 79.4192, 'pop': 500000, 'density': 3600, 'tier': 3, 'income': 'medium', 'radius_km': 11, 'category': 'city'},
    # Tamil Nadu
    {'name': 'Chennai CBD (Anna Salai)', 'state': 'Tamil Nadu', 'district': 'Chennai', 'lat': 13.0827, 'lng': 80.2707, 'pop': 11500000, 'density': 15500, 'tier': 1, 'income': 'high', 'radius_km': 24, 'category': 'city'},
    {'name': 'OMR IT Corridor, Chennai', 'state': 'Tamil Nadu', 'district': 'Chennai', 'lat': 12.9249, 'lng': 80.2285, 'pop': 550000, 'density': 11000, 'tier': 1, 'income': 'high', 'radius_km': 11, 'category': 'benchmark'},
    {'name': 'Coimbatore', 'state': 'Tamil Nadu', 'district': 'Coimbatore', 'lat': 11.0168, 'lng': 76.9558, 'pop': 2300000, 'density': 5000, 'tier': 2, 'income': 'high', 'radius_km': 15, 'category': 'city'},
    {'name': 'Madurai', 'state': 'Tamil Nadu', 'district': 'Madurai', 'lat': 9.9252, 'lng': 78.1198, 'pop': 1700000, 'density': 5400, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Tiruchirappalli', 'state': 'Tamil Nadu', 'district': 'Tiruchirappalli', 'lat': 10.7905, 'lng': 78.7047, 'pop': 1150000, 'density': 4900, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Salem', 'state': 'Tamil Nadu', 'district': 'Salem', 'lat': 11.6643, 'lng': 78.1460, 'pop': 1000000, 'density': 4600, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    # West Bengal
    {'name': 'Kolkata Central (Park Street)', 'state': 'West Bengal', 'district': 'Kolkata', 'lat': 22.5726, 'lng': 88.3639, 'pop': 15000000, 'density': 24000, 'tier': 1, 'income': 'medium', 'radius_km': 26, 'category': 'city'},
    {'name': 'Salt Lake Sector V, Kolkata', 'state': 'West Bengal', 'district': 'North 24 Parganas', 'lat': 22.5700, 'lng': 88.4340, 'pop': 450000, 'density': 13500, 'tier': 1, 'income': 'high', 'radius_km': 9, 'category': 'benchmark'},
    # Rajasthan
    {'name': 'Jaipur Central', 'state': 'Rajasthan', 'district': 'Jaipur', 'lat': 26.9124, 'lng': 75.7873, 'pop': 4100000, 'density': 6800, 'tier': 2, 'income': 'medium', 'radius_km': 18, 'category': 'city'},
    {'name': 'Jodhpur', 'state': 'Rajasthan', 'district': 'Jodhpur', 'lat': 26.2389, 'lng': 73.0243, 'pop': 1650000, 'density': 4500, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Kota Industrial Hub', 'state': 'Rajasthan', 'district': 'Kota', 'lat': 25.2138, 'lng': 75.8648, 'pop': 1300000, 'density': 4300, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Udaipur', 'state': 'Rajasthan', 'district': 'Udaipur', 'lat': 24.5854, 'lng': 73.7125, 'pop': 700000, 'density': 3400, 'tier': 3, 'income': 'medium', 'radius_km': 12, 'category': 'city'},
    # Uttar Pradesh
    {'name': 'Lucknow Central', 'state': 'Uttar Pradesh', 'district': 'Lucknow', 'lat': 26.8467, 'lng': 80.9462, 'pop': 3900000, 'density': 6200, 'tier': 2, 'income': 'medium', 'radius_km': 18, 'category': 'city'},
    {'name': 'Kanpur Industrial Metro', 'state': 'Uttar Pradesh', 'district': 'Kanpur Nagar', 'lat': 26.4499, 'lng': 80.3319, 'pop': 3200000, 'density': 9800, 'tier': 2, 'income': 'medium', 'radius_km': 18, 'category': 'city'},
    {'name': 'Varanasi', 'state': 'Uttar Pradesh', 'district': 'Varanasi', 'lat': 25.3176, 'lng': 82.9739, 'pop': 1800000, 'density': 6000, 'tier': 3, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Agra', 'state': 'Uttar Pradesh', 'district': 'Agra', 'lat': 27.1767, 'lng': 78.0081, 'pop': 2200000, 'density': 5700, 'tier': 3, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Prayagraj (Allahabad)', 'state': 'Uttar Pradesh', 'district': 'Prayagraj', 'lat': 25.4358, 'lng': 81.8463, 'pop': 1600000, 'density': 5500, 'tier': 3, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Meerut', 'state': 'Uttar Pradesh', 'district': 'Meerut', 'lat': 28.9845, 'lng': 77.7064, 'pop': 1800000, 'density': 6200, 'tier': 2, 'income': 'medium', 'radius_km': 15, 'category': 'city'},
    {'name': 'Bareilly', 'state': 'Uttar Pradesh', 'district': 'Bareilly', 'lat': 28.3670, 'lng': 79.4304, 'pop': 1100000, 'density': 4800, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Aligarh', 'state': 'Uttar Pradesh', 'district': 'Aligarh', 'lat': 27.8974, 'lng': 78.0880, 'pop': 1050000, 'density': 4900, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Gorakhpur', 'state': 'Uttar Pradesh', 'district': 'Gorakhpur', 'lat': 26.7606, 'lng': 83.3732, 'pop': 1200000, 'density': 5100, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    # Madhya Pradesh
    {'name': 'Indore Commercial Hub', 'state': 'Madhya Pradesh', 'district': 'Indore', 'lat': 22.7196, 'lng': 75.8577, 'pop': 3300000, 'density': 6400, 'tier': 2, 'income': 'medium', 'radius_km': 16, 'category': 'city'},
    {'name': 'Bhopal', 'state': 'Madhya Pradesh', 'district': 'Bhopal', 'lat': 23.2599, 'lng': 77.4126, 'pop': 2500000, 'density': 4800, 'tier': 2, 'income': 'medium', 'radius_km': 15, 'category': 'city'},
    {'name': 'Gwalior', 'state': 'Madhya Pradesh', 'district': 'Gwalior', 'lat': 26.2183, 'lng': 78.1828, 'pop': 1400000, 'density': 4400, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Jabalpur', 'state': 'Madhya Pradesh', 'district': 'Jabalpur', 'lat': 23.1815, 'lng': 79.9864, 'pop': 1550000, 'density': 4600, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Ujjain', 'state': 'Madhya Pradesh', 'district': 'Ujjain', 'lat': 23.1765, 'lng': 75.7885, 'pop': 700000, 'density': 3800, 'tier': 3, 'income': 'medium', 'radius_km': 12, 'category': 'city'},
    # Punjab & Chandigarh
    {'name': 'Chandigarh Capital Precinct', 'state': 'Chandigarh', 'district': 'Chandigarh', 'lat': 30.7333, 'lng': 76.7794, 'pop': 1500000, 'density': 9500, 'tier': 2, 'income': 'high', 'radius_km': 14, 'category': 'city'},
    {'name': 'Ludhiana Industrial Hub', 'state': 'Punjab', 'district': 'Ludhiana', 'lat': 30.9010, 'lng': 75.8573, 'pop': 2000000, 'density': 5900, 'tier': 2, 'income': 'high', 'radius_km': 15, 'category': 'city'},
    {'name': 'Amritsar', 'state': 'Punjab', 'district': 'Amritsar', 'lat': 31.6340, 'lng': 74.8723, 'pop': 1400000, 'density': 5100, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Jalandhar', 'state': 'Punjab', 'district': 'Jalandhar', 'lat': 31.3260, 'lng': 75.5762, 'pop': 1100000, 'density': 5200, 'tier': 3, 'income': 'high', 'radius_km': 13, 'category': 'city'},
    # Bihar
    {'name': 'Patna', 'state': 'Bihar', 'district': 'Patna', 'lat': 25.5941, 'lng': 85.1376, 'pop': 2700000, 'density': 7800, 'tier': 2, 'income': 'medium', 'radius_km': 15, 'category': 'city'},
    {'name': 'Gaya', 'state': 'Bihar', 'district': 'Gaya', 'lat': 24.7955, 'lng': 85.0002, 'pop': 650000, 'density': 4100, 'tier': 3, 'income': 'medium', 'radius_km': 11, 'category': 'city'},
    # Odisha
    {'name': 'Bhubaneswar Smart City', 'state': 'Odisha', 'district': 'Khordha', 'lat': 20.2961, 'lng': 85.8245, 'pop': 1400000, 'density': 4600, 'tier': 2, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Cuttack', 'state': 'Odisha', 'district': 'Cuttack', 'lat': 20.4625, 'lng': 85.8828, 'pop': 750000, 'density': 4400, 'tier': 3, 'income': 'medium', 'radius_km': 12, 'category': 'city'},
    {'name': 'Rourkela Steel City', 'state': 'Odisha', 'district': 'Sundargarh', 'lat': 22.2604, 'lng': 84.8536, 'pop': 600000, 'density': 3800, 'tier': 3, 'income': 'high', 'radius_km': 11, 'category': 'industrial'},
    # Kerala
    {'name': 'Kochi Marine & IT Hub', 'state': 'Kerala', 'district': 'Ernakulam', 'lat': 9.9312, 'lng': 76.2673, 'pop': 2400000, 'density': 5800, 'tier': 2, 'income': 'high', 'radius_km': 15, 'category': 'city'},
    {'name': 'Thiruvananthapuram', 'state': 'Kerala', 'district': 'Thiruvananthapuram', 'lat': 8.5241, 'lng': 76.9366, 'pop': 1900000, 'density': 5300, 'tier': 2, 'income': 'high', 'radius_km': 14, 'category': 'city'},
    {'name': 'Kozhikode', 'state': 'Kerala', 'district': 'Kozhikode', 'lat': 11.2588, 'lng': 75.7804, 'pop': 1200000, 'density': 5100, 'tier': 3, 'income': 'high', 'radius_km': 13, 'category': 'city'},
    # Assam & Northeast
    {'name': 'Guwahati Gateway City', 'state': 'Assam', 'district': 'Kamrup Metropolitan', 'lat': 26.1445, 'lng': 91.7362, 'pop': 1400000, 'density': 4200, 'tier': 2, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Shillong', 'state': 'Meghalaya', 'district': 'East Khasi Hills', 'lat': 25.5788, 'lng': 91.8933, 'pop': 250000, 'density': 2800, 'tier': 3, 'income': 'medium', 'radius_km': 10, 'category': 'city'},
    {'name': 'Agartala', 'state': 'Tripura', 'district': 'West Tripura', 'lat': 23.8315, 'lng': 91.2868, 'pop': 450000, 'density': 3600, 'tier': 3, 'income': 'medium', 'radius_km': 11, 'category': 'city'},
    # Chhattisgarh & Jharkhand
    {'name': 'Raipur', 'state': 'Chhattisgarh', 'district': 'Raipur', 'lat': 21.2514, 'lng': 81.6296, 'pop': 1600000, 'density': 4400, 'tier': 2, 'income': 'medium', 'radius_km': 14, 'category': 'city'},
    {'name': 'Bilaspur', 'state': 'Chhattisgarh', 'district': 'Bilaspur', 'lat': 22.0797, 'lng': 82.1391, 'pop': 500000, 'density': 3400, 'tier': 3, 'income': 'medium', 'radius_km': 11, 'category': 'city'},
    {'name': 'Jamshedpur Industrial City', 'state': 'Jharkhand', 'district': 'East Singhbhum', 'lat': 22.8046, 'lng': 86.2029, 'pop': 1650000, 'density': 4700, 'tier': 3, 'income': 'high', 'radius_km': 13, 'category': 'industrial'},
    {'name': 'Ranchi', 'state': 'Jharkhand', 'district': 'Ranchi', 'lat': 23.3441, 'lng': 85.3096, 'pop': 1550000, 'density': 4500, 'tier': 2, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Dhanbad Mining & Coal Hub', 'state': 'Jharkhand', 'district': 'Dhanbad', 'lat': 23.7957, 'lng': 86.4304, 'pop': 1300000, 'density': 4900, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'industrial'},
    # Northern Hills & J&K
    {'name': 'Dehradun', 'state': 'Uttarakhand', 'district': 'Dehradun', 'lat': 30.3165, 'lng': 78.0322, 'pop': 1000000, 'density': 3600, 'tier': 3, 'income': 'medium', 'radius_km': 12, 'category': 'city'},
    {'name': 'Haridwar', 'state': 'Uttarakhand', 'district': 'Haridwar', 'lat': 29.9457, 'lng': 78.1642, 'pop': 400000, 'density': 3500, 'tier': 3, 'income': 'medium', 'radius_km': 11, 'category': 'city'},
    {'name': 'Shimla', 'state': 'Himachal Pradesh', 'district': 'Shimla', 'lat': 31.1048, 'lng': 77.1734, 'pop': 220000, 'density': 2400, 'tier': 3, 'income': 'high', 'radius_km': 9, 'category': 'city'},
    {'name': 'Srinagar', 'state': 'Jammu & Kashmir', 'district': 'Srinagar', 'lat': 34.0837, 'lng': 74.7973, 'pop': 1450000, 'density': 4000, 'tier': 3, 'income': 'medium', 'radius_km': 13, 'category': 'city'},
    {'name': 'Jammu', 'state': 'Jammu & Kashmir', 'district': 'Jammu', 'lat': 32.7266, 'lng': 74.8570, 'pop': 750000, 'density': 3900, 'tier': 3, 'income': 'medium', 'radius_km': 12, 'category': 'city'},
    # Goa
    {'name': 'Panaji Capital', 'state': 'Goa', 'district': 'North Goa', 'lat': 15.4909, 'lng': 73.8278, 'pop': 270000, 'density': 3200, 'tier': 3, 'income': 'high', 'radius_km': 10, 'category': 'city'},
    {'name': 'Margao Commercial Center', 'state': 'Goa', 'district': 'South Goa', 'lat': 15.2832, 'lng': 73.9862, 'pop': 160000, 'density': 2900, 'tier': 3, 'income': 'high', 'radius_km': 9, 'category': 'city'},
]

def _build_all_settlements() -> List[Dict[str, Any]]:
    settlements = []
    seen_names = set()

    for g in COMPREHENSIVE_GAZETTEER:
        name = g['name']
        cat = g.get('category', 'city')
        dist = g.get('district', '')
        lat, lng = g['lat'], g['lng']

        matched_known = None
        for k, val in KNOWN_POPS.items():
            if k.lower() in name.lower() and ('gidc' not in name.lower() and 'ward' not in name.lower()):
                matched_known = val
                break

        if matched_known:
            pop, dens, tier, inc, rad = matched_known
        elif cat in ('ward', 'benchmark'):
            pop = 320000
            dens = 16500
            tier = 1 if any(c in dist for c in ['Ahmedabad', 'Surat', 'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad']) else 2
            inc = 'high'
            rad = 8
        elif cat == 'industrial':
            pop = 95000
            dens = 3400
            tier = 2 if any(c in name for c in ['Sanand', 'Dahej', 'Hazira', 'Vapi', 'Hinjawadi', 'Chakan']) else 3
            inc = 'high' if any(c in name for c in ['Sanand', 'Dahej', 'Hazira', 'Vapi', 'Reliance']) else 'medium'
            rad = 10
        elif 'pilgrim' in g.get('subTitle', '').lower() or 'temple' in g.get('subTitle', '').lower() or 'jyotirlinga' in g.get('subTitle', '').lower():
            pop = 135000
            dens = 3100
            tier = 3
            inc = 'medium'
            rad = 9
        else:
            pop = 145000
            dens = 2800
            tier = 3 if 'Rural' not in dist else 4
            inc = 'medium'
            rad = 8

        state = 'National' if dist in ('Mumbai', 'Mumbai Suburban', 'New Delhi', 'Bengaluru Urban', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Gurugram') else 'Gujarat'
        settlements.append({
            'name': name,
            'state': state,
            'district': dist,
            'lat': lat,
            'lng': lng,
            'pop': pop,
            'density': dens,
            'tier': tier,
            'income': inc,
            'radius_km': rad,
            'category': cat,
        })
        seen_names.add(name.lower())

    for h in PAN_INDIA_HUBS:
        if h['name'].lower() not in seen_names:
            settlements.append(h)
            seen_names.add(h['name'].lower())

    return settlements

ALL_SETTLEMENTS = _build_all_settlements()

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
            (26.449, 74.639), (24.585, 73.712), (23.850, 72.950), (23.597, 73.072),
            (23.022, 72.571), (22.691, 72.863), (22.307, 73.181), (21.705, 72.995),
            (21.170, 72.831), (20.946, 72.952), (20.610, 72.930), (20.389, 72.910),
            (19.076, 72.877), (18.520, 73.856), (16.852, 74.581), (15.849, 74.497),
            (15.364, 75.124), (14.464, 75.921), (13.340, 77.100), (12.971, 77.594),
            (12.916, 79.132), (13.082, 80.270)
        ]
    },
    # NH-47 (Ahmedabad - Sanand - Limbdi - Chotila - Rajkot Corridor)
    {
        "name": "NH-47 Ahmedabad-Rajkot Expressway Link",
        "class": "expressway",
        "points": [
            (23.022, 72.571), (22.986, 72.381), (22.836, 72.361), (22.560, 71.810),
            (22.727, 71.637), (22.420, 71.210), (22.303, 70.802)
        ]
    },
    # NH-8D / NH-151 (Rajkot - Gondal - Jetpur - Junagadh - Keshod - Veraval/Somnath)
    {
        "name": "NH-151 Rajkot-Junagadh-Somnath Corridor",
        "class": "national_highway",
        "points": [
            (22.303, 70.802), (21.960, 70.790), (21.750, 70.620), (21.522, 70.457),
            (21.300, 70.380), (21.150, 70.250), (20.907, 70.367)
        ]
    },
    # NH-51 (Saurashtra Coastal Arterial Corridor)
    {
        "name": "NH-51 Coastal Arterial Corridor",
        "class": "national_highway",
        "points": [
            (22.239, 68.967), (21.641, 69.609), (21.100, 70.120), (20.907, 70.367),
            (20.820, 71.020), (20.910, 71.400), (21.090, 71.770), (21.350, 72.050),
            (21.764, 72.151)
        ]
    },
    # Bharuch - Dahej PCPIR Port Expressway
    {
        "name": "Bharuch-Dahej PCPIR Port Expressway",
        "class": "expressway",
        "points": [
            (21.705, 72.995), (21.680, 72.820), (21.710, 72.580)
        ]
    },
    # NH-27 (Porbandar - Rajkot - Morbi - Samakhiali - Palanpur)
    {
        "name": "NH-27 East-West Arterial Corridor",
        "class": "national_highway",
        "points": [
            (21.641, 69.609), (21.750, 70.250), (22.303, 70.802), (22.812, 70.838),
            (23.250, 70.600), (23.480, 71.050), (23.830, 71.600), (24.172, 72.434),
            (24.585, 73.712), (24.888, 74.626), (25.213, 75.864), (25.448, 78.568),
            (26.449, 80.331), (26.846, 80.946), (26.760, 83.373), (26.120, 85.360),
            (25.770, 87.470), (26.727, 88.395), (26.144, 91.736)
        ]
    },
    # NH-41 / SH-41 (Ahmedabad - Kalol - Mehsana - Siddhpur - Patan - Palanpur)
    {
        "name": "North Gujarat Arterial (SH-41 / NH-58)",
        "class": "state_highway",
        "points": [
            (23.022, 72.571), (23.215, 72.636), (23.242, 72.498), (23.588, 72.369),
            (23.850, 72.130), (24.172, 72.434), (24.330, 72.850)
        ]
    },
    # NH-53 (Surat - Bardoli - Vyara - Songadh - Dhule)
    {
        "name": "NH-53 Surat-Dhule Trans-National Highway",
        "class": "national_highway",
        "points": [
            (21.100, 72.680), (21.170, 72.831), (21.120, 73.110), (21.112, 73.402),
            (21.160, 73.610), (20.900, 74.770)
        ]
    },
    # Vadodara - Halol - Godhra - Dahod Corridor (NH-47 / SH-5)
    {
        "name": "Vadodara-Halol-Godhra-Dahod Corridor",
        "class": "national_highway",
        "points": [
            (22.307, 73.181), (22.498, 73.473), (22.775, 73.614), (22.836, 74.255)
        ]
    },
    # NH-44 (North-South Grand Corridor)
    {
        "name": "NH-44 North-South Grand Corridor",
        "class": "expressway",
        "points": [
            (34.083, 74.797), (32.726, 74.857), (31.634, 74.872), (30.901, 75.857),
            (29.390, 76.963), (28.614, 77.209), (27.176, 78.008), (26.218, 78.182),
            (25.448, 78.568), (24.180, 78.740), (21.145, 79.088), (19.664, 78.532),
            (17.385, 78.486), (15.828, 78.037), (14.681, 77.600), (12.971, 77.594),
            (11.664, 78.146), (9.925, 78.119), (8.256, 77.545)
        ]
    },
    # NH-19 (Delhi - Kanpur - Varanasi - Kolkata)
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
    # NH-52 (Jaipur - Kota - Indore)
    {
        "name": "NH-52 Jaipur-Kota-Indore Corridor",
        "class": "national_highway",
        "points": [
            (26.912, 75.787), (25.213, 75.864), (24.500, 75.800), (23.176, 75.788),
            (22.719, 75.857)
        ]
    },
    # NH-65 (Pune - Solapur - Hyderabad - Vijayawada)
    {
        "name": "NH-65 Pune-Hyderabad-Vijayawada Corridor",
        "class": "national_highway",
        "points": [
            (18.520, 73.856), (17.659, 75.906), (17.385, 78.486), (16.506, 80.648)
        ]
    }
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

    decay = gaussian(dist_m, sigma=max(radius_m * 0.75, 4000.0))

    norm_pop = min(settlement["pop"] / 2000000.0, 1.0)
    density_factor = min(settlement["density"] / 14000.0, 1.0)

    urban_influence = (norm_pop * 0.40 + density_factor * 0.60) * decay

    if 24.5 <= lat <= 28.5 and 80.0 <= lng <= 88.0:
        rural_base = 45.0
    elif 20.0 <= lat <= 24.8 and 68.0 <= lng <= 74.5:
        rural_base = 38.0
    elif 11.0 <= lat <= 15.0:
        rural_base = 42.0
    elif 25.0 <= lat <= 28.5 and 69.5 <= lng <= 73.5:
        rural_base = 24.0
    elif lat >= 23.5 and lng <= 70.5:
        rural_base = 26.0
    else:
        rural_base = 35.0

    score = rural_base + (urban_influence * (96.0 - rural_base))
    score = round(max(22.0, min(score, 98.0)), 1)

    est_catchment_pop = int(max(400, settlement["pop"] * (0.05 + 0.95 * decay) * 0.22))

    if dist_m <= radius_m * 0.4:
        label = f"Urban Core — {settlement['name']} ({settlement['district']})"
    elif dist_m <= radius_m * 1.0:
        label = f"Suburban Growth Belt — {settlement['name']} ({dist_m / 1000:.1f}km)"
    elif dist_m <= radius_m * 2.0:
        label = f"Perimeter Hinterland — {settlement['name']} Transit Influence"
    else:
        label = f"Rural Agricultural Basin ({settlement['district']} District)"

    return score, label, est_catchment_pop, settlement["income"]


def get_hierarchical_transport_score(lat: float, lng: float) -> Tuple[float, str]:
    """Calculate distance-decay transportation accessibility score across India."""
    dist_m, corridor_name = get_hierarchical_transport(lat, lng)

    if dist_m <= 1000:
        score = 94.0 + min((1000 - dist_m) / 1000.0 * 4.0, 4.0)
        label = f"Direct Highway Frontage (< 1km to {corridor_name})"
    elif dist_m <= 4000:
        score = 82.0 + (4000 - dist_m) / 3000.0 * 12.0
        label = f"High Arterial Connectivity ({dist_m / 1000:.1f}km to {corridor_name})"
    elif dist_m <= 12000:
        score = 64.0 + (12000 - dist_m) / 8000.0 * 18.0
        label = f"Regional Highway Link ({dist_m / 1000:.1f}km to {corridor_name})"
    elif dist_m <= 25000:
        score = 48.0 + (25000 - dist_m) / 13000.0 * 16.0
        label = f"Secondary Feeder Access ({dist_m / 1000:.1f}km to {corridor_name})"
    else:
        score = max(32.0, 48.0 - (dist_m - 25000) / 25000.0 * 16.0)
        label = f"Remote Feeder Route (> 25km to {corridor_name})"

    return round(score, 1), label


def get_hierarchical_poi_score(lat: float, lng: float) -> Tuple[float, str]:
    """Calculate commercial POI and retail density across India."""
    settlement, dist_m = get_hierarchical_settlement(lat, lng)
    trans_dist_m, corr_name = get_hierarchical_transport(lat, lng)
    radius_m = settlement["radius_km"] * 1000.0

    urban_decay = gaussian(dist_m, sigma=radius_m * 0.65)
    hwy_decay = gaussian(trans_dist_m, sigma=2200.0)

    cat = settlement.get("category", "city")
    tier = settlement.get("tier", 3)

    if cat in ("ward", "benchmark") or tier == 1:
        cat_mult = 1.0
        base_poi = 48.0
    elif cat == "industrial":
        cat_mult = 0.85
        base_poi = 42.0
    elif tier == 2:
        cat_mult = 0.80
        base_poi = 38.0
    elif tier == 3:
        cat_mult = 0.70
        base_poi = 34.0
    else:
        cat_mult = 0.55
        base_poi = 30.0

    density_val = (urban_decay * 0.7 + hwy_decay * 0.3) * cat_mult
    score = base_poi + min(density_val * 50.0, 50.0)
    score = round(min(max(score, 25.0), 98.0), 1)

    if score >= 80:
        label = f"Dense Commercial Cluster — {settlement['name']}"
    elif score >= 60:
        label = f"Active Retail & Commercial Precinct — {settlement['name']}"
    elif score >= 45:
        label = f"Highway Commercial & Service Node ({corr_name})"
    else:
        label = f"Dispersed Local Convenience Nodes ({settlement['district']} District)"

    return score, label


def get_hierarchical_landuse_score(lat: float, lng: float, site_type: str = "ev_charging") -> Tuple[float, str]:
    """Classify and score land use compatibility for any location in India."""
    settlement, dist_m = get_hierarchical_settlement(lat, lng)
    trans_dist_m, _ = get_hierarchical_transport(lat, lng)
    radius_m = settlement["radius_km"] * 1000.0
    cat = settlement.get("category", "city")

    is_core = dist_m <= radius_m * 0.4
    is_suburban = radius_m * 0.4 < dist_m <= radius_m * 1.1
    is_industrial_hub = (cat == "industrial") or ("GIDC" in settlement["name"]) or ("SIR" in settlement["name"]) or ("Port" in settlement["name"])

    is_wasteland = (lat >= 23.3 and lng <= 70.8) or (lat >= 25.5 and lng <= 72.5)

    if is_industrial_hub:
        zone = f"Industrial GIDC & Logistics Corridor — {settlement['name']}"
        ev_score = 82.0
        retail_score = 48.0
        warehouse_score = 96.0
        solar_score = 72.0
        wind_score = 70.0
        telecom_score = 80.0
    elif is_wasteland:
        zone = "Revenue Wasteland / Open Scrub"
        ev_score = 35.0
        retail_score = 25.0
        warehouse_score = 65.0
        solar_score = 96.0
        wind_score = 94.0
        telecom_score = 65.0
    elif is_core and (cat in ("ward", "benchmark") or settlement.get("tier", 3) <= 2):
        zone = f"Commercial & High-Density Mixed Urban Zone — {settlement['name']}"
        ev_score = 92.0
        retail_score = 95.0
        warehouse_score = 35.0
        solar_score = 25.0
        wind_score = 20.0
        telecom_score = 88.0
    elif is_core or is_suburban:
        zone = f"Urban Municipal & Commercial Zone — {settlement['name']}"
        ev_score = 80.0
        retail_score = 78.0
        warehouse_score = 72.0
        solar_score = 55.0
        wind_score = 50.0
        telecom_score = 82.0
    elif trans_dist_m <= 2500.0:
        zone = "Highway Commercial & Transport Frontage Ribbon"
        ev_score = 88.0
        retail_score = 72.0
        warehouse_score = 92.0
        solar_score = 70.0
        wind_score = 70.0
        telecom_score = 78.0
    else:
        zone = f"Agricultural & Rural Alluvial Plain ({settlement['district']} District)"
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
    is_coastal = False
    coastal_label = ""
    if (22.2 <= lat <= 23.1 and 69.0 <= lng <= 70.5) or (21.0 <= lat <= 22.2 and 72.0 <= lng <= 72.52):
        is_coastal = True
        coastal_label = "Coastal Regulation Zone / Marine Tidal Area"
    elif (8.0 <= lat <= 20.5 and 72.5 <= lng <= 76.5) and abs(lng - (72.8 + (lat - 19.0) * -0.05)) < 0.15:
        is_coastal = True
        coastal_label = "Arabian Sea Coastal Buffer Zone"
    elif (10.0 <= lat <= 22.0 and 79.5 <= lng <= 88.5) and abs(lng - (80.2 + (lat - 13.0) * 0.7)) < 0.20:
        is_coastal = True
        coastal_label = "Bay of Bengal Coastal Buffer Zone"

    if is_coastal:
        return 45.0, coastal_label

    if 21.65 <= lat <= 21.95 and 72.8 <= lng <= 75.0:
        return 55.0, "Narmada River Alluvial Basin / Seasonal Floodplain"
    elif 21.05 <= lat <= 21.35 and 72.7 <= lng <= 73.8:
        return 58.0, "Tapi River Floodplain Zone"
    elif 22.75 <= lat <= 23.35 and 72.50 <= lng <= 72.75:
        return 65.0, "Sabarmati Watershed Plain"
    elif 25.0 <= lat <= 28.5 and 77.0 <= lng <= 86.0 and (abs(lat - (28.6 - (lng - 77.2) * 0.35)) < 0.25):
        return 52.0, "Indo-Gangetic Riparian Basin / Monsoonal Drainage"
    elif 23.6 <= lat <= 24.6 and 68.5 <= lng <= 71.5:
        return 40.0, "Rann Saline Inundation & Seasonal Salt Marsh"

    return 92.0, "Low Environmental Risk Zone (Stable Inundation Free)"


def get_national_solar_ghi(lat: float, lng: float) -> Tuple[float, str, Dict[str, Any]]:
    """Calibrated Global Horizontal Irradiance (GHI) across all Indian climatic zones."""
    if lat >= 24.5 and lng <= 73.0:
        ghi = 5.9 + (lat - 24.5) * 0.08 - abs(lng - 71.0) * 0.05
    elif 12.0 <= lat <= 20.0 and 74.5 <= lng <= 79.0:
        ghi = 5.4 + (20.0 - lat) * 0.03 - abs(lng - 76.5) * 0.04
    elif lat <= 12.0:
        ghi = 5.1 - (12.0 - lat) * 0.08
    elif lat >= 25.0 and lng >= 77.0:
        ghi = 5.0 - (lat - 25.0) * 0.06 - (lng - 77.0) * 0.03
    else:
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
