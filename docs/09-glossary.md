# Glossary

[← Design decisions](08-design-decisions.md) · [README](../README.md) · [Next: Compliance mappings →](10-compliance-mappings.md)

## Assessment

A contextual editorial opinion containing a judgement, reason and one or more tiers.

## Attestation

A timestamped, traceable record for one pipeline component execution, linking an actor and identified actions to risks, applied controls and successful control evidence.

## Data ingestion pattern, module and component

A pattern describes a reusable ingestion approach. It is composed of the five module types, and each module is composed of its defined functional component types.

## Cardinality

The permitted number of values. `1..*` means one or more; `0..1` means optional and at most one.

## Class and instance

A class is a type, such as `DataRegulationLandscapeEntry`. GDPR is an instance of that class.

## Compliance mapping

An attributable assertion connecting two entries, with its own relation, authority, version, status and source. It is not proof of an organisation's compliance.

## Concept and concept scheme

A SKOS concept is an approved classification idea. A concept scheme is a named collection of such concepts.

## Controlled vocabulary

An approved set of values used consistently instead of arbitrary strings.

## Cypher

Neo4j's graph query language.

## Datatype property and object property

A datatype property links a resource to a literal value. An object property links one resource to another resource.

## Domain and range

Semantic declarations describing the expected subject and object of an RDF property.

## Evidence status

A marker identifying whether a statement was directly observed, normalised, identity-reviewed, sourced from an official document or introduced as modelling vocabulary.

## Graph, node and relationship

A graph contains identifiable things and named connections. Neo4j calls the things nodes and the connections relationships.

## IRI

An Internationalised Resource Identifier: RDF's globally scoped identifier for a resource or vocabulary term.

## Label

In RDF/SKOS, human-readable text. In Neo4j, a node type such as `LandscapeEntry`.

## Labelled property graph

Neo4j's graph model, in which nodes and relationships carry labels or types and key-value properties.

## Literal

Text, a number, a Boolean, a date or another value rather than a link to a resource.

## Namespace and prefix

A namespace provides the stable IRI base. A prefix such as `dl:` is a readable abbreviation for it.

## Ontology

A formal definition of classes, properties, relationships and meanings in a domain.

## OWL, RDF and RDFS

W3C technologies for graph data and semantic modelling. RDF supplies the graph statements; RDFS and OWL add schema and logical meaning.

## Schema first

Defining meaning, controlled terms and validation rules before loading actual records.

## SHACL and shape

SHACL validates RDF. A shape is a collection of rules applied to selected nodes.

## SKOS and taxonomy

SKOS is the W3C model used here for controlled taxonomies: organised classification concepts and broader/narrower relationships.

## Turtle

A human-readable RDF syntax normally stored in `.ttl` files.

## Uniqueness constraint

A database rule preventing two nodes under a constrained label from sharing the same key.
