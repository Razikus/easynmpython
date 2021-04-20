from enum import Enum
from .byteflagenum import ByteFlagEnum
class APSecurityFlag(ByteFlagEnum):
    NONE = 0x0
    PAIR_WEP40 = 0x1
    PAIR_WEP104 = 0x2
    PAIR_TKIP = 0x4
    PAIR_CCMP = 0x8
    GROUP_WEP40 = 0x10
    GROUP_WEP104 = 0x20
    GROUP_TKIP = 0x40
    GROUP_CCMP = 0x80
    KEY_MGMT_PSK = 0x100
    KEY_MGMT_802_1X = 0x200
    KEY_MGMT_SAE = 0x400
    KEY_MGMT_OWE = 0x800
    KEY_MGMT_OWE_TM = 0x1000
    KEY_MGMT_EAP_SUITE_B_192 = 0x2000
