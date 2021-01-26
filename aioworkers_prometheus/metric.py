from typing import Dict, Optional, Tuple, Type

from aioworkers.core.base import LoggingEntity
from aioworkers.core.config import ValueExtractor
from prometheus_client import metrics

# true
from .registry import REGISTRY, get_registry


class Metric(LoggingEntity):
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
        cfg = config.new_parent(logger=__package__)
        super().set_config(cfg)
        registry = self.config.get('registry', REGISTRY)
        namespace = self.config.get('namespace')
        cfg_metrics = self.config.get('metrics', {})
        for attr, params in cfg_metrics.items():
            kw = dict(params)
            m_name = kw.setdefault('name', attr)
            m_type = kw.pop('type', 'gauge')
            cls = self.METRICS[m_type]
            m_registry = kw.get('registry', registry)
            kw['registry'] = get_registry(m_registry)
            m_namespace = kw.setdefault('namespace', namespace)
            cache_key = (m_registry, m_namespace, m_name, m_type)
            metric: Optional[metrics.MetricWrapperBase] = self._cache.get(cache_key)
            if metric is None:
                metric = cls(**kw)
                self._cache[cache_key] = metric
            setattr(self, attr, metric)
