import os
import tempfile

import pytest
from aiohttp import client

import aioworkers_prometheus.service


@pytest.fixture
def config_yaml(unused_tcp_port_factory):
    port = unused_tcp_port_factory()
    return f"""
    prometheus:
        cls: aioworkers_prometheus.service.Service
        labels:
            env: prod
        port: {port}
        graphite:
            address: localhost:{port}
    """


async def test_port(context):
    assert context.prometheus is not None
    url = f"http://localhost:{context.prometheus.config.port}"
    async with client.ClientSession() as session:
        async with session.get(url) as r:
            assert r.status == 200, await r.text()
            data = await r.read()
    assert data


@pytest.fixture
def tmp_dir(mocker):
    env = "PROMETHEUS_MULTIPROC_DIR"
    with tempfile.TemporaryDirectory() as d:
        mocker.patch.object(os, "environ", {env: d})
        mocker.patch.object(aioworkers_prometheus.service, "MULTIPROC_DIR", d)
        yield d


async def test_multiproc_generate_latest(tmp_dir, context):
    await context.prometheus.generate_latest()
