import httpx

from gateway.config import Settings
from gateway.main import create_app


async def test_lifespan_creates_and_closes_client() -> None:
    app = create_app(settings=Settings(_env_file=None))

    async with app.router.lifespan_context(app):
        client = app.state.client

        assert isinstance(client, httpx.AsyncClient)
        assert not client.is_closed

    assert client.is_closed


async def test_injected_client_is_used_and_left_open() -> None:
    injected = httpx.AsyncClient()
    app = create_app(settings=Settings(_env_file=None), client=injected)

    assert app.state.client is injected

    async with app.router.lifespan_context(app):
        pass

    assert not injected.is_closed

    await injected.aclose()
