""" Boundary Element Method package BEM++ """
__all__ = [
    'Grid', 'config', '__version__', 'Options', 'space', 'scalar_space',
    'assembly', 'Context'
]

from .grid import Grid
from . import space
from . import assembly
from .assembly import Context
from .space import scalar as scalar_space
from . import config
from .options import Options
# A fair number of packages expose version info via similar variable
from .config import version as __version__
