from enum import Enum


class TimeResolutionUnitEnum(str, Enum):
    SECOND = "second"
    HOUR = "hour"
    DAILY = "day"
    WEEKLY = "week"
