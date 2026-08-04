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
