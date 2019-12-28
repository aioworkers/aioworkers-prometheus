import logging
from functools import lru_cache

from prometheus_client import registry

REGISTRY = 'REGISTRY'

logger = logging.getLogger('aioworkers_prometheus')


@lru_cache(None)
def get_registry(name: str = REGISTRY) -> registry.CollectorRegistry:
    if name == REGISTRY:
        return registry.REGISTRY
    else:
        return registry.CollectorRegistry(auto_describe=True)
