import unittest
from modules.findings import analyze_findings
from modules.score import score_findings

class CyberLabTests(unittest.TestCase):
    def test_findings(self):
        findings=analyze_findings([23,80]); self.assertEqual(findings[0]["severity"],"HIGH")
    def test_score_range(self):
        result=score_findings(analyze_findings([23,80]),None,None); self.assertTrue(0<=result["score"]<=100); self.assertIn(result["grade"],"ABCDF")

if __name__=="__main__": unittest.main()
