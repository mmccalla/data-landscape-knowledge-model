# Contributors

[← README](../README.md)

The repository uses [pre-commit](https://pre-commit.com/) for hygiene, secret safety, cruft rejection, Turtle validation (`riot`), SHACL (`pyshacl`), and Neo4j CSV projection integrity. Install and enable it once:

```sh
python3 -m pip install pre-commit pyshacl
# Apache Jena riot must also be on PATH (see 07-loading-and-validation.md)
pre-commit install
```

Run every configured check against the complete repository before submitting a change:

```sh
pre-commit run --all-files
```

`graph.html` is excluded from text hygiene hooks because it is a generated standalone artefact of about 800KB. Domain hooks map to the scripts under `scripts/check-*.py` and follow the [loading and validation guide](07-loading-and-validation.md).
