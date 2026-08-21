# Handoff: gap remediation

> Status: historical — work landed on main (through 1.0.9 / 1.0.10). Not a living runbook.

Use this with a **fresh agent context**. Do not re-litigate authorship, namespaces, shopfront, or public/Pages decisions unless the plan conflicts with the repo.

## Repo state

- **Remote:** `mmccalla/data-landscape-knowledge-model` (must stay **private**)
- **Default branch:** `main`
- **Working branch (typology already in progress):** `Data-Product-Typology` — product typology is largely implemented here; expect uncommitted or unpushed typology + plan files. Prefer continue on this branch (or branch from it), not a blind reset to `main`, unless Mark says otherwise.
- **Plan to execute:** [`gap-remediation-plan.md`](gap-remediation-plan.md) — **source of truth** for slices, exit bar, and locks
- **Prior plan (done / superseded in places):** [`data-product-typology-plan.md`](data-product-typology-plan.md) — do not re-run; read only for history
- **Prior handoff:** [`HANDOFF-product-typology.md`](HANDOFF-product-typology.md)
- **Namespace:** `https://polymathic.co.uk/data-landscape/{ontology,taxonomy,instance}/`
- **Copyright:** catalogue data © Entropy Data; derived model © Mark McCalla. Ltd = affiliation only, not on `LICENSE` or `assertedBy`
- **Authorship / namespace tests:** `tests/test_authorship_consistency.py`, `tests/test_namespace_consistency.py`

## What is already true in the model

- Thin **data-product typology** exists: `DataProduct`, personal-data posture (`PII` / `NO_PII`), industry verticals (`banking`, `insurance`, `retail`, `health`, `public-sector`, `telecoms` — **no** `cross-sector`).
- Reified product mappings: `ProductStandardRelevance` / `ProductRegulatoryRelevance` (not bare `usesStandard` / `relevantRegulation`).
- ~12 curated products in [`product-instances.ttl`](product-instances.ttl); graph selectors for product / vertical / posture beside pipeline type.
- OpenLineage is an **ADOPT** landscape standard but (as of the gap review) had **no** pipeline component CIM and **no** product consideration — that is P0 of this plan.
- Product dropdown lists all products; vertical/posture scope the graph neighbourhood.

## Why this remediation exists (gap register summary)

**P0 — competence / honesty**

1. No lineage capability (component or explicit gap) despite ADOPT OpenLineage and Airflow/dbt CIMs.
2. Product CQ answers stereotyped (ODPS+ODCS); weak vertical differentiation.
3. Product scope ignores CRM neighbourhood — under-answers obligations vs existing component evidence.

**P1 — coherence** (ADOPT orphans, bare CRMs, ISO 27001 / EU AI Act / NIST 800-53 mismatch, design jurisdiction, ODPS vs odpspec, empty matrix cells).

**P2 — catalogue debt** (declare by default; optional thin follow-ons).

A deeper review (modelling + fallacy/bias + external refs) is summarised in conversation history; **do not re-open the full scan unless implementing a slice needs evidence**. Trust [`gap-remediation-plan.md`](gap-remediation-plan.md).

## Pre-implementation locks (already decided — do not reopen)

| Lock | Decision |
|---|---|
| CRM-aware product scope | **`productScopeFor` / UI view only.** No new product→regulation or product→CRM triples from the walk. ADR in [`docs/08-design-decisions.md`](docs/08-design-decisions.md) when slice 3 lands. |
| Lineage module | **Orchestrate** (OpenLineage job/run emission). Not Govern unless Mark explicitly revisits. |
| Lineage hang-point | New **lineage-emission** component — do **not** overload `metadata-registration`. |
| Airflow / OpenLineage | Airflow remains orchestration CIM; OpenLineage is separate CIM. Do not claim Airflow “is” OpenLineage. |
| Compliance | Design prompts only — never applicability / “must comply”. |
| Repo | Stay **private**; no Pages, public flip, or tags unless Mark asks. |

## How to execute

1. Read [`gap-remediation-plan.md`](gap-remediation-plan.md) **end to end** (including pre-implementation locks and slice order).
2. Confirm branch/worktree state (`git status`, current branch). Do not discard typology work.
3. Work **one slice at a time** in plan order:  
   `1 lineage → 3 CRM-aware scope (or with 2) → 2 product differentiation → 5 ↔ 4 → 6 → 7 declare P2 → 8 hygiene`
4. Load skills named in the plan: ontology/KG modelling, logical-fallacy-review, cognitive-bias-review, kiss, incremental-implementation, tdd, spec-driven-development.
5. Prefer TDD for `productScopeFor` / graph / CSV behaviour.
6. CSV projection: keep in sync with TTL (repo has no single official projector — follow existing patterns; fix EOL via pre-commit).
7. Before claiming a slice or the whole remediation done: `npm test`, `pre-commit run --all-files`, `gh repo view --json isPrivate,visibility`.
8. **Do not commit or push** unless Mark explicitly asks.
9. Do **not** flip public, enable Pages, or tag unless Mark asks.

## Progress

- **Slices 1–3, 2 (P0 done, uncommitted):** lineage emission + OpenLineage CIM; CRM-aware `productScopeFor` (view-only); per-vertical product differentiation.
- **Slices 5 ↔ 4 (P1 done, uncommitted):** CRMs for bare components + ISO 27001 CRM; Batch A ADOPT CIMs; Batch B catalogue-only declaration; EU AI Act / NIST remain CRM-surfaced.
- **Slice 6 (done, uncommitted):** optional `hasDesignJurisdiction` (+ UK concept); ODPS vs odpspec contrast on public-sector; empty matrix cells declared intentionally empty.
- **Slice 7 (done, uncommitted):** P2 catalogue debt declared in design-decisions + package overview.
- **Slice 8 (done, uncommitted):** package counts **499 / 1136**; `npm test` and `pre-commit run --all-files` pass; repo **PRIVATE**. Do not commit unless Mark asks.

## In-slice discipline (from plan review)

- Prefer **intentionally empty** matrix cells over inventing weak products.
- Do not reuse regulation `APPLIES_IN` semantics for product design-jurisdiction (distinct property/prompt).
- Prefer product/`SourcedMapping` patterns for gaps over overloading compliance `no-coverage` if shapes disagree.
- Do not attach OpenLineage (or ODPS+ODCS) to every product for symmetry.
- Catalogue inclusion ≠ need for CIM/CRM.

## Suggested first message to the new agent

> Execute [`gap-remediation-plan.md`](gap-remediation-plan.md) starting at slice 1 (lineage-emission under Orchestrate + OpenLineage CIM). Read [`HANDOFF-gap-remediation.md`](HANDOFF-gap-remediation.md) first. Honour pre-implementation locks (CRM walk is view-only; lineage under Orchestrate). Continue on the existing typology branch; repo must stay private. Do not commit unless asked.
