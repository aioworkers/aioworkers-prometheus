import os
from pathlib import Path

try:
    # true
    from .version import __version__
except ImportError:
    __version__ = "0.0.0a"

MULTIPROC_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR")
if not MULTIPROC_DIR:
    MULTIPROC_DIR = os.environ.get("prometheus_multiproc_dir")

BASE = Path(__file__).parent

configs = (BASE / "config.ini",)
