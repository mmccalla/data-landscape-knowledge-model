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
        citation_bib = (ROOT / "CITATION.bib").read_text(encoding="utf-8")
        citation_cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

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
        self.assertIn(f"{TRANSFORMATION_AUTHOR}’s derived model", attribution)
        self.assertIn(f"copyright (c) 2026 {TRANSFORMATION_AUTHOR}".lower(), ontology.lower())
        self.assertNotIn("Entropy Data · Knowledge model", template)
        self.assertRegex(template, rf'<p class="eyebrow">{re.escape(TRANSFORMATION_AUTHOR)}</p>')
        self.assertIn('href="https://www.entropy-data.com/"', template)
        self.assertIn('href="https://www.data-landscape.com/"', template)
        self.assertIn('href="https://www.data-landscape.com/regulation.html"', template)
        self.assertIn("Thank you", template)
        self.assertIn("https://github.com/mmccalla/data-landscape-knowledge-model/issues", template)
        self.assertIn("https://www.linkedin.com/in/mark001/", template)
        self.assertNotIn("mailto:", template)

        for label, text in (
            ("README", readme),
            ("ATTRIBUTION", attribution),
            ("CITATION.bib", citation_bib),
            ("CITATION.cff", citation_cff),
            ("CONTRIBUTING", contributing),
            ("graph template", template),
            ("ontology", ontology),
        ):
            self.assertNotIn(AFFILIATION, text, f"{label} must not name the Ltd affiliation")

    def test_component_regulatory_mappings_are_asserted_by_the_transformation_author(self):
        turtle = (ROOT / "component-regulatory-mappings.ttl").read_text(encoding="utf-8")
        asserted = re.findall(r'dl:assertedBy "([^"]+)"', turtle)
        self.assertEqual(38, len(asserted))
        self.assertEqual({TRANSFORMATION_AUTHOR}, set(asserted))
        self.assertNotIn(AFFILIATION, turtle)

        with (ROOT / "nodes.csv").open(newline="", encoding="utf-8") as handle:
            rows = [
                row
                for row in csv.DictReader(handle)
                if "ComponentRegulatoryMapping" in row[":LABEL"]
            ]
        self.assertEqual(38, len(rows))
        self.assertEqual({TRANSFORMATION_AUTHOR}, {row["assertedBy"] for row in rows})


if __name__ == "__main__":
    unittest.main()
