"""Comprehensive Nationwide and All-33 Gujarat Districts Gazetteer.

Contains curated spatial records for:
- All 33 Gujarat District HQs
- All major Gujarat Talukas, Sub-districts, Municipal Wards, Ports, and GIDCs
- Premier National Metros, Tech Corridors, and Renewable Epicenters
"""

from typing import List, Dict, Any

COMPREHENSIVE_GAZETTEER: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. AHMEDABAD (Urban, Rural & Industrial Talukas)
    # =========================================================================
    {"id": "loc-sg-highway", "name": "SG Highway Commercial Corridor", "subTitle": "Bodakdev - Thaltej - Sola Arterial Axis, Ahmedabad", "lat": 23.0378, "lng": 72.5112, "category": "benchmark", "district": "Ahmedabad"},
    {"id": "loc-bodakdev", "name": "Bodakdev Urban Ward", "subTitle": "SG Highway Judges Bungalow Precinct, Ahmedabad", "lat": 23.0373, "lng": 72.5074, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-sbr", "name": "Sindhu Bhavan Road (SBR)", "subTitle": "High-Street Retail & Corporate Corridor, Ahmedabad", "lat": 23.0450, "lng": 72.4980, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-prahladnagar", "name": "Prahlad Nagar Corporate Road", "subTitle": "Makarba - Vejalpur Commercial Zone, Ahmedabad", "lat": 23.0125, "lng": 72.5085, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-satellite", "name": "Satellite & Shivranjani", "subTitle": "Dense Mixed Commercial Residential Hub, Ahmedabad", "lat": 23.0305, "lng": 72.5178, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-vastrapur", "name": "Vastrapur Lake & IIM Ahmedabad", "subTitle": "Institutional & Premium Retail District, Ahmedabad", "lat": 23.0350, "lng": 72.5293, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-navrangpura", "name": "Navrangpura Commercial District", "subTitle": "CG Road, Municipal Market & Law Garden, Ahmedabad", "lat": 23.0365, "lng": 72.5611, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-bopal", "name": "Bopal & South Bopal (SOBO)", "subTitle": "Rapidly Expanding Western Residential Suburban Hub, Ahmedabad", "lat": 23.0338, "lng": 72.4646, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-thaltej", "name": "Thaltej Commercial & Shilaj Axis", "subTitle": "West Ahmedabad Transit Oriented Corridor, Ahmedabad", "lat": 23.0543, "lng": 72.5085, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-gota", "name": "Gota & SG Highway North", "subTitle": "Sarkhej-Gandhinagar High-Density Urban Expansion, Ahmedabad", "lat": 23.1070, "lng": 72.5410, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-chandkheda", "name": "Chandkheda & Motera Stadium Precinct", "subTitle": "Narendra Modi Stadium Urban Transit Hub, Ahmedabad", "lat": 23.1022, "lng": 72.5975, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-maninagar", "name": "Maninagar & Kankaria Lake Front", "subTitle": "South Ahmedabad Commercial & Cultural Epicenter, Ahmedabad", "lat": 22.9978, "lng": 72.6026, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-nikol", "name": "Nikol & Naroda Industrial Axis", "subTitle": "East Ahmedabad Commercial Trading & Industrial Ward, Ahmedabad", "lat": 23.0510, "lng": 72.6680, "category": "ward", "district": "Ahmedabad"},
    {"id": "loc-sanand-gidc", "name": "Sanand GIDC Mega Automotive Corridor", "subTitle": "Heavy Industrial & Auto OEM Cluster, Ahmedabad Rural", "lat": 22.9868, "lng": 72.3814, "category": "benchmark", "district": "Ahmedabad Rural"},
    {"id": "loc-changodar", "name": "Changodar Industrial & Logistics Park", "subTitle": "Sarkhej-Bavla National Highway Freight Corridor, Ahmedabad Rural", "lat": 22.9234, "lng": 72.4285, "category": "industrial", "district": "Ahmedabad Rural"},
    {"id": "loc-bavla", "name": "Bavla Industrial & Grain Hub", "subTitle": "NH-47 Rice Milling & Engineering Cluster, Ahmedabad Rural", "lat": 22.8360, "lng": 72.3610, "category": "city", "district": "Ahmedabad Rural"},
    {"id": "loc-dholka", "name": "Dholka Historical & Pharma Town", "subTitle": "Pharmaceutical & Engineering Manufacturing Taluka, Ahmedabad Rural", "lat": 22.7200, "lng": 72.4400, "category": "city", "district": "Ahmedabad Rural"},
    {"id": "loc-viramgam", "name": "Viramgam Railway Junction & Commercial Hub", "subTitle": "Major Rail Logistics & Cotton Processing Taluka, Ahmedabad Rural", "lat": 23.1250, "lng": 72.0350, "category": "city", "district": "Ahmedabad Rural"},
    {"id": "loc-mandal", "name": "Mandal Industrial Node", "subTitle": "Mandal-Becharaji Special Investment Region, Ahmedabad Rural", "lat": 23.2800, "lng": 71.9150, "category": "industrial", "district": "Ahmedabad Rural"},
    {"id": "loc-detroj", "name": "Detroj-Rampura Taluka Center", "subTitle": "North Ahmedabad Agri-Logistics & Rail Junction, Ahmedabad Rural", "lat": 23.3320, "lng": 72.1880, "category": "city", "district": "Ahmedabad Rural"},
    {"id": "loc-dhandhuka", "name": "Dhandhuka Regional Gateway", "subTitle": "Bhal Region Agricultural & Cotton Commercial Taluka, Ahmedabad Rural", "lat": 22.3700, "lng": 71.9800, "category": "city", "district": "Ahmedabad Rural"},
    {"id": "loc-dholera-sir", "name": "Dholera Special Investment Region (SIR)", "subTitle": "Greenfield Smart Industrial City & Semiconductor Node, Ahmedabad Rural", "lat": 22.2472, "lng": 72.1908, "category": "industrial", "district": "Ahmedabad Rural"},

    # =========================================================================
    # 2. GANDHINAGAR (Capital & Talukas)
    # =========================================================================
    {"id": "loc-gift-city", "name": "GIFT City International FinTech Zone", "subTitle": "India's Flagship IFSC Smart City, Gandhinagar", "lat": 23.1601, "lng": 72.6841, "category": "benchmark", "district": "Gandhinagar"},
    {"id": "loc-gandhinagar-central", "name": "Gandhinagar Central (Sector 10-21)", "subTitle": "Capital Administrative & Secretariat Sector, Gandhinagar", "lat": 23.2156, "lng": 72.6369, "category": "city", "district": "Gandhinagar"},
    {"id": "loc-infocity", "name": "Infocity IT & Software Park", "subTitle": "Major IT/ITES Corridor & Innovation Hub, Gandhinagar", "lat": 23.1904, "lng": 72.6288, "category": "industrial", "district": "Gandhinagar"},
    {"id": "loc-kudasan", "name": "Kudasan & Raysan Urban Corridor", "subTitle": "High-Density Residential & Commercial Hub, Gandhinagar", "lat": 23.1760, "lng": 72.6320, "category": "ward", "district": "Gandhinagar"},
    {"id": "loc-sargasan", "name": "Sargasan Cross Roads & SG Highway Extension", "subTitle": "Retail & Mixed-Use Corporate Corridor, Gandhinagar", "lat": 23.1950, "lng": 72.6020, "category": "ward", "district": "Gandhinagar"},
    {"id": "loc-kalol-gandhinagar", "name": "Kalol GIDC Industrial Estate", "subTitle": "Heavy Engineering, Chemicals & Textile Hub, Gandhinagar", "lat": 23.2420, "lng": 72.4980, "category": "industrial", "district": "Gandhinagar"},
    {"id": "loc-mansa", "name": "Mansa Commercial & Agricultural Town", "subTitle": "North Gandhinagar Agricultural Market & Taluka Center", "lat": 23.4250, "lng": 72.6600, "category": "city", "district": "Gandhinagar"},
    {"id": "loc-dehgam", "name": "Dehgam Industrial & Transport Node", "subTitle": "East Gandhinagar Agro-Trading & GIDC Taluka Center", "lat": 23.1680, "lng": 72.8120, "category": "city", "district": "Gandhinagar"},

    # =========================================================================
    # 3. VADODARA (CBD, Wards & Rural Talukas)
    # =========================================================================
    {"id": "loc-vadodara-central", "name": "Vadodara Central Business District", "subTitle": "Sayajigunj, Station Area & Alkapuri, Vadodara", "lat": 22.3072, "lng": 73.1812, "category": "city", "district": "Vadodara"},
    {"id": "loc-vadodara-alkapuri", "name": "Alkapuri Central Commercial Hub", "subTitle": "R.C. Dutt Road Premier Business District, Vadodara", "lat": 22.3106, "lng": 73.1812, "category": "benchmark", "district": "Vadodara"},
    {"id": "loc-vadodara-akota", "name": "Akota & Gotri Commercial Corridor", "subTitle": "West Vadodara High-Density Retail & Healthcare Axis", "lat": 22.3015, "lng": 73.1614, "category": "ward", "district": "Vadodara"},
    {"id": "loc-vadodara-makarpura", "name": "Makarpura GIDC Industrial Estate", "subTitle": "Major Electrical & Heavy Engineering Hub, Vadodara", "lat": 22.2536, "lng": 73.1950, "category": "industrial", "district": "Vadodara"},
    {"id": "loc-manjalpur", "name": "Manjalpur Urban Commercial Hub", "subTitle": "South Vadodara High-Street Retail & Residential Zone, Vadodara", "lat": 22.2680, "lng": 73.1920, "category": "ward", "district": "Vadodara"},
    {"id": "loc-karelibaug", "name": "Karelibaug & Fatehgunj Civic Precinct", "subTitle": "Heritage & Educational University District, Vadodara", "lat": 22.3250, "lng": 73.1980, "category": "ward", "district": "Vadodara"},
    {"id": "loc-nandesari-gidc", "name": "Nandesari GIDC Petrochemical Complex", "subTitle": "Bulk Drugs, Intermediates & Chemical Industrial Belt, Vadodara", "lat": 22.4100, "lng": 73.0900, "category": "industrial", "district": "Vadodara"},
    {"id": "loc-padra", "name": "Padra Pharma & Agri Taluka", "subTitle": "Major Pharmaceutical Formulation Cluster, Vadodara Rural", "lat": 22.2350, "lng": 73.0850, "category": "city", "district": "Vadodara Rural"},
    {"id": "loc-savli-gidc", "name": "Savli GIDC Mega Engineering SEZ", "subTitle": "Bombardier Rail & Heavy Power Equipment Cluster, Vadodara Rural", "lat": 22.5600, "lng": 73.2200, "category": "industrial", "district": "Vadodara Rural"},
    {"id": "loc-karjan", "name": "Karjan NH-48 Transport & Agro Hub", "subTitle": "National Highway Corridor & Cotton Trading Taluka, Vadodara Rural", "lat": 22.0520, "lng": 73.1200, "category": "city", "district": "Vadodara Rural"},
    {"id": "loc-dabhoi", "name": "Dabhoi Heritage Fort & Commercial Node", "subTitle": "Historic Fortified Town & Narrow Gauge Rail Capital, Vadodara Rural", "lat": 22.1800, "lng": 73.4300, "category": "city", "district": "Vadodara Rural"},
    {"id": "loc-shinor", "name": "Shinor Narmada Riverfront Town", "subTitle": "Agri-Trading & Riverine Horticultural Taluka, Vadodara Rural", "lat": 21.9150, "lng": 73.3400, "category": "city", "district": "Vadodara Rural"},

    # =========================================================================
    # 4. SURAT (Textile, Diamond & Coastal Talukas)
    # =========================================================================
    {"id": "loc-surat-central", "name": "Surat Central & Ring Road Textile Market", "subTitle": "Asia's Premier Textile & Fabric Trading Capital, Surat", "lat": 21.1959, "lng": 72.8302, "category": "city", "district": "Surat"},
    {"id": "loc-surat-vesu", "name": "Vesu Commercial Luxury Retail Hub", "subTitle": "South Surat High-Density Premium Corridor, Surat", "lat": 21.1442, "lng": 72.7712, "category": "ward", "district": "Surat"},
    {"id": "loc-surat-diamond-bourse", "name": "Surat Diamond Bourse (DREAM City)", "subTitle": "Khajod Global Gems & Jewelry Trading Capital, Surat", "lat": 21.1219, "lng": 72.7661, "category": "benchmark", "district": "Surat"},
    {"id": "loc-surat-hazira", "name": "Hazira Port Industrial Belt", "subTitle": "Deep-Water LNG, Steel & Heavy Petrochemical Terminal, Surat", "lat": 21.1158, "lng": 72.6482, "category": "industrial", "district": "Surat"},
    {"id": "loc-adajan", "name": "Adajan & Pal Riverside Precinct", "subTitle": "West Surat High-Density Commercial & Residential Corridor, Surat", "lat": 21.1980, "lng": 72.7950, "category": "ward", "district": "Surat"},
    {"id": "loc-piplod", "name": "Piplod & Dumas Road Leisure Hub", "subTitle": "Entertainment, Mall & Hospitality Strip, Surat", "lat": 21.1550, "lng": 72.7580, "category": "ward", "district": "Surat"},
    {"id": "loc-sachin-gidc", "name": "Sachin GIDC Textile & Diamond SEZ", "subTitle": "Export Processing Zone & Chemical Manufacturing, Surat", "lat": 21.0850, "lng": 72.8800, "category": "industrial", "district": "Surat"},
    {"id": "loc-pandesara-gidc", "name": "Pandesara GIDC Industrial Estate", "subTitle": "Dyeing, Printing & Synthetic Fabric Cluster, Surat", "lat": 21.1400, "lng": 72.8350, "category": "industrial", "district": "Surat"},
    {"id": "loc-katargam", "name": "Katargam Diamond Cutting Hub", "subTitle": "Global Rough Diamond Processing Epicenter, Surat", "lat": 21.2250, "lng": 72.8350, "category": "ward", "district": "Surat"},
    {"id": "loc-bardoli", "name": "Bardoli Sugar & Agro-Industrial Capital", "subTitle": "Asia's Largest Sugar Factory & Historical Freedom Hub, Surat", "lat": 21.1200, "lng": 73.1100, "category": "city", "district": "Surat"},
    {"id": "loc-olpad", "name": "Olpad Aquaculture & Gas Exploration Node", "subTitle": "Coastal Shrimp Farming & Petrochemical Taluka, Surat", "lat": 21.3300, "lng": 72.7500, "category": "city", "district": "Surat"},
    {"id": "loc-kamrej", "name": "Kamrej NH-48 Transport & Transit Node", "subTitle": "Major Freight Gateway to North Gujarat & Mumbai, Surat", "lat": 21.2700, "lng": 72.9600, "category": "city", "district": "Surat"},
    {"id": "loc-palsana", "name": "Palsana Textile Industrial Corridor", "subTitle": "Synthetic Yarn Weaving & Modern Powerlooms Node, Surat", "lat": 21.0800, "lng": 72.9800, "category": "industrial", "district": "Surat"},

    # =========================================================================
    # 5. RAJKOT (Engineering, Foundry & Saurashtra Heart)
    # =========================================================================
    {"id": "loc-rajkot-ringroad", "name": "150 Feet Ring Road Commercial Axis", "subTitle": "West Rajkot Retail, Hospitality & Healthcare Corridor, Rajkot", "lat": 22.2850, "lng": 70.7680, "category": "city", "district": "Rajkot"},
    {"id": "loc-rajkot-central", "name": "Rajkot Central & Yagnik Road", "subTitle": "Saurashtra Commercial & Financial Epicenter, Rajkot", "lat": 22.3039, "lng": 70.8022, "category": "city", "district": "Rajkot"},
    {"id": "loc-rajkot-aji", "name": "Aji GIDC & Shapar Industrial Zone", "subTitle": "Engineering, Casting & Diesel Engine Capital, Rajkot", "lat": 22.2514, "lng": 70.8142, "category": "industrial", "district": "Rajkot"},
    {"id": "loc-metoda-gidc", "name": "Metoda GIDC Auto Component Cluster", "subTitle": "Precision Engineering, Bearings & Machine Tools SEZ, Rajkot", "lat": 22.2400, "lng": 70.6900, "category": "industrial", "district": "Rajkot"},
    {"id": "loc-gondal", "name": "Gondal Heritage Palace & Agri Mandi", "subTitle": "Gujarat's Largest Red Chilli & Groundnut Mandi, Rajkot", "lat": 21.9600, "lng": 70.8000, "category": "city", "district": "Rajkot"},
    {"id": "loc-jetpur", "name": "Jetpur Block Print & Saree Dyeing Hub", "subTitle": "World-Renowned Cotton Printing & Dyeing Cluster, Rajkot", "lat": 21.7550, "lng": 70.6200, "category": "city", "district": "Rajkot"},
    {"id": "loc-dhoraji", "name": "Dhoraji Plastic & Oil Milling Town", "subTitle": "Recycled Plastic Processing & Groundnut Oil Taluka, Rajkot", "lat": 21.7300, "lng": 70.4500, "category": "city", "district": "Rajkot"},
    {"id": "loc-upleta", "name": "Upleta Agri-Logistics & Cotton Hub", "subTitle": "Moj River Basin Agricultural Trading Taluka, Rajkot", "lat": 21.7350, "lng": 70.2800, "category": "city", "district": "Rajkot"},
    {"id": "loc-jasdan", "name": "Jasdan Brass & Farm Implement Hub", "subTitle": "Agricultural Machinery & Automobile Repair Cluster, Rajkot", "lat": 22.0300, "lng": 71.2000, "category": "city", "district": "Rajkot"},

    # =========================================================================
    # 6. BHAVNAGAR & BOTAD
    # =========================================================================
    {"id": "loc-bhavnagar-city", "name": "Bhavnagar Central & Waghawadi Road", "subTitle": "Commercial High-Street & Civic Center, Bhavnagar", "lat": 21.7645, "lng": 72.1519, "category": "city", "district": "Bhavnagar"},
    {"id": "loc-alang-shipyard", "name": "Alang Ship Recycling & Marine Yard", "subTitle": "World's Largest Ship Breaking Cluster, Bhavnagar", "lat": 21.4167, "lng": 72.1833, "category": "industrial", "district": "Bhavnagar"},
    {"id": "loc-bhavnagar-chitra", "name": "Chitra GIDC Industrial Estate", "subTitle": "Plastics, Chemicals & Small-Scale Manufacturing, Bhavnagar", "lat": 21.7856, "lng": 72.1124, "category": "industrial", "district": "Bhavnagar"},
    {"id": "loc-sihor", "name": "Sihor Steel Rolling & Ceramic Hub", "subTitle": "Re-rolling Mills & Historical Brass Metal Cluster, Bhavnagar", "lat": 21.7000, "lng": 71.9600, "category": "industrial", "district": "Bhavnagar"},
    {"id": "loc-palitana", "name": "Palitana Shatrunjaya Heritage Shrine", "subTitle": "World-Renowned Sacred Jain Temple City, Bhavnagar", "lat": 21.5200, "lng": 71.8300, "category": "city", "district": "Bhavnagar"},
    {"id": "loc-talaja", "name": "Talaja Rock-Cut Buddhist Caves & Mandi", "subTitle": "Shetrunji River Basin Agricultural & Trading Town, Bhavnagar", "lat": 21.3500, "lng": 72.0400, "category": "city", "district": "Bhavnagar"},
    {"id": "loc-mahuva", "name": "Mahuva Onion & Dehydration Capital", "subTitle": "India's Dehydrated White Onion & Coastal Coconut Port, Bhavnagar", "lat": 21.0900, "lng": 71.7600, "category": "city", "district": "Bhavnagar"},
    {"id": "loc-botad-city", "name": "Botad Central Diamond & Cotton Mandi", "subTitle": "District Headquarters & Diamond Cutting Hub, Botad", "lat": 22.1700, "lng": 71.6600, "category": "city", "district": "Botad"},
    {"id": "loc-gadhada", "name": "Gadhada Swaminarayan Heritage Shrine", "subTitle": "Gopinathji Temple Pilgrimage & Agricultural Center, Botad", "lat": 21.9700, "lng": 71.5700, "category": "city", "district": "Botad"},
    {"id": "loc-sarangpur", "name": "Sarangpur Kashtbhanjan Hanuman Shrine", "subTitle": "Major Spiritual Pilgrimage Epicenter, Botad", "lat": 22.1400, "lng": 71.7400, "category": "city", "district": "Botad"},

    # =========================================================================
    # 7. JAMNAGAR & DEVBHUMI DWARKA
    # =========================================================================
    {"id": "loc-jamnagar-refinery", "name": "Jamnagar Petrochemical & Refining Belt", "subTitle": "Motikhavdi World-Scale Refinery Complex, Jamnagar", "lat": 22.4707, "lng": 70.0577, "category": "benchmark", "district": "Jamnagar"},
    {"id": "loc-jamnagar-city", "name": "Jamnagar City & Brass Parts Cluster", "subTitle": "Precision Hardware & Commercial Center, Jamnagar", "lat": 22.4707, "lng": 70.0724, "category": "city", "district": "Jamnagar"},
    {"id": "loc-dared-gidc", "name": "Dared GIDC Brass Parts Estate", "subTitle": "National Brass Extrusions & Electrical Components, Jamnagar", "lat": 22.4300, "lng": 70.0650, "category": "industrial", "district": "Jamnagar"},
    {"id": "loc-dhrol", "name": "Dhrol Historical Town & Agri Mandi", "subTitle": "Bhutarmori Historic Plains & Trading Taluka, Jamnagar", "lat": 22.5600, "lng": 70.4150, "category": "city", "district": "Jamnagar"},
    {"id": "loc-kalavad", "name": "Kalavad Industrial & Cotton Node", "subTitle": "Oil Mill Processing & Groundnut Trading, Jamnagar", "lat": 22.2100, "lng": 70.3800, "category": "city", "district": "Jamnagar"},
    {"id": "loc-dwarka", "name": "Dwarka Sacred Coastline & Jagat Mandir", "subTitle": "Char Dham Pilgrimage & Marine Coastal Corridor, Devbhumi Dwarka", "lat": 22.2400, "lng": 68.9680, "category": "benchmark", "district": "Devbhumi Dwarka"},
    {"id": "loc-khambhalia", "name": "Khambhalia District Headquarters", "subTitle": "Famous Desi Ghee & Metal Craft Center, Devbhumi Dwarka", "lat": 22.2050, "lng": 69.6500, "category": "city", "district": "Devbhumi Dwarka"},
    {"id": "loc-mithapur", "name": "Mithapur Chemicals & Solar Complex", "subTitle": "Tata Chemicals Soda Ash & Coastal Industrial Port, Devbhumi Dwarka", "lat": 22.4100, "lng": 69.0050, "category": "industrial", "district": "Devbhumi Dwarka"},
    {"id": "loc-okha", "name": "Okha Deep Sea Port & Bet Dwarka Ferry", "subTitle": "Strategic Naval & Commercial Maritime Terminal, Devbhumi Dwarka", "lat": 22.4650, "lng": 69.0700, "category": "industrial", "district": "Devbhumi Dwarka"},

    # =========================================================================
    # 8. JUNAGADH, GIR SOMNATH & PORBANDAR
    # =========================================================================
    {"id": "loc-junagadh-city", "name": "Junagadh Central Heritage & Civic Hub", "subTitle": "Girnar Foothills Commercial & Tourism Center, Junagadh", "lat": 21.5222, "lng": 70.4579, "category": "city", "district": "Junagadh"},
    {"id": "loc-keshod", "name": "Keshod Airport & Trading Taluka", "subTitle": "Regional Airport & Agri-Commodity Mandi, Junagadh", "lat": 21.3000, "lng": 70.2500, "category": "city", "district": "Junagadh"},
    {"id": "loc-mangrol-junagadh", "name": "Mangrol Marine Fisheries & Port", "subTitle": "Seafood Export & Coastal Agricultural Taluka, Junagadh", "lat": 21.1200, "lng": 70.1150, "category": "industrial", "district": "Junagadh"},
    {"id": "loc-manavadar", "name": "Manavadar Cotton Ginning Capital", "subTitle": "High-Yield White Gold Cotton Ginning Hub, Junagadh", "lat": 21.4950, "lng": 70.1350, "category": "city", "district": "Junagadh"},
    {"id": "loc-visavadar", "name": "Visavadar Gir Foothills Gateway", "subTitle": "Gir Lion Sanctuary Buffer & Agro-Produce Taluka, Junagadh", "lat": 21.3800, "lng": 70.7100, "category": "city", "district": "Junagadh"},
    {"id": "loc-veraval", "name": "Veraval Commercial Fishing Port", "subTitle": "India's Foremost Marine Fisheries & Seafood Hub, Gir Somnath", "lat": 20.9000, "lng": 70.3600, "category": "industrial", "district": "Gir Somnath"},
    {"id": "loc-somnath", "name": "Somnath Jyotirlinga Sacred Temple", "subTitle": "First Among the 12 Jyotirlingas, Sacred Coastline, Gir Somnath", "lat": 20.8880, "lng": 70.4010, "category": "benchmark", "district": "Gir Somnath"},
    {"id": "loc-talala", "name": "Talala Gir Kesar Mango Capital", "subTitle": "GI-Tagged World Famous Kesar Mango Mandi, Gir Somnath", "lat": 21.0500, "lng": 70.5200, "category": "city", "district": "Gir Somnath"},
    {"id": "loc-kodinar", "name": "Kodinar Sugar Mills & Coastal Belt", "subTitle": "Ambuja Cement Plants & Sugarcane Processing, Gir Somnath", "lat": 20.7900, "lng": 70.7000, "category": "industrial", "district": "Gir Somnath"},
    {"id": "loc-una", "name": "Una Coastal Commercial Gateway", "subTitle": "Gateway to Diu Island & Coastal Trade Hub, Gir Somnath", "lat": 20.8250, "lng": 71.0400, "category": "city", "district": "Gir Somnath"},
    {"id": "loc-porbandar-city", "name": "Porbandar Heritage Port & Kirti Mandir", "subTitle": "Mahatma Gandhi Birthplace & All-Weather Deep Port, Porbandar", "lat": 21.6417, "lng": 69.6293, "category": "city", "district": "Porbandar"},
    {"id": "loc-ranavav", "name": "Ranavav Cement & Mining Cluster", "subTitle": "Limestone Quarrying & Heavy Cement Plants, Porbandar", "lat": 21.6850, "lng": 69.7500, "category": "industrial", "district": "Porbandar"},
    {"id": "loc-kutiyana", "name": "Kutiyana Bhadar Basin Town", "subTitle": "Bhadar River Fertile Agricultural Taluka, Porbandar", "lat": 21.6300, "lng": 69.9800, "category": "city", "district": "Porbandar"},

    # =========================================================================
    # 9. KUTCH (Great Rann, Ports, Wind & Heritage)
    # =========================================================================
    {"id": "loc-mundra-port", "name": "Mundra Port SEZ Logistics Hub", "subTitle": "Deep-Water Container Terminal Freight Corridor, Kutch", "lat": 22.8394, "lng": 69.7214, "category": "benchmark", "district": "Kutch"},
    {"id": "loc-gandhidham-kandla", "name": "Gandhidham & Deendayal Port (Kandla)", "subTitle": "Major Dry Cargo Port, Timber & Logistics Node, Kutch", "lat": 23.0753, "lng": 70.1337, "category": "industrial", "district": "Kutch"},
    {"id": "loc-bhuj-city", "name": "Bhuj Central Heritage & Commercial Hub", "subTitle": "Kutch District Headquarters & Transport Node, Bhuj", "lat": 23.2420, "lng": 69.6669, "category": "city", "district": "Kutch"},
    {"id": "loc-mandvi-beach", "name": "Mandvi Port & Coastal Wind Belt", "subTitle": "Historic Shipbuilding Yard, Wind Corridor & Beach Resort, Kutch", "lat": 22.8330, "lng": 69.3550, "category": "city", "district": "Kutch"},
    {"id": "loc-anjar", "name": "Anjar Mega Welspun Industrial City", "subTitle": "Textiles, Steel Pipes & Heavy Manufacturing, Kutch", "lat": 23.1150, "lng": 70.0250, "category": "industrial", "district": "Kutch"},
    {"id": "loc-nakhatrana", "name": "Nakhatrana Wind Corridor Center", "subTitle": "Sub-Station Electrical Grid & Wind Turbine Hub, Kutch", "lat": 23.3500, "lng": 69.2600, "category": "industrial", "district": "Kutch"},
    {"id": "loc-naliya", "name": "Naliya & Abdasa Wind Ridgeline", "subTitle": "Premier High-Wind Resource Belt (8.4 m/s), Kutch", "lat": 23.2600, "lng": 68.8300, "category": "city", "district": "Kutch"},
    {"id": "loc-lakhpat", "name": "Lakhpat Ancient Fort & Kori Creek", "subTitle": "Border Fortress & High-Wind Coastal Zone, Kutch", "lat": 23.8300, "lng": 68.7800, "category": "city", "district": "Kutch"},
    {"id": "loc-khavda", "name": "Khavda Mega Renewable Energy Park", "subTitle": "30,000 MW Solar & Wind Hybrid Energy Complex, Kutch", "lat": 23.8500, "lng": 69.7200, "category": "benchmark", "district": "Kutch"},
    {"id": "loc-rapar", "name": "Rapar Vagad Gateway", "subTitle": "Dholavira Harappan UNESCO Site Gateway & Mandi, Kutch", "lat": 23.5700, "lng": 70.6300, "category": "city", "district": "Kutch"},
    {"id": "loc-bhachau", "name": "Bhachau Transport & Mineral Node", "subTitle": "NH-41 Strategic Freight Junction & Silica Sand Mining, Kutch", "lat": 23.2900, "lng": 70.3500, "category": "city", "district": "Kutch"},

    # =========================================================================
    # 10. BHARUCH & NARMADA
    # =========================================================================
    {"id": "loc-dahej-pcpir", "name": "Dahej PCPIR & Port Terminal", "subTitle": "Petrochemicals & Petroleum Investment Zone, Bharuch", "lat": 21.7125, "lng": 72.5855, "category": "benchmark", "district": "Bharuch"},
    {"id": "loc-ankleshwar-gidc", "name": "Ankleshwar GIDC Chemical Estate", "subTitle": "Asia's Foremost Chemical & Pharma Cluster, Bharuch", "lat": 21.6264, "lng": 73.0031, "category": "industrial", "district": "Bharuch"},
    {"id": "loc-bharuch-central", "name": "Bharuch Central & Golden Bridge Axis", "subTitle": "Narmada Riverfront Commercial & Transport Hub, Bharuch", "lat": 21.7051, "lng": 72.9959, "category": "city", "district": "Bharuch"},
    {"id": "loc-panoli-gidc", "name": "Panoli GIDC Industrial Estate", "subTitle": "Specialty Chemicals, Pharma & Pigments SEZ, Bharuch", "lat": 21.5300, "lng": 72.9600, "category": "industrial", "district": "Bharuch"},
    {"id": "loc-jambusar", "name": "Jambusar Agro & Chemical Town", "subTitle": "North Bharuch Cotton & Fine Chemicals Taluka", "lat": 22.0500, "lng": 72.8000, "category": "city", "district": "Bharuch"},
    {"id": "loc-jhagadia-gidc", "name": "Jhagadia Mega Industrial Estate", "subTitle": "Global MNC Chemical & Glass Manufacturing Hub, Bharuch", "lat": 21.7200, "lng": 73.1500, "category": "industrial", "district": "Bharuch"},
    {"id": "loc-statue-of-unity", "name": "Ekta Nagar / Kevadia (Statue of Unity)", "subTitle": "World's Tallest Monument & International Mega Tourism Hub, Narmada", "lat": 21.8380, "lng": 73.7191, "category": "benchmark", "district": "Narmada"},
    {"id": "loc-rajpipla", "name": "Rajpipla Heritage Capital", "subTitle": "District Headquarters, Palaces & Forest Gateway, Narmada", "lat": 21.8700, "lng": 73.5000, "category": "city", "district": "Narmada"},
    {"id": "loc-dediapada", "name": "Dediapada Shoolpaneshwar Wildlife Gateway", "subTitle": "Tribal Forestry, Herbal & Waterfall Eco-Tourism, Narmada", "lat": 21.6300, "lng": 73.5900, "category": "city", "district": "Narmada"},

    # =========================================================================
    # 11. ANAND & KHEDA (Charotar Dairy & Agri Hub)
    # =========================================================================
    {"id": "loc-anand-amul", "name": "Anand Agri & Amul Dairy Corridor", "subTitle": "India's Milk Capital & Agro-Processing Zone, Anand", "lat": 22.5645, "lng": 72.9289, "category": "city", "district": "Anand"},
    {"id": "loc-vvn", "name": "Vallabh Vidyanagar Educational Hub", "subTitle": "Premier Engineering & University Knowledge Township, Anand", "lat": 22.5530, "lng": 72.9240, "category": "ward", "district": "Anand"},
    {"id": "loc-karamsad", "name": "Karamsad Sardar Patel Heritage Town", "subTitle": "Civic & Medical Education Precinct, Anand", "lat": 22.5480, "lng": 72.8990, "category": "city", "district": "Anand"},
    {"id": "loc-khambhat", "name": "Khambhat (Cambay) Port & Agate Stone", "subTitle": "Historical Gulf of Khambhat Port & Halwasan Craft, Anand", "lat": 22.3150, "lng": 72.6200, "category": "city", "district": "Anand"},
    {"id": "loc-petlad", "name": "Petlad Textile & Tobacco Trade Node", "subTitle": "Charotar Fertile Agricultural & Trading Center, Anand", "lat": 22.4700, "lng": 72.8000, "category": "city", "district": "Anand"},
    {"id": "loc-borsad", "name": "Borsad Historical Town & Tobacco Hub", "subTitle": "Sardar Patel Freedom Movement & Agri Trading, Anand", "lat": 22.4100, "lng": 72.9000, "category": "city", "district": "Anand"},
    {"id": "loc-umreth", "name": "Umreth Commercial Trading Town", "subTitle": "Silk & Brass Kitchenware Craft Taluka, Anand", "lat": 22.7000, "lng": 73.1200, "category": "city", "district": "Anand"},
    {"id": "loc-nadiad", "name": "Nadiad Central & Santram Mandir", "subTitle": "Kheda District Largest Commercial & Educational Hub", "lat": 22.6916, "lng": 72.8634, "category": "city", "district": "Kheda"},
    {"id": "loc-dakor", "name": "Dakor Ranchhodraiji Sacred Temple", "subTitle": "Premier Krishna Pilgrimage Shrine, Kheda", "lat": 22.7550, "lng": 73.1500, "category": "benchmark", "district": "Kheda"},
    {"id": "loc-kapadvanj", "name": "Kapadvanj Historic Glass & Soap Center", "subTitle": "Trading Junction & Mohammedi Kund Heritage, Kheda", "lat": 23.0200, "lng": 73.0700, "category": "city", "district": "Kheda"},
    {"id": "loc-kheda-city", "name": "Kheda Historic Riverfront Town", "subTitle": "Vatrak-Shedhi Confluence District Seat, Kheda", "lat": 22.7500, "lng": 72.6850, "category": "city", "district": "Kheda"},

    # =========================================================================
    # 12. PANCHMAHAL, DAHOD & MAHISAGAR
    # =========================================================================
    {"id": "loc-godhra-central", "name": "Godhra Central & Station Road", "subTitle": "Panchmahal District Headquarters & Rail Junction", "lat": 22.7758, "lng": 73.6149, "category": "city", "district": "Panchmahal"},
    {"id": "loc-halol-gidc", "name": "Halol Mega Industrial Corridor", "subTitle": "Hero MotoCorp, MG Motor & Sun Pharma Automobile Belt, Panchmahal", "lat": 22.5000, "lng": 73.4700, "category": "industrial", "district": "Panchmahal"},
    {"id": "loc-pavagadh", "name": "Pavagadh Mahakali Shrine & Champaner", "subTitle": "UNESCO World Heritage Site & Ropeway Mountain Pilgrimage, Panchmahal", "lat": 22.4600, "lng": 73.5300, "category": "benchmark", "district": "Panchmahal"},
    {"id": "loc-kalol-panchmahal", "name": "Kalol Industrial Town", "subTitle": "Engineering, Foundry & Chemical Ancillaries, Panchmahal", "lat": 22.6050, "lng": 73.4500, "category": "industrial", "district": "Panchmahal"},
    {"id": "loc-dahod-central", "name": "Dahod Central Smart City Hub", "subTitle": "Smart City Headquarters & Interstate Commercial Gateway, Dahod", "lat": 22.8373, "lng": 74.2536, "category": "city", "district": "Dahod"},
    {"id": "loc-dahod-railway", "name": "Dahod Electric Locomotive Works", "subTitle": "Indian Railways 9000HP High-Power Electric Locomotive Factory, Dahod", "lat": 22.8450, "lng": 74.2600, "category": "industrial", "district": "Dahod"},
    {"id": "loc-jhalod", "name": "Jhalod Interstate Trade Mandi", "subTitle": "Rajasthan-MP Border Commercial Agro-Produce Hub, Dahod", "lat": 23.1000, "lng": 74.1500, "category": "city", "district": "Dahod"},
    {"id": "loc-limkheda", "name": "Limkheda Forest & Transit Node", "subTitle": "Tribal Agro-Trading & Highway Corridor, Dahod", "lat": 22.8300, "lng": 73.9900, "category": "city", "district": "Dahod"},
    {"id": "loc-lunawada", "name": "Lunawada Palace & District Headquarters", "subTitle": "Veri Dam & Mahisagar Administrative Capital", "lat": 23.1300, "lng": 73.6150, "category": "city", "district": "Mahisagar"},
    {"id": "loc-balasinor", "name": "Balasinor Dinosaur Fossil Park (Raiyoli)", "subTitle": "World's 3rd Largest Dinosaur Hatchery & Heritage Town, Mahisagar", "lat": 22.9550, "lng": 73.3350, "category": "benchmark", "district": "Mahisagar"},
    {"id": "loc-santrampur", "name": "Santrampur Forest Hill Town", "subTitle": "Suthar-Bheel Tribal Heritage & Suki Dam Gateway, Mahisagar", "lat": 23.1850, "lng": 73.8900, "category": "city", "district": "Mahisagar"},

    # =========================================================================
    # 13. BANASKANTHA & PATAN (North Gujarat Border)
    # =========================================================================
    {"id": "loc-palanpur-city", "name": "Palanpur Diamond & Banas Dairy Hub", "subTitle": "District Headquarters, Fragrance City & Dairy Epicenter", "lat": 24.1724, "lng": 72.4286, "category": "city", "district": "Banaskantha"},
    {"id": "loc-deesa", "name": "Deesa Mega Potato & Cold Storage Capital", "subTitle": "India's Foremost Potato Processing & River Banas Mandi, Banaskantha", "lat": 24.2580, "lng": 72.1780, "category": "city", "district": "Banaskantha"},
    {"id": "loc-ambaji", "name": "Ambaji Arasur Shaktipeeth Temple", "subTitle": "Major Marble Mining Belt & Sacred Pilgrimage Mountain, Banaskantha", "lat": 24.3300, "lng": 72.8500, "category": "benchmark", "district": "Banaskantha"},
    {"id": "loc-dhanera", "name": "Dhanera Agri-Commodity Market", "subTitle": "Castor & Mustard Seed Processing Center, Banaskantha", "lat": 24.5100, "lng": 72.0200, "category": "city", "district": "Banaskantha"},
    {"id": "loc-tharad", "name": "Tharad International Border Gateway", "subTitle": "Amritsar-Jamnagar Expressway Logistics Node, Banaskantha", "lat": 24.3900, "lng": 71.6300, "category": "city", "district": "Banaskantha"},
    {"id": "loc-patan-city", "name": "Patan Historic Patola Silk & Capital", "subTitle": "Medieval Solanki Capital & Heritage Silk Weaving, Patan", "lat": 23.8500, "lng": 72.1200, "category": "city", "district": "Patan"},
    {"id": "loc-rani-ki-vav", "name": "Rani ki Vav UNESCO Stepwell", "subTitle": "Architectural Masterpiece Stepwell & World Heritage, Patan", "lat": 23.8588, "lng": 72.1017, "category": "benchmark", "district": "Patan"},
    {"id": "loc-siddhpur", "name": "Siddhpur Saraswati Sacred Matru Gaya", "subTitle": "Bohra Heritage Mansions & Holy River Saraswati, Patan", "lat": 23.9180, "lng": 72.3780, "category": "city", "district": "Patan"},
    {"id": "loc-radhanpur", "name": "Radhanpur Desert & Kutch Gateway", "subTitle": "NH-27 East-West Freight Highway Hub, Patan", "lat": 23.8300, "lng": 71.6100, "category": "city", "district": "Patan"},

    # =========================================================================
    # 14. MEHSANA, SABARKANTHA & ARAVALLI
    # =========================================================================
    {"id": "loc-mehsana-city", "name": "Mehsana Central & Dudhsagar Dairy", "subTitle": "Oil & Natural Gas Corp (ONGC) Hub & Dairy Capital, Mehsana", "lat": 23.5880, "lng": 72.3693, "category": "city", "district": "Mehsana"},
    {"id": "loc-unjha", "name": "Unjha Asia Cumin & Isabgol Spice Capital", "subTitle": "Asia's Largest APMC Spice & Oilseed Market, Mehsana", "lat": 23.8050, "lng": 72.3950, "category": "city", "district": "Mehsana"},
    {"id": "loc-kadi", "name": "Kadi Cotton Ginning & Ceramic Hub", "subTitle": "High-Density Industrial Factories & Cotton Oil Mills, Mehsana", "lat": 23.3000, "lng": 72.3300, "category": "industrial", "district": "Mehsana"},
    {"id": "loc-visnagar", "name": "Visnagar Copper & Brass Metal Market", "subTitle": "Educational Township & Healthcare Services Hub, Mehsana", "lat": 23.7000, "lng": 72.5500, "category": "city", "district": "Mehsana"},
    {"id": "loc-vadnagar", "name": "Vadnagar Ancient Heritage City", "subTitle": "Archaeological Excavations, Kirti Toran & Cultural Node, Mehsana", "lat": 23.7850, "lng": 72.6350, "category": "city", "district": "Mehsana"},
    {"id": "loc-becharaji", "name": "Becharaji Auto Hub & Bahucharaji Temple", "subTitle": "Maruti Suzuki Mega Car Assembly & Pilgrimage, Mehsana", "lat": 23.5000, "lng": 72.0300, "category": "industrial", "district": "Mehsana"},
    {"id": "loc-himatnagar", "name": "Himatnagar Ceramic & Sabar Dairy Hub", "subTitle": "District Seat, Vitrified Tiles & Cattle Feed Mega Plants", "lat": 23.5977, "lng": 72.9698, "category": "city", "district": "Sabarkantha"},
    {"id": "loc-idar", "name": "Idar Granite Hills & Fort Town", "subTitle": "Historic Fort & Wooden Toy Toymaking Center, Sabarkantha", "lat": 23.8350, "lng": 73.0000, "category": "city", "district": "Sabarkantha"},
    {"id": "loc-prantij", "name": "Prantij Jaggery (Gur) Mandi", "subTitle": "NH-48 Agricultural Confectionery & Trade Node, Sabarkantha", "lat": 23.4450, "lng": 72.8550, "category": "city", "district": "Sabarkantha"},
    {"id": "loc-modasa", "name": "Modasa Commercial Trading Epicenter", "subTitle": "District Headquarters, Trade Route to Rajasthan, Aravalli", "lat": 23.4600, "lng": 73.3000, "category": "city", "district": "Aravalli"},
    {"id": "loc-bayad", "name": "Bayad Groundnut & Agri Mandi", "subTitle": "Vatrak River Basin Agro-Produce Taluka, Aravalli", "lat": 23.2300, "lng": 73.2200, "category": "city", "district": "Aravalli"},
    {"id": "loc-shamlaji", "name": "Shamlaji Gadadhar Temple & Border", "subTitle": "Ancient Temple & NH-48 Multi-Modal Checkpoint, Aravalli", "lat": 23.6800, "lng": 73.3800, "category": "benchmark", "district": "Aravalli"},

    # =========================================================================
    # 15. NAVSARI, VALSAD, DANG & TAPI (South Gujarat Coast & Hills)
    # =========================================================================
    {"id": "loc-navsari-city", "name": "Navsari Diamond Cutting & Parsi Heritage", "subTitle": "District Headquarters, Twin City to Surat & Floral Hub, Navsari", "lat": 20.9467, "lng": 72.9520, "category": "city", "district": "Navsari"},
    {"id": "loc-bilimora", "name": "Bilimora Port & Mango Export Center", "subTitle": "Ambika River Estuary, Timber & Alfonso Mango Hub, Navsari", "lat": 20.7600, "lng": 72.9600, "category": "city", "district": "Navsari"},
    {"id": "loc-chikhli", "name": "Chikhli NH-48 Express Junction", "subTitle": "National Highway Logistics Interchange & Agro-Trading, Navsari", "lat": 20.7550, "lng": 73.0600, "category": "city", "district": "Navsari"},
    {"id": "loc-vapi-gidc", "name": "Vapi Mega GIDC Industrial Estate", "subTitle": "Chemicals, Paper, Dyes & Packaging Hub, Valsad", "lat": 20.3893, "lng": 72.9106, "category": "industrial", "district": "Valsad"},
    {"id": "loc-valsad-city", "name": "Valsad Coastal City & Tithal Beach", "subTitle": "District Headquarters, Horticultural & Railway Divisional Hub, Valsad", "lat": 20.5992, "lng": 72.9342, "category": "city", "district": "Valsad"},
    {"id": "loc-pardi", "name": "Pardi Grassland & Industrial Estate", "subTitle": "Textile Weaving & Highway Commercial Corridor, Valsad", "lat": 20.5100, "lng": 72.9500, "category": "city", "district": "Valsad"},
    {"id": "loc-umbergaon", "name": "Umbergaon GIDC & Film Studio Port", "subTitle": "Gujarat's Southernmost Maritime Industrial Town, Valsad", "lat": 20.1900, "lng": 72.7600, "category": "industrial", "district": "Valsad"},
    {"id": "loc-ahwa", "name": "Ahwa Forest District Headquarters", "subTitle": "Breathtaking Teak & Bamboo Hill Capital, Dang", "lat": 20.7580, "lng": 73.6840, "category": "city", "district": "Dang"},
    {"id": "loc-saputara", "name": "Saputara Hill Station Resort", "subTitle": "Gujarat's Sole Hill Resort at 1000m Elevation, Dang", "lat": 20.5750, "lng": 73.7500, "category": "benchmark", "district": "Dang"},
    {"id": "loc-waghai", "name": "Waghai Botanical Gardens & Timber Gate", "subTitle": "Ambika River Valley & Dang Forest Gateway, Dang", "lat": 20.7700, "lng": 73.5000, "category": "city", "district": "Dang"},
    {"id": "loc-vyara", "name": "Vyara Heritage Capital & Fort", "subTitle": "District Headquarters, Agro-Food & Timber Center, Tapi", "lat": 21.1100, "lng": 73.4000, "category": "city", "district": "Tapi"},
    {"id": "loc-songadh", "name": "Songadh Fort & JK Paper Mills", "subTitle": "Heavy Paper Manufacturing & Ukai Dam Gateway, Tapi", "lat": 21.1700, "lng": 73.5600, "category": "industrial", "district": "Tapi"},

    # =========================================================================
    # 16. MORBI, SURENDRANAGAR & AMRELI
    # =========================================================================
    {"id": "loc-morbi-ceramic", "name": "Morbi Ceramic Industrial Cluster", "subTitle": "National Ceramic Tile & Sanitaryware Capital, Morbi", "lat": 22.8120, "lng": 70.8380, "category": "benchmark", "district": "Morbi"},
    {"id": "loc-wankaner", "name": "Wankaner Heritage Palace & Ceramic Unit", "subTitle": "Firebrick, Refractory & Royal Heritage Town, Morbi", "lat": 22.6100, "lng": 70.9600, "category": "city", "district": "Morbi"},
    {"id": "loc-surendranagar-city", "name": "Surendranagar Central & Cotton Trade", "subTitle": "Cotton City & Ginning Epicenter of Gujarat, Surendranagar", "lat": 22.7284, "lng": 71.6370, "category": "city", "district": "Surendranagar"},
    {"id": "loc-wadhwan", "name": "Wadhwan Historic Metal & Stone Town", "subTitle": "Heritage Brass Utensils & Bandhani Textile Center, Surendranagar", "lat": 22.7000, "lng": 71.6800, "category": "ward", "district": "Surendranagar"},
    {"id": "loc-dhrangadhra", "name": "Dhrangadhra Soda Ash & Stone Quarry", "subTitle": "DCW Heavy Chemicals & Yellow Stone Heritage, Surendranagar", "lat": 22.9900, "lng": 71.4600, "category": "industrial", "district": "Surendranagar"},
    {"id": "loc-chotila", "name": "Chotila Chamunda Mata Temple Mountain", "subTitle": "Prominent Volcanic Hill Pilgrimage on NH-47, Surendranagar", "lat": 22.4200, "lng": 71.1900, "category": "benchmark", "district": "Surendranagar"},
    {"id": "loc-limbdi", "name": "Limbdi Highway Commercial Junction", "subTitle": "Ahmedabad-Rajkot Expressway Rest & Logistics Hub, Surendranagar", "lat": 22.5650, "lng": 71.8000, "category": "city", "district": "Surendranagar"},
    {"id": "loc-thangadh", "name": "Thangadh Ceramic Sanitaryware Cluster", "subTitle": "Vitrified Wash Basins, Tiles & Insulators Town, Surendranagar", "lat": 22.5800, "lng": 71.2000, "category": "industrial", "district": "Surendranagar"},
    {"id": "loc-amreli-city", "name": "Amreli Central & Diamond Trading Mandi", "subTitle": "District Headquarters, Cotton & Agri Trading Hub, Amreli", "lat": 21.6032, "lng": 71.2221, "category": "city", "district": "Amreli"},
    {"id": "loc-savarkundla", "name": "Savarkundla Weighing Scales Capital", "subTitle": "Mechanical & Electronic Weighing Machine Industry, Amreli", "lat": 21.3300, "lng": 71.3100, "category": "city", "district": "Amreli"},
    {"id": "loc-pipavav-port", "name": "Pipavav Port & Heavy Marine Shipyard", "subTitle": "All-Weather Deep Water Container Terminal & Naval Yard, Amreli", "lat": 20.9100, "lng": 71.5000, "category": "benchmark", "district": "Amreli"},
    {"id": "loc-rajula", "name": "Rajula Industrial Corridor", "subTitle": "Cement Plants, Port Connectivity & Wind Corridors, Amreli", "lat": 21.0400, "lng": 71.4300, "category": "city", "district": "Amreli"},
    {"id": "loc-jafrabad", "name": "Jafrabad Coastal Fishing Port", "subTitle": "High-Wind Marine Corridor & Salt Production, Amreli", "lat": 20.8700, "lng": 71.3650, "category": "industrial", "district": "Amreli"},

    # =========================================================================
    # 17. CHHOTA UDAIPUR
    # =========================================================================
    {"id": "loc-chhota-udaipur", "name": "Chhota Udaipur Tribal Heritage Seat", "subTitle": "District Seat, Dolomite Mining & Pithora Art Center", "lat": 22.3050, "lng": 74.0150, "category": "city", "district": "Chhota Udaipur"},
    {"id": "loc-bodeli", "name": "Bodeli Banana & Agricultural Mandi", "subTitle": "Commercial Junction & Agro-Logistics Center, Chhota Udaipur", "lat": 22.2600, "lng": 73.7200, "category": "city", "district": "Chhota Udaipur"},
    {"id": "loc-sankheda", "name": "Sankheda Lacquerware Wooden Furniture Hub", "subTitle": "GI-Tagged Handcrafted Royal Lacquered Furniture Craft Town", "lat": 22.1600, "lng": 73.5850, "category": "city", "district": "Chhota Udaipur"},

    # =========================================================================
    # 18. PAN-INDIA ECONOMIC, IT & LOGISTICS HUBS
    # =========================================================================
    {"id": "loc-mumbai-bkc", "name": "Bandra Kurla Complex (BKC)", "subTitle": "India's Premier International Financial District, Mumbai, Maharashtra", "lat": 19.0657, "lng": 72.8687, "category": "benchmark", "district": "Mumbai"},
    {"id": "loc-mumbai-nariman", "name": "Nariman Point & Marine Drive", "subTitle": "Historic Corporate Financial Headquarters Axis, Mumbai, Maharashtra", "lat": 18.9260, "lng": 72.8230, "category": "benchmark", "district": "Mumbai"},
    {"id": "loc-mumbai-andheri", "name": "Andheri East MIDC & SEEPZ", "subTitle": "Jewelry Export, IT SEZ & Metro Transit Epicenter, Mumbai, Maharashtra", "lat": 19.1197, "lng": 72.8687, "category": "industrial", "district": "Mumbai"},
    {"id": "loc-mumbai-powai", "name": "Powai Hiranandani & IIT Bombay", "subTitle": "High-Tech Startup Corridor & Knowledge Hub, Mumbai, Maharashtra", "lat": 19.1176, "lng": 72.9060, "category": "ward", "district": "Mumbai"},
    {"id": "loc-navi-mumbai-vashi", "name": "Vashi Commercial Center & APMC", "subTitle": "Navi Mumbai Commercial & Wholesale Trade Epicenter, Maharashtra", "lat": 19.0771, "lng": 72.9986, "category": "city", "district": "Navi Mumbai"},
    {"id": "loc-delhi-connaught", "name": "Connaught Place (CP) & Barakhamba", "subTitle": "National Capital Premier Central Business District, New Delhi", "lat": 28.6304, "lng": 77.2177, "category": "benchmark", "district": "New Delhi"},
    {"id": "loc-gurgaon-cybercity", "name": "Cyber City DLF Phase 2 & 3", "subTitle": "Global Fortune 500 Corporate Technology Corridor, Gurugram, Haryana", "lat": 28.4950, "lng": 77.0890, "category": "benchmark", "district": "Gurugram"},
    {"id": "loc-noida-sec62", "name": "Noida Sector 62 Institutional & IT Hub", "subTitle": "Major Software Innovation & Educational SEZ, Noida, UP", "lat": 28.6280, "lng": 77.3680, "category": "industrial", "district": "Noida"},
    {"id": "loc-bengaluru-whitefield", "name": "Whitefield International Tech Park (ITPB)", "subTitle": "India's Silicon Valley Flagship Technology Hub, Bengaluru, Karnataka", "lat": 12.9856, "lng": 77.7375, "category": "benchmark", "district": "Bengaluru"},
    {"id": "loc-bengaluru-ecity", "name": "Electronic City Phase 1 & 2", "subTitle": "Electronics, Semiconductor & Software SEZ, Bengaluru, Karnataka", "lat": 12.8452, "lng": 77.6602, "category": "industrial", "district": "Bengaluru"},
    {"id": "loc-bengaluru-koramangala", "name": "Koramangala Startup District", "subTitle": "Premier Indian Unicorn Startup & High-Street Axis, Bengaluru, Karnataka", "lat": 12.9352, "lng": 77.6245, "category": "ward", "district": "Bengaluru"},
    {"id": "loc-bengaluru-indiranagar", "name": "Indiranagar 100 Feet Road", "subTitle": "High-Street Retail, Dining & Commercial Hub, Bengaluru, Karnataka", "lat": 12.9784, "lng": 77.6408, "category": "ward", "district": "Bengaluru"},
    {"id": "loc-hyderabad-hitec", "name": "Hitec City & Cyber Towers", "subTitle": "Cyberabad Global Tech Campus Corridor, Hyderabad, Telangana", "lat": 17.4504, "lng": 78.3808, "category": "benchmark", "district": "Hyderabad"},
    {"id": "loc-hyderabad-gachibowli", "name": "Gachibowli Financial District", "subTitle": "Global Banking, Fintech & IT Tower Hub, Hyderabad, Telangana", "lat": 17.4401, "lng": 78.3489, "category": "ward", "district": "Hyderabad"},
    {"id": "loc-chennai-omr", "name": "OMR (Old Mahabalipuram Road) IT Highway", "subTitle": "Tidel Park to Siruseri IT Corridor, Chennai, Tamil Nadu", "lat": 12.9724, "lng": 80.2508, "category": "benchmark", "district": "Chennai"},
    {"id": "loc-chennai-guindy", "name": "Guindy Industrial Estate & Olympia Tech", "subTitle": "Heart of Chennai Transit & Electronics Cluster, Chennai, Tamil Nadu", "lat": 13.0067, "lng": 80.2026, "category": "industrial", "district": "Chennai"},
    {"id": "loc-pune-hinjewadi", "name": "Hinjewadi Rajiv Gandhi Infotech Park", "subTitle": "Phases 1-3 Software Export & Technology Hub, Pune, Maharashtra", "lat": 18.5913, "lng": 73.7389, "category": "benchmark", "district": "Pune"},
    {"id": "loc-pune-magarpatta", "name": "Magarpatta Cybercity & Hadapsar", "subTitle": "Gated Smart City & Tech SEZ, Pune, Maharashtra", "lat": 18.5135, "lng": 73.9312, "category": "ward", "district": "Pune"},
    {"id": "loc-kolkata-saltlake", "name": "Salt Lake Sector V IT Corridor", "subTitle": "Eastern India's Premier Electronics & IT Hub, Kolkata, West Bengal", "lat": 22.5802, "lng": 88.4326, "category": "benchmark", "district": "Kolkata"},
    {"id": "loc-jaipur-sitapura", "name": "Sitapura Industrial Area & RIICO SEZ", "subTitle": "Gems, Jewelry & IT Technology Corridor, Jaipur, Rajasthan", "lat": 26.7800, "lng": 75.8200, "category": "industrial", "district": "Jaipur"},
    {"id": "loc-jaisalmer-wind", "name": "Jaisalmer Wind Park Complex", "subTitle": "India's Premier Desert Wind Farm Corridor (7.9 m/s), Rajasthan", "lat": 26.9157, "lng": 70.9083, "category": "benchmark", "district": "Jaisalmer"},
    {"id": "loc-muppandal-wind", "name": "Muppandal Wind Farm Supercluster", "subTitle": "Asia's Premier Mountain Pass High-Wind Belt (8.9 m/s), Tamil Nadu", "lat": 8.2589, "lng": 77.5458, "category": "benchmark", "district": "Kanyakumari"},
]
