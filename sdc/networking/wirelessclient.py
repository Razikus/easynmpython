
import dbus
from .wificapability import WifiCapability
from .apsecurityflag import APSecurityFlag
from .apmode import APModeFlag
from .apflag import APFlag

class WirelessClient:
    def __init__(self, bus, device):
        self.lastScan = -1
        self.bus = bus
        self.device = device
    def getDeviceProxy(self):
        return self.bus.get_object("org.freedesktop.NetworkManager", self.device["devicePath"])

    def getWiFiIface(self):
        dev_proxy = self.getDeviceProxy()
        wifi_iface = dbus.Interface(dev_proxy, "org.freedesktop.NetworkManager.Device.Wireless")
        wifi_prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        return wifi_iface, wifi_prop_iface


    def getLastScanOfWireless(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        lastScan = wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device.Wireless", "LastScan")
        return lastScan

    def getWirelessCapabilities(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        return WifiCapability.getAllFlagsFor(wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device.Wireless", "WirelessCapabilities"))
        
        


    def requestWirelessScan(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        lastScan = wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device.Wireless", "LastScan")
        try:
            wifi_iface.RequestScan({})
            return True
        except dbus.exceptions.DBusException as e:
            if(e.get_dbus_message() == "Scanning not allowed immediately following previous scan"):
                return False
            elif(e.get_dbus_message() == "Scanning not allowed while already scanning"):
                return False
            else:
                raise e

    def getAccessPoints(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        aps = wifi_iface.GetAccessPoints()
        all_aps = []
        for path in aps:
            apNow = dict()
            ap_proxy = self.bus.get_object("org.freedesktop.NetworkManager", path)
            ap_prop_iface = dbus.Interface(ap_proxy, "org.freedesktop.DBus.Properties")
            Flags = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "Flags"
            )
            apNow["flags"] = APFlag.getAllFlagsFor(Flags)
            WpaFlags = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "WpaFlags"
            )
            apNow["wpa"] = APSecurityFlag.getAllFlagsFor(WpaFlags)

            RsnFlags = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "RsnFlags"
            )
            apNow["rsn"] = APSecurityFlag.getAllFlagsFor(WpaFlags)
            Ssid = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "Ssid"
            )
            joined = "".join([chr(x) for x in Ssid])
            apNow["ssid"] = joined
            Frequency = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "Frequency"
            )
            apNow["frequency"] = str(Frequency)
            HwAddress = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "HwAddress"
            )
            apNow["bssid"] = str(HwAddress)
            Mode = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "Mode"
            )
            apNow["mode"] = APModeFlag(Mode)
            MaxBitrate = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "MaxBitrate"
            )
            apNow["maxbitrate"] = str(MaxBitrate)
            Strength = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "Strength"
            )
            apNow["strength"] = int(Strength)
            LastSeen = ap_prop_iface.Get(
                "org.freedesktop.NetworkManager.AccessPoint", "LastSeen"
            )
            apNow["lastSeen"] = int(LastSeen)
            print(joined, WpaFlags)
            all_aps.append(apNow)
            

            
        return all_aps