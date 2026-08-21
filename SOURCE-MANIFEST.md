# Source manifest

This manifest records the machine-readable inputs used to generate the package on 21 August 2026.

| Source | Records | SHA-256 |
|---|---:|---|
| `https://www.data-landscape.com/standards.json` | 81 | `3c383ed32cba51b739b6013a8fad448e2daffe8cc56e5c3fd71ca2d9ded1dcd3` |
| [`standard-extensions.json`](standard-extensions.json) | 3 | `65899eb780a37c025a6290dc185e89a70bb5f2730f4831610127cc43a36febf0` |
| `https://www.data-landscape.com/regulation.json` | 73 | `5175284093e98f652cb6205a3308cddd4f5c88043b200086d7151622761602ee` |

The regulation source was reconciled to 19 categories and the displayed jurisdiction filters: EU 16, Global 54 and US 9. Compound source labels overlap between those filters.

The official mapping URLs are recorded on each `ComplianceMapping` instance and explained in [`ATTRIBUTION.md`](ATTRIBUTION.md).

The thirty-eight curated component regulatory mappings cite primary sources from EUR-Lex, California statute, the US Department of Health and Human Services / eCFR, NIST, ISO and the Basel Committee. Their exact requirement references and source versions are recorded in [`component-regulatory-mappings.ttl`](component-regulatory-mappings.ttl). They are local interpretations rather than upstream source records. All fifteen pipeline component types now have at least one CRM; residual incompleteness is catalogue skew toward instruments with precise public citations, not blank component types.
