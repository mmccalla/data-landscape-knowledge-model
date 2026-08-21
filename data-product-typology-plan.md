---
name: thin product typology
overview: Add a thin data-product typology (personal-data posture plus industry vertical) with curated examples and a graph selector, without a product catalogue or compliance engine.
todos:
  - id: schema-vocabulary
    content: Add DataProduct class, PII posture and industry-vertical concepts, and properties linking products to standards and vertical-relevant regulations
    status: pending
  - id: shelfwarmers-instance
    content: Model shelf-warmers as retail + no PII, with sourced standard links and explicit non-links
    status: pending
  - id: second-contrast-instance
    content: Add one contrasting product (e.g. banking or health + PII) so vertical and PII selectors are meaningful
    status: pending
  - id: projection-and-graph
    content: Project products into CSV/graph; add product / vertical / PII selectors that do not replace pipeline type
    status: pending
  - id: docs-and-readme
    content: Document the typology; align README Data Products once the selector exists
    status: pending
  - id: hygiene-gate
    content: Tests for vocabulary, instances, and graph behaviour; npm test and pre-commit
    status: pending
isProject: false
---

# Thin product typology

> Status: historical — work landed on main (through 1.0.9 / 1.0.10). Not a living runbook.

## Overview

**Goal.** An architect can ask of a **data product**, not only a pipeline pattern: given personal-data posture and **industry vertical**, which standards and obligations are relevant, with sources — and see the gaps the shelf-warmers note already describes.

**Scope.** Minimal ontology + taxonomy, SHACL, a handful of curated product instances, Neo4j CSV projection, graph selectors beside pipeline type, docs and README alignment.

**Non-goals.** Full product catalogue, ODCS/ODPS import, live Entropy Data sync, automatic legal applicability for every regulation, Pages, or public flip.

## Approach

Keep **pipeline type** as “how you build”. Add an orthogonal product axis: **what you publish**.

Replace binary regulated / unregulated with **industry vertical**. Vertical is finer-grained and actionable: banking surfaces DORA / BCBS-shaped context; health surfaces HIPAA-shaped context; retail may show little sector law when the product is no-PII. “Unregulated” was a blunt label; vertical says *which regime*, not only *whether*.

```text
Pipeline type → modules → components → standards / regulatory context
Product → PII posture + industry vertical → linked standards / vertical-relevant regulations / explicit gaps
```

Do not overload existing regulation categories or jurisdictions as a fake vertical. Categories classify instruments; jurisdictions classify geography; **vertical classifies the product’s industry stance**.

## Acceptance / exit bar

- Ontology and taxonomy define `DataProduct` with:
  - personal-data posture (`PII` / `NO_PII`);
  - industry vertical as a controlled SKOS scheme (not free text).
- Starter verticals in v1: at least `banking`, `insurance`, `retail`, `health`, plus `cross-sector` (or `general`) for products that are not sector-specific. Further verticals can be added later without schema redesign.
- At least two product instances:
  - shelf-warmers: `NO_PII` + `retail` (or `cross-sector` if that fits better once authored);
  - one contrast: `PII` + `banking` *or* `health` (pick one in-slice), linked to existing component-regulatory paths so the graph shows sector-relevant obligation context.
- Explicit non-links stay honest (OpenLineage, Iceberg vs Snowflake).
- `graph.html` can scope by product and/or vertical and/or PII posture; pipeline selector remains.
- Counts stay in [docs/00-package-overview.md](docs/00-package-overview.md); README stays narrative.
- `npm test` and `pre-commit run --all-files` pass. Repo stays private.

## Frozen decisions

- **Two product dimensions in v1:** personal-data posture + industry vertical. No third axis yet (no separate regulated boolean, no AI high-risk tier, no jurisdiction on the product — jurisdiction already lives on regulation entries).
- **No `REGULATED` / `UNREGULATED` enum.** Sector stance replaces it. A retail no-PII product simply has sparse regulatory links; that is the signal.
- **Vertical → regulation links are curated**, not inferred by keyword from the whole landscape. Prefer reuse of existing `ComponentRegulatoryMapping` evidence where the product’s pipeline path already has it; add product-to-regulation relevance only when needed and sourced.
- **Curated examples, not sync.** Authored instances only.
- **Gaps are features.** Do not invent lineage or store links.
- **Namespace** `https://polymathic.co.uk/data-landscape/...`. Copyright / `assertedBy` Mark McCalla; Ltd affiliation only.
- **No compliance claims.** Vertical and PII posture are design-inspection aids, not legal determinations of applicability.

## Unknowns

| Unknown | Resolve in-slice |
|---|---|
| Shelf-warmers vertical: `retail` vs `cross-sector` | Prefer `retail` if the demo is a retail catalogue product; else `cross-sector`. |
| Contrast vertical: banking vs health | Prefer **banking** for UK/EU FS audience alignment (DORA / BCBS already in the model); health if HIPAA path is clearer in one sitting. |
| Graph UI: filter by vertical, by product, or both | Prefer **vertical** (+ optional product pick). PII can be a second filter or derived from the selected product. |
| Public sector as a v1 vertical | Include in the scheme only if an instance will use it; otherwise add the concept later. |

## Skills

Load when building: `kiss-principle`, `spec-driven-development`, `incremental-implementation`, `test-strategy`, `tdd-practice`. Load ontology / knowledge-graph modelling skills for the schema slice.

## Tasks / slices

### 1. Schema and vocabulary

**Files:** [`ontology.ttl`](ontology.ttl), [`taxonomy.ttl`](taxonomy.ttl), [`shapes.ttl`](shapes.ttl), short docs updates.

**Behaviour:**

- Add `DataProduct` as a first-class class (not a subclass of `DataPipelineComponent`).
- Add SKOS scheme **Industry vertical** with starter concepts: banking, insurance, retail, health, cross-sector (labels in UK English).
- Add personal-data posture concepts: `PII`, `NO_PII`.
- Properties: `hasPersonalDataPosture`, `inIndustryVertical` (cardinality: exactly one of each in v1 unless multi-vertical is forced — default **one primary vertical**).
- Optional links from product to standards and to regulation entries as curated relevance; reuse evidence-status vocabulary.
- SHACL: required id, label, both dimensions, evidenceStatus.

**Verify:** riot + pyshacl green.

**Stop:** no instances yet.

### 2. Shelf-warmers instance

**Files:** e.g. `product-instances.ttl`, projection inputs, overview artefact row.

**Behaviour:**

- Product: shelf-warmers; `NO_PII`; vertical `retail` or `cross-sector` (decide per Unknowns).
- Link ODPS, ODCS, dbt where already modelled.
- Do not invent OpenLineage or Iceberg links.
- `assertedBy` Mark McCalla.

**Verify:** validates; overview counts updated.

**Stop:** slice 3 before claiming a typology in the UI.

### 3. Contrast instance

**Files:** same product instance file.

**Behaviour:**

- Second product: `PII` + `banking` (or health); minimal curated links into existing regulatory context (e.g. secure read / GDPR and, for banking, DORA-shaped component mappings already in the model).
- Clearly labelled as curated example, not a client artefact.

**Verify:** products differ on both PII and vertical in data.

**Stop:** projection/UI next, or combine with slice 4 if cheaper.

### 4. Projection and graph selector

**Files:** CSV projection, [`src/graph.template.html`](src/graph.template.html), tests, optional README still.

**Behaviour:**

- Project product nodes, posture, vertical, and links.
- Selectors: industry vertical and/or product; keep pipeline type.
- Scoping: selecting banking shows banking product(s) and their linked standards/regulations; selecting retail shows shelf-warmers and its thinner regulatory neighbourhood.
- Empty-state copy mentions pipeline and product filters.

**Verify:** tests that retail/no-PII and banking/PII scopes differ in visible regulatory mapping nodes.

**Stop:** local `graph.html` only.

### 5. Docs and README

**Files:** [`README.md`](README.md), [`docs/00-package-overview.md`](docs/00-package-overview.md), design note if needed.

**Behaviour:**

- README Data Products: how to open the product/vertical-scoped view + shelf-warmers findings.
- Overview: artefact list, product counts, new evidence or vocabulary notes.
- Limitations: vertical and PII are curated inspection aids, not legal sector classification.

**Verify:** narrative matches graph.

### 6. Hygiene gate

```sh
npm test
pre-commit run --all-files
gh repo view mmccalla/data-landscape-knowledge-model --json isPrivate,visibility
```

Stay private. Tag only on explicit request.

## Out of scope

- Live sync from Entropy Data / ODCS
- Product marketplace metadata, SLAs, pricing
- Inferring vertical from product name or auto-tagging all 73 regulations per vertical
- Replacing pipeline patterns with products
- Public visibility, Pages, social posts
