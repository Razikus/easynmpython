from enum import IntEnum 
class APModeFlag(IntEnum ):
    UNKNOWN = 0
    ADHOC = 1
    INFRA = 2
    AP = 3
    MESH = 4
    