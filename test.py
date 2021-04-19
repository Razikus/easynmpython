from sdc.networking.client import NetworkingClient
from sdc.networking.devicetype import DeviceType
from sdc.networking.wirelessclient import WirelessClient
from sdc.networking.wificapability import WifiCapability
import dbus
import json

bus = dbus.SystemBus()

a = NetworkingClient(bus)
wifiDevices = a.getDevicesViaType(DeviceType.WiFi)
wDevice = wifiDevices[0]
wireless = WirelessClient(bus, wDevice)
print(wireless.requestWirelessScan())
aps = (wireless.getAccessPoints())
print(json.dumps(aps))
# for ap in aps:
#     print(ap)
caps = wireless.getWirelessCapabilities()
print(caps)