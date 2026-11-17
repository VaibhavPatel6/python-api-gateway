# python-api-gateway

An async API gateway in Python (FastAPI, httpx): routing, JWT and API-key auth, per-client rate limiting, load shedding and upstream health checks. Work in progress.

## Development setup

Requires [uv](https://docs.astral.sh/uv/). Python 3.14 is pinned in `.python-version`.

```bash
uv sync                          # create .venv and install dependencies
uv run pre-commit install        # one time per clone: run checks before every commit
```

Checks (the pre-commit hook runs all four):

```bash
uv run ruff format .
uv run ruff check .
uv run mypy
uv run pytest
```

Run the gateway locally:

```bash
uv run uvicorn gateway.main:app --reload
```
