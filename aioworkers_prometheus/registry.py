import logging
from functools import lru_cache
from multiprocessing import Queue
from threading import Thread
from typing import Dict

from prometheus_client import registry

REGISTRY = 'REGISTRY'

logger = logging.getLogger('aioworkers_prometheus')


@lru_cache(None)
def get_registry(name: str = REGISTRY) -> registry.CollectorRegistry:
    if name == REGISTRY:
        return registry.REGISTRY
    else:
        return registry.CollectorRegistry(auto_describe=True)


class Receiver:
    def __init__(self, queue: Queue, metrics: Dict):
        self._queue = queue
        self._metrics = metrics

    def process_msg(self, mid, *args):
        metric = self._metrics[mid]
        metric.from_msg(*args)

    def process(self):
        while True:
            msg = self._queue.get()
            try:
                self.process_msg(*msg)
            except Exception:
                logger.exception('Metric message error')

    def start(self):
        tr = Thread(target=self.process, daemon=True)
        tr.start()
