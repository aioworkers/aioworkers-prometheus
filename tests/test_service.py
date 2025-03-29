import os
import tempfile
from urllib.request import urlopen

import pytest
from aioworkers.core.context import Context

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


async def test_port(context: Context):
    assert context.prometheus is not None
    url = f"http://localhost:{context.prometheus.config.port}"
    r = await context.loop.run_in_executor(None, urlopen, url)
    assert r.status == 200, r.read()
    data = r.read()
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
