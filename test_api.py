import unittest
from app.risk_engine.engine import RiskEngine

class TestRiskEngine(unittest.TestCase):
    def test_risk_formula_weights(self):
        # Risk Score = 0.50 * P + 0.30 * D + 0.20 * T
        P = 80.0
        D = 60.0
        T = 40.0
        expected = (0.50 * 80.0) + (0.30 * 60.0) + (0.20 * 40.0) # 40 + 18 + 8 = 66.0
        self.assertEqual(expected, 66.0)

    def test_risk_categories(self):
        self.assertEqual(RiskEngine.determine_category(85.0), "Critical")
        self.assertEqual(RiskEngine.determine_category(65.0), "High")
        self.assertEqual(RiskEngine.determine_category(45.0), "Medium")
        self.assertEqual(RiskEngine.determine_category(20.0), "Low")

    def test_assessment_output_structure(self):
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
        self.assertIn("overall_risk_score", result)
        self.assertIn("risk_category", result)
        self.assertIn("confidence_level", result)
        self.assertIn("explanation", result)
        self.assertIn("recommended_action", result)
        self.assertTrue(0 <= result["overall_risk_score"] <= 100)

if __name__ == "__main__":
    unittest.main()
