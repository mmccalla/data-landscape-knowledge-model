---
name: gap remediation
overview: Close P0 competence gaps (lineage capability, product differentiation, CRM-aware product scope), then P1 coherence, then declare or thinly reduce P2 catalogue debt—without becoming a compliance engine or inventing unsourced edges.
todos:
  - id: p0-lineage-capability
    content: Add lineage-emission under Orchestrate + OpenLineage CIM; reify explicit gaps; update tests/docs
    status: completed
  - id: p0-product-differentiation
    content: Diversify product CONSIDERS_* beyond ODPS+ODCS using existing landscape entries and sourced rationales
    status: completed
  - id: p0-crm-aware-scope
    content: Extend productScopeFor (view-only) for CRM neighbourhood; ADR in design-decisions; no materialised product→reg edges
    status: completed
  - id: p1-adopt-cim-batch
    content: Map highest-value ADOPT standards to components with sourced CIMs; leave the rest catalogue-only by declaration
    status: completed
  - id: p1-crm-and-iso-coherence
    content: CRM for the three bare components; align ISO 27001 / EU AI Act / NIST 800-53 across product and component layers
    status: completed
  - id: p1-jurisdiction-and-odps-disambiguation
    content: Optional design-jurisdiction on products; expose ODPS vs odpspec contrast; fill empty vertical/posture cells
    status: completed
  - id: p2-declared-debt
    content: Document catalogue debt; optional thin slices for quality/observability, no-coverage reification, capital-markets vertical, Snowflake prose→model
    status: completed
  - id: hygiene-gate
    content: npm test, pre-commit, private-repo check; update package counts and design-decisions ADR notes
    status: completed
isProject: false
---

# Gap remediation plan

> Status: historical — work landed on main (through 1.0.9 / 1.0.10). Not a living runbook.

## Overview

**Goal.** An architect inspecting a data product or pipeline sees *honest* capability (including lineage), *differentiated* design prompts by vertical/posture, and *obligation neighbourhood* grounded in existing component-regulatory evidence—without turning the package into a compliance engine.

**Scope.** Ontology/taxonomy/SHACL only where needed; curated CIMs/CRMs/product mappings; `productScopeFor` behaviour; CSV projection; tests; docs/README/design-decisions. Repo stays **private**.

**Non-goals.** Mapping all 66 unmapped standards or 64 unmapped regulations; automatic legal applicability; live Entropy sync; inventing Snowflake as a landscape “standard” without an evidence rule; Pages/public flip.

## Relationship to prior plan

[`data-product-typology-plan.md`](data-product-typology-plan.md) delivered the thin typology. This plan **supersedes** two of its freezes where the gap register showed competence failures:

| Prior freeze | Remains / changes |
|---|---|
| Gaps are features; do not invent lineage links | **Change:** inventing *unsourced* links stays forbidden; a **lineage-emission component** + sourced OpenLineage CIM is now in scope because ADOPT + Airflow/dbt CIMs make silence dishonest. |
| No jurisdiction on the product | **Change (thin):** optional **design jurisdiction prompt** on products (not applicability). Regulation jurisdiction remains authoritative for instruments. |
| Curated product regs; prefer CRM reuse | **Keep and strengthen:** product scope must *surface* CRM neighbourhood reachable from considered standards/components. |
| No compliance claims | **Keep.** |
| Namespace / authorship | **Keep.** |

## Principles

1. **Sourced or explicit gap.** Every new edge is reified with rationale + authoritative source, or modelled as typed `no-coverage` / documented catalogue debt.
2. **Capability before decoration.** Do not hang OpenLineage on products until a pipeline component can own the CIM.
3. **Differentiate with existing entries.** Prefer standards/regulations already in the landscape; do not mint catalogue entries solely to fill a matrix cell.
4. **Design prompt ≠ applicability.** Product and CRM edges remain consideration / relevance, not “this org must comply”.
5. **MECE for vertical/posture examples.** Empty matrix cells get one curated product *or* an explicit “intentionally empty” note in docs—not silent holes.
6. **Fallacy guards.** Avoid ODPS+ODCS hasty generalisation; avoid association (lineage prose → Iceberg Catalog); avoid false dilemma on store options; avoid argument-from-silence on ADOPT orphans.

## Acceptance / exit bar

### P0 (must)

- [x] A `lineage-emission` (name finalised in-slice) `DataPipelineComponentType` exists under **Orchestrate** (pre-implementation lock).
- [x] At least one `ComponentImplementationMapping`: that component → `standard:openlineage`, sourced (OpenLineage spec / Airflow provider docs).
- [x] Retail Stock (and any other honest non-link) uses a **reified** gap or mapping-relation `no-coverage` where still true (e.g. no Snowflake store option)—not prose alone.
- [x] Product `CONSIDERS_STANDARD` set is no longer {ODPS, ODCS}×12; each vertical has at least one distinctive consideration beyond the pair (or an explicit sourced reason why the pair alone is enough).
- [x] Selecting a product in `graph.html` includes CRM-reachable regulations/components via considered standards (see slice 3)—regression-tested; **view-only** (no materialised product→regulation triples from the walk).
- [x] `npm test` + `pre-commit run --all-files` pass; repo private.

### P1 (should, before calling remediation “done”)

- [x] Prioritised ADOPT→CIM batch landed (not all 26).
- [x] Three components currently without CRM have at least one sourced CRM each, **or** documented intentional blank with design-decisions note (store-write should not stay blank without justification).
- [x] ISO 27001 / EU AI Act / NIST 800-53 coherence fixed (see slice 5).
- [x] Design-jurisdiction prompts on health (and other mismatched) products; ODPS vs `odpspec` contrast visible on ≥1 product mapping set.
- [x] Empty vertical/posture cells filled or declared.

### P2 (declare or optional thin slices)

- [x] Catalogue debt stated in docs with counts and “not a defect” rule retained for intentional blanks.
- [x] Optional follow-ons listed; none block P0/P1 exit.

## Pre-implementation locks (resolve before coding)

These are cheap, material if left fuzzy. They supersede earlier “prefer Govern” wording in this plan.

| Tension | Why it matters | Locked decision |
|---|---|---|
| CRM walk = view vs asserted facts | Projecting inferred regs into CSV/TTL as real edges invents applicability-shaped facts. | P0 scope expansion is **`productScopeFor` / UI only**. **No** new product→regulation (or product→CRM) triples from the walk. When slice 3 lands, document as a **view rule** in [`docs/08-design-decisions.md`](docs/08-design-decisions.md). |
| Govern vs Orchestrate for lineage | Wrong module forces `HAS_COMPONENT` rename/migration across all patterns. | Lineage-emission hangs under **Orchestrate** (OpenLineage job/run emission is operational). Use Govern only if the component is redefined as policy/control of lineage rather than emission—out of scope unless revisited explicitly. |

## Frozen decisions for this remediation

- **Lineage hangs on a new component under Orchestrate**, not by overloading `metadata-registration` (that stays catalog/registry-oriented; Iceberg Catalog CIM remains).
- **OpenLineage CIM is primary**; Airflow/dbt remain orchestration/processing options. Do **not** claim Airflow “is” OpenLineage; optional note in mapping rationale that Airflow *emits* OpenLineage events (official provider).
- **Product scope CRM walk is view-layer only** (`productScopeFor` / graph UI). Graph-derived neighbourhood must not be materialised as product mapping assertions unless a later, explicit slice says otherwise.
- **Jurisdiction on products is optional, multi-valued design prompt** (e.g. `UK`, `EU`, `US`) pointing readers at regulation `APPLIES_IN`—never “in scope for GDPR”.
- **P2 catalogue-only majority stays** unless a competency question fails.

## Unknowns

| Unknown | Resolve in-slice |
|---|---|
| PROV | Keep catalogue + assess; no forced CIM unless a second lineage option is wanted for contrast. |
| How wide is “distinctive” product std? | Minimum one non-{ODPS,ODCS} standard **or** one distinctive regulation set that is not GDPR-clone, per vertical. |
| Design jurisdiction representation | Prefer SKOS concepts or controlled notations reused from existing `Jurisdiction` individuals if they fit; else thin datatype/annotation on `DataProduct`. |
| Capital-markets vertical (P2) | Prefer **defer** unless banking coarseness blocks a P1 product; else add `capital-markets` SKOS + retarget trade product. |
| Snowflake | Prefer **explicit no-coverage** on store-write for Retail Stock + prose; add landscape entry only if an evidence rule for commercial platforms is agreed. |

## Skills

Load when building: `ontology-and-knowledge-graph-modeling`, `logical-fallacy-review`, `cognitive-bias-review`, `kiss-principle`, `incremental-implementation`, `tdd-practice`, `spec-driven-development`.

## Approach sketch

```text
P0.1  Orchestrate ──HAS_COMPONENT──▶ lineage-emission ──CIM──▶ OpenLineage
P0.2  DataProduct ──ProductStandard/RegulatoryRelevance──▶ distinctive landscape entries
P0.3  productScopeFor (view only — do not assert into TTL/CSV):
        product → PSR/PRR → standards/regulations
             └→ standards ← CIM ← components → CRM → regulations (+ categories)
```

External anchors to cite in mapping rationales (not as applicability):

- OpenLineage object model and integrations (Airflow, Spark, dbt)
- Bitol ODCS lineage RFC (design lineage complementary to OpenLineage)
- ODPS-spec lineage metadata fields (for odpspec disambiguation slice)

---

## Tasks / slices

### 1. P0 — Lineage capability (gap 1)

**Files:** ontology (if component class individuals live there), pattern/module TTL or instance files that define components, `component-mappings.ttl`, CSV projection, `scripts/graph-selection.mjs` only if needed, tests, docs/08-design-decisions, README shelf-warmers note.

**Do:**

1. Add component type **lineage-emission** (final label UK English) under **Orchestrate** (locked); wire `HAS_COMPONENT` for all ingestion patterns that already share the module set (same pattern as other shared components).
2. Author CIM → `standard:openlineage` with rationale + primary sources (OpenLineage spec; optionally Airflow OpenLineage provider as supporting).
3. Optionally second CIM later (none required in this slice).
4. Replace prose-only OpenLineage gap on Retail Stock with either:
   - a product `ProductStandardRelevance` **or**
   - a typed gap using the product/`SourcedMapping` pattern (prefer over overloading compliance `mapping-relation-no-coverage` if shapes disagree)—smallest SHACL-valid extension.
5. Keep Iceberg non-link for Retail Stock honest (Snowflake); prefer reified store no-coverage over prose.
6. Tests: component exists under Orchestrate; CIM endpoint OpenLineage; retail still does not falsely claim Iceberg/OpenLineage implementation if still non-covering.

**Exit:** OpenLineage is no longer an ADOPT orphan relative to the pipeline typology.

### 2. P0 — Product CQ differentiation (gap 2)

**Files:** `product-instances.ttl`, CSV, tests, README, docs/04-instances.

**Do:**

1. Inventory current 12 products’ `CONSIDERS_*` (baseline: ODPS+ODCS monoculture).
2. For each vertical, add **sourced** distinctive considerations from *existing* landscape entries, e.g. (illustrative—confirm in-slice against nodes):
   - **banking / capital markets:** keep/extend Iceberg, BCBS 239, DORA; add OpenLineage where lineage-emission now exists.
   - **retail:** keep dbt; consider data-quality standard sparingly if CIM exists by then, else defer quality to P2.
   - **health:** keep HIPAA where US-prompted; ensure UK/EU products emphasise GDPR (and design jurisdiction)—avoid HIPAA-only UK care-home.
   - **insurance:** keep ISO 27001 only if P1 CRM coherence lands in same PR or immediately after.
   - **telecoms:** NIS2 already; consider observability/OpenTelemetry only after P1/P2 OTel CIM—or skip.
   - **public-sector:** keep JSON Schema + ISO 11179; consider DCAT if rationale is solid.
3. Guarding rule: do **not** attach ODPS+ODCS+OpenLineage to every product “for symmetry” (symmetry bias).
4. Tests: assert per-vertical distinctive sets; forbid identical std+reg bags across all products.

**Exit:** Vertical selector changes the consideration neighbourhood in a human-explainable way.

### 3. P0 — CRM-aware product scope (gap 3)

**Files:** `scripts/graph-selection.mjs`, `src/graph.template.html` (hint text), `tests/graph-selection.test.mjs`, docs.

**Do:**

1. Extend `productScopeFor` after collecting considered standards (**view only** — pre-implementation lock):
   - find CIMs with `IMPLEMENTATION_OPTION` → those standards;
   - include those mapping nodes + `MAPS_COMPONENT_TYPE` components;
   - from those components, follow CRM `MAPS_COMPONENT_TYPE` (in) → `REGULATORY_CONTEXT` regulations;
   - include CRM nodes + regulation categories/governance as today for regs.
2. Do **not** write product→regulation, product→CRM, or equivalent triples into TTL/CSV from this walk. Scope expansion is **UI/`productScopeFor` neighbourhood only**.
3. When landing the slice, add an ADR bullet in `docs/08-design-decisions.md`: CRM-aware product scope is a view rule, not asserted knowledge.
4. Optional toggle later; v1 can always-on when any product/vertical/posture filter is active.
5. Tests: banking product scope includes at least one CRM-backed regulation not necessarily listed on the product (e.g. NIST 800-53 if reachable via ODCS/OPA/Airflow path)—assert with fixtures; assert projection files gain no new product regulatory edges from the walk alone.
6. Update hint copy so users do not read CRM neighbourhood as “this product must comply”.

**Exit:** Product CQ uses component evidence already paid for in the model, without materialising applicability-shaped facts.

### 4. P1 — ADOPT standards without CIM (gap 4)

**Files:** `component-mappings.ttl`, maybe component list if a hang-point is missing, CSV, tests, docs.

**Do:**

1. Rank the 26 ADOPT-unmapped standards by (a) already have a natural component, (b) appear in product stories, (c) official integration with mapped tools.
2. **Batch A (land):** e.g. Kafka→messaging/source or interconnection hang-point; Spark→processing/workload; Parquet (+ maybe Avro)→file-format via store or interconnection; JSON Schema / OpenAPI→schema or contracts components; OpenTelemetry→new or lineage-adjacent observability component **only if** P2 quality/observability slice is pulled forward.
3. **Batch B (declare):** remainder stay catalogue-only; list IDs in design-decisions / overview as intentional incompleteness.
4. Never map ADOPT→CIM without a component that semantically fits (no dumping onto `metadata-registration`).

**Exit:** High-value ADOPT orphans cleared; remainder explicitly declared.

### 5. P1 — CRM / ISO / AI Act / NIST coherence (gaps 5–6)

**Files:** `component-regulatory-mappings.ttl`, `product-instances.ttl`, CSV, tests.

**Do:**

1. For `trigger-invocation`, `workload-planning`, `store-write-data-product`: add ≥1 sourced CRM **or** document intentional blank (store-write blank needs a written reason—products land there).
2. **ISO 27001:** either add CRM from a sensible component (often secure-*/failure-isolation / store) with primary source, **or** remove product consideration until CRM exists.
3. **EU AI Act / NIST 800-53:** add thin product considerations only where a curated product is AI-relevant or control-baseline-relevant; otherwise leave CRM-only and document that product scope (slice 3) is how they surface.
4. Tests for coherence: every `CONSIDERS_REGULATION` target either has ≥1 CRM somewhere **or** is allowlisted as product-only with rationale flag in evidenceStatus.

**Exit:** No floating product regs; no “surprise” CRM-only regs unexplained by scope docs.

### 6. P1 — Jurisdiction, ODPS disambiguation, matrix cells (gaps 7–9)

**Files:** ontology/shapes/taxonomy as needed, `product-instances.ttl`, CSV, graph selectors if filtering by design jurisdiction is wanted (optional), tests, docs.

**Do:**

1. Add optional product design-jurisdiction prompt(s); set health products so UK/EU care-home is not HIPAA-shaped without US prompt.
2. On ≥1 product (prefer public-sector or retail definition-heavy), add `ProductStandardRelevance` to `odpspec` **or** a sourced “consider Bitol ODPS not LF ODPS-spec” rationale on the ODPS mapping—and document the naming collision in docs/09-glossary or instances doc.
3. Fill empty cells with one product each **or** mark intentionally empty:
   - health NO_PII (e.g. aggregated activity / reference clinical codes without PII)
   - insurance NO_PII (e.g. actuarial risk tables)
   - telecoms NO_PII (e.g. network inventory)
   - public-sector PII (e.g. citizen benefits eligibility)
4. Hygiene: SHACL minCount 0 for new optional jurisdiction; counts updated.

**Exit:** Matrix explainable; ODPS collision visible; health jurisdiction mismatch risk reduced.

### 7. P2 — Catalogue debt (gaps 10–14)

**Files:** primarily docs (`08-design-decisions`, `00-package-overview`); optional thin instance slices.

**Do (declare by default):**

| Gap | Default disposition |
|---|---|
| 10 Catalogue-only majority | Declare counts + rule: inclusion ≠ mapping. |
| 11 Only 3 crosswalks | Keep official-evidence-only rule; add crosswalks only with OFFICIAL_SOURCE. |
| 12 Quality & observability orphaned | Optional slice: `observability-signal` / `data-quality-check` components + OTel / Great Expectations CIMs—after P0/P1. |
| 13 Negative links not reified | When touching products in P0/P1, prefer reified no-coverage; backlog any remaining prose gaps. |
| 14 Capital-markets-as-banking; Snowflake prose | Optional: `capital-markets` vertical; Snowflake as explicit store no-coverage / platform note—not a fake standard. |

**Exit:** Debt is visible and owned; no silent expectation that 84/73 are all wired.

### 8. Hygiene gate

- Update package overview counts; README narrative only where behaviour changed.
- ADR notes in `docs/08-design-decisions.md` for: lineage component; CRM-aware product scope; design jurisdiction; catalogue debt rule.
- `npm test`, `pre-commit run --all-files`, `gh repo view --json isPrivate,visibility`.
- No commit/PR unless asked.

## Suggested execution order

```text
1 (lineage component + OpenLineage CIM)
  → 3 (CRM-aware scope)   # can start once CIMs exist for considered stds
  → 2 (product differentiation, including OpenLineage where earned)
  → 5 (CRM/ISO coherence) ↔ 4 (ADOPT CIM batch) in parallel if careful
  → 6 (jurisdiction, ODPS-spec, matrix)
  → 7 (declare P2)
  → 8 (hygiene)
```

Slice 3 before or with 2: differentiation that adds standards automatically enriches CRM neighbourhood once walk exists.

## Fallacy / bias checklist (review each PR)

- [x] No ODPS+ODCS clone across new products without distinctive edge.
- [x] No OpenLineage on every product “for completeness”.
- [x] No CRM neighbourhood presented as applicability.
- [x] No dumping unrelated ADOPT standards onto `metadata-registration`.
- [x] No HIPAA on UK-only design prompts without US jurisdiction prompt.
- [x] Catalogue inclusion not treated as proof of mapping need.

## Out of scope reminders

- Public Pages, public repo, tags.
- Full ODCS/ODPS import or Entropy sync.
- Clause-level regulatory equivalence.
- Re-litigating authorship/namespaces.
