"""Gateway application.

`create_app()` builds a fresh app so tests can make their own copies.
`app` is the instance uvicorn runs: `uv run uvicorn gateway.main:app`.
"""

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="python-api-gateway")

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
