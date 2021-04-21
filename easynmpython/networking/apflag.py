# from enum import Enum
from .byteflagenum import ByteFlagEnum
class APFlag(ByteFlagEnum):
    NONE = 0x0
    PRIVACY = 0x1
    WPS = 0x2
    WPS_PBC = 0x4
    WPS_PIN = 0x8
    