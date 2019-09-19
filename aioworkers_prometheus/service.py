from aioworkers.core.base import AbstractEntity
from prometheus_client import start_http_server


class Service(AbstractEntity):
    """Thread service"""

    def set_config(self, config):
        port = config.get_int('port', default=0)
        if port:
            start_http_server(port=port)
        super().set_config(config)
