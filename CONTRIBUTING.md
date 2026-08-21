# Contributing

Thank you for interest in improving this package. It is a derived model over Entropy Data’s Data Landscape catalogues (MIT), with transformation and curated mappings by Mark McCalla.

## Before you start

1. Read [`README.md`](README.md), [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`LICENSE`](LICENSE).
2. Keep compliance language as **design prompts**, never as legal determinations of applicability.
3. Do not commit working plans or agent handoffs (`HANDOFF-*.md`, `*-plan.md`).

## Local checks

```sh
npm install
npm test
pre-commit run --all-files   # requires riot (Apache Jena) and pyshacl on PATH
```

Rebuild the standalone graph after CSV changes:

```sh
npm run build
```

## Pull requests

- Prefer small, reviewable changes with a clear rationale.
- Update living docs under `docs/` when counts, shapes or behaviours change.
- Retain dual MIT notices and attribution when redistributing data.
- CI runs `npm test` on pull requests to `main`.

## Authorship boundary

Catalogue wording and publisher assessments remain attributable to Entropy Data / Simon Harrer. Ontology structure, SHACL, curated component and product mappings, Neo4j projection and this repository’s documentation are Mark McCalla’s derived work.
