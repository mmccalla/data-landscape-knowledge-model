# Handoff: thin product typology

Use this with a **fresh agent context**. Do not re-litigate authorship, namespaces, or shopfront decisions unless the plan conflicts with the repo.

## Repo state (after Docs Updates / tag 1.0.8)

- **Remote:** `mmccalla/data-landscape-knowledge-model` (must stay **private**)
- **Default branch:** `main`
- **Plan to execute:** [`data-product-typology-plan.md`](data-product-typology-plan.md) (source of truth for slices and exit bar)
- **Namespace:** `https://polymathic.co.uk/data-landscape/{ontology,taxonomy,instance}/`
- **Copyright:** catalogue data © Entropy Data; derived model © Mark McCalla. Ltd = affiliation only, not on `LICENSE` or `assertedBy`
- **Authorship tests:** `tests/test_authorship_consistency.py`, `tests/test_namespace_consistency.py`

## What the docs work already did

- README is a short first-person narrative: pipelines (graph + still) then data products (shelf-warmers worked example).
- Package inventory, counts, model diagram live in [`docs/00-package-overview.md`](docs/00-package-overview.md).
- Contributor checks → [`docs/contributors.md`](docs/contributors.md); rebuild graph → [`docs/rebuild-graph.md`](docs/rebuild-graph.md).
- Counts are **not** on the README.

## Product typology — decisions locked in the plan

| Axis | v1 values |
|---|---|
| Personal data posture | `PII` / `NO_PII` |
| Industry vertical | `banking`, `insurance`, `retail`, `health`, `cross-sector` |

- **No** binary `REGULATED` / `UNREGULATED`.
- Pipeline type stays; product/vertical/PII selectors are orthogonal.
- Curated instances only (no live Entropy sync). Gaps (OpenLineage, Iceberg vs Snowflake) stay honest.
- Suggested examples: shelf-warmers = retail + `NO_PII`; contrast = banking + `PII` (UK/EU FS audience).

## How to execute

1. Read [`data-product-typology-plan.md`](data-product-typology-plan.md) end to end.
2. Work **one slice at a time** (schema → shelf-warmers → contrast → projection/graph → docs → hygiene).
3. Load skills named in the plan when building.
4. Prefer TDD for graph/CSV behaviour.
5. Before claiming done: `npm test`, `pre-commit run --all-files`, confirm repo still private.
6. Do **not** flip public, enable Pages, or tag unless Mark asks.

## Open choices to resolve in-slice (see plan Unknowns)

- Shelf-warmers vertical: `retail` vs `cross-sector`
- Contrast vertical: banking (preferred) vs health
- Graph UI: filter by vertical and/or product; PII as filter or derived from product

## Suggested first message to the new agent

> Execute [`data-product-typology-plan.md`](data-product-typology-plan.md) on a new branch from `main`. Follow slices in order. Repo must stay private. Read [`HANDOFF-product-typology.md`](HANDOFF-product-typology.md) for context already decided.
