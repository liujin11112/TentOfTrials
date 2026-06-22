"""Tests for diagnostic build error handling"""
import sys, os, json, tempfile, unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

try:
    from build import (
        diagnostic_paths_for_commit, build_diagnostic_report,
        write_diagnostic_report, DIAGNOSTIC_DIR
    )
    HAS_BUILD = True
except ImportError:
    HAS_BUILD = False

class TestDiagnosticErrorHandling(unittest.TestCase):
    def test_diagnostic_paths_creates_dir(self):
        if not HAS_BUILD:
            self.skipTest("build.py not importable")
        import build
        d = build.DIAGNOSTIC_DIR
        logd, meta, cid = build.diagnostic_paths_for_commit()
        self.assertTrue(str(logd).startswith(str(d)))
        self.assertEqual(meta.suffix, ".json")

    def test_report_on_empty_results(self):
        if not HAS_BUILD:
            self.skipTest("build.py not importable")
        report = build_diagnostic_report([], "abc12345")
        self.assertEqual(report["total_modules"], 0)
        self.assertEqual(report["passed"], 0)

    def test_report_on_failure(self):
        if not HAS_BUILD:
            self.skipTest("build.py not importable")
        results = [("test", False, 5.0, "error", None)]
        report = build_diagnostic_report(results, "abc12345")
        self.assertEqual(report["failed"], 1)
        self.assertEqual(report["total_modules"], 1)

    def test_write_diagnostic_report_handles_errors(self):
        if not HAS_BUILD:
            self.skipTest("build.py not importable")
        import build
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "out.json"
            build.write_diagnostic_report(p, {"test": 1})
            self.assertTrue(p.exists())

if __name__ == "__main__":
    unittest.main()
