# Ontology walkthrough

[← README](../README.md) · [Next: Taxonomy →](02-taxonomy.md)

## What is an ontology?

An ontology defines the language of the model: the types of things, the properties they may carry and the meanings of their relationships. It resembles a database schema, but emphasises shared meaning rather than a particular storage engine.

[`ontology.ttl`](../ontology.ttl) uses RDF, RDFS and OWL in Turtle syntax. It defines the language; it does not contain the 157 landscape records.

## Principal classes

```text
LandscapeEntry
├── DataStandardLandscapeEntry
└── DataRegulationLandscapeEntry

LandscapeAssessment
SourcedMapping
├── ComplianceMapping
└── ComponentMapping
    ├── ComponentImplementationMapping
    └── ComponentRegulatoryMapping
DataIngestionPattern
DataPipelineModule
DataPipelineComponent
Attestation
```

| Class | Meaning |
|---|---|
| `LandscapeEntry` | A record curated into either landscape. |
| `DataStandardLandscapeEntry` | A record in the open-standards landscape. |
| `DataRegulationLandscapeEntry` | A record in the regulation and compliance landscape. |
| `LandscapeAssessment` | The publisher's judgement, reason and tiers for a standard-landscape entry. |
| `ComplianceMapping` | A versioned and attributable assertion connecting two entries. |
| `SourcedMapping` | The shared provenance, version and status boundary for mapping assertions. |
| `ComponentMapping` | The shared parent for implementation and regulatory component mappings. |
| `DataIngestionPattern` | The parent of the six ingestion-pattern classes. |
| `DataPipelineModule` | The parent of Define, Trigger, Orchestrate, Govern and Store module classes. |
| `DataPipelineComponent` | The parent of the listed functional component classes. |
| `ComponentImplementationMapping` | A curated design-time option linking a component type to a landscape entry. |
| `ComponentRegulatoryMapping` | A curated assertion that a component is relevant to a precisely cited regulatory requirement; it is not a compliance claim. |
| `Attestation` | A traceable record of an actor's action, risks, controls and successful control evidence. |

The subclass names describe landscape membership. They do not assert that everything in the standards landscape is a formal standard or that everything in the regulation landscape is a law.

## Common entry properties

```text
LandscapeEntry
├── identifier
├── preferred label
├── fullName
├── firstReleaseYear
├── governanceStatement
├── statusStatement
└── hasGovernanceType ──→ GovernanceType
```

`DataStandardLandscapeEntry` additionally has standard categories, optional `whyAStandard`, `isNiche` and an assessment. `DataRegulationLandscapeEntry` additionally has regulation categories, descriptions, reference links, a preserved source jurisdiction label and normalised jurisdiction relationships.

## Why there are two ODRL and OPA entry nodes

Each landscape makes its own statements about ODRL and OPA. Their category, governance wording and status can differ. The model therefore retains two source-specific entry nodes and connects them with `describesSameResourceAs`.

This avoids losing source context while recording the confirmed identity of the underlying resource. It is not an extraction-source class.

## Compliance mappings

```text
ComplianceMapping
├── mappingSourceEntry ───────→ LandscapeEntry
├── mappingTargetEntry ───────→ LandscapeEntry
├── hasMappingRelation ───────→ MappingRelation
├── hasMappingAuthorityType ──→ MappingAuthorityType
├── assertedBy
├── authoritativeSource
├── sourceVersion
└── mappingStatus
```

A mapping is a node because it has identity, provenance, version and status. It does not assert operational compliance. `COMPLIES_WITH` and `SATISFIES` are deliberately absent from this catalogue-level ontology.

Component regulatory mappings use the same provenance-first pattern. They connect one component type to one `DataRegulationLandscapeEntry` through `regulatoryContext` and require a human-readable requirement reference, rationale and primary source.

## Ingestion structure

Each of the six pattern subclasses requires the five module types through `hasModule`. Each module class requires only its listed component types through `hasComponent`. These are schema restrictions; concrete pipelines and pattern instances remain out of scope.

## Attestation traceability

An attestation requires its own ID, pipeline ID, module ID, component ID and timestamp. It links to an identified actor and identified actions, risks, controls and evidence. A risk points to its action, a control points to the risk it mitigates, and successful evidence points to its control.

## Literals and relationships

A datatype property points to a literal:

```turtle
inst:standard-openapi dl:firstReleaseYear "2011"^^xsd:gYear .
```

An object property points to another resource:

```turtle
inst:standard-openapi
    dl:inStandardCategory tax:standard-category-contracts .
```

## Domain, range and validation

RDFS domains and ranges explain meaning. They do not make missing data invalid. SHACL supplies the operational publication rules described in [the SHACL walkthrough](03-shacl.md).

## Namespace

| Prefix | Namespace |
|---|---|
| `dl:` | `https://www.entropy-data.com/data-landscape/ontology/` |
| `tax:` | `https://www.entropy-data.com/data-landscape/taxonomy/` |
| `inst:` | `https://www.entropy-data.com/data-landscape/instance/` |

## When this artefact changes

Change the ontology when a class, property or relationship meaning changes. Adding another record under existing terms changes an instance file, not the ontology.
