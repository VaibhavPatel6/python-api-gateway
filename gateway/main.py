"""Gateway application.

`create_app()` builds a fresh app so tests can make their own copies.
`app` is the instance uvicorn runs: `uv run uvicorn gateway.main:app`.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from gateway.config import Settings


def create_app(
    settings: Settings | None = None, client: httpx.AsyncClient | None = None
) -> FastAPI:
    # Default settings
    if settings is None:
        settings = Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if client is None:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as upstream_client:
                app.state.client = upstream_client
                yield
        else:
            yield

    app = FastAPI(title="python-api-gateway", lifespan=lifespan)
    app.state.settings = settings
    app.state.client = client

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
