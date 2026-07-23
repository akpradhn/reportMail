# Contributing

Thanks for helping improve reportmail. Please open an issue before large changes so the design can be discussed.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
mypy src/reportmail
```

Add focused tests for behaviour changes, keep public APIs typed and documented, and avoid JavaScript or email-hostile layout techniques. Run the three example scripts when changing rendering. Pull requests should explain user-visible behaviour and any email-client trade-offs.

## Releasing

1. Move the release notes from `Unreleased` into a versioned section in `CHANGELOG.md`.
2. Set `__version__` in `src/reportmail/__init__.py` to the new version.
3. Run `pytest`, `ruff check .`, `mypy src/reportmail`, `python -m build`, and `twine check dist/*`.
4. Commit the release, create a tag matching the version (for example, `v0.1.0`), and push the tag.
5. Create the matching GitHub release. The publish workflow will build and upload the artifacts to PyPI using Trusted Publishing.

PyPI must be configured with a trusted publisher for repository `akpradhn/reportMail`, workflow `publish-to-pypi.yml`, and environment `pypi`. Protect the GitHub `pypi` environment with required approval.
