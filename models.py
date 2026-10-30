from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
)
from sqlalchemy.orm import relationship
from app.database.session import Base

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_code = Column(String(50), unique=True, index=True, nullable=False)
    zone_name = Column(String(100), nullable=False)
    boundary_geojson = Column(JSON, nullable=False)
    representative_latitude = Column(Float, nullable=False)
    representative_longitude = Column(Float, nullable=False)
    elevation_m = Column(Float, nullable=True)
    baseline_drainage_factor = Column(Float, default=50.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    risk_assessments = relationship("RiskAssessment", back_populates="zone")
    actions = relationship("ActionRecommendation", back_populates="zone")
    citizen_reports = relationship("CitizenReport", back_populates="zone")

class WeatherObservation(Base):
    __tablename__ = "weather_observations"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rainfall_1h = Column(Float, default=0.0)
    rainfall_3h = Column(Float, default=0.0)
    rainfall_24h = Column(Float, default=0.0)
    rainfall_72h = Column(Float, default=0.0)
    forecast_6h = Column(Float, default=0.0)
    forecast_24h = Column(Float, default=0.0)
    temperature = Column(Float, nullable=True)
    relative_humidity = Column(Float, nullable=True)
    raw_payload = Column(JSON, nullable=True)
    source = Column(String(100), default="Open-Meteo Forecast & Historical API")
    retrieved_at = Column(DateTime, default=datetime.utcnow)

class DrainageFeature(Base):
    __tablename__ = "drainage_features"
    
    id = Column(Integer, primary_key=True, index=True)
    osm_id = Column(String(100), index=True, nullable=False)
    feature_type = Column(String(50), nullable=False)  # drain, ditch, canal, river, stream
    name = Column(String(150), nullable=True)
    geometry = Column(JSON, nullable=False)            # GeoJSON geometry
    available_tags = Column(JSON, nullable=True)
    source = Column(String(100), default="OpenStreetMap Overpass API")
    retrieved_at = Column(DateTime, default=datetime.utcnow)

class TerrainSample(Base):
    __tablename__ = "terrain_samples"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation_m = Column(Float, nullable=False)
    source = Column(String(100), default="Open-Meteo Elevation API (Copernicus DEM GLO-90)")
    retrieved_at = Column(DateTime, default=datetime.utcnow)

class CitizenReport(Base):
    __tablename__ = "citizen_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_number = Column(String(50), unique=True, index=True, nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)
    reporter_name = Column(String(100), nullable=True)
    location = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    severity = Column(String(20), nullable=False)       # Low, Medium, High, Critical
    water_depth_cm = Column(Float, nullable=True)
    verification_status = Column(String(30), default="Submitted")  # Submitted, Under Review, Verified, Rejected, Resolved
    duplicate_warning = Column(Boolean, default=False)
    reported_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    zone = relationship("Zone", back_populates="citizen_reports")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    rainfall_score = Column(Float, nullable=False)       # P (0-100)
    drainage_indicator = Column(Float, nullable=False)   # D (0-100)
    terrain_indicator = Column(Float, nullable=False)    # T (0-100)
    overall_risk_score = Column(Float, nullable=False)   # Score = 0.50*P + 0.30*D + 0.20*T
    risk_category = Column(String(20), nullable=False)   # Low, Medium, High, Critical
    confidence_level = Column(String(20), nullable=False)# Low, Medium, High
    explanation = Column(Text, nullable=False)
    contributing_factors = Column(JSON, nullable=True)
    is_simulated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    zone = relationship("Zone", back_populates="risk_assessments")
    actions = relationship("ActionRecommendation", back_populates="assessment")

class ActionRecommendation(Base):
    __tablename__ = "action_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    action_code = Column(String(50), unique=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("risk_assessments.id"), nullable=True)
    action_type = Column(String(100), nullable=False)     # Drainage inspection, Drain cleaning review, etc.
    description = Column(Text, nullable=False)
    priority = Column(String(20), nullable=False)         # Critical, High, Medium, Low
    status = Column(String(30), default="Pending Review") # Pending Review, Approved, Assigned, Inspection in Progress, Completed, Rejected
    assigned_team = Column(String(100), nullable=True)
    inspection_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    zone = relationship("Zone", back_populates="actions")
    assessment = relationship("RiskAssessment", back_populates="actions")

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_name = Column(String(100), nullable=False)
    input_parameters = Column(JSON, nullable=False)
    baseline_score = Column(Float, nullable=False)
    simulated_score = Column(Float, nullable=False)
    zone_results = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DataSourceLog(Base):
    __tablename__ = "data_source_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(100), nullable=False)
    endpoint = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False)          # LIVE, RECENT, HISTORICAL, ESTIMATED, SYNTHETIC, MISSING, STALE, ERROR
    last_success = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    spatial_resolution = Column(String(100), nullable=True)
    geographic_coverage = Column(String(100), nullable=True)
    limitations = Column(Text, nullable=True)
    retrieved_at = Column(DateTime, default=datetime.utcnow)
