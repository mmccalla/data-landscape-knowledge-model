# Instance walkthrough

[← SHACL](03-shacl.md) · [README](../README.md) · [Next: Neo4j CSV →](05-neo4j-csv.md)

## What is an instance?

A class is a type; an instance is a particular record of that type.

```text
Class:    DataStandardLandscapeEntry
Instance: OpenAPI

Class:    DataRegulationLandscapeEntry
Instance: GDPR
```

## Four instance files

| File | Contents |
|---|---|
| [`instances.ttl`](../instances.ttl) | 84 standard-landscape entries and 84 assessments. |
| [`regulation-instances.ttl`](../regulation-instances.ttl) | 73 regulation-landscape entries. |
| [`mapping-instances.ttl`](../mapping-instances.ttl) | Three officially supported mapping assertions. |
| [`component-mappings.ttl`](../component-mappings.ttl) | 29 curated component-to-landscape implementation options. |

They are separate so each domain can be refreshed without pretending that all statements came from the same source or have the same semantics.

Airflow, Prefect and Temporal are local, officially sourced extensions rather than upstream landscape observations. Their assessments are explicitly editorial. Component mappings are candidate design options, not proof that a tool completely implements a component in every pipeline context.

## Standard example

```turtle
inst:standard-openapi
    a dl:LandscapeEntry, dl:DataStandardLandscapeEntry ;
    dl:identifier "openapi" ;
    skos:prefLabel "OpenAPI"@en-GB ;
    dl:inStandardCategory tax:standard-category-contracts .
```

Its separate assessment carries Adopt, its reason and its tier.

## Regulation example

```turtle
inst:regulation-gdpr
    a dl:LandscapeEntry, dl:DataRegulationLandscapeEntry ;
    dl:inRegulationCategory tax:regulation-category-eu-data-and-ai-acts ;
    dl:sourceJurisdictionLabel "EU" ;
    dl:appliesIn tax:jurisdiction-eu .
```

Descriptions and reference URLs are included because they are important to understanding and checking regulation-landscape entries.

## Identity cases

- The two source IDs `odps` and `odpspec` remain separate even though both display “ODPS”.
- Lance is one standard entry with two standard-category memberships.
- ODRL and OPA each have one entry per landscape. Confirmed `describesSameResourceAs` links connect the pairs while preserving their source-specific statements.

## Jurisdiction normalisation

An entry with source text `EU / Germany` receives two `appliesIn` relationships. The source text remains available in `sourceJurisdictionLabel`, so the transformation is reversible and auditable.

## What is not included

- logos and other purely visual assets;
- guessed legal obligations;
- mappings based only on similar wording;
- operational claims that an organisation complies.

Source wording remains attributed under the upstream MIT licence. See [`ATTRIBUTION.md`](../ATTRIBUTION.md).
