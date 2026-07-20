# Contributing

Thanks for helping improve reportmail. Please open an issue before large changes so the design can be discussed.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

Add focused tests for behaviour changes, keep public APIs typed and documented, and avoid JavaScript or email-hostile layout techniques. Run the three example scripts when changing rendering. Pull requests should explain user-visible behaviour and any email-client trade-offs.

