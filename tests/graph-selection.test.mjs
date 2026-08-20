import test from "node:test";
import assert from "node:assert/strict";

import { dagLineageFor, productScopeFor } from "../scripts/graph-selection.mjs";

test("selection includes DAG ancestors and descendants but excludes sibling branches", () => {
  const levels = new Map([
    ["pattern", 0], ["module", 1], ["sibling-module", 1],
    ["component", 2], ["sibling-component", 2], ["mapping", 3],
  ]);
  const links = [
    {id: "l1", source: "pattern", target: "module"},
    {id: "l2", source: "pattern", target: "sibling-module"},
    {id: "l3", source: "module", target: "component"},
    {id: "l4", source: "sibling-module", target: "sibling-component"},
    {id: "l5", source: "mapping", target: "component"},
    {id: "l6", source: "component", target: "sibling-component"},
  ];
  const result = dagLineageFor("component", links, id => levels.get(id));
  assert.deepEqual([...result.nodeIds].sort(), ["component", "mapping", "module", "pattern"]);
  assert.deepEqual([...result.linkIds].sort(), ["l1", "l3", "l5"]);
});

test("selection accepts D3-resolved object endpoints", () => {
  const result = dagLineageFor("a", [{id: "l1", source: {id: "a"}, target: {id: "b"}}], id => ({a: 0, b: 1})[id]);
  assert.deepEqual([...result.nodeIds].sort(), ["a", "b"]);
  assert.deepEqual([...result.linkIds], ["l1"]);
});

test("retail banking and health product scopes differ via reified mappings only", () => {
  const nodes = [
    {id: "product:retail-stock-data-product", labels: ["DataProduct"], personalDataPosture: "NO_PII", industryVertical: "retail"},
    {id: "product:banking-customer-data-product", labels: ["DataProduct"], personalDataPosture: "PII", industryVertical: "banking"},
    {id: "product:health-customer-data-product", labels: ["DataProduct"], personalDataPosture: "PII", industryVertical: "health"},
    {id: "product-standard:retail-stock-odps", labels: ["ProductStandardRelevance"]},
    {id: "product-standard:retail-stock-dbt", labels: ["ProductStandardRelevance"]},
    {id: "product-standard:banking-customer-odps", labels: ["ProductStandardRelevance"]},
    {id: "product-standard:banking-customer-odcs", labels: ["ProductStandardRelevance"]},
    {id: "product-regulatory:banking-customer-gdpr", labels: ["ProductRegulatoryRelevance"]},
    {id: "product-regulatory:banking-customer-dora", labels: ["ProductRegulatoryRelevance"]},
    {id: "product-regulatory:health-customer-hipaa", labels: ["ProductRegulatoryRelevance"]},
    {id: "standard:odps", labels: ["DataStandardLandscapeEntry"]},
    {id: "standard:odcs", labels: ["DataStandardLandscapeEntry"]},
    {id: "standard:dbt", labels: ["DataStandardLandscapeEntry"]},
    {id: "regulation:gdpr", labels: ["DataRegulationLandscapeEntry"]},
    {id: "regulation:dora", labels: ["DataRegulationLandscapeEntry"]},
    {id: "regulation:hipaa", labels: ["DataRegulationLandscapeEntry"]},
    {id: "regulation:nist-800-53", labels: ["DataRegulationLandscapeEntry"]},
    {id: "component-mapping:data-contract-definition-odcs", labels: ["ComponentImplementationMapping"]},
    {id: "component-mapping:validation-and-contract-binding-odcs", labels: ["ComponentImplementationMapping"]},
    {id: "component-type:data-contract-definition", labels: ["DataPipelineComponentType"]},
    {id: "component-type:validation-and-contract-binding", labels: ["DataPipelineComponentType"]},
    {id: "component-regulatory:validation-and-contract-binding-nist-800-53", labels: ["ComponentRegulatoryMapping"]},
    {id: "component-regulatory:secure-read-access-gdpr", labels: ["ComponentRegulatoryMapping"]},
    {id: "industry-vertical:retail", labels: ["Concept", "IndustryVertical"]},
    {id: "industry-vertical:banking", labels: ["Concept", "IndustryVertical"]},
    {id: "industry-vertical:health", labels: ["Concept", "IndustryVertical"]},
    {id: "personal-data-posture:no-pii", labels: ["Concept", "PersonalDataPosture"]},
    {id: "personal-data-posture:pii", labels: ["Concept", "PersonalDataPosture"]},
  ];
  const links = [
    {id: "r1", source: "product:retail-stock-data-product", target: "personal-data-posture:no-pii", type: "HAS_PERSONAL_DATA_POSTURE"},
    {id: "r2", source: "product:retail-stock-data-product", target: "industry-vertical:retail", type: "IN_INDUSTRY_VERTICAL"},
    {id: "r3", source: "product-standard:retail-stock-odps", target: "product:retail-stock-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "r4", source: "product-standard:retail-stock-odps", target: "standard:odps", type: "CONSIDERS_STANDARD"},
    {id: "r5", source: "product-standard:retail-stock-dbt", target: "product:retail-stock-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "r6", source: "product-standard:retail-stock-dbt", target: "standard:dbt", type: "CONSIDERS_STANDARD"},
    {id: "b1", source: "product:banking-customer-data-product", target: "personal-data-posture:pii", type: "HAS_PERSONAL_DATA_POSTURE"},
    {id: "b2", source: "product:banking-customer-data-product", target: "industry-vertical:banking", type: "IN_INDUSTRY_VERTICAL"},
    {id: "b3", source: "product-standard:banking-customer-odps", target: "product:banking-customer-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "b4", source: "product-standard:banking-customer-odps", target: "standard:odps", type: "CONSIDERS_STANDARD"},
    {id: "b3b", source: "product-standard:banking-customer-odcs", target: "product:banking-customer-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "b4b", source: "product-standard:banking-customer-odcs", target: "standard:odcs", type: "CONSIDERS_STANDARD"},
    {id: "b5", source: "product-regulatory:banking-customer-gdpr", target: "product:banking-customer-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "b6", source: "product-regulatory:banking-customer-gdpr", target: "regulation:gdpr", type: "CONSIDERS_REGULATION"},
    {id: "b7", source: "product-regulatory:banking-customer-dora", target: "product:banking-customer-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "b8", source: "product-regulatory:banking-customer-dora", target: "regulation:dora", type: "CONSIDERS_REGULATION"},
    {id: "h1", source: "product:health-customer-data-product", target: "industry-vertical:health", type: "IN_INDUSTRY_VERTICAL"},
    {id: "h2", source: "product-regulatory:health-customer-hipaa", target: "product:health-customer-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "h3", source: "product-regulatory:health-customer-hipaa", target: "regulation:hipaa", type: "CONSIDERS_REGULATION"},
    {id: "c1", source: "component-mapping:data-contract-definition-odcs", target: "standard:odcs", type: "IMPLEMENTATION_OPTION"},
    {id: "c2", source: "component-mapping:data-contract-definition-odcs", target: "component-type:data-contract-definition", type: "MAPS_COMPONENT_TYPE"},
    {id: "c3", source: "component-mapping:validation-and-contract-binding-odcs", target: "standard:odcs", type: "IMPLEMENTATION_OPTION"},
    {id: "c4", source: "component-mapping:validation-and-contract-binding-odcs", target: "component-type:validation-and-contract-binding", type: "MAPS_COMPONENT_TYPE"},
    {id: "crm1", source: "component-regulatory:validation-and-contract-binding-nist-800-53", target: "component-type:validation-and-contract-binding", type: "MAPS_COMPONENT_TYPE"},
    {id: "crm2", source: "component-regulatory:validation-and-contract-binding-nist-800-53", target: "regulation:nist-800-53", type: "REGULATORY_CONTEXT"},
    {id: "m1", source: "component-regulatory:secure-read-access-gdpr", target: "regulation:gdpr", type: "REGULATORY_CONTEXT"},
  ];

  const retail = productScopeFor({verticalId: "industry-vertical:retail"}, nodes, links);
  const banking = productScopeFor({verticalId: "industry-vertical:banking"}, nodes, links);
  const health = productScopeFor({verticalId: "industry-vertical:health"}, nodes, links);

  assert.ok(retail.has("product:retail-stock-data-product"));
  assert.ok(retail.has("standard:dbt"));
  assert.ok(retail.has("product-standard:retail-stock-odps"));
  // Retail does not consider ODCS, so ODCS→validation CRM neighbourhood stays out.
  assert.equal(retail.has("regulation:nist-800-53"), false);
  assert.equal(retail.has("component-regulatory:validation-and-contract-binding-nist-800-53"), false);
  assert.equal(retail.has("component-regulatory:secure-read-access-gdpr"), false);

  assert.ok(banking.has("product:banking-customer-data-product"));
  assert.ok(banking.has("regulation:gdpr"));
  assert.ok(banking.has("regulation:dora"));
  assert.ok(banking.has("product-regulatory:banking-customer-gdpr"));
  assert.equal(banking.has("standard:dbt"), false);
  // View-only CRM walk: ODCS → validation CIM → NIST 800-53 CRM (not asserted on the product).
  assert.ok(banking.has("standard:odcs"));
  assert.ok(banking.has("component-mapping:validation-and-contract-binding-odcs"));
  assert.ok(banking.has("component-type:validation-and-contract-binding"));
  assert.ok(banking.has("component-regulatory:validation-and-contract-binding-nist-800-53"));
  assert.ok(banking.has("regulation:nist-800-53"));
  assert.equal(banking.has("component-regulatory:secure-read-access-gdpr"), false);

  assert.ok(health.has("product:health-customer-data-product"));
  assert.ok(health.has("regulation:hipaa"));
  assert.equal(health.has("regulation:dora"), false);
  assert.equal(health.has("regulation:nist-800-53"), false);
});

test("product scope CRM walk skips no-coverage standard considerations", () => {
  const nodes = [
    {id: "product:retail-stock-data-product", labels: ["DataProduct"], personalDataPosture: "NO_PII", industryVertical: "retail"},
    {id: "product-standard:retail-stock-openlineage", labels: ["ProductStandardRelevance"]},
    {id: "standard:openlineage", labels: ["DataStandardLandscapeEntry"]},
    {id: "mapping-relation:no-coverage", labels: ["Concept", "MappingRelation"]},
    {id: "component-mapping:lineage-emission-openlineage", labels: ["ComponentImplementationMapping"]},
    {id: "component-type:lineage-emission", labels: ["DataPipelineComponentType"]},
    {id: "industry-vertical:retail", labels: ["Concept", "IndustryVertical"]},
  ];
  const links = [
    {id: "r1", source: "product:retail-stock-data-product", target: "industry-vertical:retail", type: "IN_INDUSTRY_VERTICAL"},
    {id: "g1", source: "product-standard:retail-stock-openlineage", target: "product:retail-stock-data-product", type: "FOR_DATA_PRODUCT"},
    {id: "g2", source: "product-standard:retail-stock-openlineage", target: "standard:openlineage", type: "CONSIDERS_STANDARD"},
    {id: "g3", source: "product-standard:retail-stock-openlineage", target: "mapping-relation:no-coverage", type: "HAS_MAPPING_RELATION"},
    {id: "c1", source: "component-mapping:lineage-emission-openlineage", target: "standard:openlineage", type: "IMPLEMENTATION_OPTION"},
    {id: "c2", source: "component-mapping:lineage-emission-openlineage", target: "component-type:lineage-emission", type: "MAPS_COMPONENT_TYPE"},
  ];
  const retail = productScopeFor({productId: "product:retail-stock-data-product"}, nodes, links);
  assert.ok(retail.has("product-standard:retail-stock-openlineage"));
  assert.ok(retail.has("standard:openlineage"));
  assert.ok(retail.has("mapping-relation:no-coverage"));
  assert.equal(retail.has("component-mapping:lineage-emission-openlineage"), false);
  assert.equal(retail.has("component-type:lineage-emission"), false);
});

test("product scope is inactive when all typology selectors are all", () => {
  assert.equal(productScopeFor({verticalId: "all", productId: "all", postureId: "all"}, [], []), null);
});
