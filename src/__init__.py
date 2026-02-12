"""
Package MapsCut - Application de découpage d'images géoréférencées
"""

__version__ = "1.0.0"
__author__ = "MapsCut Development Team"

from .raster_processing import RasterProcessor
from .cutting import PageCutter
from .export import Exporter
from .interface import MainWindow

__all__ = ['RasterProcessor', 'PageCutter', 'Exporter', 'MainWindow']
