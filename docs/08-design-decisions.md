# Design decisions

[← Loading](07-loading-and-validation.md) · [README](../README.md) · [Next: Glossary →](09-glossary.md)

## Use landscape-specific subclasses

**Decision:** `LandscapeEntry` has `DataStandardLandscapeEntry` and `DataRegulationLandscapeEntry` subclasses.

**Reason:** The names state which curated landscape supplied the record without falsely declaring every entry intrinsically a formal standard or law.

## Keep assessments separate

Judgement, reason and tier belong to `LandscapeAssessment`, not the standard entry. They are contextual editorial opinions and do not apply to the regulation landscape.

## Use GovernanceType

The source field `standardization` is represented as `hasGovernanceType`. Its definition covers the principal authority or stewardship arrangement. This is clearer across laws, standards, foundations and communities than `InstrumentKind`.

## Keep category schemes separate

The two landscapes organise different questions. Their categories therefore use separate SKOS schemes and Neo4j relationships, preventing accidental cross-classification.

## Preserve and normalise jurisdiction

The exact source label is retained while compound values become multiple controlled relationships. `Global` is not treated as a geographic parent.

## Preserve separate ODRL and OPA entries

The landscapes provide different contextual statements about the same underlying resources. Each landscape entry remains separate and the confirmed pairs are linked with `describesSameResourceAs`. This avoids data loss and avoids the very strong semantics of `owl:sameAs`.

## Represent mappings as nodes

Mappings have authority, version, status and supporting documentation. A `ComplianceMapping` node can carry that context and later connect individual controls or provisions.

## Avoid unqualified compliance predicates

Frameworks do not themselves comply with laws, and adopting a standard does not necessarily satisfy legislation. The model uses scoped terms such as Maps to and Supports evidence for. Operational `COMPLIES_WITH` claims belong to assessed organisations, systems or activities outside this catalogue model.

## Use only official mapping evidence

The delivered mapping layer includes only three reviewed examples from official publishers or regulators. A page merely hosting a community mapping is not automatically treated as endorsing its correctness; authority type remains explicit.

## Separate pattern structure, implementation options and runtime evidence

Patterns, modules and components define reusable structure. `ComponentImplementationMapping` records candidate technologies separately. `Attestation` records what a concrete pipeline execution actually did and proved. This prevents design guidance from being mistaken for runtime compliance evidence.

`ComponentRegulatoryMapping` is a third, separate concern: it identifies why a component is relevant to a cited requirement. The mapping is curated interpretation grounded in a primary source, not an assertion by the regulator and not evidence that a pipeline complies. Incomplete component coverage is intentional; blank components are not treated as defects.

## Lineage emission under Orchestrate

**Decision:** Operational lineage hang-point is a distinct `LineageEmission` component under **Orchestrate**, with OpenLineage as its primary implementation option. It is not folded into Store `MetadataRegistration` (catalog/registry-oriented; Iceberg Catalog CIM remains there).

**Reason:** OpenLineage job/run/dataset events are emitted during pipeline execution. Keeping lineage under Orchestrate avoids overloading metadata registration and avoids claiming that Airflow “is” OpenLineage: Airflow remains an orchestration CIM; it may emit OpenLineage events via a provider.

**Retail Stock honesty:** Where a curated product deliberately does not adopt OpenLineage or Iceberg, the non-link is a `ProductStandardRelevance` with `hasMappingRelation` `no-coverage`, not prose alone and not a fake Snowflake landscape entry.

## CRM-aware product scope is a view rule

**Decision:** When a product, vertical or posture filter is active, `productScopeFor` expands from considered standards to reachable `ComponentImplementationMapping` nodes, their mapped component types, and `ComponentRegulatoryMapping` regulations. This expansion is **UI / selection only**.

**Reason:** Component regulatory evidence is already paid for in the model. Surfacing it beside a product answers obligation-neighbourhood questions without inventing product→regulation or product→CRM triples that would look like applicability. Explicit `no-coverage` product-standard mappings remain visible but do not drive the CIM/CRM walk.

## ADOPT catalogue-only remainder (Batch B)

**Decision:** After Batch A CIMs (Kafka→source connectivity; Spark→workload execution; Parquet→store/write; JSON Schema, OpenAPI and Avro→data contract definition), the remaining ADOPT standards stay catalogue-only until a fitting component exists. Inclusion in the landscape is not a requirement to invent a hang-point.

**Batch B IDs (intentional incompleteness):** `a2a`, `amqp`, `arrow`, `asyncapi`, `avro-schema`, `beam`, `csv`, `dpds`, `graphql`, `great-expectations`, `grpc`, `ibis`, `json`, `mcp`, `mdx`, `mqtt`, `oors`, `orc`, `protobuf`, `quack`, `sql`, `sql-ddl`, `unity-catalog`, `xml`, `xmla`, `yaml`. OpenTelemetry and quality tooling remain deferred with the optional P2 observability/quality slice — do not dump them onto `metadata-registration`.

## ISO 27001 / EU AI Act / NIST coherence

**Decision:** ISO/IEC 27001 now has a sourced CRM from secure read access (Annex A.5.15), so the insurance-claims product consideration is no longer floating. EU AI Act and NIST SP 800-53 remain primarily CRM-backed (validation, secure access, failure isolation, and related components). They are not hung on every product; product selectors surface them via the CRM-aware view when a considered standard reaches those components.

## Design jurisdiction is a prompt, not applicability

**Decision:** Optional multi-valued `hasDesignJurisdiction` on `DataProduct` points readers at regulation `APPLIES_IN` neighbourhoods. It does **not** reuse regulation applicability semantics and does not assert that any instrument applies to the product or organisation. UK is modelled as a jurisdiction concept so UK/EU care-home examples can be prompted without implying US HIPAA shape; US-prompted health products keep HIPAA considerations.

## Vertical × posture matrix cells left intentionally empty

**Decision:** Prefer declare over inventing weak products. The curated typology leaves these cells empty on purpose:

- health × NO_PII
- insurance × NO_PII
- telecoms × NO_PII
- public-sector × PII

Filled cells remain the twelve curated products; absence is not a silent hole.

## Catalogue inclusion is not a mapping obligation (P2 debt)

**Decision:** Most landscape standards and regulations remain catalogue-only. Inclusion answers “what exists in the landscape,” not “must hang on a component or product.” Crosswalks stay official-evidence-only (`OFFICIAL_SOURCE`). Quality and observability hang-points (OpenTelemetry, Great Expectations, and similar) stay deferred until a dedicated component slice — do not dump them onto `metadata-registration`. Negative product gaps touched in P0/P1 use reified `no-coverage` where earned; remaining prose gaps are backlog. Capital-markets-as-banking coarseness and Snowflake-as-prose (not a fake landscape standard) are owned notes, not silent defects.

## Keep extensions distinct from upstream observations

Airflow, Prefect and Temporal are source-backed local extensions. Their entries use `OFFICIAL_SOURCE_EXTENSION`; their judgement, reason and tier use `EDITORIAL_ASSESSMENT`. This avoids attributing local decisions to the upstream landscape publisher.

## Preserve source omissions

Optional fields remain optional. Missing rationales are not completed from descriptions or third-party prose. Status statements remain text because they mix edition, publication and applicability information.

## Bias and reasoning review

- **Symmetry bias:** regulation records are not forced to have standard judgements or tiers.
- **Authority bias:** landscape inclusion and official hosting are not treated as proof of legal sufficiency.
- **Confirmation bias:** counts are reconciled independently by source ID, category and jurisdiction membership.
- **False precision:** broad document-level mappings are not converted into clause-level equivalence.
- **Sycophancy check:** requested strong relationship ideas were retained only in safer, evidence-bounded forms.
