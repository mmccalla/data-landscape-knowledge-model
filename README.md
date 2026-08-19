# Data Landscape knowledge model

> **Catalogues** by [Simon Harrer](https://www.data-landscape.com/) / Entropy Data, MIT-licensed.  
> **Regulation sub-landscape** originally donated by Mark McCalla, curated by Simon Harrer.  
> **This repository** is Mark McCalla’s schema-first transformation of those catalogues (Enterprise Solutions Consulting Ltd). It is not published by Entropy Data.  
> **Licence:** catalogue data © Entropy Data, MIT; transformation by Mark McCalla. Keep [LICENSE](LICENSE) and [ATTRIBUTION.md](ATTRIBUTION.md).

You are designing CDC ingestion for EU personal data in a bank. Which open standards should you pick, and which regulations actually attach to those pipeline components?

That is the job. In 2026 the same pipelines carry GDPR, DORA, NIS2 and the AI Act. The useful question is which obligations attach to an ingestion pattern, with sources.

The catalogues already live at [data-landscape.com](https://www.data-landscape.com/) and the [regulation map](https://www.data-landscape.com/regulation.html). Simon’s site is the map people keep using. This package is a queryable version of that map: ingestion pattern → component → standard and regulatory context, with evidence grades. Wrapping the catalogues does not create a new landscape.

Open [`graph.html`](graph.html) in a browser (local file; no server). Choose a **Data pipeline type** — for example Batch file ingestion — rather than the full landscape at once.

![Batch file ingestion pattern scoped to related modules, components, and regulatory context](docs/images/pipeline-graph.png)

### Who this is for

- UK and EU enterprise and data architects in financial services, insurance and the public sector, who choose standards and then need a regulator-shaped story.
- Data platform and data-mesh consultants who currently do this mapping in slides.
- People already around Entropy Data and ODCS: adjacent context, not a product to buy.

**84** Data Standard Landscape entries (81 upstream plus three source-backed extensions) and **73** Data Regulation Landscape entries sit behind that question. Official crosswalks are limited to the three assertions with cited sources; that bound is deliberate.

## Start with the four layers

Think of the package as a governed catalogue:

1. **Ontology:** defines the types of things and relationships that may exist.
2. **Taxonomy:** defines approved classification values and their hierarchy.
3. **SHACL:** defines the data-quality rules that publishable records must pass.
4. **Instances:** supplies the actual landscape entries and sourced mappings.

The Neo4j CSV and Cypher files then project the same model into a labelled property graph.

```text
Ontology → Taxonomy → SHACL → Instances → Neo4j projection
```

This is “schema first, instances last”.

## The model in one picture

```text
LandscapeEntry
├── DataStandardLandscapeEntry
│   ├── IN_STANDARD_CATEGORY ──→ StandardCategory
│   ├── HAS_GOVERNANCE_TYPE ──→ GovernanceType
│   └── HAS_ASSESSMENT ───────→ LandscapeAssessment
│                                ├── JUDGED_AS ──→ Judgement
│                                └── HAS_TIER ──→ Tier
│
└── DataRegulationLandscapeEntry
    ├── IN_REGULATION_CATEGORY → RegulationCategory
    ├── APPLIES_IN ────────────→ Jurisdiction
    └── HAS_GOVERNANCE_TYPE ───→ GovernanceType

ComplianceMapping
├── SOURCE_ENTRY ──────────────→ LandscapeEntry
├── TARGET_ENTRY ──────────────→ LandscapeEntry
├── HAS_MAPPING_RELATION ──────→ MappingRelation
└── HAS_AUTHORITY_TYPE ────────→ MappingAuthorityType

ComponentRegulatoryMapping
├── MAPS_COMPONENT_TYPE ───────→ DataPipelineComponent
└── REGULATORY_CONTEXT ────────→ DataRegulationLandscapeEntry

DataIngestionPattern
├── BatchFileIngestion
├── APIPullIngestion
├── EventDrivenIngestion
├── DatabaseCDCIngestion
├── ObjectStoreReplication
└── TableFormatStreaming
    └── HAS_MODULE ─────────────→ DataPipelineModule
                                  └── HAS_COMPONENT ──→ DataPipelineComponent

Attestation
├── pipelineId / moduleId / componentId / timestamp
├── PERFORMED_BY ───────────────→ Actor
├── RECORDS_ACTION ─────────────→ Action ←── RISK_FOR_ACTION ── Risk
├── RECORDS_CONTROL ────────────→ Control ── MITIGATES_RISK ──→ Risk
└── RECORDS_EVIDENCE ───────────→ ControlEvidence ── EVIDENCE_FOR_CONTROL ──→ Control
```

The subclass names deliberately describe membership in a landscape. A `DataRegulationLandscapeEntry` may be a law, standard, control catalogue or assurance scheme. `GovernanceType` identifies how the entry is established or stewarded.

## Why the assessment is separate

Adopt, Assess, Situational and Caution are publisher opinions about Data Standard Landscape entries. They can change without changing the underlying entry.

The regulation landscape does not use those judgements or tiers. Its relevance depends instead on matters such as jurisdiction and context.

## Why mappings are separate nodes

An official crosswalk has its own authority, version, status and supporting URL. A `ComplianceMapping` therefore represents the mapping assertion explicitly. It does **not** claim that a framework itself “complies with” a law or that adopting a standard automatically satisfies legislation.

The delivered mappings are limited to three assertions supported by official sources. That is the honest set, not a backlog:

- CSA CCM maps to NIST CSF;
- CSA CCM maps to ISO/IEC 27001;
- the approved EU Cloud Code of Conduct supports evidence relating to GDPR compliance.

## Package contents

| Artefact | Purpose | Walkthrough |
|---|---|---|
| [`ontology.ttl`](ontology.ttl) | Classes, properties and relationship meanings. | [Ontology](docs/01-ontology.md) |
| [`taxonomy.ttl`](taxonomy.ttl) | Categories, judgements, tiers, governance types, jurisdictions and mapping terms. | [Taxonomy](docs/02-taxonomy.md) |
| [`shapes.ttl`](shapes.ttl) | Validation rules for entries, assessments, concepts and mappings. | [SHACL](docs/03-shacl.md) |
| [`instances.ttl`](instances.ttl) | Data Standard Landscape entries and assessments. | [Instances](docs/04-instances.md) |
| [`regulation-instances.ttl`](regulation-instances.ttl) | Data Regulation Landscape entries. | [Instances](docs/04-instances.md) |
| [`mapping-instances.ttl`](mapping-instances.ttl) | Officially supported mapping assertions. | [Mappings](docs/10-compliance-mappings.md) |
| [`component-mappings.ttl`](component-mappings.ttl) | Curated implementation options linking pipeline components to landscape entries. | [Instances](docs/04-instances.md) |
| [`component-regulatory-mappings.ttl`](component-regulatory-mappings.ttl) | Curated, primary-source-backed regulatory context for pipeline components. | [Mappings](docs/10-compliance-mappings.md) |
| [`graph.html`](graph.html) | Standalone D3 visualisation with node-type filters and pipeline-scoped views. | Open directly in a browser. |
| [`nodes.csv`](nodes.csv) | Neo4j nodes for all RDF resources. | [Neo4j CSV](docs/05-neo4j-csv.md) |
| [`relationships.csv`](relationships.csv) | Neo4j relationships. | [Neo4j CSV](docs/05-neo4j-csv.md) |
| [`neo4j-schema.cypher`](neo4j-schema.cypher) | Neo4j keys, constraints and indexes. | [Neo4j schema](docs/06-neo4j-schema.md) |
| [`ATTRIBUTION.md`](ATTRIBUTION.md) | Authorship, reuse and transformation boundary. | [Attribution](ATTRIBUTION.md) |
| [`CITATION.bib`](CITATION.bib) | BibTeX citations. | [Citation](CITATION.bib) |
| [`SOURCE-MANIFEST.md`](SOURCE-MANIFEST.md) | Input URLs, record counts and checksums. | [Source manifest](SOURCE-MANIFEST.md) |
| [`standard-extensions.json`](standard-extensions.json) | The three locally curated, officially sourced standard entries. | [Source manifest](SOURCE-MANIFEST.md) |
| [`LICENSE`](LICENSE) | Dual MIT notice: catalogue data © Entropy Data; derived model © Mark McCalla. | [Licence](LICENSE) |

## Suggested reading paths

### I have a pipeline pattern and need the attached obligations

1. Open [`graph.html`](graph.html) and scope a pipeline type.
2. [Compliance mappings](docs/10-compliance-mappings.md)
3. [Design decisions](docs/08-design-decisions.md)

### I am completely new to knowledge modelling

1. [Glossary](docs/09-glossary.md)
2. [Ontology](docs/01-ontology.md)
3. [Taxonomy](docs/02-taxonomy.md)
4. [SHACL](docs/03-shacl.md)
5. [Instances](docs/04-instances.md)
6. [Design decisions](docs/08-design-decisions.md)

### I want to use the Neo4j projection

1. [Neo4j CSV projection](docs/05-neo4j-csv.md)
2. [Neo4j schema](docs/06-neo4j-schema.md)
3. [Loading and validation](docs/07-loading-and-validation.md)

### I need the schema and validation rules

1. [Glossary](docs/09-glossary.md)
2. [Ontology](docs/01-ontology.md)
3. [Taxonomy](docs/02-taxonomy.md)
4. [SHACL](docs/03-shacl.md)
5. [Instances](docs/04-instances.md)

## Counts and reconciliation

| Measure | Count |
|---|---:|
| Data Standard Landscape records | 84 |
| Upstream / locally extended standard records | 81 / 3 |
| Unique standard display names | 83 |
| Standard category memberships | 85 |
| Data Regulation Landscape records | 73 |
| Regulation categories | 19 |
| Regulation category memberships | 73 |
| Normalised jurisdiction memberships | 81 |
| Confirmed cross-landscape identity links | 2 pairs: ODRL and OPA |
| Official mapping assertions | 3 |
| Component implementation mappings | 29 |
| Component regulatory mappings | 33 |
| Neo4j nodes | 414 |
| Neo4j relationships | 963 |

Compound jurisdiction labels explain why 73 regulation entries produce 81 jurisdiction memberships. For example, `EU / Germany` becomes links to both European Union and Germany while the original text is preserved.

## Direct, normalised and modelled information

The `evidenceStatus` value distinguishes how a statement entered the graph:

- `DIRECT_OBSERVATION`: present in the supplied landscape data;
- `NORMALISED_FROM_SOURCE`: deterministically split or normalised from a source value;
- `IDENTITY_CONFIRMED`: a reviewed cross-landscape identity link;
- `OFFICIAL_SOURCE`: supported by a separately identified official document;
- `MODELLED_VOCABULARY`: terminology introduced by this model;
- `OFFICIAL_SOURCE_EXTENSION`: a local landscape extension grounded in official product documentation;
- `EDITORIAL_ASSESSMENT`: a locally curated judgement and tier rather than an upstream statement;
- `CURATED_DESIGN_MAPPING`: a design-time implementation option, not a claim of complete capability coverage.
- `CURATED_REGULATORY_RELEVANCE`: a curated component-to-requirement relevance assertion grounded in a primary source; not regulator endorsement and not proof of compliance.

## Namespace

Locally defined IRIs are minted for this derived model (not by Entropy Data) under:

```text
https://polymathic.co.uk/data-landscape/ontology/
https://polymathic.co.uk/data-landscape/taxonomy/
https://polymathic.co.uk/data-landscape/instance/
```

## Important limitations

- This package is not legal advice.
- A mapping is not proof that an organisation, system or processing activity complies.
- Status text may contain edition and applicability information but is not converted into legal lifecycle dates.
- Only mappings supported by the cited official sources are included.
- Source descriptions and editorial wording remain attributable to the upstream landscape.
- Historical snapshots require an explicit versioning extension.

## Attribution and responsible reuse

Catalogue data and publisher-authored wording are © Entropy Data, MIT, from Simon Harrer’s Data Landscape. The regulation sub-landscape was originally donated by Mark McCalla and has since been curated by Simon Harrer. This GitHub repository is Mark McCalla’s derived model, not a publication by Entropy Data. Retain [`ATTRIBUTION.md`](ATTRIBUTION.md), [`CITATION.bib`](CITATION.bib) and [`LICENSE`](LICENSE) when redistributing this package or a substantial part of its data.

## External standards and documentation

- [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)
- [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/)
- [Neo4j constraints](https://neo4j.com/docs/cypher-manual/current/constraints/)
- [NIST CSF Informative References](https://www.nist.gov/cyberframework/informative-references)
- [European Data Protection Board code-of-conduct register](https://www.edpb.europa.eu/registers/register-of-consistency-and-of-accountability-tools/codes-of-conduct_en)

## Contributor checks

The repository uses [pre-commit](https://pre-commit.com/) for hygiene, secret safety, cruft rejection, Turtle validation (`riot`), SHACL (`pyshacl`), and Neo4j CSV projection integrity. Install and enable it once:

```sh
python3 -m pip install pre-commit pyshacl
# Apache Jena riot must also be on PATH (see docs/07-loading-and-validation.md)
pre-commit install
```

Run every configured check against the complete repository before submitting a change:

```sh
pre-commit run --all-files
```

`graph.html` is excluded from text hygiene hooks (it is a generated ~800KB standalone artefact). Domain hooks map to the scripts under `scripts/check-*.py` and align with the [loading and validation guide](docs/07-loading-and-validation.md).
## Rebuild the standalone graph

[`graph.html`](graph.html) contains D3 and the complete CSV projection inline, so it opens locally without a web server or network connection. Rebuild it after changing either CSV file:

```sh
npm install
npm run build
npm test
```
