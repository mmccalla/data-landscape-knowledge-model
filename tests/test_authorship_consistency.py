import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSFORMATION_AUTHOR = "Mark McCalla"
AFFILIATION = "Enterprise Solutions Consulting Ltd"
UPSTREAM_COPYRIGHT = "Copyright (c) 2026 Entropy Data"


class AuthorshipConsistencyTests(unittest.TestCase):
    def test_licence_names_both_copyrights(self):
        licence = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(UPSTREAM_COPYRIGHT, licence)
        self.assertIn(f"Copyright (c) 2026 {TRANSFORMATION_AUTHOR}", licence)
        self.assertIn("MIT License", licence)
        self.assertLess(
            licence.index(UPSTREAM_COPYRIGHT),
            licence.index(f"Copyright (c) 2026 {TRANSFORMATION_AUTHOR}"),
        )
        self.assertNotIn(AFFILIATION, licence)

    def test_notices_do_not_attribute_this_model_to_entropy_data(self):
        attribution = (ROOT / "ATTRIBUTION.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        ontology = (ROOT / "ontology.ttl").read_text(encoding="utf-8")
        template = (ROOT / "src" / "graph.template.html").read_text(encoding="utf-8")

        self.assertIn(f"Copyright (c) 2026 {TRANSFORMATION_AUTHOR}", attribution)
        self.assertNotIn(
            "Component regulatory mappings are original curated interpretations by Entropy Data",
            attribution,
        )
        self.assertIn(
            f"Component regulatory mappings are original curated interpretations by {TRANSFORMATION_AUTHOR}",
            attribution,
        )
        self.assertIn("catalogue data © Entropy Data", readme)
        self.assertIn(f"transformation by {TRANSFORMATION_AUTHOR}", readme)
        self.assertIn(AFFILIATION, readme)
        self.assertIn(AFFILIATION, (ROOT / "CITATION.bib").read_text(encoding="utf-8"))
        self.assertIn(AFFILIATION, template)
        self.assertIn(f"copyright (c) 2026 {TRANSFORMATION_AUTHOR}".lower(), ontology.lower())
        self.assertNotIn(AFFILIATION, ontology)
        self.assertNotIn("Entropy Data · Knowledge model", template)

    def test_component_regulatory_mappings_are_asserted_by_the_transformation_author(self):
        turtle = (ROOT / "component-regulatory-mappings.ttl").read_text(encoding="utf-8")
        asserted = re.findall(r'dl:assertedBy "([^"]+)"', turtle)
        self.assertEqual(33, len(asserted))
        self.assertEqual({TRANSFORMATION_AUTHOR}, set(asserted))
        self.assertNotIn(AFFILIATION, turtle)

        with (ROOT / "nodes.csv").open(newline="", encoding="utf-8") as handle:
            rows = [
                row
                for row in csv.DictReader(handle)
                if "ComponentRegulatoryMapping" in row[":LABEL"]
            ]
        self.assertEqual(33, len(rows))
        self.assertEqual({TRANSFORMATION_AUTHOR}, {row["assertedBy"] for row in rows})


if __name__ == "__main__":
    unittest.main()
