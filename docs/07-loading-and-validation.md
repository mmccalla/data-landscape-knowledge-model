# Loading and validation guide

[← Neo4j schema](06-neo4j-schema.md) · [README](../README.md) · [Next: Design decisions →](08-design-decisions.md)

## RDF validation

Parse every Turtle artefact:

```sh
riot --validate ontology.ttl
riot --validate taxonomy.ttl
riot --validate shapes.ttl
riot --validate instances.ttl
riot --validate regulation-instances.ttl
riot --validate mapping-instances.ttl
```

Combine the data graph and run SHACL:

```sh
riot --formatted=turtle \
  ontology.ttl taxonomy.ttl instances.ttl \
  regulation-instances.ttl mapping-instances.ttl > bundle.ttl

pyshacl -s shapes.ttl bundle.ttl
```

Expected result: `Conforms: True`.

## Neo4j bulk import

Place the CSV files in an import-readable directory:

```sh
neo4j-admin database import full \
  --nodes=nodes.csv \
  --relationships=relationships.csv \
  <database>
```

Then apply [`neo4j-schema.cypher`](../neo4j-schema.cypher). Bulk import creates a new database; do not point it at an existing populated database.

## Expected principal counts

```cypher
MATCH (n:DataStandardLandscapeEntry) RETURN count(n);   // 81
MATCH (n:DataRegulationLandscapeEntry) RETURN count(n); // 73
MATCH (n:LandscapeAssessment) RETURN count(n);          // 81
MATCH (n:ComplianceMapping) RETURN count(n);             // 3
MATCH (n:LandscapeEntry)-[:APPLIES_IN]->() RETURN count(*); // 81
```

## Example queries

Find Contracts entries and judgements:

```cypher
MATCH (s:DataStandardLandscapeEntry)
      -[:IN_STANDARD_CATEGORY]->(:StandardCategory {id: 'contracts'})
MATCH (s)-[:HAS_ASSESSMENT]->(a)-[:JUDGED_AS]->(j:Judgement)
RETURN s.name, j.name, a.judgementReason ORDER BY s.name;
```

Find regulation entries relevant in both the US and global scopes:

```cypher
MATCH (r:DataRegulationLandscapeEntry)-[:APPLIES_IN]->(us:Jurisdiction {id:'us'})
MATCH (r)-[:APPLIES_IN]->(global:Jurisdiction {id:'global'})
RETURN r.name, r.statusStatement ORDER BY r.name;
```

Inspect official mappings:

```cypher
MATCH (source)<-[:SOURCE_ENTRY]-(m:ComplianceMapping)-[:TARGET_ENTRY]->(target)
MATCH (m)-[:HAS_MAPPING_RELATION]->(relation:MappingRelation)
RETURN source.name, relation.name, target.name,
       m.assertedBy, m.authoritativeSource;
```

Find the two confirmed cross-landscape identity pairs:

```cypher
MATCH (s:DataStandardLandscapeEntry)
      -[:DESCRIBES_SAME_RESOURCE_AS]->(r:DataRegulationLandscapeEntry)
RETURN s.name, r.name;
```

## Integrity checks

The build must verify:

- 81 standards and 73 regulation entries;
- 82 standard and 73 regulation category memberships;
- 81 normalised jurisdiction memberships;
- two cross-landscape identity pairs;
- three official mappings;
- unique CSV import IDs;
- no dangling relationship endpoints;
- consistent CSV column widths;
- positive SHACL conformance and negative-fixture rejection;
- absence of placeholder namespaces and extraction-source classes.

Do not weaken a shape merely to make invalid data pass. Resolve whether the fault is in source data, normalisation, taxonomy or the constraint itself.
