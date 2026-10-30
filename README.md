# CIVISENSE
## Predict. Prioritize. Prevent.
### Smart Urban Waterlogging Prevention and Municipal Response Intelligence System
**Pilot Geography:** Chandigarh, India (Lat: 30.7333°N, Lon: 76.7794°E)

---

## 1. Executive Summary

Urban waterlogging during convective downpours causes severe disruption, infrastructure inundation, traffic paralysis, and economic losses across Indian cities. **CIVISENSE** is a full-stack municipal intelligence platform engineered for urban local bodies (ULBs), disaster management authorities, and city engineering departments.

Piloting in the Union Territory of **Chandigarh, India**, CiviSense replaces reactive flood response with proactive prevention by synthesizing:
1. **Live Meteorological Telemetry:** Real-time hourly precipitation, 24h antecedent rainfall, and 6h/24h forecast projections from **Open-Meteo**.
2. **Topographic Depression Analysis:** Macro-slope and depressional vulnerability from **Open-Meteo Elevation API (Copernicus DEM GLO-90, ~90m resolution)**.
3. **Hydrological Channel Mapping:** Mapped natural streams (*choes* like N-Choe, Sukhna Choe, Patiala Ki Rao) and stormwater conduits from **OpenStreetMap Overpass API**.
4. **Citizen Field Intelligence:** Mobile ground observations with GPS coordinates, depth estimation, photo verification, and spatial duplicate clustering.
5. **Municipal Operations Tracking:** Automated task dispatch, jetting machine mobilization, and priority de-silting workflows.

---

## 2. System Architecture

```
[ Open-Meteo Forecast & History ] ──┐
[ Open-Meteo Elevation (Copernicus) ]─┼─► [ Central Data Services & Cache ] ──► [ CiviSense Central Risk Engine ]
[ OpenStreetMap Overpass Waterways ]─┤       (Weather, Terrain, Drainage)          (Score = 0.50*P + 0.30*D + 0.20*T)
[ Citizen Mobile Field Reports ] ────┘                                                       │
                                                                                             ▼
                                                        [ Relational SQLite Database: civisense.db ]
                                                                                             │
                                                                                             ▼
                                                        [ REST API Layer & Full-Featured Responsive Frontend ]
                                                        (12 Connected Modules, GIS Leaflet Map, Decision Lab)
```

### Color Palette & Design System
- **Deep Forest Slate:** `#172B36` (Command shell & header background)
- **Warm Ivory:** `#F3F1E9` (Content backdrop & card surfaces)
- **Muted Teal:** `#267C78` (Primary brand accents & action elements)
- **Soft Sage:** `#83A69A` (Subtle indicators & badges)
- **Amber:** `#D69A42` (Warnings & what-if simulator accents)
- **Critical Terracotta:** `#C75C54` (Severe alerts & notifications)
- **Risk Hierarchy:**
  - `Critical (80–100):` `#B94B48`
  - `High (60–79):` `#D18A35`
  - `Medium (35–59):` `#D2B64B`
  - `Low (0–34):` `#438A69`

---

## 3. The Central CiviSense Risk Engine

All modules in CiviSense consume a unified, transparent, explainable multi-criteria formula:

$$\text{Risk Score} = 0.50 \times P + 0.30 \times D + 0.20 \times T$$

- **$P$ (Precipitation Score, 0–100, 50% Weight):**
  - Instantaneous hourly precipitation rate ($0 - 40\text{ pts}$).
  - Short-term convective accumulation over 3h & 6h forecast ($0 - 30\text{ pts}$).
  - Cumulative 24h antecedent soil saturation ($0 - 30\text{ pts}$).
- **$D$ (Drainage Vulnerability, 0–100, 30% Weight):**
  - Baseline sector conduit capacity and mapped OSM channel density ($D_0$).
  - Stress modifier from simulated siltation, trash obstruction, or de-silting improvements ($\pm 50\%$).
- **$T$ (Terrain Depression Indicator, 0–100, 20% Weight):**
  - Relative elevation delta normalized against Chandigarh's southwest gradient ($365\text{m}$ northeast foothills down to $310\text{m}$ southwest plains).
- **Confidence Scoring:**
  - Automatically computed ($High / Medium / Low$) based on 4 criteria: live meteorological feed active ($35\text{ pts}$), 90m DEM sampled ($30\text{ pts}$), OSM channels indexed ($20\text{ pts}$), and verified field reports ($15\text{ pts}$).

---

## 4. The 12 Application Modules

1. **City Overview Command Center (Module 1):** Real-time city metrics, rainfall sparklines, critical zone count, and top 5 vulnerable sectors.
2. **GIS Risk Map (Module 2):** Leaflet GIS map with 10 Chandigarh pilot sectors, risk choropleth coloring, OSM waterways vector overlays, citizen markers, and interactive zone inspection drawer.
3. **Weather Intelligence (Module 3):** Open-Meteo multi-window rainfall aggregations ($1\text{h}, 3\text{h}, 24\text{h}, 72\text{h}$ observation and $6\text{h}, 24\text{h}$ forecast) with 24-hour hourly precipitation bar chart.
4. **Zone Intelligence (Module 4):** Sector-by-sector deep dive showing elevation, relative depression, baseline drainage factor, and citizen incidents.
5. **Citizen Waterlogging Reporting (Module 5):** Public responsive reporting form with GPS acquisition, photo preview, severity rating, and operator triage desk (duplicate proximity warning, verification).
6. **Explainable Risk Intelligence (Module 6):** Mathematical breakdown of scores, factor weights ($0.5P + 0.3D + 0.2T$), sensitivity slider testing, and natural-language justifications.
7. **Prevention Priority Centre (Module 7):** Comprehensive priority ranking table of all 10 sectors with search, category filtering, and one-click dispatch.
8. **Action & Inspection Management (Module 8):** Simulated municipal operations workflow for task assignment, crew tracking, and status transitions (*Pending Review &rarr; Approved &rarr; In Progress &rarr; Completed*).
9. **Decision Lab / What-If Simulator (Module 9):** Signature interactive simulation engine with sliders for rainfall ($0 - 150\text{ mm/h}$), drainage stress ($\pm 50\%$), and presets (*Cloudburst, Choked Siphons, Post-Desilting*) with live before/after recalculation.
10. **Data Trust Centre (Module 10):** Uncompromising transparency dashboard displaying API endpoints, sync timestamps, spatial resolutions, and declared limitations.
11. **Reports & Real CSV Export (Module 11):** Official municipal assessment layout, printable stylesheet, and real CSV download (`/api/export/csv`).
12. **Judge Demo Mode (Module 12):** Interactive 15-step guided walkthrough banner with *Next/Prev* navigation leading evaluators step-by-step through the entire prevention lifecycle.

---

## 5. Pilot Geography: Chandigarh & Punjab Tricity (32 Monitored Sectors)

Thirty-two representative sectors across Chandigarh UT and Punjab Tricity (Mohali / SAS Nagar, Zirakpur, Kharar, Dera Bassi, New Chandigarh) are actively monitored across all four risk phases:

### Phase I: Critical Risk Hotspots (80 – 100)
1. **Mohali Phase 7 (`PB-MOH-PH7`):** Commercial arterial bowl & chronic waterlogging ($317\text{m}$, Punjab).
2. **Dera Bassi Ghaggar Basin (`PB-DER-GHG`):** Regional depression near Ghaggar River spillway ($298\text{m}$, Punjab).
3. **Zirakpur VIP Road (`PB-ZIR-VIP`):** High density bottleneck with choked culverts ($308\text{m}$, Punjab).
4. **Zirakpur Baltana (`PB-ZIR-BAL`):** Downstream floodplain of Sukhna Choe ($305\text{m}$, Punjab).

### Phase II: High Risk Sectors (60 – 79)
5. **Kharar Landran Road (`PB-KHA-LND`):** Unpaved low basin corridor ($312\text{m}$, Punjab).
6. **Industrial Area Phase I (`CHD-IND-01`):** Low-lying basin near Sukhna Choe ($322\text{m}$, Chandigarh).
7. **Manimajra (`CHD-MAN-01`):** Old housing board low-lying settlement ($326\text{m}$, Chandigarh).
8. **Sector 52 (`CHD-SEC-52`):** South boundary drainage basin ($320\text{m}$, Chandigarh).
9. **Mohali Phase 1 (`PB-MOH-PH1`):** N-Choe outfall industrial area ($321\text{m}$, Punjab).
10. **Kharar NH-21 Dip (`PB-KHA-NH21`):** Flyover under-bridge dip ($315\text{m}$, Punjab).
11. **Industrial Area Phase II (`CHD-IND-02`):** Railway underpass corridor ($318\text{m}$, Chandigarh).
12. **Maloya (`CHD-MAL-01`):** Western peri-urban low corridor ($325\text{m}$, Chandigarh).
13. **Mohali Sector 70 (`PB-MOH-SEC70`):** Mattaur village depression ($316\text{m}$, Punjab).
14. **Dhanas (`CHD-DHA-01`):** Patiala Ki Rao stream corridor ($335\text{m}$, Chandigarh).

### Phase III: Medium Risk Sectors (35 – 59)
15. **Sector 45 (`CHD-SEC-45`):** Burail village outskirts ($328\text{m}$, Chandigarh).
16. **Sector 43 (`CHD-SEC-43`):** Regional ISBT bus terminal ($329\text{m}$, Chandigarh).
17. **Mohali Sector 82 (`PB-MOH-SEC82`):** JLPL Industrial Park ($311\text{m}$, Punjab).
18. **Sector 26 (`CHD-SEC-26`):** Grain & vegetable mandi corridor ($339\text{m}$, Chandigarh).
19. **Sector 22 (`CHD-SEC-22`):** Shastri Market & mixed urban core ($341\text{m}$, Chandigarh).
20. **Mohali Phase 3B2 (`PB-MOH-3B2`):** Commercial market hub ($324\text{m}$, Punjab).
21. **Mohali Phase 9 (`PB-MOH-PH9`):** PCA cricket stadium enclave ($319\text{m}$, Punjab).
22. **Sector 20 (`CHD-SEC-20`):** Dense residential inner grid ($338\text{m}$, Chandigarh).
23. **Sector 34 (`CHD-SEC-34`):** Sub-city commercial & education hub ($337\text{m}$, Chandigarh).
24. **Sector 35 (`CHD-SEC-35`):** Commercial arterial avenue ($336\text{m}$, Chandigarh).
25. **Sector 17 (`CHD-SEC-17`):** Pedestrian plaza civic core ($348\text{m}$, Chandigarh).
26. **Sector 15 (`CHD-SEC-15`):** Panjab University south periphery ($346\text{m}$, Chandigarh).

### Phase IV: Low Risk Sectors (0 – 34)
27. **Mohali IT City (`PB-MOH-ITCITY`):** Planned campus with detention basins ($314\text{m}$, Punjab).
28. **Mohali Aerocity (`PB-MOH-AERO`):** Engineered airport corridor ($315\text{m}$, Punjab).
29. **Sector 8 (`CHD-SEC-08`):** Residential northern ridge ($355\text{m}$, Chandigarh).
30. **Sukhna Lake Enclave (`CHD-SUK-01`):** Catchment foothills rim ($362\text{m}$, Chandigarh).
31. **New Chandigarh Mullanpur (`PB-MULL-ECO`):** Eco City foothills ($358\text{m}$, Punjab).
32. **Sector 1 (`CHD-SEC-01`):** Capitol Complex & High Court ridge ($365\text{m}$, Chandigarh).

---

## 6. How to Run CiviSense

### Method A: Single-Click Launcher (Windows)
Double-click `run_civisense.bat` or run:
```powershell
.\run_civisense.bat
```
This automatically boots the server on `http://127.0.0.1:8000` and launches your default web browser.

### Method B: Standalone Node.js Prototype Runner
```powershell
set ELECTRON_RUN_AS_NODE=1
C:\Users\VICTUS\AppData\Local\Programs\antigravity\Antigravity.exe server.js
```
Open `http://127.0.0.1:8000` in your browser.

### Method C: Standard Python FastAPI Backend
If you have a Python environment with pip:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Interactive API docs are available at `http://127.0.0.1:8000/docs`.

---

## 7. Running Verification & Integration Tests

CiviSense includes two comprehensive automated test suites:

### 1. Risk Engine Mathematical Unit Tests
```powershell
$env:PYTHONHOME = "C:\Program Files\MySQL\MySQL Workbench 8.0\python"
$env:PYTHONPATH = "C:\Users\VICTUS\.gemini\antigravity\scratch\civisense\backend"
& "C:\Program Files\MySQL\MySQL Workbench 8.0\python.exe" backend\app\tests\test_engine.py
```
**Output:**
```
Testing CIVISENSE Risk Engine...
[PASS] Test formula weights (0.50*P + 0.30*D + 0.20*T = 66.0)
[PASS] Test risk categories (Critical, High, Medium, Low)
[PASS] Test zone assessment generated valid score: 55.1/100, category: Medium
All Risk Engine tests PASSED successfully!
```

### 2. Full-Stack End-to-End Integration Test Suite
```powershell
& "C:\Users\VICTUS\AppData\Roaming\Antigravity\bin\agy-node.cmd" backend\tests\integration_test.js
```
**Output:**
```
==================================================
 RUNNING CIVISENSE INTEGRATION TEST SUITE
==================================================
[PASS] 1. GET /api/health
[PASS] 2. GET /api/config
[PASS] 3. GET /api/zones (10 Chandigarh Pilot Sectors)
[PASS] 4. GET /api/weather/current (Open-Meteo Integration)
[PASS] 5. GET /api/drainage/features (OSM Waterways)
[PASS] 6. GET /api/reports (Citizen Reports)
[PASS] 7. GET /api/actions (Municipal Actions)
[PASS] 8. POST /api/scenarios/simulate (Decision Lab simulated score delta: +56.5)
[PASS] 9. GET /api/data-sources/status (Data Trust Centre)
[PASS] 10. GET /api/export/csv (Verified CSV structure with headers and zones)
[PASS] 11. GET / (Frontend HTML delivered with title and all modules)
==================================================
 INTEGRATION TESTS COMPLETE: 11 PASSED, 0 FAILED
==================================================
```

---

## 8. Data Provenance & Declared Limitations

| Provider / Layer | Dataset | Spatial Resolution | Limitations |
|---|---|---|---|
| **Open-Meteo Weather** | ECMWF IFS / DWD ICON | $\sim 1.5 - 9\text{ km}$ grid | Numerical model forecast output; not a calibrated physical rain-gauge network. |
| **Open-Meteo Elevation** | Copernicus DEM GLO-90 | $\sim 90\text{ meters}$ | Macro-topographic slope; does not capture micro-curbs, localized $20\text{cm}$ potholes, or speed breakers. |
| **OpenStreetMap Overpass** | Mapped Waterways | Vector geometries | Crowdsourced vectors; does not represent a certified municipal hydraulic survey or reflect real-time pipe blockage. |
| **Citizen Reports** | Field GPS Reports | $\sim 5 - 15\text{ meters}$ | Citizen reports require operator triage; unverified reports are explicitly flagged and separated from ground truth. |
| **Municipal Actions** | Simulated Workflows | Administrative units | Prototype operational simulation; does not trigger live municipal sirens or physical contractor dispatch. |

---

## 9. Final Acceptance Matrix

- [x] Responsive full-stack application running from $360\text{px}$ mobile to $1920\text{px}$ desktop.
- [x] Real-time Open-Meteo weather integration with hourly forecast and accumulation windows.
- [x] Real-time Open-Meteo Elevation API (Copernicus DEM 90m) integration.
- [x] OpenStreetMap Overpass hydrological drainage layer with GeoJSON rendering.
- [x] Central Explainable Risk Engine ($0.50P + 0.30D + 0.20T$).
- [x] Interactive Leaflet GIS Risk Map with sector choropleths, choe stream vectors, and report markers.
- [x] Citizen reporting form with GPS coordinates and operator verification triage.
- [x] Prevention Priority Centre with sortable, filterable municipal rankings.
- [x] Action and inspection management workflow.
- [x] Decision Lab / What-If Scenario Simulator with presets and dynamic recalculation.
- [x] Data Trust Centre with live API statuses and limitations disclosure.
- [x] Real functional CSV export (`/api/export/csv`).
- [x] Interactive 15-step Judge Demo Mode guided tour.
- [x] 100% passing unit and integration tests.
