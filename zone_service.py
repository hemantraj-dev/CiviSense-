from typing import List, Dict, Any, Optional
from datetime import datetime
from app.risk_engine.engine import RiskEngine

CHANDIGARH_PUNJAB_ZONES = [
    # ---------------- CRITICAL RISK HOTSPOTS (CHRONIC FLOOD BOWLS) ----------------
    {
        "id": 1,
        "zone_code": "CHD-IND-01",
        "zone_name": "Industrial Area Phase I (Low-lying Sukhna Spillway Basin)",
        "representative_latitude": 30.7055,
        "representative_longitude": 76.8012,
        "elevation_m": 322.0,
        "baseline_drainage_factor": 88.0,
        "mapped_drain_count": 3,
        "description": "Chronic topographical depression adjacent to Sukhna Choe spillway. Silt buildup and packaging waste block collector siphons, producing knee-deep inundation during heavy rain.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7930, 30.7130], [76.8110, 30.7130], [76.8110, 30.6980], [76.7930, 30.6980], [76.7930, 30.7130]]]
        }
    },
    {
        "id": 2,
        "zone_code": "PB-ZIR-BAL",
        "zone_name": "Zirakpur Baltana (Sukhna Choe Downstream Floodplain, Punjab)",
        "representative_latitude": 30.6620,
        "representative_longitude": 76.8350,
        "elevation_m": 305.0,
        "baseline_drainage_factor": 94.0,
        "mapped_drain_count": 2,
        "description": "Low-lying floodplain downstream of Chandigarh's Sukhna Choe. High seasonal discharge from the Shivaliks causes severe backwater pooling and structural basement submergence.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.8250, 30.6720], [76.8450, 30.6720], [76.8450, 30.6520], [76.8250, 30.6520], [76.8250, 30.6720]]]
        }
    },
    {
        "id": 3,
        "zone_code": "PB-MOH-PH7",
        "zone_name": "Mohali Phase 7 (Commercial Arterial & Low Dip, Punjab)",
        "representative_latitude": 30.7010,
        "representative_longitude": 76.7150,
        "elevation_m": 317.0,
        "baseline_drainage_factor": 91.0,
        "mapped_drain_count": 1,
        "description": "Known urban bowl along Mohali's internal collector grid. Overloaded brick conduits and road surface depressions entrap vehicular traffic during downpours.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7050, 30.7090], [76.7250, 30.7090], [76.7250, 30.6930], [76.7050, 30.6930], [76.7050, 30.7090]]]
        }
    },
    {
        "id": 4,
        "zone_code": "PB-KHA-LND",
        "zone_name": "Kharar Landran Road (Rapidly Urbanized Low Plain, Punjab)",
        "representative_latitude": 30.7410,
        "representative_longitude": 76.6520,
        "elevation_m": 312.0,
        "baseline_drainage_factor": 90.0,
        "mapped_drain_count": 1,
        "description": "Dense unplanned commercial expansion lacking dedicated stormwater trunk lines. Runoff cascades onto low-lying carriageways and parking corridors.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.6400, 30.7510], [76.6640, 30.7510], [76.6640, 30.7310], [76.6400, 30.7310], [76.6400, 30.7510]]]
        }
    },
    {
        "id": 5,
        "zone_code": "PB-DER-GHG",
        "zone_name": "Dera Bassi Ghaggar Basin (River Spillway Corridor, Punjab)",
        "representative_latitude": 30.5890,
        "representative_longitude": 76.8450,
        "elevation_m": 298.0,
        "baseline_drainage_factor": 95.0,
        "mapped_drain_count": 2,
        "description": "Deepest regional depression near Ghaggar River confluence. Backwater surge creates flash inundation of industrial approach roads and residential colonies.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.8300, 30.6010], [76.8600, 30.6010], [76.8600, 30.5770], [76.8300, 30.5770], [76.8300, 30.6010]]]
        }
    },
    {
        "id": 6,
        "zone_code": "CHD-MAN-01",
        "zone_name": "Manimajra (Old Housing Board Basin, Chandigarh)",
        "representative_latitude": 30.7245,
        "representative_longitude": 76.8450,
        "elevation_m": 326.0,
        "baseline_drainage_factor": 87.0,
        "mapped_drain_count": 1,
        "description": "High-density peri-urban settlement across railway tracks. Legacy underground storm network chronically overloaded during cloudburst events.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.8350, 30.7320], [76.8550, 30.7320], [76.8550, 30.7170], [76.8350, 30.7170], [76.8350, 30.7320]]]
        }
    },
    {
        "id": 7,
        "zone_code": "PB-ZIR-VIP",
        "zone_name": "Zirakpur VIP Road (Dense Urban Corridor Bottleneck, Punjab)",
        "representative_latitude": 30.6410,
        "representative_longitude": 76.8180,
        "elevation_m": 308.0,
        "baseline_drainage_factor": 92.0,
        "mapped_drain_count": 1,
        "description": "High commercial traffic strip. Inadequate roadside storm culverts and heavy silt deposits cause chronic surface pooling exceeding 40 cm depth.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.8080, 30.6510], [76.8280, 30.6510], [76.8280, 30.6310], [76.8080, 30.6310], [76.8080, 30.6510]]]
        }
    },

    # ---------------- HIGH RISK SECTORS (ELEVATED VULNERABILITY) ----------------
    {
        "id": 8,
        "zone_code": "CHD-IND-02",
        "zone_name": "Industrial Area Phase II (Railway Underpass Corridor)",
        "representative_latitude": 30.6942,
        "representative_longitude": 76.7925,
        "elevation_m": 318.0,
        "baseline_drainage_factor": 78.0,
        "mapped_drain_count": 2,
        "description": "Downstream industrial sector with heavy vehicular movement and railway underpasses highly susceptible to rapid water entrapment.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7850, 30.7010], [76.8020, 30.7010], [76.8020, 30.6870], [76.7850, 30.6870], [76.7850, 30.7010]]]
        }
    },
    {
        "id": 9,
        "zone_code": "PB-MOH-PH1",
        "zone_name": "Mohali Phase 1 (Industrial Area Near N-Choe Outfall, Punjab)",
        "representative_latitude": 30.7180,
        "representative_longitude": 76.7190,
        "elevation_m": 321.0,
        "baseline_drainage_factor": 80.0,
        "mapped_drain_count": 2,
        "description": "Located at confluence of Chandigarh's N-Choe entering Mohali territory. Siltation around highway bridges causes storm discharge backflow.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7100, 30.7260], [76.7280, 30.7260], [76.7280, 30.7100], [76.7100, 30.7100], [76.7100, 30.7260]]]
        }
    },
    {
        "id": 10,
        "zone_code": "CHD-SEC-52",
        "zone_name": "Sector 52 (South Chandigarh Boundary Drainage Basin)",
        "representative_latitude": 30.7020,
        "representative_longitude": 76.7320,
        "elevation_m": 320.0,
        "baseline_drainage_factor": 79.0,
        "mapped_drain_count": 1,
        "description": "Border sector adjacent to Mohali boundary. Topographic dip collects local surface runoff from Sector 43 and Sector 44 corridors.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7240, 30.7090], [76.7400, 30.7090], [76.7400, 30.6950], [76.7240, 30.6950], [76.7240, 30.7090]]]
        }
    },
    {
        "id": 11,
        "zone_code": "CHD-SEC-43",
        "zone_name": "Sector 43 (ISBT Bus Terminal & High Density Hub)",
        "representative_latitude": 30.7180,
        "representative_longitude": 76.7410,
        "elevation_m": 329.0,
        "baseline_drainage_factor": 72.0,
        "mapped_drain_count": 2,
        "description": "Inter-state bus terminal interchange. Vast impermeable paved aprons create intense surface runoff concentration around entry ramps.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7340, 30.7240], [76.7480, 30.7240], [76.7480, 30.7120], [76.7340, 30.7120], [76.7340, 30.7240]]]
        }
    },
    {
        "id": 12,
        "zone_code": "CHD-MAL-01",
        "zone_name": "Maloya (Western Peri-Urban Low Corridor)",
        "representative_latitude": 30.7320,
        "representative_longitude": 76.7210,
        "elevation_m": 325.0,
        "baseline_drainage_factor": 76.0,
        "mapped_drain_count": 1,
        "description": "Peripheral rehabilitation colony bordering Punjab border. Flat grade and narrow roadside stormwater channels experience water stagnation.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7120, 30.7400], [76.7300, 30.7400], [76.7300, 30.7240], [76.7120, 30.7240], [76.7120, 30.7400]]]
        }
    },
    {
        "id": 13,
        "zone_code": "PB-KHA-NH21",
        "zone_name": "Kharar Flyover Sub-surface Highway Dip (NH-21, Punjab)",
        "representative_latitude": 30.7490,
        "representative_longitude": 76.6430,
        "elevation_m": 315.0,
        "baseline_drainage_factor": 75.0,
        "mapped_drain_count": 1,
        "description": "Under-bridge service lanes along the Chandigarh-Ludhiana Highway corridor subject to rapid stormwater pooling during convective surges.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.6320, 30.7580], [76.6540, 30.7580], [76.6540, 30.7400], [76.6320, 30.7400], [76.6320, 30.7580]]]
        }
    },
    {
        "id": 14,
        "zone_code": "CHD-DHA-01",
        "zone_name": "Dhanas (Patiala Ki Rao Choe Corridor)",
        "representative_latitude": 30.7580,
        "representative_longitude": 76.7490,
        "elevation_m": 335.0,
        "baseline_drainage_factor": 74.0,
        "mapped_drain_count": 1,
        "description": "North-western periphery bordering Patiala Ki Rao stream. Surface soil siltation causes backflow into service roads during high channel levels.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7390, 30.7670], [76.7590, 30.7670], [76.7590, 30.7490], [76.7390, 30.7490], [76.7390, 30.7670]]]
        }
    },
    {
        "id": 15,
        "zone_code": "PB-MOH-SEC70",
        "zone_name": "Mohali Sector 70 (Mattaur Village Depression, Punjab)",
        "representative_latitude": 30.6980,
        "representative_longitude": 76.7110,
        "elevation_m": 316.0,
        "baseline_drainage_factor": 73.0,
        "mapped_drain_count": 1,
        "description": "Organic village settlement surrounded by planned sectors. Significant natural elevation dip creates localized water accumulation.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7020, 30.7060], [76.7200, 30.7060], [76.7200, 30.6900], [76.7020, 30.6900], [76.7020, 30.7060]]]
        }
    },
    {
        "id": 16,
        "zone_code": "CHD-SEC-45",
        "zone_name": "Sector 45 (Burail Urban Village Outskirts)",
        "representative_latitude": 30.7110,
        "representative_longitude": 76.7620,
        "elevation_m": 328.0,
        "baseline_drainage_factor": 71.0,
        "mapped_drain_count": 1,
        "description": "Dense semi-urban fringe surrounding Burail village. High waste accumulation and low drain gradient slow down rainwater discharge.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7540, 30.7180], [76.7700, 30.7180], [76.7700, 30.7040], [76.7540, 30.7040], [76.7540, 30.7180]]]
        }
    },
    {
        "id": 17,
        "zone_code": "CHD-SEC-26",
        "zone_name": "Sector 26 (Grain & Vegetable Mandi Corridor)",
        "representative_latitude": 30.7290,
        "representative_longitude": 76.8090,
        "elevation_m": 339.0,
        "baseline_drainage_factor": 70.0,
        "mapped_drain_count": 2,
        "description": "Mandi wholesale market corridor with frequent vegetable debris and silt deposits clogging roadside catchpits and storm conduits.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.8010, 30.7360], [76.8170, 30.7360], [76.8170, 30.7220], [76.8010, 30.7220], [76.8010, 30.7360]]]
        }
    },
    {
        "id": 18,
        "zone_code": "PB-MOH-SEC82",
        "zone_name": "Mohali Sector 82 (JLPL Industrial Park, Punjab)",
        "representative_latitude": 30.6650,
        "representative_longitude": 76.7420,
        "elevation_m": 311.0,
        "baseline_drainage_factor": 68.0,
        "mapped_drain_count": 2,
        "description": "Southern industrial expansion with extensive paved footprint. Storm conduits require periodic clearance to prevent factory gate waterlogging.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7320, 30.6740], [76.7520, 30.6740], [76.7520, 30.6560], [76.7320, 30.6560], [76.7320, 30.6740]]]
        }
    },
    {
        "id": 19,
        "zone_code": "CHD-SEC-22",
        "zone_name": "Sector 22 (Shastri Market & Mixed Urban Core)",
        "representative_latitude": 30.7288,
        "representative_longitude": 76.7725,
        "elevation_m": 341.0,
        "baseline_drainage_factor": 67.0,
        "mapped_drain_count": 1,
        "description": "High footfall market corridor. High solid waste and silt accumulation near roadside gully traps reduces storm discharge rate.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7660, 30.7340], [76.7790, 30.7340], [76.7790, 30.7230], [76.7660, 30.7230], [76.7660, 30.7340]]]
        }
    },

    # ---------------- MEDIUM RISK SECTORS (MODERATE STRESS) ----------------
    {
        "id": 20,
        "zone_code": "PB-MOH-3B2",
        "zone_name": "Mohali Phase 3B2 (Commercial Market Hub, Punjab)",
        "representative_latitude": 30.7120,
        "representative_longitude": 76.7260,
        "elevation_m": 324.0,
        "baseline_drainage_factor": 56.0,
        "mapped_drain_count": 2,
        "description": "Vibrant commercial and dining hub. Moderate drainage resilience with localized water accumulation around parking lanes during storm peaks.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7180, 30.7190], [76.7340, 30.7190], [76.7340, 30.7050], [76.7180, 30.7050], [76.7180, 30.7190]]]
        }
    },
    {
        "id": 21,
        "zone_code": "CHD-SEC-20",
        "zone_name": "Sector 20 (Dense Residential Inner Grid)",
        "representative_latitude": 30.7210,
        "representative_longitude": 76.7820,
        "elevation_m": 338.0,
        "baseline_drainage_factor": 54.0,
        "mapped_drain_count": 2,
        "description": "Established residential sector with planned underground conduits. Street corner gullies prone to seasonal autumn leaf and silt blockage.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7740, 30.7280], [76.7900, 30.7280], [76.7900, 30.7140], [76.7740, 30.7140], [76.7740, 30.7280]]]
        }
    },
    {
        "id": 22,
        "zone_code": "CHD-SEC-17",
        "zone_name": "Sector 17 (City Centre Commercial Core)",
        "representative_latitude": 30.7398,
        "representative_longitude": 76.7827,
        "elevation_m": 348.0,
        "baseline_drainage_factor": 48.0,
        "mapped_drain_count": 2,
        "description": "Pedestrian plaza with extensive paved coverage. Vulnerable to brief surface ponding around underpasses during intense downpours.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7760, 30.7440], [76.7890, 30.7440], [76.7890, 30.7350], [76.7760, 30.7350], [76.7760, 30.7440]]]
        }
    },
    {
        "id": 23,
        "zone_code": "CHD-SEC-34",
        "zone_name": "Sector 34 (Sub-City Commercial Centre)",
        "representative_latitude": 30.7230,
        "representative_longitude": 76.7680,
        "elevation_m": 337.0,
        "baseline_drainage_factor": 49.0,
        "mapped_drain_count": 2,
        "description": "Major educational and coaching institute hub. High vehicular and pedestrian parking with moderate stormwater conveyance.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7600, 30.7300], [76.7760, 30.7300], [76.7760, 30.7160], [76.7600, 30.7160], [76.7600, 30.7300]]]
        }
    },
    {
        "id": 24,
        "zone_code": "CHD-SEC-35",
        "zone_name": "Sector 35 (Commercial & Hotel Avenue)",
        "representative_latitude": 30.7225,
        "representative_longitude": 76.7589,
        "elevation_m": 336.0,
        "baseline_drainage_factor": 48.0,
        "mapped_drain_count": 2,
        "description": "Commercial arterial avenue near Dakshin Marg. Moderate drainage resilience, roadside depressions along service roads prone to standing water.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7520, 30.7280], [76.7650, 30.7280], [76.7650, 30.7170], [76.7520, 30.7170], [76.7520, 30.7280]]]
        }
    },
    {
        "id": 25,
        "zone_code": "PB-MOH-PH9",
        "zone_name": "Mohali Phase 9 (PCA Stadium Enclave, Punjab)",
        "representative_latitude": 30.6910,
        "representative_longitude": 76.7350,
        "elevation_m": 319.0,
        "baseline_drainage_factor": 47.0,
        "mapped_drain_count": 2,
        "description": "Surrounds the international cricket stadium with dedicated wide stormwater drains and grassed overflow swales.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7250, 30.6990], [76.7450, 30.6990], [76.7450, 30.6830], [76.7250, 30.6830], [76.7250, 30.6990]]]
        }
    },
    {
        "id": 26,
        "zone_code": "CHD-SEC-15",
        "zone_name": "Sector 15 (Panjab University South Periphery)",
        "representative_latitude": 30.7510,
        "representative_longitude": 76.7680,
        "elevation_m": 346.0,
        "baseline_drainage_factor": 45.0,
        "mapped_drain_count": 2,
        "description": "University residential and student market sector. Steady north-to-south gradient maintains reasonable gravity storm discharge.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7600, 30.7580], [76.7760, 30.7580], [76.7760, 30.7440], [76.7600, 30.7440], [76.7600, 30.7580]]]
        }
    },

    # ---------------- LOW RISK SECTORS (HIGH ELEVATION & HIGH CONVEYANCE) ----------------
    {
        "id": 27,
        "zone_code": "CHD-SUK-01",
        "zone_name": "Sukhna Lake Catchment & Enclave (Northeastern Periphery)",
        "representative_latitude": 30.7421,
        "representative_longitude": 76.8188,
        "elevation_m": 362.0,
        "baseline_drainage_factor": 30.0,
        "mapped_drain_count": 3,
        "description": "Shivalik foothills catchment rim. Rapid surface runoff generation that discharges naturally into Sukhna Lake reservoir.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.8090, 30.7510], [76.8280, 30.7510], [76.8280, 30.7330], [76.8090, 30.7330], [76.8090, 30.7510]]]
        }
    },
    {
        "id": 28,
        "zone_code": "CHD-SEC-01",
        "zone_name": "Sector 1 (Capitol Complex & High Court Enclave)",
        "representative_latitude": 30.7585,
        "representative_longitude": 76.8055,
        "elevation_m": 365.0,
        "baseline_drainage_factor": 22.0,
        "mapped_drain_count": 3,
        "description": "Highest elevation zone in Chandigarh at base of Shivalik hills. Steep natural incline ensures rapid gravitational water runoff.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7970, 30.7670], [76.8140, 30.7670], [76.8140, 30.7500], [76.7970, 30.7500], [76.7970, 30.7670]]]
        }
    },
    {
        "id": 29,
        "zone_code": "CHD-SEC-08",
        "zone_name": "Sector 8 (Residential North Ridge)",
        "representative_latitude": 30.7450,
        "representative_longitude": 76.7920,
        "elevation_m": 355.0,
        "baseline_drainage_factor": 25.0,
        "mapped_drain_count": 2,
        "description": "Low-density residential sector on the northern ridge with wide green belts, open permeable lawns, and effective road gutters.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7840, 30.7530], [76.8000, 30.7530], [76.8000, 30.7370], [76.7840, 30.7370], [76.7840, 30.7530]]]
        }
    },
    {
        "id": 30,
        "zone_code": "PB-MOH-AERO",
        "zone_name": "Mohali Aerocity (Engineered Airport Corridor, Punjab)",
        "representative_latitude": 30.6480,
        "representative_longitude": 76.7790,
        "elevation_m": 315.0,
        "baseline_drainage_factor": 26.0,
        "mapped_drain_count": 3,
        "description": "Modern master-planned airport corridor constructed with oversized concrete box conduits, retention swales, and positive fall.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7650, 30.6580], [76.7930, 30.6580], [76.7930, 30.6380], [76.7650, 30.6380], [76.7650, 30.6580]]]
        }
    },
    {
        "id": 31,
        "zone_code": "PB-MOH-ITCITY",
        "zone_name": "Mohali IT City (Knowledge Park Campus, Punjab)",
        "representative_latitude": 30.6350,
        "representative_longitude": 76.7620,
        "elevation_m": 314.0,
        "baseline_drainage_factor": 28.0,
        "mapped_drain_count": 3,
        "description": "Modern institutional sector with dedicated on-site rainwater harvesting basins, permeable paving, and zero waterlogging history.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7500, 30.6450], [76.7740, 30.6450], [76.7740, 30.6250], [76.7500, 30.6250], [76.7500, 30.6450]]]
        }
    },
    {
        "id": 32,
        "zone_code": "PB-MULL-ECO",
        "zone_name": "New Chandigarh Mullanpur (Eco City Foothills, Punjab)",
        "representative_latitude": 30.7890,
        "representative_longitude": 76.7210,
        "elevation_m": 358.0,
        "baseline_drainage_factor": 24.0,
        "mapped_drain_count": 2,
        "description": "Eco City township on the north-western foothills. High elevation and preserved natural drainage nallahs prevent surface accumulation.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[[76.7080, 30.8010], [76.7340, 30.8010], [76.7340, 30.7770], [76.7080, 30.7770], [76.7080, 30.8010]]]
        }
    }
]

class ZoneService:
    def __init__(self):
        self.zones = CHANDIGARH_PUNJAB_ZONES

    def get_all_zones(self) -> List[Dict[str, Any]]:
        return self.zones

    def get_zone_by_id(self, zone_id: int) -> Optional[Dict[str, Any]]:
        for z in self.zones:
            if z["id"] == zone_id:
                return z
        return None

    def assess_all_zones(self, weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        assessments = []
        for zone in self.zones:
            assessment = RiskEngine.assess_zone(
                rainfall_1h=weather_data.get("rainfall_1h", 0.0),
                rainfall_3h=weather_data.get("rainfall_3h", 0.0),
                rainfall_24h=weather_data.get("rainfall_24h", 0.0),
                forecast_6h=weather_data.get("forecast_6h", 0.0),
                forecast_24h=weather_data.get("forecast_24h", 0.0),
                baseline_drainage_factor=zone["baseline_drainage_factor"],
                mapped_drain_count=zone["mapped_drain_count"],
                elevation_m=zone["elevation_m"],
                has_live_weather=weather_data.get("is_live", True),
                has_elevation_sample=True,
                has_drainage_features=True,
                verified_reports_count=1 if zone["id"] in [1, 2, 3, 4, 5, 6, 7] else 0
            )
            assessment["zone_id"] = zone["id"]
            assessment["zone_code"] = zone["zone_code"]
            assessment["zone_name"] = zone["zone_name"]
            assessment["elevation_m"] = zone["elevation_m"]
            assessments.append(assessment)
            
        assessments.sort(key=lambda x: x["overall_risk_score"], reverse=True)
        for rank, item in enumerate(assessments, start=1):
            item["priority_rank"] = rank
            
        return assessments

zone_service = ZoneService()
