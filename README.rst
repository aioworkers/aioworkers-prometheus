aioworkers-prometheus
=====================

.. image:: https://github.com/aioworkers/aioworkers-prometheus/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-prometheus/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/aioworkers/aioworkers-prometheus/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aioworkers/aioworkers-prometheus

.. image:: https://img.shields.io/pypi/v/aioworkers-prometheus.svg
  :target: https://pypi.org/project/aioworkers-prometheus
  :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-prometheus.svg
  :target: https://pypi.org/project/aioworkers-prometheus
  :alt: Python versions


Use
---

.. code-block:: yaml

    metric:
      registry: aioworkers
      namespace: aioworkers_test_metric
      metrics:
        counter:
          type: counter
          name: test_counter
          documentation: Counter for tests
        histogram:
          type: histogram
          name: test_histogram
          documentation: Histogram for tests
          buckets: [30, 90, 100, 200, 400, 800]


Use in code

.. code-block:: python

    context.metric.counter.inc()
    context.metric.histogram.observe(542)

    with context.metric.histogram.time():
        await asyncio.sleep(1)


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

Install dev requirements:


.. code-block:: shell

    pipenv install --dev --skip-lock


Run tests:

.. code-block:: shell

    pipenv run pytest
