# Security policy

## Supported versions

Security fixes are applied on the default branch (`main`) of this repository. Tagged releases document published snapshots; prefer reporting against current `main`.

## Reporting a vulnerability

Please **do not** open a public issue for security-sensitive reports.

Email Mark McCalla via the contact details on [polymathic.co.uk](https://polymathic.co.uk/) (or open a private GitHub security advisory on this repository if that feature is enabled).

Include:

- a description of the issue and its impact;
- steps to reproduce, or a proof of concept where practical;
- any suggested remediation.

You should receive an acknowledgement within a few working days.

## Scope notes

This package is a **derived knowledge model and visualisation**, not a hosted service. Typical concerns include:

- accidental disclosure of credentials or private paths in commits or generated artefacts;
- supply-chain issues in GitHub Actions or npm dependencies used to build `graph.html`;
- misleading compliance claims in documentation (treated as documentation defects, not product “breaches”).

Catalogue data remains © Entropy Data under MIT; report upstream catalogue issues to the publishers of [data-landscape.com](https://www.data-landscape.com/).
