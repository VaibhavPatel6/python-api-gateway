import time
from collections.abc import AsyncIterator

import httpx
import pytest

from upstreams.echo.app import app as echo_app


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=echo_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://echo") as c:
        yield c


async def test_echoes_method_path_query_headers_and_body(
    client: httpx.AsyncClient,
) -> None:
    response = await client.post(
        "/users/42", params={"a": "1"}, headers={"x-test": "hello"}, content=b"ping"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["method"] == "POST"
    assert data["path"] == "/users/42"
    assert data["query"] == {"a": "1"}
    assert data["headers"]["x-test"] == "hello"
    assert data["body"] == "ping"


async def test_delay_ms_waits_before_replying(client: httpx.AsyncClient) -> None:
    start = time.monotonic()
    response = await client.get("/", params={"delay_ms": 50})
    elapsed = time.monotonic() - start

    assert response.status_code == 200
    assert elapsed >= 0.045


async def test_negative_delay_is_rejected(client: httpx.AsyncClient) -> None:
    response = await client.get("/", params={"delay_ms": -1})

    assert response.status_code == 422
