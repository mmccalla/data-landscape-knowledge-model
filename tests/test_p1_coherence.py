"""P1 coherence: CRM coverage, ADOPT CIM batch, product-reg CRM link."""

from __future__ import annotations

import csv
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_MAPPINGS = ROOT / "component-mappings.ttl"
COMPONENT_REGULATORY = ROOT / "component-regulatory-mappings.ttl"
PRODUCT_INSTANCES = ROOT / "product-instances.ttl"
DESIGN_DECISIONS = ROOT / "docs" / "08-design-decisions.md"
NODES = ROOT / "nodes.csv"
MAPPING_EXPLANATIONS = ROOT / "src" / "mapping-explanations.json"

BATCH_A = (
    "source-connectivity-kafka",
    "workload-execution-orchestration-spark",
    "store-write-data-product-parquet",
    "data-contract-definition-json-schema",
    "data-contract-definition-openapi",
    "data-contract-definition-avro",
)


class CrmCoherenceTests(unittest.TestCase):
    def test_named_bare_components_now_have_crm(self):
        text = COMPONENT_REGULATORY.read_text(encoding="utf-8")
        for component in (
            "TriggerInvocation",
            "WorkloadPlanning",
            "StoreWriteDataProduct",
            "LineageEmission",
        ):
            self.assertIn(f"dl:mapsComponentType dl:{component}", text)

    def test_iso_27001_has_at_least_one_crm(self):
        text = COMPONENT_REGULATORY.read_text(encoding="utf-8")
        self.assertIn('dl:identifier "secure-read-access-iso-27001"', text)
        self.assertIn("dl:regulatoryContext inst:regulation-iso-27001", text)

    def test_every_product_regulation_has_crm_somewhere(self):
        prod = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        crm = COMPONENT_REGULATORY.read_text(encoding="utf-8")
        product_regs = set(re.findall(r"dl:considersRegulation inst:regulation-(\S+)", prod))
        crm_regs = set(re.findall(r"dl:regulatoryContext inst:regulation-(\S+)", crm))
        floating = sorted(product_regs - crm_regs)
        self.assertEqual([], floating, f"product regs without CRM: {floating}")


class AdoptCimBatchTests(unittest.TestCase):
    def test_batch_a_cims_exist(self):
        text = COMPONENT_MAPPINGS.read_text(encoding="utf-8")
        for identifier in BATCH_A:
            self.assertIn(f'dl:identifier "{identifier}"', text)

    def test_batch_b_declared_in_design_decisions(self):
        text = DESIGN_DECISIONS.read_text(encoding="utf-8")
        self.assertIn("ADOPT catalogue-only", text)
        self.assertIn("great-expectations", text)
        self.assertIn("unity-catalog", text)

    def test_csv_and_explanations_cover_batch_a(self):
        with NODES.open(newline="", encoding="utf-8") as handle:
            nodes = {row[":ID"] for row in csv.DictReader(handle)}
        explanations = json.loads(MAPPING_EXPLANATIONS.read_text(encoding="utf-8"))
        for identifier in BATCH_A:
            mid = f"component-mapping:{identifier}"
            self.assertIn(mid, nodes)
            self.assertIn(mid, explanations)


if __name__ == "__main__":
    unittest.main()
