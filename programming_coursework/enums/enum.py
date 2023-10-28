from enum import unique

from .auto_recognizable_str_enum import AutoCheckRecognizableStrEnum


@unique
class MarketTrend(AutoCheckRecognizableStrEnum):
    VOLATILE = 'volatile'
    INCREASING = 'increasing'
    DECREASING = 'decreasing'
    OTHER = 'other'
