# Neo4j schema walkthrough

[← Neo4j CSV](05-neo4j-csv.md) · [README](../README.md) · [Next: Loading →](07-loading-and-validation.md)

[`neo4j-schema.cypher`](../neo4j-schema.cypher) protects identifiers and creates search structures after bulk import.

## Uniqueness constraints

Unique `id` constraints are created for:

- `DataStandardLandscapeEntry`;
- `DataRegulationLandscapeEntry`;
- `LandscapeAssessment`;
- `ComplianceMapping`;
- `ComponentImplementationMapping`;
- `ComponentRegulatoryMapping`;
- ingestion pattern, module and component types;
- attestation, actor, action, risk, control and evidence identifiers;
- `Concept`.

```cypher
CREATE CONSTRAINT standard_entry_id_unique IF NOT EXISTS
FOR (n:DataStandardLandscapeEntry) REQUIRE n.id IS UNIQUE;
```

Identifiers are source-scoped: ODRL and OPA occur in both landscapes. Uniqueness is therefore enforced separately for each subclass, while CSV import IDs remain globally unique. Names are also not unique because two different standard source records are displayed as ODPS.

## Range indexes

Indexes support common lookup and sorting by:

- landscape-entry name;
- landscape-entry first release year;
- standard-entry name;
- regulation-entry name;
- concept name.
- attestation pipeline, module and component IDs.

## Full-text indexes

`landscape_entry_search` covers names, descriptions, governance, status and optional rationale. `assessment_search` covers judgement reasons.

## Import order

For a new database, bulk import the CSVs and then apply the schema. For incremental loading, create constraints first and use a controlled `MERGE` pipeline.

The Cypher targets Neo4j 5.x/current syntax. Validate against the deployed Neo4j major version before production use.
