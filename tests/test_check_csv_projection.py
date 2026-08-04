import csv
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_SCANNER = ROOT / "scripts" / "check-csv-projection.py"


class CsvProjectionScannerTests(unittest.TestCase):
    def write_projection(self, directory: Path, nodes: list[dict[str, str]], relationships: list[dict[str, str]]) -> None:
        node_fields = [":ID", "id", "name", "evidenceStatus", ":LABEL"]
        relationship_fields = [":START_ID", ":END_ID", ":TYPE", "evidenceStatus"]
        with (directory / "nodes.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=node_fields, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(nodes)
        with (directory / "relationships.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=relationship_fields, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(relationships)

    def run_scanner(self, nodes: list[dict[str, str]], relationships: list[dict[str, str]]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory_name:
            directory = Path(directory_name)
            script = directory / "scripts" / "check-csv-projection.py"
            script.parent.mkdir(parents=True)
            script.write_text(CSV_SCANNER.read_text(encoding="utf-8"), encoding="utf-8")
            self.write_projection(directory, nodes, relationships)
            return subprocess.run(
                ["python3", str(script)],
                capture_output=True,
                check=False,
                text=True,
                cwd=directory,
            )

    def test_rejects_dangling_relationship_endpoint(self):
        result = self.run_scanner(
            nodes=[
                {
                    ":ID": "component-type:secure-read-access",
                    "id": "secure-read-access",
                    "name": "Secure read access",
                    "evidenceStatus": "MODELLED_VOCABULARY",
                    ":LABEL": "DataPipelineComponentType",
                }
            ],
            relationships=[
                {
                    ":START_ID": "component-regulatory:missing",
                    ":END_ID": "component-type:secure-read-access",
                    ":TYPE": "MAPS_COMPONENT_TYPE",
                    "evidenceStatus": "CURATED_REGULATORY_RELEVANCE",
                }
            ],
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("dangling :START_ID", result.stderr)

    def test_accepts_consistent_projection(self):
        result = self.run_scanner(
            nodes=[
                {
                    ":ID": "a",
                    "id": "a",
                    "name": "A",
                    "evidenceStatus": "DIRECT_OBSERVATION",
                    ":LABEL": "DataStandardLandscapeEntry",
                },
                {
                    ":ID": "b",
                    "id": "b",
                    "name": "B",
                    "evidenceStatus": "DIRECT_OBSERVATION",
                    ":LABEL": "DataRegulationLandscapeEntry",
                },
            ],
            relationships=[
                {
                    ":START_ID": "a",
                    ":END_ID": "b",
                    ":TYPE": "DESCRIBES_SAME_RESOURCE_AS",
                    "evidenceStatus": "IDENTITY_CONFIRMED",
                }
            ],
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
