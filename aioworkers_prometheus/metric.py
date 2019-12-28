from aioworkers.core.base import LoggingEntity
from prometheus_client import metrics

# true
from .registry import REGISTRY, get_registry


class Metric(LoggingEntity):
    METRICS = dict(
        counter=metrics.Counter,
        enum=metrics.Enum,
        gauge=metrics.Gauge,
        histogram=metrics.Histogram,
        info=metrics.Info,
        summary=metrics.Summary,
    )

    def set_config(self, config):
        cfg = config.new_parent(logger='aioworkers_prometheus')
        super().set_config(cfg)
        registry = self.config.get('registry', REGISTRY)
        namespace = self.config.get('namespace')
        metrics = self.config.get('metrics', {})
        for attr, params in metrics.items():
            kw = dict(params)
            kw.setdefault('name', attr)
            cls = self.METRICS[kw.pop('type', 'gauge')]
            kw['registry'] = get_registry(kw.get('registry', registry))
            kw.setdefault('namespace', namespace)
            metric = cls(**kw)
            setattr(self, attr, metric)
