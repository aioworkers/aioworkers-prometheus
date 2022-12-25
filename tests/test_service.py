import pytest
from aiohttp import client


@pytest.fixture
def config_yaml():
    return """
    prometheus:
        cls: aioworkers_prometheus.service.Service
        port: 8000
        graphite:
            address: localhost:8000
    """


async def test_port(context):
    assert context.prometheus is not None
    url = f"http://localhost:{context.prometheus.config.port}"
    async with client.ClientSession() as session:
        async with session.get(url) as r:
            assert r.status == 200, await r.text()
            data = await r.read()
    assert data
