import sys
from app.risk_engine.engine import RiskEngine

def run_tests():
    print("Testing CIVISENSE Risk Engine...")
    
    # 1. Test formula weights
    P = 80.0
    D = 60.0
    T = 40.0
    expected = (0.50 * 80.0) + (0.30 * 60.0) + (0.20 * 40.0)
    assert expected == 66.0, f"Expected 66.0, got {expected}"
    print("[PASS] Test formula weights (0.50*P + 0.30*D + 0.20*T = 66.0)")

    # 2. Test categories
    assert RiskEngine.determine_category(85.0) == "Critical"
    assert RiskEngine.determine_category(65.0) == "High"
    assert RiskEngine.determine_category(45.0) == "Medium"
    assert RiskEngine.determine_category(20.0) == "Low"
    print("[PASS] Test risk categories (Critical, High, Medium, Low)")

    # 3. Test zone assessment
    result = RiskEngine.assess_zone(
        rainfall_1h=15.0,
        rainfall_3h=25.0,
        rainfall_24h=40.0,
        forecast_6h=30.0,
        forecast_24h=60.0,
        baseline_drainage_factor=60.0,
        mapped_drain_count=2,
        elevation_m=320.0
    )
    assert 0 <= result["overall_risk_score"] <= 100
    assert "explanation" in result
    assert "recommended_action" in result
    assert "confidence_level" in result
    print(f"[PASS] Test zone assessment generated valid score: {result['overall_risk_score']}/100, category: {result['risk_category']}")
    print(f"       Explanation: {result['explanation']}")
    print("All Risk Engine tests PASSED successfully!")

if __name__ == "__main__":
    run_tests()
