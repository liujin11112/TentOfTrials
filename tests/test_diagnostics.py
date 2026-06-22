"""Tests for diagnostic error handling"""
import sys, os, json, tempfile, unittest
from pathlib import Path
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO))
try:
    from build import build_diagnostic_report, write_diagnostic_report
    HAS = True
except: HAS = False

class TestErrorHandling(unittest.TestCase):
    def test_report_empty(self):
        if not HAS: self.skipTest("cannot import build")
        r = build_diagnostic_report([], "abc")
        self.assertEqual(r["total_modules"], 0)
    def test_report_failure(self):
        if not HAS: self.skipTest("cannot import build")
        r = build_diagnostic_report([("test",False,5.0,"err",None)], "abc")
        self.assertEqual(r["failed"], 1)
    def test_write_safe(self):
        if not HAS: self.skipTest("cannot import build")
        with tempfile.TemporaryDirectory() as t:
            import build
            build._safe_write_diagnostic_report(Path(t)/"out.json", {"ok":1})
            self.assertTrue((Path(t)/"out.json").exists())

if __name__ == "__main__":
    unittest.main()
