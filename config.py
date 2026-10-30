from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CIVISENSE"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = "sqlite:///./civisense.db"
    
    # Pilot Geography: Chandigarh, India
    PILOT_CITY: str = "Chandigarh, India"
    CHANDIGARH_LAT: float = 30.7333
    CHANDIGARH_LON: float = 76.7794
    TIMEZONE: str = "Asia/Kolkata"
    
    # External APIs
    OPEN_METEO_FORECAST_URL: str = "https://api.open-meteo.com/v1/forecast"
    OPEN_METEO_HISTORICAL_URL: str = "https://archive-api.open-meteo.com/v1/archive"
    OPEN_METEO_ELEVATION_URL: str = "https://api.open-meteo.com/v1/elevation"
    OVERPASS_API_URL: str = "https://overpass-api.de/api/interpreter"
    
    # Caching durations (seconds)
    WEATHER_CACHE_TTL: int = 900       # 15 minutes
    DRAINAGE_CACHE_TTL: int = 86400    # 24 hours
    TERRAIN_CACHE_TTL: int = 604800    # 7 days
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
