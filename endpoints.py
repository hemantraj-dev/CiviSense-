from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.services.weather_service import weather_service
from app.services.drainage_service import drainage_service
from app.services.terrain_service import terrain_service
from app.services.zone_service import zone_service
from app.services.data_quality_service import data_quality_service
from app.risk_engine.engine import RiskEngine

from app.schemas.schemas import (
    CitizenReportCreate, CitizenReportStatusUpdate,
    ActionRecommendationCreate, ActionRecommendationUpdate,
    ScenarioSimulateRequest, ScenarioSaveRequest
)

router = APIRouter()

# In-memory storage for demonstration operational workflows
CITIZEN_REPORTS_DB: List[Dict[str, Any]] = [
    {
        "id": 1,
        "report_number": "REP-2026-001",
        "zone_id": 4,
        "reporter_name": "Sanjay Sharma",
        "location": "Plot 182, Industrial Area Phase I near drain culvert",
        "latitude": 30.7048,
        "longitude": 76.8021,
        "description": "Standing water roughly 25-30 cm deep accumulating across main access road. Culvert grate blocked by discarded packaging material.",
        "image_url": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=600&q=80",
        "severity": "High",
        "water_depth_cm": 28.0,
        "verification_status": "Verified",
        "duplicate_warning": False,
        "reported_at": "2026-10-30T10:15:00",
        "created_at": "2026-10-30T10:15:00"
    },
    {
        "id": 2,
        "report_number": "REP-2026-002",
        "zone_id": 8,
        "reporter_name": "Pooja Verma",
        "location": "Old Ropar Road, near Modern Housing Complex gate, Manimajra",
        "latitude": 30.7235,
        "longitude": 76.8432,
        "description": "Roadside storm drain overflowing onto pedestrian footpath. Two motorbikes slipped earlier.",
        "image_url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80",
        "severity": "Critical",
        "water_depth_cm": 35.0,
        "verification_status": "Under Review",
        "duplicate_warning": False,
        "reported_at": "2026-10-30T11:40:00",
        "created_at": "2026-10-30T11:40:00"
    },
    {
        "id": 3,
        "report_number": "REP-2026-003",
        "zone_id": 2,
        "reporter_name": "Aman Deep Singh",
        "location": "Rear Service Lane, Block C, Sector 22-B",
        "latitude": 30.7295,
        "longitude": 76.7712,
        "description": "Slow drainage after mild shower. Water pooling at road bend, approx 10cm depth.",
        "image_url": None,
        "severity": "Medium",
        "water_depth_cm": 12.0,
        "verification_status": "Submitted",
        "duplicate_warning": False,
        "reported_at": "2026-10-30T14:20:00",
        "created_at": "2026-10-30T14:20:00"
    }
]

ACTIONS_DB: List[Dict[str, Any]] = [
    {
        "id": 1,
        "action_code": "ACT-2026-081",
        "zone_id": 4,
        "zone_name": "Industrial Area Phase I (Low-lying Pocket)",
        "assessment_id": 4,
        "action_type": "Drain Cleaning & Silt Clearance Review",
        "description": "Deploy emergency jetting machine to de-silt collector drain siphon near Plot 182 before next rainfall forecast window.",
        "priority": "Critical",
        "status": "In Progress",
        "assigned_team": "MC Rapid Response Crew 2 (South Zone)",
        "inspection_notes": "Crew mobilized. Silt removal in progress. Grate debris cleared.",
        "created_at": "2026-10-30T10:45:00",
        "updated_at": "2026-10-30T12:00:00"
    },
    {
        "id": 2,
        "action_code": "ACT-2026-082",
        "zone_id": 8,
        "zone_name": "Manimajra (Low-lying Urban Settlement)",
        "assessment_id": 8,
        "action_type": "Waterlogging Site Verification & Pump Standby",
        "description": "Inspect road culvert near Modern Housing Complex. Place 1x 100 HP diesel dewatering pump on standby.",
        "priority": "High",
        "status": "Approved",
        "assigned_team": "Manimajra Drainage Division (Subdivision 4)",
        "inspection_notes": "Approved by Executive Engineer. Pump dispatched to site depot.",
        "created_at": "2026-10-30T11:55:00",
        "updated_at": "2026-10-30T12:30:00"
    },
    {
        "id": 3,
        "action_code": "ACT-2026-083",
        "zone_id": 2,
        "zone_name": "Sector 22 (Dense Mixed Urban Market)",
        "assessment_id": 2,
        "action_type": "Roadside Gully Trap Inspection",
        "description": "Inspect Shastri Market perimeter catchpits and clear accumulated plastic waste from grates.",
        "priority": "Medium",
        "status": "Pending Review",
        "assigned_team": "Central Zone Maintenance",
        "inspection_notes": "Pending routine shift assignment.",
        "created_at": "2026-10-30T14:35:00",
        "updated_at": "2026-10-30T14:35:00"
    }
]

SAVED_SCENARIOS_DB: List[Dict[str, Any]] = [
    {
        "id": 1,
        "scenario_name": "Monsoon Cloudburst Stress (75mm/h Downpour)",
        "input_parameters": {
            "rainfall_mm": 75.0,
            "drainage_stress_pct": 35.0,
            "terrain_vulnerability_adj": 10.0
        },
        "baseline_score": 38.4,
        "simulated_score": 84.6,
        "created_at": "2026-10-30T09:00:00"
    },
    {
        "id": 2,
        "scenario_name": "Post-Desilting Preventive Clean (-40% Vulnerability)",
        "input_parameters": {
            "rainfall_mm": 30.0,
            "drainage_stress_pct": -40.0,
            "terrain_vulnerability_adj": 0.0
        },
        "baseline_score": 42.1,
        "simulated_score": 24.8,
        "created_at": "2026-10-30T09:30:00"
    }
]

# 1. Health & Config
@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "pilot_geography": settings.PILOT_CITY,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/config")
def get_config():
    return {
        "project_name": settings.PROJECT_NAME,
        "pilot_city": settings.PILOT_CITY,
        "center_coordinates": {
            "latitude": settings.CHANDIGARH_LAT,
            "longitude": settings.CHANDIGARH_LON
        },
        "timezone": settings.TIMEZONE,
        "weights": {
            "rainfall": RiskEngine.WEIGHT_RAINFALL,
            "drainage": RiskEngine.WEIGHT_DRAINAGE,
            "terrain": RiskEngine.WEIGHT_TERRAIN
        },
        "categories": {
            "critical": "80-100",
            "high": "60-79",
            "medium": "35-59",
            "low": "0-34"
        }
    }

@router.get("/data-sources/status")
async def get_data_sources_status():
    weather = await weather_service.get_chandigarh_weather()
    drainage = await drainage_service.get_chandigarh_drainage()
    return data_quality_service.get_data_sources_status(
        weather_live=weather.get("is_live", True),
        drainage_live=drainage.get("is_live", True)
    )

# 2. Weather
@router.get("/weather/current")
async def get_weather_current():
    return await weather_service.get_chandigarh_weather()

@router.get("/weather/forecast")
async def get_weather_forecast():
    w = await weather_service.get_chandigarh_weather()
    return {
        "forecast_6h_mm": w["forecast_6h"],
        "forecast_24h_mm": w["forecast_24h"],
        "hourly_series": w["hourly_series"],
        "retrieved_at": w["retrieved_at"],
        "attribution": w["attribution"]
    }

@router.get("/weather/history")
async def get_weather_history():
    w = await weather_service.get_chandigarh_weather()
    return {
        "rainfall_1h_mm": w["rainfall_1h"],
        "rainfall_3h_mm": w["rainfall_3h"],
        "rainfall_24h_mm": w["rainfall_24h"],
        "rainfall_72h_mm": w["rainfall_72h"],
        "retrieved_at": w["retrieved_at"]
    }

# 3. Drainage
@router.get("/drainage/features")
async def get_drainage_features():
    return await drainage_service.get_chandigarh_drainage()

@router.get("/drainage/summary")
async def get_drainage_summary():
    d = await drainage_service.get_chandigarh_drainage()
    return {
        "feature_count": d["feature_count"],
        "label": d["label"],
        "disclaimer": d["disclaimer"],
        "source": d["source"],
        "retrieved_at": d["retrieved_at"]
    }

# 4. Terrain
@router.get("/terrain/samples")
async def get_terrain_samples():
    zones = zone_service.get_all_zones()
    coords = [{"lat": z["representative_latitude"], "lon": z["representative_longitude"], "zone_id": z["id"]} for z in zones]
    return await terrain_service.get_elevations(coords)

@router.get("/terrain/zones/{zone_id}")
async def get_terrain_by_zone(zone_id: int):
    zone = zone_service.get_zone_by_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    res = await terrain_service.get_elevations([{
        "lat": zone["representative_latitude"],
        "lon": zone["representative_longitude"],
        "zone_id": zone["id"]
    }])
    return res[0] if res else {"elevation_m": zone["elevation_m"]}

# 5. Zones & Zone Intelligence
@router.get("/zones")
async def get_zones():
    weather = await weather_service.get_chandigarh_weather()
    assessments = zone_service.assess_all_zones(weather)
    assess_map = {a["zone_id"]: a for a in assessments}
    
    zones = zone_service.get_all_zones()
    enriched = []
    for z in zones:
        copy_z = dict(z)
        ass = assess_map.get(z["id"], {})
        copy_z["latest_risk_score"] = ass.get("overall_risk_score", 0.0)
        copy_z["risk_category"] = ass.get("risk_category", "Low")
        copy_z["confidence_level"] = ass.get("confidence_level", "Medium")
        copy_z["priority_rank"] = ass.get("priority_rank", 10)
        copy_z["recommended_action"] = ass.get("recommended_action", "")
        enriched.append(copy_z)
    return enriched

@router.get("/zones/{zone_id}")
def get_zone(zone_id: int):
    zone = zone_service.get_zone_by_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

@router.get("/zones/{zone_id}/intelligence")
async def get_zone_intelligence(zone_id: int):
    zone = zone_service.get_zone_by_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    weather = await weather_service.get_chandigarh_weather()
    assessment = RiskEngine.assess_zone(
        rainfall_1h=weather.get("rainfall_1h", 0.0),
        rainfall_3h=weather.get("rainfall_3h", 0.0),
        rainfall_24h=weather.get("rainfall_24h", 0.0),
        forecast_6h=weather.get("forecast_6h", 0.0),
        forecast_24h=weather.get("forecast_24h", 0.0),
        baseline_drainage_factor=zone["baseline_drainage_factor"],
        mapped_drain_count=zone["mapped_drain_count"],
        elevation_m=zone["elevation_m"],
        has_live_weather=weather.get("is_live", True),
        has_elevation_sample=True,
        has_drainage_features=True,
        verified_reports_count=len([r for r in CITIZEN_REPORTS_DB if r.get("zone_id") == zone_id and r.get("verification_status") == "Verified"])
    )
    zone_reports = [r for r in CITIZEN_REPORTS_DB if r.get("zone_id") == zone_id]
    zone_actions = [a for a in ACTIONS_DB if a.get("zone_id") == zone_id]
    
    return {
        "zone": zone,
        "assessment": assessment,
        "weather_context": weather,
        "reports": zone_reports,
        "actions": zone_actions
    }

# 6. Risk Engine
@router.get("/risk/assessments")
async def get_all_assessments():
    weather = await weather_service.get_chandigarh_weather()
    return zone_service.assess_all_zones(weather)

@router.post("/risk/assess")
def assess_custom_zone(
    rainfall_1h: float = Body(0.0),
    rainfall_3h: float = Body(0.0),
    rainfall_24h: float = Body(0.0),
    forecast_6h: float = Body(0.0),
    forecast_24h: float = Body(0.0),
    baseline_drainage_factor: float = Body(50.0),
    mapped_drain_count: int = Body(1),
    elevation_m: float = Body(330.0)
):
    return RiskEngine.assess_zone(
        rainfall_1h=rainfall_1h,
        rainfall_3h=rainfall_3h,
        rainfall_24h=rainfall_24h,
        forecast_6h=forecast_6h,
        forecast_24h=forecast_24h,
        baseline_drainage_factor=baseline_drainage_factor,
        mapped_drain_count=mapped_drain_count,
        elevation_m=elevation_m
    )

@router.get("/risk/zones/{zone_id}")
async def get_zone_risk(zone_id: int):
    zone = zone_service.get_zone_by_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    weather = await weather_service.get_chandigarh_weather()
    return RiskEngine.assess_zone(
        rainfall_1h=weather.get("rainfall_1h", 0.0),
        rainfall_3h=weather.get("rainfall_3h", 0.0),
        rainfall_24h=weather.get("rainfall_24h", 0.0),
        forecast_6h=weather.get("forecast_6h", 0.0),
        forecast_24h=weather.get("forecast_24h", 0.0),
        baseline_drainage_factor=zone["baseline_drainage_factor"],
        mapped_drain_count=zone["mapped_drain_count"],
        elevation_m=zone["elevation_m"]
    )

# 7. Citizen Reports
@router.post("/reports")
def create_report(report: CitizenReportCreate):
    # Detect potential duplicate by proximity (within ~150 meters of existing reports)
    is_duplicate = False
    for r in CITIZEN_REPORTS_DB:
        dist = ((r["latitude"] - report.latitude)**2 + (r["longitude"] - report.longitude)**2)**0.5
        if dist < 0.0015:  # roughly 150 meters
            is_duplicate = True
            break

    new_id = len(CITIZEN_REPORTS_DB) + 1
    new_report = {
        "id": new_id,
        "report_number": f"REP-2026-{new_id:03d}",
        "zone_id": report.zone_id or 1,
        "reporter_name": report.reporter_name or "Anonymous Citizen",
        "location": report.location,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "description": report.description,
        "image_url": report.image_url,
        "severity": report.severity,
        "water_depth_cm": report.water_depth_cm or 15.0,
        "verification_status": "Submitted",
        "duplicate_warning": is_duplicate,
        "reported_at": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat()
    }
    CITIZEN_REPORTS_DB.insert(0, new_report)
    return new_report

@router.get("/reports")
def get_reports(status: Optional[str] = None):
    if status:
        return [r for r in CITIZEN_REPORTS_DB if r.get("verification_status") == status]
    return CITIZEN_REPORTS_DB

@router.get("/reports/{report_id}")
def get_report(report_id: int):
    for r in CITIZEN_REPORTS_DB:
        if r["id"] == report_id:
            return r
    raise HTTPException(status_code=404, detail="Citizen report not found")

@router.patch("/reports/{report_id}/status")
def update_report_status(report_id: int, update: CitizenReportStatusUpdate):
    for r in CITIZEN_REPORTS_DB:
        if r["id"] == report_id:
            r["verification_status"] = update.verification_status
            if update.duplicate_warning is not None:
                r["duplicate_warning"] = update.duplicate_warning
            return r
    raise HTTPException(status_code=404, detail="Citizen report not found")

# 8. Action Management
@router.post("/actions")
def create_action(action: ActionRecommendationCreate):
    new_id = len(ACTIONS_DB) + 1
    zone = zone_service.get_zone_by_id(action.zone_id)
    new_act = {
        "id": new_id,
        "action_code": f"ACT-2026-{80 + new_id:03d}",
        "zone_id": action.zone_id,
        "zone_name": zone["zone_name"] if zone else f"Zone {action.zone_id}",
        "assessment_id": action.assessment_id,
        "action_type": action.action_type,
        "description": action.description,
        "priority": action.priority,
        "status": "Pending Review",
        "assigned_team": action.assigned_team or "Unassigned Municipal Crew",
        "inspection_notes": "Created via CiviSense Prevention Command.",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    ACTIONS_DB.insert(0, new_act)
    return new_act

@router.get("/actions")
def get_actions(status: Optional[str] = None):
    if status:
        return [a for a in ACTIONS_DB if a.get("status") == status]
    return ACTIONS_DB

@router.get("/actions/{action_id}")
def get_action(action_id: int):
    for a in ACTIONS_DB:
        if a["id"] == action_id:
            return a
    raise HTTPException(status_code=404, detail="Action not found")

@router.patch("/actions/{action_id}")
def update_action(action_id: int, update: ActionRecommendationUpdate):
    for a in ACTIONS_DB:
        if a["id"] == action_id:
            if update.status:
                a["status"] = update.status
            if update.assigned_team:
                a["assigned_team"] = update.assigned_team
            if update.inspection_notes:
                a["inspection_notes"] = update.inspection_notes
            if update.priority:
                a["priority"] = update.priority
            a["updated_at"] = datetime.utcnow().isoformat()
            return a
    raise HTTPException(status_code=404, detail="Action not found")

# 9. Scenarios / Decision Lab
@router.post("/scenarios/simulate")
async def simulate_scenario(req: ScenarioSimulateRequest):
    weather = await weather_service.get_chandigarh_weather()
    zones = zone_service.get_all_zones()
    
    simulated_results = []
    baseline_scores = []
    simulated_scores = []
    
    for z in zones:
        # Baseline assessment with live weather
        base = RiskEngine.assess_zone(
            rainfall_1h=weather.get("rainfall_1h", 0.0),
            rainfall_3h=weather.get("rainfall_3h", 0.0),
            rainfall_24h=weather.get("rainfall_24h", 0.0),
            forecast_6h=weather.get("forecast_6h", 0.0),
            forecast_24h=weather.get("forecast_24h", 0.0),
            baseline_drainage_factor=z["baseline_drainage_factor"],
            mapped_drain_count=z["mapped_drain_count"],
            elevation_m=z["elevation_m"]
        )
        baseline_scores.append(base["overall_risk_score"])
        
        # User simulated parameters
        sim = RiskEngine.assess_zone(
            rainfall_1h=req.rainfall_mm,
            rainfall_3h=req.rainfall_mm * 1.5,
            rainfall_24h=req.rainfall_mm * 2.5,
            forecast_6h=req.rainfall_mm * 0.8,
            forecast_24h=req.rainfall_mm * 1.2,
            baseline_drainage_factor=z["baseline_drainage_factor"],
            mapped_drain_count=z["mapped_drain_count"],
            elevation_m=z["elevation_m"],
            drainage_stress_pct=req.drainage_stress_pct,
            terrain_stress_adj=req.terrain_vulnerability_adj,
            simulated=True
        )
        sim["zone_id"] = z["id"]
        sim["zone_code"] = z["zone_code"]
        sim["zone_name"] = z["zone_name"]
        sim["baseline_score"] = base["overall_risk_score"]
        sim["score_diff"] = round(sim["overall_risk_score"] - base["overall_risk_score"], 1)
        simulated_scores.append(sim["overall_risk_score"])
        simulated_results.append(sim)

    simulated_results.sort(key=lambda x: x["overall_risk_score"], reverse=True)
    for r, item in enumerate(simulated_results, start=1):
        item["simulated_rank"] = r

    avg_base = round(sum(baseline_scores) / len(baseline_scores), 1)
    avg_sim = round(sum(simulated_scores) / len(simulated_scores), 1)

    return {
        "city_baseline_avg": avg_base,
        "city_simulated_avg": avg_sim,
        "score_delta": round(avg_sim - avg_base, 1),
        "zones_count": len(simulated_results),
        "critical_zones_count": len([s for s in simulated_results if s["risk_category"] == "Critical"]),
        "high_zones_count": len([s for s in simulated_results if s["risk_category"] == "High"]),
        "results": simulated_results
    }

@router.post("/scenarios")
def save_scenario(req: ScenarioSaveRequest):
    new_id = len(SAVED_SCENARIOS_DB) + 1
    new_scen = {
        "id": new_id,
        "scenario_name": req.scenario_name,
        "input_parameters": req.input_parameters,
        "baseline_score": req.baseline_score,
        "simulated_score": req.simulated_score,
        "created_at": datetime.utcnow().isoformat()
    }
    SAVED_SCENARIOS_DB.insert(0, new_scen)
    return new_scen

@router.get("/scenarios")
def get_scenarios():
    return SAVED_SCENARIOS_DB

@router.get("/scenarios/{scenario_id}")
def get_scenario(scenario_id: int):
    for s in SAVED_SCENARIOS_DB:
        if s["id"] == scenario_id:
            return s
    raise HTTPException(status_code=404, detail="Scenario not found")

# 10. Analytics
@router.get("/analytics/overview")
async def get_analytics_overview():
    weather = await weather_service.get_chandigarh_weather()
    assessments = zone_service.assess_all_zones(weather)
    
    crit = len([a for a in assessments if a["risk_category"] == "Critical"])
    high = len([a for a in assessments if a["risk_category"] == "High"])
    med = len([a for a in assessments if a["risk_category"] == "Medium"])
    low = len([a for a in assessments if a["risk_category"] == "Low"])
    
    verified_reports = len([r for r in CITIZEN_REPORTS_DB if r.get("verification_status") == "Verified"])
    pending_reports = len([r for r in CITIZEN_REPORTS_DB if r.get("verification_status") in ["Submitted", "Under Review"]])
    active_actions = len([a for a in ACTIONS_DB if a.get("status") in ["Pending Review", "Approved", "In Progress"]])
    
    return {
        "pilot_city": settings.PILOT_CITY,
        "weather": weather,
        "zones_total": len(assessments),
        "risk_breakdown": {
            "critical": crit,
            "high": high,
            "medium": med,
            "low": low
        },
        "citizen_reports": {
            "total": len(CITIZEN_REPORTS_DB),
            "verified": verified_reports,
            "pending": pending_reports
        },
        "actions": {
            "total": len(ACTIONS_DB),
            "active": active_actions
        },
        "top_priority_zone": assessments[0] if assessments else None
    }

@router.get("/analytics/risk-distribution")
async def get_risk_distribution():
    weather = await weather_service.get_chandigarh_weather()
    assessments = zone_service.assess_all_zones(weather)
    return [
        {"name": "Critical (80-100)", "count": len([a for a in assessments if a["risk_category"] == "Critical"]), "color": "#B94B48"},
        {"name": "High (60-79)", "count": len([a for a in assessments if a["risk_category"] == "High"]), "color": "#D18A35"},
        {"name": "Medium (35-59)", "count": len([a for a in assessments if a["risk_category"] == "Medium"]), "color": "#D2B64B"},
        {"name": "Low (0-34)", "count": len([a for a in assessments if a["risk_category"] == "Low"]), "color": "#438A69"}
    ]

@router.get("/analytics/rainfall-trend")
async def get_rainfall_trend():
    w = await weather_service.get_chandigarh_weather()
    return w.get("hourly_series", [])
