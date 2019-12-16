aioworkers-prometheus
=====================

.. image:: https://travis-ci.org/aioworkers/aioworkers-prometheus.svg?branch=master
  :target: https://travis-ci.org/aioworkers/aioworkers-prometheus

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-prometheus.svg
  :target: https://pypi.python.org/pypi/aioworkers-prometheus
  :alt: Python versions

.. image:: https://img.shields.io/pypi/v/aioworkers-prometheus.svg
  :target: https://pypi.python.org/pypi/aioworkers-prometheus


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
        prefix: aioworker.test


Development
-----------

Install dev requirements:


.. code-block:: shell

    pipenv install --dev --skip-lock


Run tests:

.. code-block:: shell

    pipenv run pytest
