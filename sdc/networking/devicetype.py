from enum import Enum
class DeviceType(Enum):
    Unknown = 0
    Generic = 14
    Ethernet = 1
    WiFi = 2
    Unused1 = 3
    Unused2 = 4
    BT = 5
    OLPC_Mesh = 6
    WIMAX = 7
    MODEM = 8
    InfiniBand = 9
    Bond = 10
    VLAN = 11
    ADSL = 12
    Bridge = 13
    Team = 15
    TUN = 16
    IP_TUNNEL = 17
    MACVLAN = 18
    VXLAN = 19
    VETH = 20
    MACSEC = 21
    Dummy = 22
    PPP = 23
    OVS_Interface = 24
    OVS_Port = 25
    OVS_Bridge = 26
    WPAN = 27
    SixLowPan = 28
    Wireguard = 29
    WiFi_P2P = 30
    VRF = 31