from pathlib import Path

try:
    from .version import __version__
except ImportError:
    __version__ = 'dev'

BASE = Path(__file__).parent

configs = (
    BASE / 'config.ini',
)
