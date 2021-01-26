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

    def set_config(self, config: ValueExtractor) -> None:
        cfg = config.new_parent(logger=__package__)
        super().set_config(cfg)
        registry = self.config.get('registry', REGISTRY)
        namespace = self.config.get('namespace')
        cfg_metrics = self.config.get('metrics', {})
        for attr, params in cfg_metrics.items():
            kw = dict(params)
            kw.setdefault('name', attr)
            cls = self.METRICS[kw.pop('type', 'gauge')]
            kw['registry'] = get_registry(kw.get('registry', registry))
            kw.setdefault('namespace', namespace)
            metric = cls(**kw)
            setattr(self, attr, metric)
