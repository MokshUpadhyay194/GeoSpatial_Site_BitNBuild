import {
  Building2, Factory, Landmark, Anchor, Store, MapPin,
} from "lucide-react";
import type { SearchResultItem } from "@/components/SearchBar";

export const COMPREHENSIVE_PRESETS: SearchResultItem[] = [
  // =========================================================================
  // 1. AHMEDABAD & GANDHINAGAR (Wards, Talukas & GIDCs)
  // =========================================================================
  { id: "loc-sg-highway", name: "SG Highway Commercial Corridor", subTitle: "Bodakdev - Thaltej - Sola Arterial Axis, Ahmedabad", lat: 23.0378, lng: 72.5112, category: "benchmark", district: "Ahmedabad", icon: Building2 },
  { id: "loc-gift-city", name: "GIFT City International FinTech Zone", subTitle: "India Flagship IFSC Smart City, Gandhinagar", lat: 23.1601, lng: 72.6841, category: "benchmark", district: "Gandhinagar", icon: Landmark },
  { id: "loc-gandhinagar-central", name: "Gandhinagar Central (Sector 10-21)", subTitle: "Capital Administrative & Commercial Sector, Gandhinagar", lat: 23.2156, lng: 72.6369, category: "city", district: "Gandhinagar", icon: Landmark },
  { id: "loc-sanand-gidc", name: "Sanand GIDC Mega Automotive Corridor", subTitle: "Heavy Industrial Auto OEM Cluster, Ahmedabad Rural", lat: 22.9868, lng: 72.3814, category: "benchmark", district: "Ahmedabad Rural", icon: Factory },
  { id: "loc-bodakdev", name: "Bodakdev Urban Ward", subTitle: "SG Highway Judges Bungalow Precinct, Ahmedabad", lat: 23.0373, lng: 72.5074, category: "ward", district: "Ahmedabad", icon: MapPin },
  { id: "loc-sbr", name: "Sindhu Bhavan Road (SBR)", subTitle: "High-Street Retail Corporate Corridor, Ahmedabad", lat: 23.0450, lng: 72.4980, category: "ward", district: "Ahmedabad", icon: Store },
  { id: "loc-prahladnagar", name: "Prahlad Nagar Corporate Road", subTitle: "Makarba - Vejalpur Commercial Zone, Ahmedabad", lat: 23.0125, lng: 72.5085, category: "ward", district: "Ahmedabad", icon: Building2 },
  { id: "loc-satellite", name: "Satellite & Shivranjani", subTitle: "Dense Mixed Commercial Residential Hub, Ahmedabad", lat: 23.0305, lng: 72.5178, category: "ward", district: "Ahmedabad", icon: MapPin },
  { id: "loc-vastrapur", name: "Vastrapur Lake & IIM Ahmedabad", subTitle: "Institutional Premium Retail District, Ahmedabad", lat: 23.0350, lng: 72.5293, category: "ward", district: "Ahmedabad", icon: Landmark },
  { id: "loc-navrangpura", name: "Navrangpura Commercial District", subTitle: "CG Road, Municipal Market Law Garden, Ahmedabad", lat: 23.0365, lng: 72.5611, category: "ward", district: "Ahmedabad", icon: Store },
  { id: "loc-bopal", name: "Bopal & South Bopal (SOBO)", subTitle: "Rapidly Expanding Western Residential Suburban Hub, Ahmedabad", lat: 23.0338, lng: 72.4646, category: "ward", district: "Ahmedabad", icon: MapPin },
  { id: "loc-thaltej", name: "Thaltej Commercial & Shilaj Axis", subTitle: "West Ahmedabad Transit Oriented Corridor, Ahmedabad", lat: 23.0543, lng: 72.5085, category: "ward", district: "Ahmedabad", icon: Building2 },
  { id: "loc-gota", name: "Gota & SG Highway North", subTitle: "Sarkhej-Gandhinagar High-Density Urban Expansion, Ahmedabad", lat: 23.1070, lng: 72.5410, category: "ward", district: "Ahmedabad", icon: MapPin },
  { id: "loc-chandkheda", name: "Chandkheda & Motera Stadium Precinct", subTitle: "Narendra Modi Stadium Urban Transit Hub, Ahmedabad", lat: 23.1022, lng: 72.5975, category: "ward", district: "Ahmedabad", icon: Landmark },
  { id: "loc-maninagar", name: "Maninagar & Kankaria Lake Front", subTitle: "South Ahmedabad Commercial & Cultural Epicenter, Ahmedabad", lat: 22.9978, lng: 72.6026, category: "ward", district: "Ahmedabad", icon: MapPin },
  { id: "loc-nikol", name: "Nikol & Naroda Industrial Axis", subTitle: "East Ahmedabad Commercial Trading & Industrial Ward, Ahmedabad", lat: 23.0510, lng: 72.6680, category: "ward", district: "Ahmedabad", icon: Factory },
  { id: "loc-changodar", name: "Changodar Industrial & Logistics Park", subTitle: "Sarkhej-Bavla National Highway Freight Corridor", lat: 22.9234, lng: 72.4285, category: "industrial", district: "Ahmedabad Rural", icon: Factory },
  { id: "loc-bavla", name: "Bavla Industrial & Grain Hub", subTitle: "NH-47 Rice Milling & Engineering Cluster, Ahmedabad Rural", lat: 22.8360, lng: 72.3610, category: "city", district: "Ahmedabad Rural", icon: Factory },
  { id: "loc-dholka", name: "Dholka Historical & Pharma Town", subTitle: "Pharmaceutical & Engineering Manufacturing Taluka, Ahmedabad Rural", lat: 22.7200, lng: 72.4400, category: "city", district: "Ahmedabad Rural", icon: Factory },
  { id: "loc-viramgam", name: "Viramgam Railway Junction & Commercial Hub", subTitle: "Major Rail Logistics & Cotton Processing Taluka, Ahmedabad Rural", lat: 23.1250, lng: 72.0350, category: "city", district: "Ahmedabad Rural", icon: Factory },
  { id: "loc-mandal", name: "Mandal Industrial Node", subTitle: "Mandal-Becharaji Special Investment Region, Ahmedabad Rural", lat: 23.2800, lng: 71.9150, category: "industrial", district: "Ahmedabad Rural", icon: Factory },
  { id: "loc-detroj", name: "Detroj-Rampura Taluka Center", subTitle: "North Ahmedabad Agri-Logistics & Rail Junction, Ahmedabad Rural", lat: 23.3320, lng: 72.1880, category: "city", district: "Ahmedabad Rural", icon: MapPin },
  { id: "loc-dhandhuka", name: "Dhandhuka Regional Gateway", subTitle: "Bhal Region Agricultural & Cotton Commercial Taluka, Ahmedabad Rural", lat: 22.3700, lng: 71.9800, category: "city", district: "Ahmedabad Rural", icon: MapPin },
  { id: "loc-dholera-sir", name: "Dholera Special Investment Region (SIR)", subTitle: "Greenfield Smart Industrial City & Semiconductor Node", lat: 22.2472, lng: 72.1908, category: "industrial", district: "Ahmedabad Rural", icon: Landmark },
  { id: "loc-infocity", name: "Infocity IT & Software Park", subTitle: "Major IT/ITES Corridor & Innovation Hub, Gandhinagar", lat: 23.1904, lng: 72.6288, category: "industrial", district: "Gandhinagar", icon: Landmark },
  { id: "loc-kudasan", name: "Kudasan & Raysan Urban Corridor", subTitle: "High-Density Residential & Commercial Hub, Gandhinagar", lat: 23.1760, lng: 72.6320, category: "ward", district: "Gandhinagar", icon: Building2 },
  { id: "loc-sargasan", name: "Sargasan Cross Roads & SG Highway Extension", subTitle: "Retail & Mixed-Use Corporate Corridor, Gandhinagar", lat: 23.1950, lng: 72.6020, category: "ward", district: "Gandhinagar", icon: Store },
  { id: "loc-kalol-gandhinagar", name: "Kalol GIDC Industrial Estate", subTitle: "Heavy Engineering, Chemicals & Textile Hub, Gandhinagar", lat: 23.2420, lng: 72.4980, category: "industrial", district: "Gandhinagar", icon: Factory },
  { id: "loc-mansa", name: "Mansa Commercial & Agricultural Town", subTitle: "North Gandhinagar Agricultural Market & Taluka Center", lat: 23.4250, lng: 72.6600, category: "city", district: "Gandhinagar", icon: MapPin },
  { id: "loc-dehgam", name: "Dehgam Industrial & Transport Node", subTitle: "East Gandhinagar Agro-Trading & GIDC Taluka Center", lat: 23.1680, lng: 72.8120, category: "city", district: "Gandhinagar", icon: Factory },

  // =========================================================================
  // 2. VADODARA (CBD & Talukas)
  // =========================================================================
  { id: "loc-vadodara-central", name: "Vadodara Central Business District", subTitle: "Sayajigunj, Station Area & Alkapuri, Vadodara", lat: 22.3072, lng: 73.1812, category: "city", district: "Vadodara", icon: Building2 },
  { id: "loc-vadodara-alkapuri", name: "Alkapuri Central Commercial Hub", subTitle: "R.C. Dutt Road Premier Business District, Vadodara", lat: 22.3106, lng: 73.1812, category: "benchmark", district: "Vadodara", icon: Store },
  { id: "loc-vadodara-makarpura", name: "Makarpura GIDC Industrial Estate", subTitle: "Major Electrical & Heavy Engineering Hub, Vadodara", lat: 22.2536, lng: 73.1950, category: "industrial", district: "Vadodara", icon: Factory },
  { id: "loc-vadodara-akota", name: "Akota & Gotri Commercial Corridor", subTitle: "West Vadodara High-Density Retail & Residential Axis", lat: 22.3015, lng: 73.1614, category: "city", district: "Vadodara", icon: Store },
  { id: "loc-manjalpur", name: "Manjalpur Urban Commercial Hub", subTitle: "South Vadodara High-Street Retail & Residential Zone, Vadodara", lat: 22.2680, lng: 73.1920, category: "ward", district: "Vadodara", icon: Store },
  { id: "loc-nandesari-gidc", name: "Nandesari GIDC Petrochemical Complex", subTitle: "Bulk Drugs, Intermediates & Chemical Industrial Belt, Vadodara", lat: 22.4100, lng: 73.0900, category: "industrial", district: "Vadodara", icon: Factory },
  { id: "loc-padra", name: "Padra Pharma & Agri Taluka", subTitle: "Major Pharmaceutical Formulation Cluster, Vadodara Rural", lat: 22.2350, lng: 73.0850, category: "city", district: "Vadodara Rural", icon: Factory },
  { id: "loc-savli-gidc", name: "Savli GIDC Mega Engineering SEZ", subTitle: "Rail & Heavy Power Equipment Cluster, Vadodara Rural", lat: 22.5600, lng: 73.2200, category: "industrial", district: "Vadodara Rural", icon: Factory },
  { id: "loc-karjan", name: "Karjan NH-48 Transport & Agro Hub", subTitle: "National Highway Corridor & Cotton Trading Taluka, Vadodara Rural", lat: 22.0520, lng: 73.1200, category: "city", district: "Vadodara Rural", icon: MapPin },
  { id: "loc-dabhoi", name: "Dabhoi Heritage Fort & Commercial Node", subTitle: "Historic Fortified Town & Narrow Gauge Rail Capital, Vadodara Rural", lat: 22.1800, lng: 73.4300, category: "city", district: "Vadodara Rural", icon: Landmark },

  // =========================================================================
  // 3. SURAT (Textile, Diamond & Coast)
  // =========================================================================
  { id: "loc-surat-central", name: "Surat Central & Ring Road Textile Market", subTitle: "Asia's Premier Textile & Fabric Trading Capital, Surat", lat: 21.1959, lng: 72.8302, category: "city", district: "Surat", icon: Building2 },
  { id: "loc-surat-vesu", name: "Vesu Commercial Luxury Retail Hub", subTitle: "South Surat High-Density Premium Corridor, Surat", lat: 21.1442, lng: 72.7712, category: "city", district: "Surat", icon: Store },
  { id: "loc-surat-diamond-bourse", name: "Surat Diamond Bourse (DREAM City)", subTitle: "Khajod Global Gems & Jewelry Trading Capital, Surat", lat: 21.1219, lng: 72.7661, category: "city", district: "Surat", icon: Landmark },
  { id: "loc-surat-hazira", name: "Hazira Port Industrial Belt", subTitle: "Deep-Water LNG Steel Heavy Petrochemical Terminal, Surat", lat: 21.1158, lng: 72.6482, category: "industrial", district: "Surat", icon: Anchor },
  { id: "loc-adajan", name: "Adajan & Pal Riverside Precinct", subTitle: "West Surat High-Density Commercial & Residential Corridor, Surat", lat: 21.1980, lng: 72.7950, category: "ward", district: "Surat", icon: Building2 },
  { id: "loc-piplod", name: "Piplod & Dumas Road Leisure Hub", subTitle: "Entertainment, Mall & Hospitality Strip, Surat", lat: 21.1550, lng: 72.7580, category: "ward", district: "Surat", icon: Store },
  { id: "loc-sachin-gidc", name: "Sachin GIDC Textile & Diamond SEZ", subTitle: "Export Processing Zone & Chemical Manufacturing, Surat", lat: 21.0850, lng: 72.8800, category: "industrial", district: "Surat", icon: Factory },
  { id: "loc-pandesara-gidc", name: "Pandesara GIDC Industrial Estate", subTitle: "Dyeing, Printing & Synthetic Fabric Cluster, Surat", lat: 21.1400, lng: 72.8350, category: "industrial", district: "Surat", icon: Factory },
  { id: "loc-katargam", name: "Katargam Diamond Cutting Hub", subTitle: "Global Rough Diamond Processing Epicenter, Surat", lat: 21.2250, lng: 72.8350, category: "ward", district: "Surat", icon: Factory },
  { id: "loc-bardoli", name: "Bardoli Sugar & Agro-Industrial Capital", subTitle: "Asia's Largest Sugar Factory & Historical Freedom Hub, Surat", lat: 21.1200, lng: 73.1100, category: "city", district: "Surat", icon: Landmark },
  { id: "loc-olpad", name: "Olpad Aquaculture & Gas Exploration Node", subTitle: "Coastal Shrimp Farming & Petrochemical Taluka, Surat", lat: 21.3300, lng: 72.7500, category: "city", district: "Surat", icon: MapPin },
  { id: "loc-kamrej", name: "Kamrej NH-48 Transport & Transit Node", subTitle: "Major Freight Gateway to North Gujarat & Mumbai, Surat", lat: 21.2700, lng: 72.9600, category: "city", district: "Surat", icon: MapPin },

  // =========================================================================
  // 4. RAJKOT & SAURASHTRA
  // =========================================================================
  { id: "loc-rajkot-ringroad", name: "150 Feet Ring Road Commercial Axis", subTitle: "West Rajkot Retail Hospitality Healthcare Corridor, Rajkot", lat: 22.2850, lng: 70.7680, category: "city", district: "Rajkot", icon: Building2 },
  { id: "loc-rajkot-central", name: "Rajkot Central & Yagnik Road", subTitle: "Saurashtra Commercial & Financial Epicenter, Rajkot", lat: 22.3039, lng: 70.8022, category: "city", district: "Rajkot", icon: Building2 },
  { id: "loc-rajkot-aji", name: "Aji GIDC & Shapar Industrial Zone", subTitle: "Engineering, Casting & Diesel Engine Capital, Rajkot", lat: 22.2514, lng: 70.8142, category: "industrial", district: "Rajkot", icon: Factory },
  { id: "loc-metoda-gidc", name: "Metoda GIDC Auto Component Cluster", subTitle: "Precision Engineering, Bearings & Machine Tools SEZ, Rajkot", lat: 22.2400, lng: 70.6900, category: "industrial", district: "Rajkot", icon: Factory },
  { id: "loc-gondal", name: "Gondal Heritage Palace & Agri Mandi", subTitle: "Gujarat's Largest Red Chilli & Groundnut Mandi, Rajkot", lat: 21.9600, lng: 70.8000, category: "city", district: "Rajkot", icon: Landmark },
  { id: "loc-jetpur", name: "Jetpur Block Print & Saree Dyeing Hub", subTitle: "World-Renowned Cotton Printing & Dyeing Cluster, Rajkot", lat: 21.7550, lng: 70.6200, category: "city", district: "Rajkot", icon: Factory },
  { id: "loc-dhoraji", name: "Dhoraji Plastic & Oil Milling Town", subTitle: "Recycled Plastic Processing & Groundnut Oil Taluka, Rajkot", lat: 21.7300, lng: 70.4500, category: "city", district: "Rajkot", icon: Factory },
  { id: "loc-jasdan", name: "Jasdan Brass & Farm Implement Hub", subTitle: "Agricultural Machinery & Automobile Repair Cluster, Rajkot", lat: 22.0300, lng: 71.2000, category: "city", district: "Rajkot", icon: Factory },

  // =========================================================================
  // 5. BHAVNAGAR & BOTAD
  // =========================================================================
  { id: "loc-bhavnagar-city", name: "Bhavnagar Central & Waghawadi Road", subTitle: "Commercial High-Street & Civic Center, Bhavnagar", lat: 21.7645, lng: 72.1519, category: "city", district: "Bhavnagar", icon: Building2 },
  { id: "loc-alang-shipyard", name: "Alang Ship Recycling & Marine Yard", subTitle: "World's Largest Ship Breaking Cluster, Bhavnagar", lat: 21.4167, lng: 72.1833, category: "industrial", district: "Bhavnagar", icon: Anchor },
  { id: "loc-bhavnagar-chitra", name: "Chitra GIDC Industrial Estate", subTitle: "Plastics, Chemicals & Small-Scale Manufacturing, Bhavnagar", lat: 21.7856, lng: 72.1124, category: "industrial", district: "Bhavnagar", icon: Factory },
  { id: "loc-sihor", name: "Sihor Steel Rolling & Ceramic Hub", subTitle: "Re-rolling Mills & Historical Brass Metal Cluster, Bhavnagar", lat: 21.7000, lng: 71.9600, category: "industrial", district: "Bhavnagar", icon: Factory },
  { id: "loc-palitana", name: "Palitana Shatrunjaya Heritage Shrine", subTitle: "World-Renowned Sacred Jain Temple City, Bhavnagar", lat: 21.5200, lng: 71.8300, category: "city", district: "Bhavnagar", icon: Landmark },
  { id: "loc-mahuva", name: "Mahuva Onion & Dehydration Capital", subTitle: "India's Dehydrated White Onion & Coastal Coconut Port, Bhavnagar", lat: 21.0900, lng: 71.7600, category: "city", district: "Bhavnagar", icon: Anchor },
  { id: "loc-botad-city", name: "Botad Central Diamond & Cotton Mandi", subTitle: "District Headquarters & Diamond Cutting Hub, Botad", lat: 22.1700, lng: 71.6600, category: "city", district: "Botad", icon: Building2 },
  { id: "loc-gadhada", name: "Gadhada Swaminarayan Heritage Shrine", subTitle: "Gopinathji Temple Pilgrimage & Agricultural Center, Botad", lat: 21.9700, lng: 71.5700, category: "city", district: "Botad", icon: Landmark },
  { id: "loc-sarangpur", name: "Sarangpur Kashtbhanjan Hanuman Shrine", subTitle: "Major Spiritual Pilgrimage Epicenter, Botad", lat: 22.1400, lng: 71.7400, category: "city", district: "Botad", icon: Landmark },

  // =========================================================================
  // 6. JAMNAGAR & DEVBHUMI DWARKA
  // =========================================================================
  { id: "loc-jamnagar-refinery", name: "Jamnagar Petrochemical & Refining Belt", subTitle: "Motikhavdi World-Scale Refinery Complex, Jamnagar", lat: 22.4707, lng: 70.0577, category: "industrial", district: "Jamnagar", icon: Factory },
  { id: "loc-jamnagar-city", name: "Jamnagar City & Brass Parts Cluster", subTitle: "Precision Hardware & Commercial Center, Jamnagar", lat: 22.4707, lng: 70.0724, category: "city", district: "Jamnagar", icon: Building2 },
  { id: "loc-dwarka", name: "Dwarka Sacred Coastline & Jagat Mandir", subTitle: "Char Dham Pilgrimage & Marine Coastal Corridor, Devbhumi Dwarka", lat: 22.2400, lng: 68.9680, category: "benchmark", district: "Devbhumi Dwarka", icon: Landmark },
  { id: "loc-khambhalia", name: "Khambhalia District Headquarters", subTitle: "Famous Desi Ghee & Metal Craft Center, Devbhumi Dwarka", lat: 22.2050, lng: 69.6500, category: "city", district: "Devbhumi Dwarka", icon: Building2 },
  { id: "loc-mithapur", name: "Mithapur Chemicals & Solar Complex", subTitle: "Tata Chemicals Soda Ash & Coastal Industrial Port, Devbhumi Dwarka", lat: 22.4100, lng: 69.0050, category: "industrial", district: "Devbhumi Dwarka", icon: Factory },
  { id: "loc-okha", name: "Okha Deep Sea Port & Bet Dwarka Ferry", subTitle: "Strategic Naval & Commercial Maritime Terminal, Devbhumi Dwarka", lat: 22.4650, lng: 69.0700, category: "industrial", district: "Devbhumi Dwarka", icon: Anchor },

  // =========================================================================
  // 7. JUNAGADH, GIR SOMNATH & PORBANDAR
  // =========================================================================
  { id: "loc-junagadh-city", name: "Junagadh Central Heritage & Civic Hub", subTitle: "Girnar Foothills Commercial & Tourism Center, Junagadh", lat: 21.5222, lng: 70.4579, category: "city", district: "Junagadh", icon: Landmark },
  { id: "loc-keshod", name: "Keshod Airport & Trading Taluka", subTitle: "Regional Airport & Agri-Commodity Mandi, Junagadh", lat: 21.3000, lng: 70.2500, category: "city", district: "Junagadh", icon: MapPin },
  { id: "loc-veraval", name: "Veraval Commercial Fishing Port", subTitle: "India's Foremost Marine Fisheries & Seafood Hub, Gir Somnath", lat: 20.9000, lng: 70.3600, category: "industrial", district: "Gir Somnath", icon: Anchor },
  { id: "loc-somnath", name: "Somnath Jyotirlinga Sacred Temple", subTitle: "First Among the 12 Jyotirlingas, Sacred Coastline, Gir Somnath", lat: 20.8880, lng: 70.4010, category: "benchmark", district: "Gir Somnath", icon: Landmark },
  { id: "loc-talala", name: "Talala Gir Kesar Mango Capital", subTitle: "GI-Tagged World Famous Kesar Mango Mandi, Gir Somnath", lat: 21.0500, lng: 70.5200, category: "city", district: "Gir Somnath", icon: Store },
  { id: "loc-porbandar-city", name: "Porbandar Heritage Port & Kirti Mandir", subTitle: "Mahatma Gandhi Birthplace & All-Weather Deep Port, Porbandar", lat: 21.6417, lng: 69.6293, category: "city", district: "Porbandar", icon: Landmark },

  // =========================================================================
  // 8. KUTCH (Ports, Towns & Wind)
  // =========================================================================
  { id: "loc-mundra-port", name: "Mundra Port SEZ Logistics Hub", subTitle: "Deep-Water Container Terminal Freight Corridor, Kutch", lat: 22.8394, lng: 69.7214, category: "benchmark", district: "Kutch", icon: Anchor },
  { id: "loc-gandhidham-kandla", name: "Gandhidham & Deendayal Port (Kandla)", subTitle: "Major Dry Cargo Port, Timber & Logistics Node, Kutch", lat: 23.0753, lng: 70.1337, category: "industrial", district: "Kutch", icon: Anchor },
  { id: "loc-bhuj-city", name: "Bhuj Central Heritage & Commercial Hub", subTitle: "Kutch District Headquarters & Transport Node, Bhuj", lat: 23.2420, lng: 69.6669, category: "city", district: "Kutch", icon: Building2 },
  { id: "loc-mandvi-beach", name: "Mandvi Port & Coastal Wind Belt", subTitle: "Historic Shipbuilding Yard, Wind Corridor & Beach Resort, Kutch", lat: 22.8330, lng: 69.3550, category: "city", district: "Kutch", icon: Anchor },
  { id: "loc-anjar", name: "Anjar Mega Welspun Industrial City", subTitle: "Textiles, Steel Pipes & Heavy Manufacturing, Kutch", lat: 23.1150, lng: 70.0250, category: "industrial", district: "Kutch", icon: Factory },
  { id: "loc-naliya", name: "Naliya & Abdasa Wind Ridgeline", subTitle: "Premier High-Wind Resource Belt (8.4 m/s), Kutch", lat: 23.2600, lng: 68.8300, category: "city", district: "Kutch", icon: MapPin },
  { id: "loc-khavda", name: "Khavda Mega Renewable Energy Park", subTitle: "30,000 MW Solar & Wind Hybrid Energy Complex, Kutch", lat: 23.8500, lng: 69.7200, category: "benchmark", district: "Kutch", icon: Factory },

  // =========================================================================
  // 9. BHARUCH & NARMADA
  // =========================================================================
  { id: "loc-dahej-pcpir", name: "Dahej PCPIR & Port Terminal", subTitle: "Petrochemicals & Petroleum Investment Zone, Bharuch", lat: 21.7125, lng: 72.5855, category: "benchmark", district: "Bharuch", icon: Factory },
  { id: "loc-ankleshwar-gidc", name: "Ankleshwar GIDC Chemical Estate", subTitle: "Asia's Foremost Chemical & Pharma Cluster, Bharuch", lat: 21.6264, lng: 73.0031, category: "industrial", district: "Bharuch", icon: Factory },
  { id: "loc-bharuch-central", name: "Bharuch Central & Golden Bridge Axis", subTitle: "Narmada Riverfront Commercial & Transport Hub, Bharuch", lat: 21.7051, lng: 72.9959, category: "city", district: "Bharuch", icon: Building2 },
  { id: "loc-statue-of-unity", name: "Ekta Nagar / Kevadia (Statue of Unity)", subTitle: "World's Tallest Monument & International Mega Tourism Hub, Narmada", lat: 21.8380, lng: 73.7191, category: "benchmark", district: "Narmada", icon: Landmark },
  { id: "loc-rajpipla", name: "Rajpipla Heritage Capital", subTitle: "District Headquarters, Palaces & Forest Gateway, Narmada", lat: 21.8700, lng: 73.5000, category: "city", district: "Narmada", icon: Landmark },

  // =========================================================================
  // 10. ANAND & KHEDA
  // =========================================================================
  { id: "loc-anand-amul", name: "Anand Agri & Amul Dairy Corridor", subTitle: "India's Dairy Capital & Agro-Processing Zone, Anand", lat: 22.5645, lng: 72.9289, category: "city", district: "Anand", icon: Landmark },
  { id: "loc-vvn", name: "Vallabh Vidyanagar Educational Hub", subTitle: "Premier Engineering & University Knowledge Township, Anand", lat: 22.5530, lng: 72.9240, category: "ward", district: "Anand", icon: Landmark },
  { id: "loc-khambhat", name: "Khambhat (Cambay) Port & Agate Stone", subTitle: "Historical Gulf of Khambhat Port & Halwasan Craft, Anand", lat: 22.3150, lng: 72.6200, category: "city", district: "Anand", icon: Anchor },
  { id: "loc-nadiad", name: "Nadiad Central & Santram Mandir", subTitle: "Kheda District Largest Commercial & Educational Hub", lat: 22.6916, lng: 72.8634, category: "city", district: "Kheda", icon: Building2 },
  { id: "loc-dakor", name: "Dakor Ranchhodraiji Sacred Temple", subTitle: "Premier Krishna Pilgrimage Shrine, Kheda", lat: 22.7550, lng: 73.1500, category: "benchmark", district: "Kheda", icon: Landmark },
  { id: "loc-kapadvanj", name: "Kapadvanj Historic Glass & Soap Center", subTitle: "Trading Junction & Mohammedi Kund Heritage, Kheda", lat: 23.0200, lng: 73.0700, category: "city", district: "Kheda", icon: Building2 },

  // =========================================================================
  // 11. PANCHMAHAL, DAHOD & MAHISAGAR
  // =========================================================================
  { id: "loc-godhra-central", name: "Godhra Central & Station Road", subTitle: "Panchmahal District Headquarters & Rail Junction", lat: 22.7758, lng: 73.6149, category: "city", district: "Panchmahal", icon: Building2 },
  { id: "loc-halol-gidc", name: "Halol Mega Industrial Corridor", subTitle: "Hero MotoCorp, MG Motor & Sun Pharma Automobile Belt, Panchmahal", lat: 22.5000, lng: 73.4700, category: "industrial", district: "Panchmahal", icon: Factory },
  { id: "loc-pavagadh", name: "Pavagadh Mahakali Shrine & Champaner", subTitle: "UNESCO World Heritage Site & Ropeway Mountain Pilgrimage, Panchmahal", lat: 22.4600, lng: 73.5300, category: "benchmark", district: "Panchmahal", icon: Landmark },
  { id: "loc-dahod-central", name: "Dahod Central Smart City Hub", subTitle: "Smart City Headquarters & Interstate Commercial Gateway, Dahod", lat: 22.8373, lng: 74.2536, category: "city", district: "Dahod", icon: Building2 },
  { id: "loc-dahod-railway", name: "Dahod Electric Locomotive Works", subTitle: "Indian Railways 9000HP High-Power Electric Locomotive Factory, Dahod", lat: 22.8450, lng: 74.2600, category: "industrial", district: "Dahod", icon: Factory },
  { id: "loc-jhalod", name: "Jhalod Interstate Trade Mandi", subTitle: "Rajasthan-MP Border Commercial Agro-Produce Hub, Dahod", lat: 23.1000, lng: 74.1500, category: "city", district: "Dahod", icon: MapPin },
  { id: "loc-lunawada", name: "Lunawada Palace & District Headquarters", subTitle: "Veri Dam & Mahisagar Administrative Capital", lat: 23.1300, lng: 73.6150, category: "city", district: "Mahisagar", icon: Building2 },
  { id: "loc-balasinor", name: "Balasinor Dinosaur Fossil Park (Raiyoli)", subTitle: "World's 3rd Largest Dinosaur Hatchery & Heritage Town, Mahisagar", lat: 22.9550, lng: 73.3350, category: "benchmark", district: "Mahisagar", icon: Landmark },

  // =========================================================================
  // 12. BANASKANTHA & PATAN
  // =========================================================================
  { id: "loc-palanpur-city", name: "Palanpur Diamond & Banas Dairy Hub", subTitle: "District Headquarters, Fragrance City & Dairy Epicenter", lat: 24.1724, lng: 72.4286, category: "city", district: "Banaskantha", icon: Building2 },
  { id: "loc-deesa", name: "Deesa Mega Potato & Cold Storage Capital", subTitle: "India's Foremost Potato Processing & River Banas Mandi, Banaskantha", lat: 24.2580, lng: 72.1780, category: "city", district: "Banaskantha", icon: Factory },
  { id: "loc-ambaji", name: "Ambaji Arasur Shaktipeeth Temple", subTitle: "Major Marble Mining Belt & Sacred Pilgrimage Mountain, Banaskantha", lat: 24.3300, lng: 72.8500, category: "benchmark", district: "Banaskantha", icon: Landmark },
  { id: "loc-patan-city", name: "Patan Historic Patola Silk & Capital", subTitle: "Medieval Solanki Capital & Heritage Silk Weaving, Patan", lat: 23.8500, lng: 72.1200, category: "city", district: "Patan", icon: Landmark },
  { id: "loc-rani-ki-vav", name: "Rani ki Vav UNESCO Stepwell", subTitle: "Architectural Masterpiece Stepwell & World Heritage, Patan", lat: 23.8588, lng: 72.1017, category: "benchmark", district: "Patan", icon: Landmark },
  { id: "loc-siddhpur", name: "Siddhpur Saraswati Sacred Matru Gaya", subTitle: "Bohra Heritage Mansions & Holy River Saraswati, Patan", lat: 23.9180, lng: 72.3780, category: "city", district: "Patan", icon: Landmark },

  // =========================================================================
  // 13. MEHSANA, SABARKANTHA & ARAVALLI
  // =========================================================================
  { id: "loc-mehsana-city", name: "Mehsana Central & Dudhsagar Dairy", subTitle: "Oil & Natural Gas Corp (ONGC) Hub & Dairy Capital, Mehsana", lat: 23.5880, lng: 72.3693, category: "city", district: "Mehsana", icon: Building2 },
  { id: "loc-unjha", name: "Unjha Asia Cumin & Isabgol Spice Capital", subTitle: "Asia's Largest APMC Spice & Oilseed Market, Mehsana", lat: 23.8050, lng: 72.3950, category: "city", district: "Mehsana", icon: Store },
  { id: "loc-kadi", name: "Kadi Cotton Ginning & Ceramic Hub", subTitle: "High-Density Industrial Factories & Cotton Oil Mills, Mehsana", lat: 23.3000, lng: 72.3300, category: "industrial", district: "Mehsana", icon: Factory },
  { id: "loc-visnagar", name: "Visnagar Copper & Brass Metal Market", subTitle: "Educational Township & Healthcare Services Hub, Mehsana", lat: 23.7000, lng: 72.5500, category: "city", district: "Mehsana", icon: Building2 },
  { id: "loc-becharaji", name: "Becharaji Auto Hub & Bahucharaji Temple", subTitle: "Maruti Suzuki Mega Car Assembly & Pilgrimage, Mehsana", lat: 23.5000, lng: 72.0300, category: "industrial", district: "Mehsana", icon: Factory },
  { id: "loc-himatnagar", name: "Himatnagar Ceramic & Sabar Dairy Hub", subTitle: "District Seat, Vitrified Tiles & Cattle Feed Mega Plants", lat: 23.5977, lng: 72.9698, category: "city", district: "Sabarkantha", icon: Building2 },
  { id: "loc-idar", name: "Idar Granite Hills & Fort Town", subTitle: "Historic Fort & Wooden Toy Toymaking Center, Sabarkantha", lat: 23.8350, lng: 73.0000, category: "city", district: "Sabarkantha", icon: Landmark },
  { id: "loc-modasa", name: "Modasa Commercial Trading Epicenter", subTitle: "District Headquarters, Trade Route to Rajasthan, Aravalli", lat: 23.4600, lng: 73.3000, category: "city", district: "Aravalli", icon: Building2 },

  // =========================================================================
  // 14. NAVSARI, VALSAD, DANG & TAPI
  // =========================================================================
  { id: "loc-navsari-city", name: "Navsari Diamond Cutting & Parsi Heritage", subTitle: "District Headquarters, Twin City to Surat & Floral Hub, Navsari", lat: 20.9467, lng: 72.9520, category: "city", district: "Navsari", icon: Building2 },
  { id: "loc-bilimora", name: "Bilimora Port & Mango Export Center", subTitle: "Ambika River Estuary, Timber & Alfonso Mango Hub, Navsari", lat: 20.7600, lng: 72.9600, category: "city", district: "Navsari", icon: Anchor },
  { id: "loc-vapi-gidc", name: "Vapi Mega GIDC Industrial Estate", subTitle: "Chemicals, Paper, Dyes & Packaging Hub, Valsad", lat: 20.3893, lng: 72.9106, category: "industrial", district: "Valsad", icon: Factory },
  { id: "loc-valsad-city", name: "Valsad Coastal City & Tithal Beach", subTitle: "District Headquarters, Horticultural & Railway Divisional Hub, Valsad", lat: 20.5992, lng: 72.9342, category: "city", district: "Valsad", icon: Building2 },
  { id: "loc-saputara", name: "Saputara Hill Station Resort", subTitle: "Gujarat's Sole Hill Resort at 1000m Elevation, Dang", lat: 20.5750, lng: 73.7500, category: "benchmark", district: "Dang", icon: Landmark },
  { id: "loc-ahwa", name: "Ahwa Forest District Headquarters", subTitle: "Breathtaking Teak & Bamboo Hill Capital, Dang", lat: 20.7580, lng: 73.6840, category: "city", district: "Dang", icon: Landmark },
  { id: "loc-vyara", name: "Vyara Heritage Capital & Fort", subTitle: "District Headquarters, Agro-Food & Timber Center, Tapi", lat: 21.1100, lng: 73.4000, category: "city", district: "Tapi", icon: Building2 },

  // =========================================================================
  // 15. MORBI, SURENDRANAGAR & AMRELI
  // =========================================================================
  { id: "loc-morbi-ceramic", name: "Morbi Ceramic Industrial Cluster", subTitle: "National Ceramic Tile & Sanitaryware Capital, Morbi", lat: 22.8120, lng: 70.8380, category: "benchmark", district: "Morbi", icon: Factory },
  { id: "loc-surendranagar-city", name: "Surendranagar Central & Cotton Trade", subTitle: "Cotton City & Ginning Epicenter of Gujarat, Surendranagar", lat: 22.7284, lng: 71.6370, category: "city", district: "Surendranagar", icon: Building2 },
  { id: "loc-chotila", name: "Chotila Chamunda Mata Temple Mountain", subTitle: "Prominent Volcanic Hill Pilgrimage on NH-47, Surendranagar", lat: 22.4200, lng: 71.1900, category: "benchmark", district: "Surendranagar", icon: Landmark },
  { id: "loc-amreli-city", name: "Amreli Central & Diamond Trading Mandi", subTitle: "District Headquarters, Cotton & Agri Trading Hub, Amreli", lat: 21.6032, lng: 71.2221, category: "city", district: "Amreli", icon: Building2 },
  { id: "loc-pipavav-port", name: "Pipavav Port & Heavy Marine Shipyard", subTitle: "All-Weather Deep Water Container Terminal & Naval Yard, Amreli", lat: 20.9100, lng: 71.5000, category: "benchmark", district: "Amreli", icon: Anchor },

  // =========================================================================
  // 16. CHHOTA UDAIPUR
  // =========================================================================
  { id: "loc-chhota-udaipur", name: "Chhota Udaipur Tribal Heritage Seat", subTitle: "District Seat, Dolomite Mining & Pithora Art Center", lat: 22.3050, lng: 74.0150, category: "city", district: "Chhota Udaipur", icon: Building2 },
  { id: "loc-bodeli", name: "Bodeli Banana & Agricultural Mandi", subTitle: "Commercial Junction & Agro-Logistics Center, Chhota Udaipur", lat: 22.2600, lng: 73.7200, category: "city", district: "Chhota Udaipur", icon: MapPin },

  // =========================================================================
  // 17. PAN-INDIA ECONOMIC, IT & LOGISTICS HUBS
  // =========================================================================
  { id: "loc-mumbai-bkc", name: "Bandra Kurla Complex (BKC)", subTitle: "India's Premier International Financial District, Mumbai, Maharashtra", lat: 19.0657, lng: 72.8687, category: "benchmark", district: "Mumbai", icon: Building2 },
  { id: "loc-mumbai-nariman", name: "Nariman Point & Marine Drive", subTitle: "Historic Corporate Financial Headquarters Axis, Mumbai, Maharashtra", lat: 18.9260, lng: 72.8230, category: "benchmark", district: "Mumbai", icon: Landmark },
  { id: "loc-mumbai-andheri", name: "Andheri East MIDC & SEEPZ", subTitle: "Jewelry Export, IT SEZ & Metro Transit Epicenter, Mumbai, Maharashtra", lat: 19.1197, lng: 72.8687, category: "industrial", district: "Mumbai", icon: Factory },
  { id: "loc-delhi-connaught", name: "Connaught Place (CP) & Barakhamba", subTitle: "National Capital Premier Central Business District, New Delhi", lat: 28.6304, lng: 77.2177, category: "benchmark", district: "New Delhi", icon: Building2 },
  { id: "loc-gurgaon-cybercity", name: "Cyber City DLF Phase 2 & 3", subTitle: "Global Fortune 500 Corporate Technology Corridor, Gurugram, Haryana", lat: 28.4950, lng: 77.0890, category: "benchmark", district: "Gurugram", icon: Building2 },
  { id: "loc-noida-sec62", name: "Noida Sector 62 Institutional & IT Hub", subTitle: "Major Software Innovation & Educational SEZ, Noida, UP", lat: 28.6280, lng: 77.3680, category: "industrial", district: "Noida", icon: Factory },
  { id: "loc-bengaluru-whitefield", name: "Whitefield International Tech Park (ITPB)", subTitle: "India's Silicon Valley Flagship Technology Hub, Bengaluru, Karnataka", lat: 12.9856, lng: 77.7375, category: "benchmark", district: "Bengaluru", icon: Building2 },
  { id: "loc-bengaluru-ecity", name: "Electronic City Phase 1 & 2", subTitle: "Electronics, Semiconductor & Software SEZ, Bengaluru, Karnataka", lat: 12.8452, lng: 77.6602, category: "industrial", district: "Bengaluru", icon: Factory },
  { id: "loc-bengaluru-koramangala", name: "Koramangala Startup District", subTitle: "Premier Indian Unicorn Startup & High-Street Axis, Bengaluru, Karnataka", lat: 12.9352, lng: 77.6245, category: "ward", district: "Bengaluru", icon: Store },
  { id: "loc-hyderabad-hitec", name: "Hitec City & Cyber Towers", subTitle: "Cyberabad Global Tech Campus Corridor, Hyderabad, Telangana", lat: 17.4504, lng: 78.3808, category: "benchmark", district: "Hyderabad", icon: Building2 },
  { id: "loc-hyderabad-gachibowli", name: "Gachibowli Financial District", subTitle: "Global Banking, Fintech & IT Tower Hub, Hyderabad, Telangana", lat: 17.4401, lng: 78.3489, category: "ward", district: "Hyderabad", icon: Building2 },
  { id: "loc-chennai-omr", name: "OMR (Old Mahabalipuram Road) IT Highway", subTitle: "Tidel Park to Siruseri IT Corridor, Chennai, Tamil Nadu", lat: 12.9724, lng: 80.2508, category: "benchmark", district: "Chennai", icon: Building2 },
  { id: "loc-pune-hinjewadi", name: "Hinjewadi Rajiv Gandhi Infotech Park", subTitle: "Phases 1-3 Software Export & Technology Hub, Pune, Maharashtra", lat: 18.5913, lng: 73.7389, category: "benchmark", district: "Pune", icon: Factory },
  { id: "loc-kolkata-saltlake", name: "Salt Lake Sector V IT Corridor", subTitle: "Eastern India's Premier Electronics & IT Hub, Kolkata, West Bengal", lat: 22.5802, lng: 88.4326, category: "benchmark", district: "Kolkata", icon: Building2 },
  { id: "loc-jaipur-sitapura", name: "Sitapura Industrial Area & RIICO SEZ", subTitle: "Gems, Jewelry & IT Technology Corridor, Jaipur, Rajasthan", lat: 26.7800, lng: 75.8200, category: "industrial", district: "Jaipur", icon: Factory },
  { id: "loc-jaisalmer-wind", name: "Jaisalmer Wind Park Complex", subTitle: "India's Premier Desert Wind Farm Corridor (7.9 m/s), Rajasthan", lat: 26.9157, lng: 70.9083, category: "benchmark", district: "Jaisalmer", icon: Factory },
  { id: "loc-muppandal-wind", name: "Muppandal Wind Farm Supercluster", subTitle: "Asia's Premier Mountain Pass High-Wind Belt (8.9 m/s), Tamil Nadu", lat: 8.2589, lng: 77.5458, category: "benchmark", district: "Kanyakumari", icon: Factory },
];
