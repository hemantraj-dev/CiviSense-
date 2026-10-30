export interface Zone {
  id: number;
  zone_code: string;
  zone_name: string;
  representative_latitude: number;
  representative_longitude: number;
  elevation_m: number;
  baseline_drainage_factor: number;
  mapped_drain_count: number;
  description: string;
  boundary_geojson: {
    type: string;
    coordinates: number[][][];
  };
  latest_risk_score?: number;
  risk_category?: 'Critical' | 'High' | 'Medium' | 'Low';
  confidence_level?: 'High' | 'Medium' | 'Low';
  recommended_action?: string;
  priority_rank?: number;
  contributing_factors?: {
    rainfall: number;
    drainage: number;
    terrain: number;
  };
}

export interface WeatherData {
  latitude: number;
  longitude: number;
  timezone: string;
  temperature: number;
  relative_humidity: number;
  current_rain_mm: number;
  rainfall_1h: number;
  rainfall_3h: number;
  rainfall_24h: number;
  rainfall_72h: number;
  forecast_6h: number;
  forecast_24h: number;
  source: string;
  attribution: string;
  retrieved_at: string;
  is_live: boolean;
  hourly_series: {
    time: string;
    full_time: string;
    precipitation_mm: number;
    probability_pct: number;
    is_forecast: boolean;
  }[];
}

export interface CitizenReport {
  id: number;
  report_number: string;
  zone_id: number;
  reporter_name?: string;
  location: string;
  latitude: number;
  longitude: number;
  description: string;
  image_url?: string;
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  water_depth_cm: number;
  verification_status: 'Submitted' | 'Under Review' | 'Verified' | 'Rejected' | 'Resolved';
  duplicate_warning: boolean;
  reported_at: string;
}

export interface MunicipalAction {
  id: number;
  action_code: string;
  zone_id: number;
  zone_name: string;
  action_type: string;
  description: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  status: 'Pending Review' | 'Approved' | 'Assigned' | 'In Progress' | 'Completed' | 'Rejected';
  assigned_team: string;
  inspection_notes?: string;
  created_at: string;
}
