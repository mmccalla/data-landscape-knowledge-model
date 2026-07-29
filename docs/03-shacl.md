# SHACL walkthrough

[← Taxonomy](02-taxonomy.md) · [README](../README.md) · [Next: Instances →](04-instances.md)

## What is SHACL?

SHACL is the W3C Shapes Constraint Language for validating RDF. The ontology explains meaning; [`shapes.ttl`](../shapes.ttl) defines what a publishable record must contain.

## Shapes in this package

### LandscapeEntryShape

Every landscape entry requires one identifier, full name, release year, governance statement, status statement and governance type, plus a preferred label.

### DataStandardLandscapeEntryShape

Requires at least one Data Standard category and exactly one Boolean `isNiche`. `whyAStandard` remains optional because the source does not supply it for every entry.

### DataRegulationLandscapeEntryShape

Requires at least one regulation category, description, reference link and normalised jurisdiction, plus exactly one preserved source jurisdiction label.

It deliberately does not require a judgement or tier.

### LandscapeAssessmentShape

Requires exactly one assessed Data Standard entry, one judgement, one reason and at least one tier.

### ComplianceMappingShape

Requires exactly one source entry, target entry, mapping relation, authority type, asserting body, official source and mapping status. A SPARQL constraint rejects a self-mapping.

### ComponentImplementationMappingShape

Requires one component type, one implementation option, a rationale and at least one authoritative source.

### Attestation shapes

Require traceable IDs for the attestation, actor, action, risk, control and evidence. The attestation also requires pipeline, module and component IDs plus a timestamp. Risks must reference actions, controls must reference mitigated risks, and evidence must reference a control and record a successful pass. Required and applied control flags must both be true.

### ConceptLabelShape

Requires every SKOS concept to have a preferred label and exactly one concept scheme.

## Reading a rule

```turtle
sh:property [
    sh:path dl:firstReleaseYear ;
    sh:datatype xsd:gYear ;
    sh:minCount 1 ;
    sh:maxCount 1
] .
```

This means there must be exactly one `firstReleaseYear`, represented as an XML Schema year.

## Why SHACL rather than only OWL?

RDF and OWL use open-world semantics: absence can mean “unknown”. Publication validation needs a closed quality contract that reports missing and malformed values. SHACL fulfils that role without changing the ontology’s meaning.

## Expected result

Validating ontology, taxonomy and all four instance files should report:

```text
Conforms: True
```

An invalid fixture should report `Conforms: False`. See [Loading and validation](07-loading-and-validation.md).
