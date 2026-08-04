# Neo4j CSV walkthrough

[← Instances](04-instances.md) · [README](../README.md) · [Next: Neo4j schema →](06-neo4j-schema.md)

## Why CSV is included

RDF represents subject–predicate–object statements. Neo4j represents labelled nodes, typed relationships and properties. [`nodes.csv`](../nodes.csv) and [`relationships.csv`](../relationships.csv) project the same model into a labelled property graph.

## Labels

Principal labels include:

```text
LandscapeEntry
├── DataStandardLandscapeEntry
└── DataRegulationLandscapeEntry

LandscapeAssessment
ComplianceMapping
ComponentImplementationMapping
ComponentRegulatoryMapping
DataIngestionPatternType
DataPipelineModuleType
DataPipelineComponentType
Concept
├── StandardCategory
├── RegulationCategory
├── Judgement
├── Tier
├── GovernanceType
├── Jurisdiction
├── MappingRelation
└── MappingAuthorityType
```

Every standard or regulation entry also has `LandscapeEntry`, enabling queries across both catalogues.

## Special headers

| Header | Meaning |
|---|---|
| `:ID` | Import-time unique endpoint key. |
| `:LABEL` | Semicolon-separated Neo4j labels. |
| `firstReleaseYear:int` | Import as an integer. |
| `isNiche:boolean` | Import as a Boolean. |

The ordinary `id` property remains after import and is protected by a uniqueness constraint.

## Relationship families

Standard-landscape relationships:

```text
IN_STANDARD_CATEGORY
HAS_ASSESSMENT
ASSESSES
JUDGED_AS
HAS_TIER
HAS_GOVERNANCE_TYPE
```

Regulation-landscape relationships:

```text
IN_REGULATION_CATEGORY
APPLIES_IN
HAS_GOVERNANCE_TYPE
```

Cross-landscape and mapping relationships:

```text
DESCRIBES_SAME_RESOURCE_AS
SOURCE_ENTRY
TARGET_ENTRY
HAS_MAPPING_RELATION
HAS_AUTHORITY_TYPE
MAPS_COMPONENT_TYPE
IMPLEMENTATION_OPTION
REGULATORY_CONTEXT
```

Ingestion structure uses `HAS_MODULE` and `HAS_COMPONENT`. Future runtime attestations use the ontology's actor, action, risk, control and evidence relationships; no concrete runtime attestations are included yet.

`BROADER` connects each detailed category to its section.

## Counts

The delivered projection contains **393 nodes** and **921 relationships**. Counts are generated rather than handwritten; the validation process checks unique import IDs and every relationship endpoint.

## RDF-to-property-graph mapping

| RDF construct | Neo4j projection |
|---|---|
| RDF class | Node label |
| Resource IRI | CSV `:ID` plus persistent `id` property |
| Literal | Node property |
| Object property | Typed relationship |
| `skos:prefLabel` | `name` property |
| `skos:broader` | `BROADER` relationship |

Two inverse identity edges and both assessment directions are deliberate Neo4j conveniences. RDF retains the canonical semantics.
