import multiprocessing
from typing import Any, Dict, Optional, Tuple, Type

from aioworkers.core.base import LoggingEntity
from aioworkers.core.config import ValueExtractor
from aioworkers.worker.base import Worker
from prometheus_client import PROCESS_COLLECTOR, metrics

# true
from . import MULTIPROC_DIR
from .registry import REGISTRY, get_registry


class Metric(Worker, LoggingEntity):
    config: ValueExtractor
    METRICS: Dict[str, Type[metrics.MetricWrapperBase]] = dict(
        counter=metrics.Counter,
        enum=metrics.Enum,
        gauge=metrics.Gauge,
        histogram=metrics.Histogram,
        info=metrics.Info,
        summary=metrics.Summary,
    )
    _cache: Dict[Tuple, metrics.MetricWrapperBase] = {}

    def set_config(self, config: ValueExtractor) -> None:
        cfg = config.new_parent(
            logger=__package__,
            autorun=bool(MULTIPROC_DIR),
            persist=True,
        )
        super().set_config(cfg)
        registry: str = self.config.get("registry", REGISTRY)
        namespace: Optional[str] = self.config.get("namespace")
        cfg_metrics = self.config.get("metrics", {})
        for attr, params in cfg_metrics.items():
            if hasattr(self, attr):
                continue
            kw = dict(params)
            m_name: str = kw.setdefault("name", attr)
            kw.setdefault("documentation", "")
            m_type: str = kw.pop("type", "gauge")
            cls = self.METRICS[m_type]
            m_registry: str = kw.get("registry", registry)
            kw["registry"] = get_registry(m_registry)
            m_namespace: Optional[str] = kw.setdefault("namespace", namespace)
            cache_key: Tuple = (m_registry, m_namespace, m_name, m_type)
            cache_key += tuple(kw.get("labelnames", ()))
            metric: Optional[metrics.MetricWrapperBase] = self._cache.get(cache_key)
            if metric is None:
                metric = cls(**kw)
                self._cache[cache_key] = metric
            setattr(self, attr, metric)

    async def run(self, value: Any = None) -> Any:
        name = multiprocessing.current_process().name
        for mf in PROCESS_COLLECTOR.collect():
            m = getattr(self, mf.name).labels(name)
            m._value.set(mf.samples[0].value)
