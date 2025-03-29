aioworkers-prometheus
=====================

.. image:: https://img.shields.io/pypi/v/aioworkers-prometheus.svg
  :target: https://pypi.org/project/aioworkers-prometheus

.. image:: https://github.com/aioworkers/aioworkers-prometheus/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-prometheus/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/aioworkers/aioworkers-prometheus/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aioworkers/aioworkers-prometheus
  :alt: Coverage

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
  :target: https://github.com/charliermarsh/ruff
  :alt: Code style: ruff

.. image:: https://img.shields.io/badge/types-Mypy-blue.svg
  :target: https://github.com/python/mypy
  :alt: Code style: Mypy

.. image:: https://readthedocs.org/projects/aioworkers-prometheus/badge/?version=latest
  :target: https://github.com/aioworkers/aioworkers-prometheus#readme
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-prometheus.svg
  :target: https://pypi.org/project/aioworkers-prometheus
  :alt: Python versions

.. image:: https://img.shields.io/pypi/dm/aioworkers-prometheus.svg
  :target: https://pypistats.org/packages/aioworkers-prometheus

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
  :alt: Hatch project
  :target: https://github.com/pypa/hatch


Use
---

.. code-block:: yaml

    metric:
      registry: aioworkers
      namespace: aioworkers_test_metric
      metrics:
        my_counter:
          type: counter
          name: test_counter
          documentation: Counter for tests
        my_histogram:
          type: histogram
          name: test_histogram
          documentation: Histogram for tests
          buckets: [30, 90, 100, 200, 400, 800]


Use in code

.. code-block:: python

    context.metric.my_counter.inc()
    context.metric.my_histogram.observe(542)

    with context.metric.my_histogram.time():
        await asyncio.sleep(1)


Add global labels to default registry to exposition

.. code-block:: yaml

    prometheus:
      registry: aioworkers
      labels:
        env: prod


Serve port 8000 for prometheus

.. code-block:: yaml

    prometheus:
      port: 8000
      registry: aioworkers


Push to graphite localhost:9090

.. code-block:: yaml

    prometheus:
      registry: aioworkers
      graphite:
        address: localhost:9090
        interval: 1m
        prefix: aioworkers.test


Development
-----------

Check code:

.. code-block:: shell

    hatch run lint:all


Format code:

.. code-block:: shell

    hatch run lint:fmt


Run tests:

.. code-block:: shell

    hatch run pytest


Run tests with coverage:

.. code-block:: shell

    hatch run cov
