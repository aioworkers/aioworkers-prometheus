from typing import Optional, cast

from aioworkers.core.base import ExecutorEntity
from aioworkers.core.config import ValueExtractor
from prometheus_client import CollectorRegistry
from prometheus_client.bridge.graphite import GraphiteBridge
from prometheus_client.exposition import generate_latest, start_http_server
from prometheus_client.multiprocess import MultiProcessCollector

from aioworkers_prometheus import MULTIPROC_DIR
from aioworkers_prometheus.registry import REGISTRY, LabelsRegistry, get_registry


class Service(ExecutorEntity):
    _registry: CollectorRegistry

    def set_config(self, config: ValueExtractor) -> None:
        super().set_config(config)
        registry = get_registry(self.config.get("registry", REGISTRY))
        if MULTIPROC_DIR:
            MultiProcessCollector(registry)
        labels = self.config.get("labels")
        if labels:
            registry = cast(
                CollectorRegistry,
                LabelsRegistry(
                    registry=registry,
                    labels=labels,
                ),
            )
        self._registry = registry

        port: int = self.config.get_int("port", default=0)
        if port:
            start_http_server(port=port, registry=registry)

        graphite: Optional[ValueExtractor] = self.config.get("graphite")
        if graphite:
            address = graphite.get("address")
            if isinstance(address, str):
                addr = address.split(":")
                address = (addr[0], int(addr[-1]))
            gb = GraphiteBridge(address, registry=registry)
            interval: float = graphite.get_duration("interval", 60)
            prefix: str = graphite.get("prefix", "")
            gb.start(interval, prefix=prefix)

    async def generate_latest(self) -> bytes:
        return await self.run_in_executor(generate_latest, self._registry)
