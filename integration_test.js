/**
 * CIVISENSE — End-to-End Integration Test Suite (In-Process Direct Runner)
 */

async function runTests() {
  console.log("==================================================");
  console.log(" RUNNING CIVISENSE INTEGRATION TEST SUITE");
  console.log("==================================================");

  // Require server directly to bind on 127.0.0.1:8000
  const path = require('node:path');
  require(path.join(__dirname, '..', '..', 'server.js'));

  // Wait 1 second for database seed and server listen
  await new Promise(r => setTimeout(r, 1000));

  let passed = 0;
  let failed = 0;

  async function testEndpoint(name, url, validator) {
    try {
      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`HTTP status ${resp.status}`);
      const data = await resp.json();
      validator(data);
      console.log(`[PASS] ${name}`);
      passed++;
    } catch (err) {
      console.error(`[FAIL] ${name}:`, err.message);
      failed++;
    }
  }

  // Test 1: GET /api/health
  await testEndpoint("1. GET /api/health", "http://127.0.0.1:8000/api/health", (data) => {
    if (data.status !== 'ok' || data.pilot_geography !== 'Chandigarh, India') {
      throw new Error("Invalid health payload");
    }
  });

  // Test 2: GET /api/config
  await testEndpoint("2. GET /api/config", "http://127.0.0.1:8000/api/config", (data) => {
    if (!data.weights || data.weights.rainfall !== 0.5) throw new Error("Invalid weights");
  });

  // Test 3: GET /api/zones
  await testEndpoint("3. GET /api/zones (32 Chandigarh & Punjab Pilot Sectors)", "http://127.0.0.1:8000/api/zones", (data) => {
    if (!Array.isArray(data) || data.length < 30) throw new Error(`Expected at least 30 zones, got ${data?.length}`);
    if (!data[0].latest_risk_score || !data[0].risk_category) throw new Error("Missing risk assessment on zone");
  });

  // Test 4: GET /api/weather/current
  await testEndpoint("4. GET /api/weather/current (Open-Meteo Integration)", "http://127.0.0.1:8000/api/weather/current", (data) => {
    if (typeof data.rainfall_1h !== 'number' || typeof data.forecast_6h !== 'number') {
      throw new Error("Missing rainfall data");
    }
  });

  // Test 5: GET /api/drainage/features
  await testEndpoint("5. GET /api/drainage/features (OSM Waterways)", "http://127.0.0.1:8000/api/drainage/features", (data) => {
    if (!Array.isArray(data.features) || data.features.length === 0) {
      throw new Error("No drainage features found");
    }
    if (!data.label.includes("OPENSTREETMAP")) throw new Error("Missing OSM label");
  });

  // Test 6: GET /api/reports
  await testEndpoint("6. GET /api/reports (Citizen Reports)", "http://127.0.0.1:8000/api/reports", (data) => {
    if (!Array.isArray(data) || data.length === 0) throw new Error("No citizen reports");
  });

  // Test 7: GET /api/actions
  await testEndpoint("7. GET /api/actions (Municipal Actions)", "http://127.0.0.1:8000/api/actions", (data) => {
    if (!Array.isArray(data) || data.length === 0) throw new Error("No actions");
  });

  // Test 8: POST /api/scenarios/simulate (Decision Lab)
  try {
    const simResp = await fetch("http://127.0.0.1:8000/api/scenarios/simulate", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        rainfall_mm: 75.0,
        drainage_stress_pct: 25.0,
        terrain_vulnerability_adj: 10.0
      })
    });
    const simData = await simResp.json();
    if (simData.score_delta > 0 && Array.isArray(simData.results)) {
      console.log(`[PASS] 8. POST /api/scenarios/simulate (Decision Lab simulated score delta: +${simData.score_delta})`);
      passed++;
    } else {
      throw new Error("Invalid simulation results");
    }
  } catch (err) {
    console.error(`[FAIL] 8. POST /api/scenarios/simulate:`, err.message);
    failed++;
  }

  // Test 9: GET /api/data-sources/status (Data Trust Centre)
  await testEndpoint("9. GET /api/data-sources/status (Data Trust Centre)", "http://127.0.0.1:8000/api/data-sources/status", (data) => {
    if (!Array.isArray(data) || data.length < 4) throw new Error("Expected at least 4 data trust providers");
  });

  // Test 10: GET /api/export/csv
  try {
    const csvResp = await fetch("http://127.0.0.1:8000/api/export/csv");
    const csvText = await csvResp.text();
    if (csvText.includes("CHD-SEC-17") && csvText.includes("Risk Score")) {
      console.log(`[PASS] 10. GET /api/export/csv (Verified CSV structure with headers and zones)`);
      passed++;
    } else {
      throw new Error("CSV missing expected contents");
    }
  } catch (err) {
    console.error(`[FAIL] 10. GET /api/export/csv:`, err.message);
    failed++;
  }

  // Test 11: GET / (Frontend HTML Delivery)
  try {
    const htmlResp = await fetch("http://127.0.0.1:8000/");
    const htmlText = await htmlResp.text();
    if (htmlText.includes("CIVISENSE") && htmlText.includes("Judge Demo Tour")) {
      console.log(`[PASS] 11. GET / (Frontend HTML delivered with title and all modules)`);
      passed++;
    } else {
      throw new Error("HTML missing expected components");
    }
  } catch (err) {
    console.error(`[FAIL] 11. GET /:`, err.message);
    failed++;
  }

  console.log("==================================================");
  console.log(` INTEGRATION TESTS COMPLETE: ${passed} PASSED, ${failed} FAILED`);
  console.log("==================================================");
  process.exit(failed > 0 ? 1 : 0);
}

runTests();
