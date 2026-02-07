"""Page components package"""
from . import *
"""Page registry - makes all pages importable"""
from .dashboard import Dashboard
from .prediction import Prediction
from .batch import Batch
from .metrics import Metrics
from .insights import Insights

__all__ = ['Dashboard', 'Prediction', 'Batch', 'Metrics', 'Insights']

