"""Behaviour checks for the thin data-product typology."""

from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology.ttl"
TAXONOMY = ROOT / "taxonomy.ttl"
SHAPES = ROOT / "shapes.ttl"
PRODUCT_INSTANCES = ROOT / "product-instances.ttl"
NODES = ROOT / "nodes.csv"
RELATIONSHIPS = ROOT / "relationships.csv"
TRANSFORM_AUTHOR = "Mark McCalla"

VERTICALS = ("banking", "insurance", "retail", "health", "public-sector", "telecoms")
POSTURES = ("PII", "NO_PII")


class ProductTypologySchemaTests(unittest.TestCase):
    def test_ontology_defines_data_product_and_reified_mappings(self):
        text = ONTOLOGY.read_text(encoding="utf-8")
        self.assertRegex(text, r"dl:DataProduct\s+a\s+owl:Class")
        self.assertNotRegex(
            text,
            r"dl:DataProduct\s+a\s+owl:Class\s*;\s*rdfs:subClassOf\s+dl:DataPipelineComponent",
        )
        self.assertIn("dl:hasPersonalDataPosture", text)
        self.assertIn("dl:inIndustryVertical", text)
        self.assertIn("dl:ProductStandardRelevance", text)
        self.assertIn("dl:ProductRegulatoryRelevance", text)
        self.assertIn("dl:forDataProduct", text)
        self.assertIn("dl:considersStandard", text)
        self.assertIn("dl:considersRegulation", text)
        self.assertNotIn("dl:usesStandard", text)
        self.assertNotIn("dl:relevantRegulation", text)
        self.assertIn("dl:PersonalDataPosture", text)
        self.assertIn("dl:IndustryVertical", text)

    def test_taxonomy_defines_vertical_and_posture_schemes(self):
        text = TAXONOMY.read_text(encoding="utf-8")
        self.assertIn("tax:industry-verticals", text)
        self.assertIn("tax:personal-data-postures", text)
        for vertical in VERTICALS:
            self.assertIn(f"tax:industry-vertical-{vertical}", text)
        for posture in POSTURES:
            key = posture.lower().replace("_", "-")
            self.assertIn(f"tax:personal-data-posture-{key}", text)

    def test_shacl_requires_product_dimensions_and_mapping_provenance(self):
        text = SHAPES.read_text(encoding="utf-8")
        self.assertIn("dl:DataProductShape", text)
        self.assertIn("dl:ProductStandardRelevanceShape", text)
        self.assertIn("dl:ProductRegulatoryRelevanceShape", text)
        self.assertIn("dl:hasPersonalDataPosture", text)
        self.assertIn("dl:inIndustryVertical", text)
        self.assertIn("dl:forDataProduct", text)
        self.assertIn("dl:considersStandard", text)
        self.assertIn("dl:considersRegulation", text)


class ProductTypologyInstanceTests(unittest.TestCase):
    def test_named_products_differ_on_posture_vertical_and_use_reified_mappings(self):
        self.assertTrue(PRODUCT_INSTANCES.is_file(), "product-instances.ttl is required")
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        self.assertIn('dl:identifier "retail-stock-data-product"', text)
        self.assertIn("Retail Stock Data Product", text)
        self.assertIn("tax:personal-data-posture-no-pii", text)
        self.assertIn("tax:industry-vertical-retail", text)

        self.assertIn('dl:identifier "banking-customer-data-product"', text)
        self.assertIn("Banking Customer Data Product", text)
        self.assertIn("tax:personal-data-posture-pii", text)
        self.assertIn("tax:industry-vertical-banking", text)

        self.assertIn('dl:identifier "health-customer-data-product"', text)
        self.assertIn("Health Customer Data Product", text)
        self.assertIn("tax:industry-vertical-health", text)
        self.assertIn('dl:identifier "insurance-policy-data-product"', text)
        self.assertIn("Insurance Policy Data Product", text)
        self.assertIn('dl:identifier "capital-markets-trade-data-product"', text)
        self.assertIn("Capital Markets Trade Data Product", text)
        self.assertIn('dl:identifier "wealth-client-portfolio-data-product"', text)
        self.assertIn("Wealth Client Portfolio Data Product", text)
        self.assertIn('dl:identifier "public-sector-reference-codes-data-product"', text)
        self.assertIn("Public Sector Reference Codes Data Product", text)
        self.assertIn('dl:identifier "telecoms-subscriber-data-product"', text)
        self.assertIn("Telecoms Subscriber Data Product", text)
        self.assertNotIn("cross-sector", text)
        self.assertEqual(12, len(re.findall(r"a dl:DataProduct", text)))

        self.assertIn("dl:ProductStandardRelevance", text)
        self.assertIn("dl:ProductRegulatoryRelevance", text)
        self.assertIn("dl:considersStandard", text)
        self.assertIn("dl:considersRegulation", text)
        self.assertIn("inst:standard-odps", text)
        self.assertIn("inst:standard-odcs", text)
        self.assertIn("inst:standard-dbt", text)
        self.assertIn("inst:regulation-gdpr", text)
        self.assertIn("inst:regulation-dora", text)
        self.assertIn("inst:regulation-hipaa", text)
        self.assertIn("inst:standard-iceberg", text)  # capital-markets trade considers Iceberg
        # Retail Stock OpenLineage/Iceberg gaps are asserted in test_lineage_capability.py
        self.assertNotIn("dl:usesStandard", text)
        self.assertNotIn("dl:relevantRegulation", text)

        asserted = re.findall(r'dl:assertedBy "([^"]+)"', text)
        self.assertTrue(asserted)
        self.assertEqual({TRANSFORM_AUTHOR}, set(asserted))


class ProductTypologyProjectionTests(unittest.TestCase):
    def test_products_and_mappings_project_into_nodes_and_links(self):
        with NODES.open(newline="", encoding="utf-8") as handle:
            nodes = list(csv.DictReader(handle))
        with RELATIONSHIPS.open(newline="", encoding="utf-8") as handle:
            relationships = list(csv.DictReader(handle))

        products = [row for row in nodes if row[":LABEL"] == "DataProduct"]
        self.assertEqual(12, len(products))
        by_id = {row[":ID"]: row for row in products}
        self.assertIn("product:retail-stock-data-product", by_id)
        self.assertIn("product:banking-customer-data-product", by_id)
        self.assertIn("product:health-customer-data-product", by_id)
        self.assertIn("product:insurance-policy-data-product", by_id)
        self.assertIn("product:insurance-claims-data-product", by_id)
        self.assertIn("product:capital-markets-trade-data-product", by_id)
        self.assertIn("product:wealth-client-portfolio-data-product", by_id)
        self.assertIn("product:retail-customer-loyalty-data-product", by_id)
        self.assertIn("product:hospital-admissions-data-product", by_id)
        self.assertIn("product:care-home-resident-data-product", by_id)
        self.assertIn("product:public-sector-reference-codes-data-product", by_id)
        self.assertIn("product:telecoms-subscriber-data-product", by_id)
        self.assertEqual("Retail Stock Data Product", by_id["product:retail-stock-data-product"]["name"])
        self.assertEqual("Banking Customer Data Product", by_id["product:banking-customer-data-product"]["name"])
        self.assertEqual("Health Customer Data Product", by_id["product:health-customer-data-product"]["name"])
        self.assertEqual("Insurance Policy Data Product", by_id["product:insurance-policy-data-product"]["name"])
        self.assertEqual("Capital Markets Trade Data Product", by_id["product:capital-markets-trade-data-product"]["name"])
        self.assertEqual("Wealth Client Portfolio Data Product", by_id["product:wealth-client-portfolio-data-product"]["name"])
        self.assertEqual("Public Sector Reference Codes Data Product", by_id["product:public-sector-reference-codes-data-product"]["name"])
        self.assertEqual("Telecoms Subscriber Data Product", by_id["product:telecoms-subscriber-data-product"]["name"])
        self.assertEqual("NO_PII", by_id["product:retail-stock-data-product"]["personalDataPosture"])
        self.assertEqual("retail", by_id["product:retail-stock-data-product"]["industryVertical"])
        self.assertEqual("PII", by_id["product:banking-customer-data-product"]["personalDataPosture"])
        self.assertEqual("banking", by_id["product:banking-customer-data-product"]["industryVertical"])
        self.assertEqual("health", by_id["product:health-customer-data-product"]["industryVertical"])
        self.assertEqual("insurance", by_id["product:insurance-policy-data-product"]["industryVertical"])
        self.assertEqual("public-sector", by_id["product:public-sector-reference-codes-data-product"]["industryVertical"])
        self.assertEqual("telecoms", by_id["product:telecoms-subscriber-data-product"]["industryVertical"])

        standard_mappings = [row for row in nodes if "ProductStandardRelevance" in row[":LABEL"]]
        regulatory_mappings = [row for row in nodes if "ProductRegulatoryRelevance" in row[":LABEL"]]
        self.assertEqual(33, len(standard_mappings))
        self.assertEqual(18, len(regulatory_mappings))

        rels = {(row[":START_ID"], row[":TYPE"], row[":END_ID"]) for row in relationships}
        self.assertIn(
            ("product-standard:retail-stock-odps", "FOR_DATA_PRODUCT", "product:retail-stock-data-product"),
            rels,
        )
        self.assertIn(
            ("product-standard:retail-stock-odps", "CONSIDERS_STANDARD", "standard:odps"),
            rels,
        )
        self.assertIn(
            ("product-regulatory:banking-customer-gdpr", "CONSIDERS_REGULATION", "regulation:gdpr"),
            rels,
        )
        self.assertIn(
            ("product-regulatory:banking-customer-dora", "CONSIDERS_REGULATION", "regulation:dora"),
            rels,
        )
        self.assertIn(
            ("product-regulatory:health-customer-hipaa", "CONSIDERS_REGULATION", "regulation:hipaa"),
            rels,
        )
        self.assertNotIn(
            ("product:retail-stock-data-product", "USES_STANDARD", "standard:odps"),
            rels,
        )
        self.assertNotIn(
            ("product:banking-customer-data-product", "RELEVANT_REGULATION", "regulation:gdpr"),
            rels,
        )


class ProductDifferentiationTests(unittest.TestCase):
    """Slice 2: verticals must not collapse to an ODPS+ODCS monoculture."""

    def _positive_bags(self):
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        products = {}
        for match in re.finditer(
            r"inst:product-(\S+) a dl:DataProduct ;(.*?)(?=\ninst:product-|\Z)",
            text,
            flags=re.S,
        ):
            product_id = match.group(1)
            block = match.group(2)
            vertical = re.search(r"tax:industry-vertical-(\S+)", block)
            products[product_id] = {
                "vertical": vertical.group(1) if vertical else "",
                "std": set(),
                "reg": set(),
            }

        for match in re.finditer(
            r"inst:product-standard-(\S+) a dl:ProductStandardRelevance ;(.*?)(?=\ninst:product-|\Z)",
            text,
            flags=re.S,
        ):
            block = match.group(2)
            if "tax:mapping-relation-no-coverage" in block:
                continue
            product = re.search(r"dl:forDataProduct inst:product-(\S+)", block)
            standard = re.search(r"dl:considersStandard inst:standard-(\S+)", block)
            if product and standard:
                products[product.group(1)].setdefault("std", set()).add(standard.group(1))

        for match in re.finditer(
            r"inst:product-regulatory-(\S+) a dl:ProductRegulatoryRelevance ;(.*?)(?=\ninst:product-|\Z)",
            text,
            flags=re.S,
        ):
            block = match.group(2)
            product = re.search(r"dl:forDataProduct inst:product-(\S+)", block)
            regulation = re.search(r"dl:considersRegulation inst:regulation-(\S+)", block)
            if product and regulation:
                products[product.group(1)].setdefault("reg", set()).add(regulation.group(1))
        return products

    def test_each_vertical_has_a_distinctive_non_odps_odcs_signal(self):
        products = self._positive_bags()
        by_vertical: dict[str, list] = {}
        for product_id, info in products.items():
            by_vertical.setdefault(info["vertical"], []).append((product_id, info))

        expected = {
            "banking": lambda std, reg: bool({"openlineage", "iceberg"} & std or {"dora", "bcbs-239"} & reg),
            "retail": lambda std, reg: "dbt" in std or "ccpa-cpra" in reg,
            "health": lambda std, reg: "hipaa" in reg or "gdpr" in reg,
            "insurance": lambda std, reg: "iso-27001" in reg or "gdpr" in reg,
            "public-sector": lambda std, reg: bool({"json-schema", "dcat"} & std or "iso-11179" in reg),
            "telecoms": lambda std, reg: "nis2" in reg,
        }
        for vertical, check in expected.items():
            self.assertIn(vertical, by_vertical, f"missing vertical {vertical}")
            self.assertTrue(
                any(check(info["std"], info["reg"]) for _, info in by_vertical[vertical]),
                f"vertical {vertical} lacks a distinctive consideration beyond ODPS+ODCS",
            )

    def test_not_all_products_share_identical_positive_bags(self):
        products = self._positive_bags()
        bags = [frozenset(info["std"] | {f"reg:{r}" for r in info["reg"]}) for info in products.values()]
        self.assertGreater(len(set(bags)), 1)

    def test_openlineage_not_attached_to_every_product_for_symmetry(self):
        products = self._positive_bags()
        with_openlineage = [pid for pid, info in products.items() if "openlineage" in info["std"]]
        self.assertIn("banking-customer-data-product", with_openlineage)
        self.assertIn("capital-markets-trade-data-product", with_openlineage)
        self.assertNotIn("retail-stock-data-product", with_openlineage)
        self.assertNotIn("wealth-client-portfolio-data-product", with_openlineage)
        self.assertLess(len(with_openlineage), len(products))

    def test_public_sector_considers_dcat_and_wealth_considers_bcbs_239(self):
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        self.assertIn('dl:identifier "public-sector-reference-codes-dcat"', text)
        self.assertIn("inst:standard-dcat", text)
        self.assertIn('dl:identifier "wealth-client-portfolio-bcbs-239"', text)
        self.assertIn("inst:regulation-bcbs-239", text)


if __name__ == "__main__":
    unittest.main()
