import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD_HOST = "entropy-data.com/data-landscape"
ONTOLOGY = "https://polymathic.co.uk/data-landscape/ontology/"
TAXONOMY = "https://polymathic.co.uk/data-landscape/taxonomy/"
INSTANCE = "https://polymathic.co.uk/data-landscape/instance/"
TURTLE_FILES = (
    "ontology.ttl",
    "taxonomy.ttl",
    "shapes.ttl",
    "instances.ttl",
    "regulation-instances.ttl",
    "mapping-instances.ttl",
    "component-mappings.ttl",
    "component-regulatory-mappings.ttl",
)


class NamespaceConsistencyTests(unittest.TestCase):
    def test_model_iris_use_polymathic_not_entropy_data(self):
        for name in TURTLE_FILES:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertNotIn(OLD_HOST, text, name)
            self.assertIn(f"@prefix dl: <{ONTOLOGY}> .", text, name)

        overview = (ROOT / "docs" / "00-package-overview.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs" / "01-ontology.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn(OLD_HOST, readme, "README.md")
        for document, text in (("docs/00-package-overview.md", overview), ("docs/01-ontology.md", docs)):
            self.assertNotIn(OLD_HOST, text, document)
            self.assertIn(ONTOLOGY, text, document)
            self.assertIn(TAXONOMY, text, document)
            self.assertIn(INSTANCE, text, document)

        ontology = (ROOT / "ontology.ttl").read_text(encoding="utf-8")
        taxonomy = (ROOT / "taxonomy.ttl").read_text(encoding="utf-8")
        instances = (ROOT / "instances.ttl").read_text(encoding="utf-8")
        self.assertIn(f"@prefix tax: <{TAXONOMY}> .", taxonomy)
        self.assertIn(f"@prefix inst: <{INSTANCE}> .", instances)
        self.assertIn(ONTOLOGY, ontology)


if __name__ == "__main__":
    unittest.main()
