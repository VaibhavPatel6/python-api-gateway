"""Echo upstream: replies with what it received.

Used as the backend behind the gateway in tests and benchmarks.
`?delay_ms=N` makes it wait N milliseconds before replying (for timeout tests).
"""

import asyncio
from typing import Annotated

from fastapi import FastAPI, Query, Request

app = FastAPI(title="echo upstream")


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def echo(
    request: Request,
    path: str,
    delay_ms: Annotated[int, Query(ge=0, le=60_000)] = 0,
) -> dict[str, object]:
    if delay_ms:
        # asyncio.sleep pauses only this request; time.sleep would block every request.
        await asyncio.sleep(delay_ms / 1000)
    body = await request.body()
    return {
        "method": request.method,
        "path": request.url.path,
        "query": dict(request.query_params),
        "headers": dict(request.headers),
        "body": body.decode("utf-8", errors="replace"),
    }
