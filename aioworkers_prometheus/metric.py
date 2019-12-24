import os
from multiprocessing import Queue
from typing import Dict

from aioworkers.core.base import LoggingEntity

# true
from . import MULTIPROC_DIR, metrics
from .metrics import QueueMetric
from .registry import REGISTRY, Receiver, get_registry


class Metric(LoggingEntity):
    METRICS = dict(
        counter=metrics.Counter,
        enum=metrics.Enum,
        gauge=metrics.Gauge,
        histogram=metrics.Histogram,
        info=metrics.Info,
        summary=metrics.Summary,
    )

    def __init__(self, *args, **kwargs):
        self._metrics: Dict = {}
        self._queue = Queue()
        self._pid = os.getpid()
        Receiver(self._queue, self._metrics).start()
        super().__init__(*args, **kwargs)

    def set_config(self, config):
        cfg = config.new_parent(logger='aioworkers_prometheus')
        super().set_config(cfg)
        registry = self.config.get('registry', REGISTRY)
        namespace = self.config.get('namespace')
        metrics = self.config.get('metrics', {})
        for mid, (attr, params) in enumerate(metrics.items()):
            kw = dict(params, queue=self._queue, mid=mid)
            cls = self.METRICS[kw.pop('type', 'gauge')]
            kw['registry'] = get_registry(kw.get('registry', registry))
            kw.setdefault('namespace', namespace)
            metric = cls(**kw)
            self._metrics[mid] = metric
            setattr(self, attr, metric)

    async def init(self):
        QueueMetric.fork = not MULTIPROC_DIR and self._pid != os.getpid()
        await super().init()
