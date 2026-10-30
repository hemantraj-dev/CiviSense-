"""CIVISENSE Central Explainable Risk Engine
Predict. Prioritize. Prevent.

Formula:
Risk Score = 0.50 * P + 0.30 * D + 0.20 * T

Where:
P = normalized rainfall-related risk, 0–100.
D = normalized drainage-related vulnerability indicator, 0–100.
T = normalized terrain vulnerability indicator, 0–100.

Categories:
- Critical: 80–100
- High: 60–79
- Medium: 35–59
- Low: 0–34
"""

from typing import Dict, Any, Tuple, List

class RiskEngine:
    WEIGHT_RAINFALL = 0.50
    WEIGHT_DRAINAGE = 0.30
    WEIGHT_TERRAIN = 0.20
    
    # Rainfall thresholds (mm)
    HOURLY_MODERATE = 10.0
    HOURLY_HEAVY = 25.0
    HOURLY_VERY_HEAVY = 50.0
    
    ACCUM_24H_MODERATE = 35.0
    ACCUM_24H_HEAVY = 70.0
    ACCUM_24H_VERY_HEAVY = 120.0

    @classmethod
    def calculate_rainfall_score(
        cls,
        rainfall_1h: float,
        rainfall_3h: float,
        rainfall_24h: float,
        forecast_6h: float,
        forecast_24h: float
    ) -> float:
        """
        Normalizes multi-interval rainfall observations and forecasts into a 0-100 risk score P.
        Accounts for recent soil saturation (24h) and imminent convective intensity (1h, 6h forecast).
        """
        # Hourly rate intensity (up to 40 pts)
        hourly_val = max(rainfall_1h, forecast_6h / 6.0)
        p_hourly = min(40.0, (hourly_val / cls.HOURLY_VERY_HEAVY) * 40.0)
        
        # 3h & 6h forecast intensity (up to 30 pts)
        imminent = max(rainfall_3h, forecast_6h)
        p_imminent = min(30.0, (imminent / 45.0) * 30.0)
        
        # Cumulative soil saturation: 24h history + 24h forecast (up to 30 pts)
        saturation = (rainfall_24h * 0.6) + (forecast_24h * 0.4)
        p_sat = min(30.0, (saturation / cls.ACCUM_24H_VERY_HEAVY) * 30.0)
        
        score = p_hourly + p_imminent + p_sat
        return round(min(100.0, max(0.0, score)), 1)

    @classmethod
    def calculate_drainage_indicator(
        cls,
        baseline_drainage_factor: float = 50.0,
        mapped_drain_count: int = 1,
        stress_modifier_pct: float = 0.0
    ) -> float:
        """
        Calculates drainage vulnerability D (0-100).
        Higher score = higher vulnerability (i.e. poorer conveyance or higher stress/blockage).
        """
        base_vulnerability = float(baseline_drainage_factor)
        
        # Mapped drain density bonus (more mapped waterways reduces vulnerability slightly)
        if mapped_drain_count > 3:
            base_vulnerability -= 8.0
        elif mapped_drain_count == 0:
            base_vulnerability += 12.0
            
        # Apply simulated or operational stress modifier (-50% to +50%)
        effective_vulnerability = base_vulnerability * (1.0 + (stress_modifier_pct / 100.0))
        return round(min(100.0, max(5.0, effective_vulnerability)), 1)

    @classmethod
    def calculate_terrain_indicator(
        cls,
        elevation_m: float,
        reference_min_m: float = 310.0,
        reference_max_m: float = 365.0,
        terrain_stress_adj: float = 0.0
    ) -> float:
        """
        Calculates terrain vulnerability T (0-100).
        In Chandigarh, the natural gradient slopes downward southwest towards Patiala Ki Rao & N-Choe.
        Lower elevation relative to the regional gradient retains higher runoff and pooling vulnerability.
        """
        elevation_span = max(10.0, reference_max_m - reference_min_m)
        clamped_elevation = min(reference_max_m, max(reference_min_m, elevation_m))
        
        # Inverted relative elevation: lowest elevation = highest vulnerability (100)
        relative_depth = (reference_max_m - clamped_elevation) / elevation_span
        terrain_score = (relative_depth * 80.0) + 10.0  # Base scale 10 to 90
        terrain_score += terrain_stress_adj
        
        return round(min(100.0, max(5.0, terrain_score)), 1)

    @classmethod
    def determine_category(cls, score: float) -> str:
        if score >= 80.0:
            return "Critical"
        if score >= 60.0:
            return "High"
        if score >= 35.0:
            return "Medium"
        return "Low"

    @classmethod
    def determine_confidence(
        cls,
        has_live_weather: bool,
        has_elevation_sample: bool,
        has_drainage_features: bool,
        verified_reports_count: int
    ) -> Tuple[str, List[str]]:
        reasons = []
        confidence_points = 0
        
        if has_live_weather:
            confidence_points += 35
            reasons.append("Real-time Open-Meteo forecast and observation data active")
        else:
            reasons.append("Weather relying on cached or fallback observation")
            
        if has_elevation_sample:
            confidence_points += 30
            reasons.append("Copernicus DEM 90m terrain elevation sampled")
        else:
            reasons.append("Elevation estimated from regional baseline")
            
        if has_drainage_features:
            confidence_points += 20
            reasons.append("OpenStreetMap mapped waterways indexed (coverage limitations apply)")
        else:
            reasons.append("Drainage mapping coverage sparse or unindexed in OSM")
            
        if verified_reports_count > 0:
            confidence_points += 15
            reasons.append(f"{verified_reports_count} verified field citizen report(s) ground-truthed")
        else:
            reasons.append("No verified ground-truthed field inspection reports in past 24h")
            
        if confidence_points >= 75:
            level = "High"
        elif confidence_points >= 45:
            level = "Medium"
        else:
            level = "Low"
            
        return level, reasons

    @classmethod
    def assess_zone(
        cls,
        rainfall_1h: float,
        rainfall_3h: float,
        rainfall_24h: float,
        forecast_6h: float,
        forecast_24h: float,
        baseline_drainage_factor: float,
        mapped_drain_count: int,
        elevation_m: float,
        has_live_weather: bool = True,
        has_elevation_sample: bool = True,
        has_drainage_features: bool = True,
        verified_reports_count: int = 0,
        drainage_stress_pct: float = 0.0,
        terrain_stress_adj: float = 0.0,
        simulated: bool = False
    ) -> Dict[str, Any]:
        """
        Executes unified risk assessment returning mathematical score, weights, top factors,
        and natural-language municipal justification.
        """
        P = cls.calculate_rainfall_score(
            rainfall_1h, rainfall_3h, rainfall_24h, forecast_6h, forecast_24h
        )
        D = cls.calculate_drainage_indicator(
            baseline_drainage_factor, mapped_drain_count, drainage_stress_pct
        )
        T = cls.calculate_terrain_indicator(
            elevation_m, terrain_stress_adj=terrain_stress_adj
        )
        
        weighted_P = round(cls.WEIGHT_RAINFALL * P, 2)
        weighted_D = round(cls.WEIGHT_DRAINAGE * D, 2)
        weighted_T = round(cls.WEIGHT_TERRAIN * T, 2)
        
        overall_score = round(weighted_P + weighted_D + weighted_T, 1)
        category = cls.determine_category(overall_score)
        confidence_level, confidence_reasons = cls.determine_confidence(
            has_live_weather, has_elevation_sample, has_drainage_features, verified_reports_count
        )
        
        # Rank top contributing factors
        factors = [
            {"factor": "Rainfall Intensity & Forecast (P)", "score": P, "weighted": weighted_P, "weight": 0.50},
            {"factor": "Drainage Infrastructure Vulnerability (D)", "score": D, "weighted": weighted_D, "weight": 0.30},
            {"factor": "Terrain & Elevation Depression (T)", "score": T, "weighted": weighted_T, "weight": 0.20}
        ]
        factors.sort(key=lambda x: x["weighted"], reverse=True)
        top_two = [f["factor"] for f in factors[:2]]
        
        # Explainable natural-language narrative
        explanation_parts = []
        if overall_score >= 80.0:
            explanation_parts.append("CRITICAL waterlogging vulnerability detected.")
        elif overall_score >= 60.0:
            explanation_parts.append("ELEVATED waterlogging risk identified.")
        elif overall_score >= 35.0:
            explanation_parts.append("MODERATE waterlogging risk under current meteorological stress.")
        else:
            explanation_parts.append("LOW waterlogging vulnerability under normal baseline conditions.")
            
        explanation_parts.append(
            f"The primary driver is {top_two[0]} contributing {factors[0]['weighted']} pts, "
            f"followed by {top_two[1]} contributing {factors[1]['weighted']} pts to the overall score of {overall_score}/100."
        )
        if P > 60:
            explanation_parts.append("Severe precipitation forecast exceeds regional storm absorption capacity.")
        if D > 65:
            explanation_parts.append("Mapped drainage indicators show restricted conveyance or elevated conveyance stress.")
        if T > 60:
            explanation_parts.append("Zone sits in a local terrain depression relative to Chandigarh's southwest slope.")
            
        explanation = " ".join(explanation_parts)
        
        # Municipal recommended action
        if overall_score >= 80.0:
            recommended_action = "Immediate preventive mobile pump deployment & pre-storm culvert clearance."
            action_priority = "Critical"
        elif overall_score >= 60.0:
            recommended_action = "Priority drainage inspection & silt trap verification within 4 hours."
            action_priority = "High"
        elif overall_score >= 35.0:
            recommended_action = "Routine roadside drain check & maintenance monitoring."
            action_priority = "Medium"
        else:
            recommended_action = "Standard baseline monitoring; no emergency intervention required."
            action_priority = "Low"
            
        return {
            "rainfall_score": P,
            "drainage_indicator": D,
            "terrain_indicator": T,
            "overall_risk_score": overall_score,
            "risk_category": category,
            "confidence_level": confidence_level,
            "confidence_reasons": confidence_reasons,
            "weights": {"P": 0.50, "D": 0.30, "T": 0.20},
            "weighted_contributions": {
                "rainfall": weighted_P,
                "drainage": weighted_D,
                "terrain": weighted_T
            },
            "top_contributing_factors": top_two,
            "explanation": explanation,
            "recommended_action": recommended_action,
            "action_priority": action_priority,
            "is_simulated": simulated
        }
