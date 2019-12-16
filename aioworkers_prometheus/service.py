from aioworkers.core.base import AbstractEntity
from prometheus_client.bridge.graphite import GraphiteBridge
from prometheus_client.exposition import start_http_server

# true
from .registry import REGISTRY, get_registry


class Service(AbstractEntity):
    def set_config(self, config):
        super().set_config(config)
        registry = get_registry(self.config.get('registry', REGISTRY))

        port = self.config.get_int('port', default=0)
        if port:
            start_http_server(port=port, registry=registry)

        graphite = self.config.get('graphite')
        if graphite:
            address = graphite.get('address')
            if isinstance(address, str):
                addr = address.split(':')
                address = (addr[0], int(addr[-1]))
            gb = GraphiteBridge(address, registry=registry)
            interval = graphite.get_duration('interval', 60)
            prefix = graphite.get('prefix', '')
            gb.start(interval, prefix=prefix)
