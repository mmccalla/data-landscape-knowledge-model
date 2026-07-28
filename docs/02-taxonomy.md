# Taxonomy walkthrough

[← Ontology](01-ontology.md) · [README](../README.md) · [Next: SHACL →](03-shacl.md)

## What is a taxonomy?

A taxonomy is an organised set of approved classification concepts. [`taxonomy.ttl`](../taxonomy.ttl) uses W3C SKOS so each value has a stable IRI, preferred label, containing scheme and—where relevant—a broader concept.

Using a relationship to a concept avoids uncontrolled variations such as `EU`, `E.U.` and `European Union` becoming unrelated strings.

## Concept schemes

The package contains separate schemes for:

- Data Standard Landscape categories;
- Data Regulation Landscape categories;
- judgements;
- tiers;
- governance types;
- jurisdictions;
- mapping relations;
- mapping authority types.

The two category schemes remain separate because “Policies” in the standards landscape and “Usage Policy & Rights” in the regulation landscape serve different classification systems.

## Data Standard Landscape categories

Six sections organise nineteen categories:

```text
Definition       Storage          Movement
Transformation   Discovery        Operations
```

For example, Contracts is broader-linked to Definition and Messaging to Movement.

## Data Regulation Landscape categories

```text
Regulation — what the law requires
├── EU Data & AI Acts
├── EU Resilience & Security Acts
└── Global & Sector Regulation

Governance & Management
├── Data Management Frameworks
├── Metadata & Quality
└── Usage Policy & Rights

Security & Risk
├── Management Systems
├── Security Controls
├── Privacy
└── Threat Intelligence

Identity & Agents
├── Identity & Access
├── Agent Identity & Trust
└── Agent Interaction

AI & Applications
├── AI Governance
└── Application & API Security

Assurance & Exchange
├── Cloud & Certification
├── Audit & Attestation
├── Software Supply Chain
└── Data Spaces & Sovereignty
```

## Governance types

The shared scheme normalises the source field named `standardization`:

| Source code | Preferred label |
|---|---|
| `law` | Law or regulation |
| `formal-standard` | Formal standard |
| `foundation` | Foundation |
| `community` | Community |
| `vendor-led` | Vendor led |

The class means the principal authority or stewardship arrangement. Only values present in a particular source appear on its entries.

## Jurisdictions

The observed labels are `EU`, `Global`, `US`, `EU / Germany` and `US / Global`. Compound labels become multiple relationships while the exact source text is retained.

`Global` is a scope indicator, not a geographic parent of every jurisdiction.

## Mapping vocabulary

Mapping relations include cautious terms such as Maps to, Supports evidence for, Partially equivalent and No coverage. Authority types distinguish regulator-issued, standards-body, source-author, bilateral, third-party and community assertions.

The vocabulary is broader than the three delivered mapping instances so future official mappings can be represented consistently.

## Observed versus modelled

Category labels and source classifications are direct observations. Splitting compound jurisdictions is deterministic normalisation. Mapping-relation and authority vocabularies are modelled structure. `evidenceStatus` preserves those distinctions.
