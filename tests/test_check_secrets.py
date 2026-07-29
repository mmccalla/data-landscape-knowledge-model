import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "check-secrets.py"


class SecretScannerTests(unittest.TestCase):
    def run_scanner(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.txt"
            candidate.write_text(content, encoding="utf-8")
            return subprocess.run(
                ["python3", str(SCANNER), str(candidate)],
                capture_output=True,
                check=False,
                text=True,
            )

    def test_rejects_common_provider_token(self):
        result = self.run_scanner("token = 'ghp_abcdefghijklmnopqrstuvwxyzABCDEFGHIJ'\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("possible GitHub token", result.stderr)

    def test_allows_placeholder_configuration(self):
        result = self.run_scanner("password = 'placeholder'\n")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
