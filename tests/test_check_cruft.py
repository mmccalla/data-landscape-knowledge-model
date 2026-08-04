import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "check-cruft.py"


class CruftScannerTests(unittest.TestCase):
    def run_scanner(self, filenames: list[str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "scripts" / "check-cruft.py"
            script.parent.mkdir(parents=True)
            script.write_text(SCANNER.read_text(encoding="utf-8"), encoding="utf-8")
            for name in filenames:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("junk\n", encoding="utf-8")
            return subprocess.run(
                ["python3", str(script)],
                capture_output=True,
                check=False,
                text=True,
                cwd=root,
            )

    def test_rejects_finder_numbered_duplicate(self):
        result = self.run_scanner(["component-regulatory-mappings 2.ttl"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("component-regulatory-mappings 2.ttl", result.stderr)

    def test_rejects_ds_store(self):
        result = self.run_scanner([".DS_Store"])
        self.assertEqual(result.returncode, 1)
        self.assertIn(".DS_Store", result.stderr)

    def test_allows_normal_repository_files(self):
        result = self.run_scanner(["component-regulatory-mappings.ttl", "scripts/uat-graph-browser.mjs"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
