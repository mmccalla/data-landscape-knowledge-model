# Source manifest

This manifest records the machine-readable inputs used to generate the package on 29 July 2026.

| Source | Records | SHA-256 |
|---|---:|---|
| `https://www.data-landscape.com/standards.json` | 81 | `a523ce0b9029c3a65e5a6a0bc16938dfc0a6155f9f768613498ac84c0e93b19c` |
| [`standard-extensions.json`](standard-extensions.json) | 3 | `65899eb780a37c025a6290dc185e89a70bb5f2730f4831610127cc43a36febf0` |
| `https://www.data-landscape.com/regulation.json` | 73 | `5175284093e98f652cb6205a3308cddd4f5c88043b200086d7151622761602ee` |

The regulation source was reconciled to 19 categories and the displayed jurisdiction filters: EU 16, Global 54 and US 9. Compound source labels overlap between those filters.

The official mapping URLs are recorded on each `ComplianceMapping` instance and explained in [`ATTRIBUTION.md`](ATTRIBUTION.md).

The thirty-three curated component regulatory mappings cite primary sources from EUR-Lex, California statute, the US Department of Health and Human Services / eCFR, NIST, ISO and the Basel Committee. Their exact requirement references and source versions are recorded in [`component-regulatory-mappings.ttl`](component-regulatory-mappings.ttl). They are local interpretations rather than upstream source records. Coverage is intentionally incomplete: components without a precise, defensible citation remain unmapped.
