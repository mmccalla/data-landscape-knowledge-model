"""P1 jurisdiction, ODPS disambiguation, and intentional matrix empties."""

from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCT_INSTANCES = ROOT / "product-instances.ttl"
TAXONOMY = ROOT / "taxonomy.ttl"
ONTOLOGY = ROOT / "ontology.ttl"
SHAPES = ROOT / "shapes.ttl"
DESIGN_DECISIONS = ROOT / "docs" / "08-design-decisions.md"
GLOSSARY = ROOT / "docs" / "09-glossary.md"
NODES = ROOT / "nodes.csv"
RELATIONSHIPS = ROOT / "relationships.csv"


class DesignJurisdictionTests(unittest.TestCase):
    def test_optional_property_and_shape(self):
        ontology = ONTOLOGY.read_text(encoding="utf-8")
        shapes = SHAPES.read_text(encoding="utf-8")
        self.assertIn("dl:hasDesignJurisdiction", ontology)
        self.assertIn("sh:path dl:hasDesignJurisdiction", shapes)
        self.assertIn("sh:minCount 0", shapes)

    def test_uk_jurisdiction_exists(self):
        self.assertIn("tax:jurisdiction-uk", TAXONOMY.read_text(encoding="utf-8"))
        with NODES.open(newline="", encoding="utf-8") as handle:
            ids = {row[":ID"] for row in csv.DictReader(handle)}
        self.assertIn("jurisdiction:uk", ids)

    def test_care_home_uk_eu_not_hipaa_shaped(self):
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        block = re.search(
            r"inst:product-care-home-resident-data-product a dl:DataProduct ;(.*?)\n\n",
            text,
            flags=re.S,
        )
        self.assertIsNotNone(block)
        body = block.group(1)
        self.assertIn("tax:jurisdiction-uk", body)
        self.assertIn("tax:jurisdiction-eu", body)
        self.assertNotIn("tax:jurisdiction-us", body)
        self.assertIn("care-home-resident-gdpr", text)
        self.assertNotIn("care-home-resident-hipaa", text)

    def test_us_health_products_keep_us_prompt(self):
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        for product in (
            "product-health-customer-data-product",
            "product-hospital-admissions-data-product",
        ):
            block = re.search(
                rf"inst:{product} a dl:DataProduct ;(.*?)\n\n",
                text,
                flags=re.S,
            )
            self.assertIsNotNone(block, product)
            self.assertIn("tax:jurisdiction-us", block.group(1))


class OdpsDisambiguationTests(unittest.TestCase):
    def test_public_sector_has_odps_and_odpspec_contrast(self):
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        self.assertIn('dl:identifier "public-sector-reference-codes-odps"', text)
        self.assertIn('dl:identifier "public-sector-reference-codes-odpspec"', text)
        self.assertIn("standard-odpspec", text)
        self.assertIn("ODPS", GLOSSARY.read_text(encoding="utf-8"))
        self.assertIn("odpspec", GLOSSARY.read_text(encoding="utf-8"))

    def test_csv_projects_odpspec_mapping(self):
        with NODES.open(newline="", encoding="utf-8") as handle:
            ids = {row[":ID"] for row in csv.DictReader(handle)}
        self.assertIn("product-standard:public-sector-reference-codes-odpspec", ids)
        with RELATIONSHIPS.open(newline="", encoding="utf-8") as handle:
            rels = {(r[":START_ID"], r[":TYPE"], r[":END_ID"]) for r in csv.DictReader(handle)}
        self.assertIn(
            (
                "product-standard:public-sector-reference-codes-odpspec",
                "CONSIDERS_STANDARD",
                "standard:odpspec",
            ),
            rels,
        )


class MatrixEmptyCellTests(unittest.TestCase):
    def test_intentionally_empty_cells_declared(self):
        text = DESIGN_DECISIONS.read_text(encoding="utf-8")
        self.assertIn("intentionally empty", text.lower())
        for phrase in ("health × NO_PII", "insurance × NO_PII", "telecoms × NO_PII", "public-sector × PII"):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
