# Compliance mapping walkthrough

[← Glossary](09-glossary.md) · [README](../README.md)

## Purpose

[`mapping-instances.ttl`](../mapping-instances.ttl) demonstrates how official crosswalks and evidential relationships can be added without making unsupported legal claims.

## Delivered mappings

| Source | Relation | Target | Authority |
|---|---|---|---|
| CSA Cloud Controls Matrix | Maps to | NIST Cybersecurity Framework | Cloud Security Alliance |
| CSA Cloud Controls Matrix | Maps to | ISO/IEC 27001 | Cloud Security Alliance |
| EU Cloud Code of Conduct | Supports evidence for | GDPR | EDPB and Belgian Data Protection Authority |

The CSA describes CCM as having machine-readable mappings to standards and frameworks. The EDPB register identifies the EU Cloud Code of Conduct as an approved transnational GDPR code.

## Why not COMPLIES_WITH?

Compliance is normally a conclusion about an organisation, system, product, processing activity or control implementation after considering applicability and evidence. A publication cannot itself comply with legislation.

Similarly, a standard may address or map to requirements without being sufficient to satisfy an entire law.

## Required evidence for future mappings

A candidate mapping should be added only when an official regulator, standards body, framework owner or clearly identified mapping author provides:

- an identifiable source and target;
- document versions or editions where available;
- the relationship or crosswalk;
- an authority or author;
- a stable supporting URL;
- publication status and limitations.

Community-submitted mappings may be represented, but must be labelled as such rather than presented as regulator or publisher endorsement.

## Future provision-level extension

The present model maps whole entries. A later extension can introduce `Control` and `RegulatoryRequirement` resources so mapping strength—equivalent, partial, related or no coverage—can be expressed at the appropriate level.

Do not infer clause-level equivalence from a broad document-level statement.

## Component regulatory context

[`component-regulatory-mappings.ttl`](../component-regulatory-mappings.ttl) adds design-time relevance mappings from pipeline component types to precisely cited requirements. Each mapping records its rationale, boundary, source version and primary source, and is asserted by Mark McCalla in this derived model. These mappings answer “which regulatory concerns should this component design consider?” They do not answer “is this pipeline compliant?”.

The delivered set (38 CRMs) covers all fifteen pipeline component types, including secure read and write access, source connectivity, state and idempotency, validation and contract binding, metadata registration, failure isolation, workload planning, trigger invocation, workload execution/orchestration, store/write data product, lineage emission, data product and data contract definition, and semantic description, with multiple independently cited regulations where the evidence supports them. Lineage emission has a BCBS 239 CRM alongside its OpenLineage CIM; that pairing is a design prompt, not an assertion that emission satisfies supervisory expectations. Residual catalogue skew toward instruments with precise public citations is accepted; balance is not forced by inventing weaker links. These mappings remain design-time relevance aids—they do not establish organisational compliance.
