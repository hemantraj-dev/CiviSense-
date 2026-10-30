from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ZoneBase(BaseModel):
    zone_code: str
    zone_name: str
    boundary_geojson: Dict[str, Any]
    representative_latitude: float
    representative_longitude: float
    elevation_m: Optional[float] = None
    baseline_drainage_factor: Optional[float] = 50.0

class ZoneOut(ZoneBase):
    id: int
    created_at: datetime
    latest_risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    confidence_level: Optional[str] = None

    class Config:
        from_attributes = True

class WeatherSummary(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    temperature: Optional[float]
    relative_humidity: Optional[float]
    current_rain_mm: float
    rainfall_1h: float
    rainfall_3h: float
    rainfall_24h: float
    rainfall_72h: float
    forecast_6h: float
    forecast_24h: float
    source: str
    retrieved_at: datetime
    is_live: bool
    hourly_series: Optional[List[Dict[str, Any]]] = None

class DrainageFeatureOut(BaseModel):
    id: int
    osm_id: str
    feature_type: str
    name: Optional[str]
    geometry: Dict[str, Any]
    available_tags: Optional[Dict[str, Any]]
    source: str
    retrieved_at: datetime

    class Config:
        from_attributes = True

class TerrainSampleOut(BaseModel):
    id: int
    zone_id: Optional[int]
    latitude: float
    longitude: float
    elevation_m: float
    source: str
    retrieved_at: datetime

    class Config:
        from_attributes = True

class CitizenReportCreate(BaseModel):
    reporter_name: Optional[str] = "Anonymous Citizen"
    location: str = Field(..., min_length=3)
    latitude: float
    longitude: float
    description: str = Field(..., min_length=5)
    image_url: Optional[str] = None
    severity: str = "Medium"
    water_depth_cm: Optional[float] = None
    zone_id: Optional[int] = None

class CitizenReportStatusUpdate(BaseModel):
    verification_status: str  # Submitted, Under Review, Verified, Rejected, Resolved
    duplicate_warning: Optional[bool] = None

class CitizenReportOut(BaseModel):
    id: int
    report_number: str
    zone_id: Optional[int]
    reporter_name: Optional[str]
    location: str
    latitude: float
    longitude: float
    description: str
    image_url: Optional[str]
    severity: str
    water_depth_cm: Optional[float]
    verification_status: str
    duplicate_warning: bool
    reported_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class RiskAssessmentOut(BaseModel):
    id: int
    zone_id: int
    zone_name: Optional[str] = None
    zone_code: Optional[str] = None
    rainfall_score: float
    drainage_indicator: float
    terrain_indicator: float
    overall_risk_score: float
    risk_category: str
    confidence_level: str
    explanation: str
    contributing_factors: Optional[Dict[str, Any]] = None
    is_simulated: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ActionRecommendationCreate(BaseModel):
    zone_id: int
    assessment_id: Optional[int] = None
    action_type: str
    description: str
    priority: str = "Medium"
    assigned_team: Optional[str] = None

class ActionRecommendationUpdate(BaseModel):
    status: Optional[str] = None
    assigned_team: Optional[str] = None
    inspection_notes: Optional[str] = None
    priority: Optional[str] = None

class ActionRecommendationOut(BaseModel):
    id: int
    action_code: str
    zone_id: int
    zone_name: Optional[str] = None
    assessment_id: Optional[int]
    action_type: str
    description: str
    priority: str
    status: str
    assigned_team: Optional[str]
    inspection_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScenarioSimulateRequest(BaseModel):
    zone_id: Optional[int] = None  # None for city-wide simulation
    rainfall_mm: float             # 0 to 150 mm
    drainage_stress_pct: float     # -50% to +50% (positive = stress/blockage, negative = improved)
    terrain_vulnerability_adj: float # -20 to +20

class ScenarioSaveRequest(BaseModel):
    scenario_name: str
    input_parameters: Dict[str, Any]
    baseline_score: float
    simulated_score: float
    zone_results: Optional[List[Dict[str, Any]]] = None

class DataSourceLogOut(BaseModel):
    id: int
    provider: str
    endpoint: str
    status: str
    last_success: Optional[datetime]
    last_error: Optional[str]
    spatial_resolution: Optional[str]
    geographic_coverage: Optional[str]
    limitations: Optional[str]
    retrieved_at: datetime

    class Config:
        from_attributes = True
