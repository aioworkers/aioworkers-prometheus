from multiprocessing import Queue
from typing import Tuple, Type

from prometheus_client import metrics

INC = 'inc'
DEC = 'dec'
SET = 'set'
OBSERVE = 'observe'
INFO = 'info'
STATE = 'state'

METHODS = [
    INC,
    DEC,
    SET,
    OBSERVE,
    INFO,
    STATE,
]
CODE = {v: k for k, v in enumerate(METHODS)}


class QueueMetric:
    fork = False
    _name: str
    _labelvalues: Tuple
    _queue: Queue
    _mid: int

    def __init__(self, *args, mid: int, queue: Queue, **kwargs):
        self._queue = queue
        self._mid = mid
        super().__init__(*args, **kwargs)  # type: ignore

    @classmethod
    def factory(cls, klass: Type[metrics.MetricWrapperBase]):
        return type(str(cls.__name__), (cls, klass), {})

    def send_msg(self, method, value):
        msg = self._mid, self._labelvalues, method, value
        self._queue.put(msg)

    def from_msg(self, labelvalues, method, value):
        m = self
        if labelvalues:
            m = m.labels(*labelvalues)
        getattr(m, METHODS[method])(value)

    def inc(self, amount=1):
        if self.fork:
            self.send_msg(CODE[INC], amount)
        else:
            super().inc(amount)

    def dec(self, amount=1):
        if self.fork:
            self.send_msg(CODE[DEC], amount)
        else:
            super().dec(amount)

    def set(self, amount=1):
        if self.fork:
            self.send_msg(CODE[SET], amount)
        else:
            super().set(amount)

    def observe(self, amount=1):
        if self.fork:
            self.send_msg(CODE[OBSERVE], amount)
        else:
            super().observe(amount)

    def info(self, val):
        if self.fork:
            self.send_msg(CODE[INFO], val)
        else:
            super().info(val)

    def state(self, state):
        if self.fork:
            self.send_msg(CODE[STATE], state)
        else:
            super().state(state)


Counter = QueueMetric.factory(metrics.Counter)
Summary = QueueMetric.factory(metrics.Summary)
Histogram = QueueMetric.factory(metrics.Histogram)
Gauge = QueueMetric.factory(metrics.Gauge)
Info = QueueMetric.factory(metrics.Info)
Enum = QueueMetric.factory(metrics.Enum)
