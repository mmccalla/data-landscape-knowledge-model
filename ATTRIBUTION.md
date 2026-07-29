# Attribution and reuse notice

## Upstream works

The instance data, controlled values and publisher-authored editorial text are derived from:

> Harrer, S. (2026). *Data Landscape: Open Standards for Modern Data Architecture*. Entropy Data. https://www.data-landscape.com/

> Harrer, S. (2026). *Data Landscape for Regulation: Laws and Compliance Frameworks for Data*. Entropy Data. https://www.data-landscape.com/regulation.html

The regulation page states that the original version of that sub-landscape was donated by Mark McCalla and has since been curated by Simon Harrer.

Machine-readable sources:

- https://www.data-landscape.com/standards.json
- https://www.data-landscape.com/regulation.json

The supplied source pages and datasets state an MIT licence. The licence and upstream copyright notice are reproduced in [`LICENSE`](LICENSE):

> Copyright (c) 2026 Entropy Data

## What is reproduced or transformed

Source-derived values include identifiers, names, full names, categories, governance and status statements, judgements and reasons, tiers, jurisdictions, descriptions, reference links, first-release years, governance classifications and available “Why a standard” explanations.

These values remain attributable to the Data Landscape. Their inclusion is not independent verification or endorsement by the author of this derived model.

Airflow, Prefect and Temporal are local extensions and are not attributed to the upstream Data Landscape dataset. Their factual descriptions are grounded in their official documentation; their judgement, reason and tier are editorial decisions in this model.

## Mapping sources

The three delivered compliance mappings are supported by separately identified official sources:

- Cloud Security Alliance, *Cloud Controls Matrix*: https://cloudsecurityalliance.org/research/cloud-controls-matrix
- Belgian Data Protection Authority, approval of the *EU Cloud Code of Conduct*: https://www.autoriteprotectiondonnees.be/index.php/lautorite-de-protection-des-donnees-approuve-son-premier-code-de-conduite-europeen
- GDPR official text, including Article 40 codes of conduct and Article 42 certification: https://eur-lex.europa.eu/eli/reg/2016/679/oj

The mappings are represented as bounded assertions with authority and source. They are not legal advice or proof of operational compliance.

Component implementation mappings cite the official documentation recorded on each mapped entry. They are candidate design options, not claims of complete feature coverage or endorsement by the upstream publisher.

## Original transformation work

The ontology structure, SKOS schemes, SHACL constraints, normalisation rules, compliance-mapping representation, RDF-to-Neo4j projection, CSVs, Cypher schema and explanatory documentation are transformation work built around the attributed source data. They must not be represented as authored by the upstream project.

## Responsible reuse

When redistributing this package or a substantial portion of its source-derived data, retain:

- this file;
- [`CITATION.bib`](CITATION.bib);
- [`LICENSE`](LICENSE).

Regulatory and framework information changes over time. Check current official documents before relying on any entry or mapping.

## Visualisation dependency

[`graph.html`](graph.html) embeds D3.js 7.9.0 for offline use. D3 is copyright 2010–2023 Mike Bostock and distributed under the ISC licence. The required licence notice is retained inside the standalone HTML file; the canonical project and licence are available at <https://github.com/d3/d3>.
