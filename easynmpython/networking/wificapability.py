from .byteflagenum import ByteFlagEnum
class WifiCapability(ByteFlagEnum):
    NONE = 0x0
    WEP40 = 0x1
    WEP104 = 0x2
    TKIP = 0x4
    CCMP = 0x8
    WPA = 0x10
    RSN = 0x20
    AP = 0x40
    ADHOC = 0x80
    FREQ_VALID = 0x100
    FREQ_2GHZ = 0x200
    FREQ_5GHZ = 0x400
    MESH = 0x1000
    IBSS_RSN = 0x2000
    