import pytest


@pytest.fixture
def aioworkers(aioworkers):
    aioworkers.plugins.default = True
    return aioworkers


@pytest.fixture
def config_yaml():
    return """
    metric:
        cls: aioworkers_prometheus.metric.Metric
        namespace: aioworkers
        metrics:
            run:  # ignore metric for exists attr
                name: run
                type: counter
                documentation: Counter for tests
            test_counter:
                name: test_counter
                type: counter
                documentation: Counter for tests
            histogram:
                name: test_histogram
                type: histogram
                documentation: histogram for tests
            gauge:
                name: test_gauge
                type: gauge
                documentation: gauge for tests
            info:
                name: test_info
                type: info
                documentation: info for tests

            enum:
                name: test_enum
                type: enum
                documentation: enum for tests
                states: [a,b]
    """


async def test_counter(context):
    assert context.metric is not None
    context.metric.test_counter.inc(45)
    assert 45 == context.metric.test_counter._value.get()

    c = context.metric.test_counter
    c.inc(4)
    assert 49 == c._value.get()

    g = context.metric.gauge
    g.set(45)
    assert 45 == g._value.get()
    g.dec(90)
    assert -45 == g._value.get()

    context.metric.histogram.observe(45)
    assert 45 == context.metric.histogram._sum.get()

    e = context.metric.enum
    e.state("a")
    assert 0 == e._value

    i = context.metric.info
    data = dict(i="1")
    i.info(data)
    assert data == i._value


async def test_run(context):
    await context.metric.run()
