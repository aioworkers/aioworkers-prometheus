import os
from pathlib import Path

try:
    from .version import __version__
except ImportError:
    __version__ = 'dev'

MULTIPROC_DIR = os.environ.get('prometheus_multiproc_dir')
BASE = Path(__file__).parent

configs = (
    BASE / 'config.ini',
)
