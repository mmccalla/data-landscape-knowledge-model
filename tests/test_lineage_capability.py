"""Behaviour checks for lineage-emission under Orchestrate and OpenLineage CIM."""

from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology.ttl"
SHAPES = ROOT / "shapes.ttl"
COMPONENT_MAPPINGS = ROOT / "component-mappings.ttl"
PRODUCT_INSTANCES = ROOT / "product-instances.ttl"
NODES = ROOT / "nodes.csv"
RELATIONSHIPS = ROOT / "relationships.csv"
MAPPING_EXPLANATIONS = ROOT / "src" / "mapping-explanations.json"


class LineageEmissionOntologyTests(unittest.TestCase):
    def test_lineage_emission_is_orchestrate_component_not_metadata_registration(self):
        text = ONTOLOGY.read_text(encoding="utf-8")
        self.assertRegex(text, r"dl:LineageEmission\s+a\s+owl:Class")
        self.assertIn("rdfs:subClassOf dl:DataPipelineComponent", text)
        self.assertIn('rdfs:label "Lineage emission"@en-GB', text)
        self.assertIn(
            "dl:OrchestrateModule rdfs:subClassOf [ a owl:Restriction ; "
            "owl:onProperty dl:hasComponent ; owl:someValuesFrom dl:LineageEmission ]",
            text,
        )
        self.assertNotIn(
            "dl:GovernModule rdfs:subClassOf [ a owl:Restriction ; "
            "owl:onProperty dl:hasComponent ; owl:someValuesFrom dl:LineageEmission ]",
            text,
        )
        self.assertNotIn(
            "dl:StoreModule rdfs:subClassOf [ a owl:Restriction ; "
            "owl:onProperty dl:hasComponent ; owl:someValuesFrom dl:LineageEmission ]",
            text,
        )
        self.assertIn("dl:hasMappingRelation", text)
        # Product gaps reuse MappingRelation; domain must not stay ComplianceMapping-only.
        self.assertNotRegex(
            text,
            r"dl:hasMappingRelation a owl:ObjectProperty ; rdfs:domain dl:ComplianceMapping ;",
        )


class LineageEmissionMappingTests(unittest.TestCase):
    def test_openlineage_cim_targets_lineage_emission(self):
        text = COMPONENT_MAPPINGS.read_text(encoding="utf-8")
        self.assertIn('dl:identifier "lineage-emission-openlineage"', text)
        self.assertIn("dl:mapsComponentType dl:LineageEmission", text)
        self.assertIn("dl:implementationOption inst:standard-openlineage", text)
        self.assertIn("https://openlineage.io/docs/spec/object-model/", text)
        # Airflow remains a separate orchestration option; do not equate it with OpenLineage.
        self.assertNotRegex(
            text,
            r"lineage-emission-openlineage[\s\S]{0,800}Apache Airflow is a candidate implementation option for lineage",
        )

    def test_retail_stock_reifies_openlineage_and_iceberg_gaps(self):
        text = PRODUCT_INSTANCES.read_text(encoding="utf-8")
        self.assertIn('dl:identifier "retail-stock-openlineage"', text)
        self.assertIn('dl:identifier "retail-stock-iceberg"', text)
        self.assertIn("tax:mapping-relation-no-coverage", text)
        self.assertIn("inst:standard-openlineage", text)
        self.assertIn("inst:standard-iceberg", text)
        for gap_id in ("retail-stock-openlineage", "retail-stock-iceberg"):
            block = re.search(
                rf'inst:product-standard-{gap_id} a dl:ProductStandardRelevance\s*;(.*?)\.',
                text,
                flags=re.DOTALL,
            )
            self.assertIsNotNone(block, f"missing gap mapping {gap_id}")
            self.assertIn("tax:mapping-relation-no-coverage", block.group(1))
        self.assertIn("Snowflake", text)
        self.assertNotIn("lineage has no component mapping", text.lower())

    def test_shacl_allows_optional_mapping_relation_on_product_standard_relevance(self):
        text = SHAPES.read_text(encoding="utf-8")
        block = re.search(
            r"dl:ProductStandardRelevanceShape a sh:NodeShape.*?(?=dl:\w+Shape a sh:NodeShape|\Z)",
            text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(block)
        self.assertIn("dl:hasMappingRelation", block.group(0))
        self.assertIn("sh:maxCount 1", block.group(0))


class LineageEmissionProjectionTests(unittest.TestCase):
    def test_csv_projects_component_cim_and_retail_gaps(self):
        with NODES.open(newline="", encoding="utf-8") as handle:
            nodes = list(csv.DictReader(handle))
        with RELATIONSHIPS.open(newline="", encoding="utf-8") as handle:
            relationships = list(csv.DictReader(handle))

        by_id = {row[":ID"]: row for row in nodes}
        self.assertIn("component-type:lineage-emission", by_id)
        self.assertEqual("Lineage emission", by_id["component-type:lineage-emission"]["name"])
        self.assertEqual(
            "DataPipelineComponentType",
            by_id["component-type:lineage-emission"][":LABEL"],
        )
        self.assertIn("component-mapping:lineage-emission-openlineage", by_id)
        self.assertIn("product-standard:retail-stock-openlineage", by_id)
        self.assertIn("product-standard:retail-stock-iceberg", by_id)

        rels = {(row[":START_ID"], row[":TYPE"], row[":END_ID"]) for row in relationships}
        self.assertIn(
            ("module-type:orchestrate", "HAS_COMPONENT", "component-type:lineage-emission"),
            rels,
        )
        self.assertNotIn(
            ("module-type:govern", "HAS_COMPONENT", "component-type:lineage-emission"),
            rels,
        )
        self.assertNotIn(
            ("module-type:store", "HAS_COMPONENT", "component-type:lineage-emission"),
            rels,
        )
        self.assertIn(
            (
                "component-mapping:lineage-emission-openlineage",
                "MAPS_COMPONENT_TYPE",
                "component-type:lineage-emission",
            ),
            rels,
        )
        self.assertIn(
            (
                "component-mapping:lineage-emission-openlineage",
                "IMPLEMENTATION_OPTION",
                "standard:openlineage",
            ),
            rels,
        )
        self.assertIn(
            (
                "product-standard:retail-stock-openlineage",
                "HAS_MAPPING_RELATION",
                "mapping-relation:no-coverage",
            ),
            rels,
        )
        self.assertIn(
            (
                "product-standard:retail-stock-iceberg",
                "HAS_MAPPING_RELATION",
                "mapping-relation:no-coverage",
            ),
            rels,
        )
        # Gaps still point at the standards they decline, but must not look like store CIM claims.
        self.assertIn(
            (
                "product-standard:retail-stock-iceberg",
                "CONSIDERS_STANDARD",
                "standard:iceberg",
            ),
            rels,
        )
        self.assertNotIn(
            (
                "product:retail-stock-data-product",
                "IMPLEMENTATION_OPTION",
                "standard:iceberg",
            ),
            rels,
        )
        self.assertNotIn(
            (
                "product:retail-stock-data-product",
                "IMPLEMENTATION_OPTION",
                "standard:openlineage",
            ),
            rels,
        )

    def test_mapping_explanation_covers_openlineage_cim(self):
        import json

        explanations = json.loads(MAPPING_EXPLANATIONS.read_text(encoding="utf-8"))
        entry = explanations["component-mapping:lineage-emission-openlineage"]
        self.assertTrue(entry["rationale"])
        self.assertTrue(entry["boundary"])
        self.assertTrue(any("openlineage.io" in source for source in entry["sources"]))
        self.assertNotIn("Airflow is OpenLineage", entry["rationale"])
        self.assertNotIn("Airflow is OpenLineage", entry["boundary"])


if __name__ == "__main__":
    unittest.main()
