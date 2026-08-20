# Data Landscape knowledge model

Inspired by [Dr Simon Harrer](https://www.data-landscape.com/)’s Data Landscape, I wanted a way to join the open-standards map to the regulation map, so an architect can ask of a real pipeline which standards apply and which UK and EU obligations are relevant, with sources. I originally donated the regulation sub-landscape; Simon has since curated it. The catalogues remain his, and Entropy Data’s, under the MIT licence. This repository is my derived model of those catalogues, prepared with Enterprise Solutions Consulting Ltd.

**Licence:** catalogue data © Entropy Data, MIT; transformation by Mark McCalla. Retain [LICENSE](LICENSE) and [ATTRIBUTION.md](ATTRIBUTION.md) if you redistribute the package.

## Data Pipelines

An architect choosing how to ingest data — for example CDC of EU personal data in a bank — still too often picks a tool, names a standard in a slide, and discovers the regulation later. In 2026 the same pipelines may sit under GDPR, DORA, NIS2 and the AI Act. This model records those links so they can be inspected rather than reconstructed from slides. The catalogues remain the public reference: [data-landscape.com](https://www.data-landscape.com/) and the [regulation map](https://www.data-landscape.com/regulation.html). What this package adds is a queryable path through them: ingestion pattern → component → standard and regulatory context, each statement carrying an evidence grade.

Open [`graph.html`](graph.html) in a browser as a local file. No server is required. Choose a **Data pipeline type** to scope the view. The figure below is Batch file ingestion.

![Batch file ingestion pattern scoped to related modules, components, and regulatory context](docs/images/pipeline-graph.png)

## Data Products

I ran Entropy Data’s shelf-warmers demo through the model to see what a real product looks like on that path. The product ties cleanly to the Open Data Product Standard (ODPS), the Open Data Contract Standard (ODCS) and dbt. OpenLineage is in the landscape, but it is not linked to a pipeline component, so lineage does not connect. Store and marketplace metadata do not connect either: the graph’s options are Iceberg and Iceberg Catalogue, and this product is a Snowflake table published in Entropy Data. The regulation entries do not apply; the product is marked no PII and low risk.

The package details and counts are in the [package overview](docs/00-package-overview.md). How to run the checks is in [Contributors](docs/contributors.md). How to rebuild [`graph.html`](graph.html) is in [Rebuild the standalone graph](docs/rebuild-graph.md).

## Important limitations

- This package is not legal advice.
- A mapping is not proof that an organisation, system or processing activity complies.
- Status text may contain edition and applicability information but is not converted into legal lifecycle dates.
- Only mappings supported by the cited official sources are included.
- Source descriptions and editorial wording remain attributable to the upstream landscape.
- Historical snapshots require an explicit versioning extension.

## Attribution and responsible reuse

Catalogue data and publisher-authored wording are © Entropy Data, MIT, from Simon Harrer’s Data Landscape. The regulation sub-landscape was originally donated by Mark McCalla and has since been curated by Simon Harrer. This GitHub repository is Mark McCalla’s derived model. Retain [`ATTRIBUTION.md`](ATTRIBUTION.md), [`CITATION.bib`](CITATION.bib) and [`LICENSE`](LICENSE) when redistributing this package or a substantial part of its data.

## External standards and documentation

- [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)
- [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/)
- [Neo4j constraints](https://neo4j.com/docs/cypher-manual/current/constraints/)
- [NIST CSF Informative References](https://www.nist.gov/cyberframework/informative-references)
- [European Data Protection Board code-of-conduct register](https://www.edpb.europa.eu/registers/register-of-consistency-and-of-accountability-tools/codes-of-conduct_en)
