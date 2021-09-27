from easynmpython.networking.client import NetworkingClient
from easynmpython.networking.devicetype import DeviceType
from easynmpython.networking.wirelessclient import WirelessClient
from easynmpython.networking.wificapability import WifiCapability
import dbus
import json
import uuid

bus = dbus.SystemBus()

a = NetworkingClient(bus)
wifiDevices = a.getDevicesViaType(DeviceType.WiFi)
wDevice = wifiDevices[0]
wireless = WirelessClient(bus, wDevice)
# print(wireless.requestWirelessScan())
# aps = (wireless.getAccessPoints())
# print(json.dumps(aps))
uuider = "3fb431e3-250e-4bc2-886e-d8705ea25661"
# try:
#     wireless.addHotspot("testowy3", "XXXXXXXXXXX", uuider)
# except:
#     pass

# try:
#     wireless.addWifiConnection("XX", "XX", str(uuid.uuid4()))
# except:
#     pass
# wireless.activateConnectionByUuid(uuider)
# for ap in aps:
#     print(ap)
# caps = wireless.getWirelessCapabilities()
# print(caps)
# wireless.deactivateCurrentConnection()
# print(wireless.isCurrentConnectionHotSpot())
#   
# print(aps)
# print(wireless.getDeviceName())
# print(json.dumps(wireless.getConnections()))
assert wireless.getAssociatedIpAddress() != None