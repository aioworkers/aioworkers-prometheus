import logging
from functools import lru_cache
from typing import Iterable, Mapping

from prometheus_client import Metric
from prometheus_client import registry as r

REGISTRY = "REGISTRY"

logger = logging.getLogger(__package__)


@lru_cache(None)
def get_registry(name: str = REGISTRY) -> r.CollectorRegistry:
    if name == REGISTRY:
        return r.REGISTRY
    else:
        return r.CollectorRegistry(auto_describe=True)


class LabelsRegistry(r.Collector):
    def __init__(self, registry: r.Collector, labels: Mapping[str, str]):
        self._registry = registry
        self._labels = labels

    def collect(self) -> Iterable[Metric]:
        for mf in self._registry.collect():
            for sample in mf.samples:
                sample.labels.update(self._labels)
            yield mf
