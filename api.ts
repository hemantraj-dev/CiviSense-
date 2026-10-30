import { Zone, WeatherData, CitizenReport, MunicipalAction } from '../types';

const BASE_URL = '/api';

export const api = {
  getHealth: () => fetch(`${BASE_URL}/health`).then(r => r.json()),
  getWeather: () => fetch(`${BASE_URL}/weather/current`).then(r => r.json()),
  getZones: (): Promise<Zone[]> => fetch(`${BASE_URL}/zones`).then(r => r.json()),
  getZoneIntelligence: (id: number) => fetch(`${BASE_URL}/zones/${id}/intelligence`).then(r => r.json()),
  getDrainageFeatures: () => fetch(`${BASE_URL}/drainage/features`).then(r => r.json()),
  getReports: (): Promise<CitizenReport[]> => fetch(`${BASE_URL}/reports`).then(r => r.json()),
  createReport: (data: Partial<CitizenReport>) => fetch(`${BASE_URL}/reports`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(r => r.json()),
  updateReportStatus: (id: number, status: string) => fetch(`${BASE_URL}/reports/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ verification_status: status })
  }).then(r => r.json()),
  getActions: (): Promise<MunicipalAction[]> => fetch(`${BASE_URL}/actions`).then(r => r.json()),
  createAction: (data: Partial<MunicipalAction>) => fetch(`${BASE_URL}/actions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(r => r.json()),
  simulateScenario: (params: { rainfall_mm: number; drainage_stress_pct: number; terrain_vulnerability_adj: number }) => 
    fetch(`${BASE_URL}/scenarios/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    }).then(r => r.json()),
  getDataTrustStatus: () => fetch(`${BASE_URL}/data-sources/status`).then(r => r.json())
};
