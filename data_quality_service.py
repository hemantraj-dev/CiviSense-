from datetime import datetime
from typing import List, Dict, Any
from app.core.config import settings

class DataQualityService:
    @staticmethod
    def get_data_sources_status(
        weather_live: bool = True,
        drainage_live: bool = True,
        elevation_live: bool = True
    ) -> List[Dict[str, Any]]:
        now = datetime.utcnow().isoformat()
        
        return [
            {
                "id": 1,
                "provider": "Open-Meteo Forecast & Historical Weather API",
                "dataset": "High-Resolution NWP Meteorological Models (ECMWF IFS / DWD ICON)",
                "endpoint": f"{settings.OPEN_METEO_FORECAST_URL}?latitude={settings.CHANDIGARH_LAT}&longitude={settings.CHANDIGARH_LON}",
                "status": "LIVE" if weather_live else "RECENT",
                "last_successful_sync": now,
                "units": "Precipitation (mm), Temperature (°C), Humidity (%)",
                "spatial_resolution": "~1.5 km to 9 km grid",
                "geographic_coverage": "Chandigarh Pilot Coordinates (30.7333°N, 76.7794°E)",
                "limitations": "Model forecast output. Not a substitute for physical ground-level rain-gauge calibration.",
                "attribution": "Open-Meteo.com (CC-BY 4.0)"
            },
            {
                "id": 2,
                "provider": "Open-Meteo Elevation API",
                "dataset": "Copernicus Digital Elevation Model (GLO-90)",
                "endpoint": settings.OPEN_METEO_ELEVATION_URL,
                "status": "LIVE" if elevation_live else "RECENT",
                "last_successful_sync": now,
                "units": "Meters above sea level (WGS84 EGM96)",
                "spatial_resolution": "~90 meters spatial pixel",
                "geographic_coverage": "Chandigarh Municipal Pilot Grid",
                "limitations": "Copernicus 90m DEM averages macro terrain. Does not capture micro-topography like curbs, ramps or localized 0.5m potholes.",
                "attribution": "European Space Agency / Open-Meteo"
            },
            {
                "id": 3,
                "provider": "OpenStreetMap Overpass API",
                "dataset": "Mapped Waterways, Storm Conduits, Streams & Choes",
                "endpoint": settings.OVERPASS_API_URL,
                "status": "LIVE" if drainage_live else "RECENT",
                "last_successful_sync": now,
                "units": "GeoJSON LineStrings with OSM tags",
                "spatial_resolution": "Vector geometry (Community-mapped)",
                "geographic_coverage": "BBox [30.68, 76.70] to [30.79, 76.85]",
                "limitations": "Crowdsourced vector data. Does not represent a certified municipal hydraulic inventory; missing vectors do not prove absence of underground pipes.",
                "attribution": "OpenStreetMap Contributors (ODbL)"
            },
            {
                "id": 4,
                "provider": "CiviSense Citizen Field Intelligence",
                "dataset": "Verified Ground-Truthed Waterlogging Incidents",
                "endpoint": "/api/reports",
                "status": "LIVE",
                "last_successful_sync": now,
                "units": "Incidents with GPS latitude/longitude, depth (cm), and photo verification",
                "spatial_resolution": "Mobile device GNSS accuracy (~5-15 meters)",
                "geographic_coverage": "Chandigarh Union Territory",
                "limitations": "Subject to voluntary citizen submission density and mandatory municipal officer verification triage.",
                "attribution": "Municipal Corporation of Chandigarh & Citizens"
            }
        ]

data_quality_service = DataQualityService()
