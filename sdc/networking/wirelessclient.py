
import dbus
from .wificapability import WifiCapability
from .apsecurityflag import APSecurityFlag
from .apmode import APModeFlag
from .apflag import APFlag
from .client import NetworkingClient
import time

class WirelessClient:
    def __init__(self, bus, device):
        self.lastScan = -1
        self.bus = bus
        self.device = device
        self.networkingClient = NetworkingClient(bus)
    def getDeviceProxy(self):
        return self.bus.get_object("org.freedesktop.NetworkManager", self.device["devicePath"])

    def getDeviceName(self):
        dev_proxy = self.getDeviceProxy()
        iface = dbus.Interface(dev_proxy, "org.freedesktop.NetworkManager.Device")
        prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        return prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")

    def getConnections(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        connections = wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device", "AvailableConnections")
        conns = []
        for conn in connections:
            con_proxy = self.bus.get_object("org.freedesktop.NetworkManager", conn)
            settings_connection = dbus.Interface(
                    con_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
            )
            sett = settings_connection.GetSettings()
            uuid = sett["connection"]["uuid"]
            if(sett.get("802-11-wireless", None) and sett["802-11-wireless"].get("ssid", None)):
                sett["802-11-wireless"]["ssid"] = "".join(chr(x) for x in sett["802-11-wireless"]["ssid"])
            conns.append({"uuid": uuid, "path": conn, "settings": sett})
            
        return conns

         

    def addWifiConnection(self, ssid, password, uid, priority = 100, autoConnect = True):
        s_con = dbus.Dictionary({
            'type': '802-11-wireless',
            'uuid': uid,
            'id': ssid,
            "autoconnect-priority": dbus.Int32(priority),
            "autoconnect": dbus.Boolean(autoConnect),
            'interface-name': self.getDeviceName()
        })

        s_wifi = dbus.Dictionary({
            'ssid': dbus.ByteArray(ssid.encode("utf8")),
            'mode': 'infrastructure',
            'hidden': dbus.Boolean(True),
        })

        s_wsec = dbus.Dictionary({
            'key-mgmt': 'wpa-psk',
            'auth-alg': 'open',
            'psk': password,
        })

        s_ip4 = dbus.Dictionary({'method': 'auto'})
        s_ip6 = dbus.Dictionary({'method': 'auto'})

        con = dbus.Dictionary({
            'connection': s_con,
            '802-11-wireless': s_wifi,
            '802-11-wireless-security': s_wsec,
            'ipv4': s_ip4,
            'ipv6': s_ip6
        })



        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
        settings.AddConnection(con)


    def getWiFiIface(self):
        dev_proxy = self.getDeviceProxy()
        wifi_iface = dbus.Interface(dev_proxy, "org.freedesktop.NetworkManager.Device.Wireless")
        wifi_prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        return wifi_iface, wifi_prop_iface

    def addHotspot(self, ssid, password, uid, priority=100, autoConnect = True):
        s_con = dbus.Dictionary({
            'type': '802-11-wireless',
            'uuid': uid,
            'id': ssid,
            "autoconnect-priority": dbus.Int32(priority),
            "autoconnect": dbus.Boolean(autoConnect),
            'interface-name': self.getDeviceName()
        })

        s_wifi = dbus.Dictionary({
            'ssid': dbus.ByteArray(ssid.encode("utf8")),
            'mode': 'ap',
            'band': 'bg',
            'hidden': dbus.Boolean(False),
        })

        s_wsec = dbus.Dictionary({
            'key-mgmt': 'wpa-psk',
            'auth-alg': 'open',
            'psk': password
        })

        addr1 = dbus.Dictionary({"address": "111.111.111.1", "prefix": dbus.UInt32(24)})
        s_ip4 = dbus.Dictionary({
            'method': 'shared',
            "address-data": dbus.Array([addr1], signature=dbus.Signature("a{sv}")),
            "gateway": "111.111.111.1"

        })
        s_ip6 = dbus.Dictionary({'method': 'ignore'})

        con = dbus.Dictionary({
            'connection': s_con,
            '802-11-wireless': s_wifi,
            '802-11-wireless-security': s_wsec,
            'ipv4': s_ip4,
            'ipv6': s_ip6,
        })

        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
        settings.AddConnection(con)

    def getLastScanOfWireless(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        lastScan = wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device.Wireless", "LastScan")
        return lastScan

    def getWirelessCapabilities(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        return WifiCapability.getAllFlagsFor(wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device.Wireless", "WirelessCapabilities"))
        

    def isCurrentConnectionHotSpot(self):
        currentUuid = self.getCurrentConnectionUuid()
        if(currentUuid == None):
            return False
        byUuid = self.networkingClient.getConnectionByUuid(currentUuid)
        if(byUuid):
            settings = byUuid["settings"]
            if(settings.get("802-11-wireless", None)):
                wirelessConfig = settings["802-11-wireless"]
                if(wirelessConfig.get("mode", None)):
                    mode = wirelessConfig["mode"]
                    return mode == "ap"
        else:
            return False

    def scanAndWait(self):
        lastScan = self.getLastScanOfWireless()
        oldLastScan = lastScan
        self.requestWirelessScan()
        while oldLastScan == lastScan:
            time.sleep(0.1)
            lastScan = self.getLastScanOfWireless()
        aps = self.getAccessPoints()
        return aps


    def scanInAccessPointMode(self):
        if(self.isCurrentConnectionHotSpot()):
            uuidOf = self.getCurrentConnectionUuid()
            self.deactivateCurrentConnection()
            aps = self.scanAndWait()
            self.activateConnectionByUuid(uuidOf)
            return aps
        else:
            return self.scanAndWait()

    def requestWirelessScan(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
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
    
    def getCurrentConnection(self):
        wifi_iface, wifi_prop_iface = self.getWiFiIface()
        activeConnectionPath = wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device", "ActiveConnection")
        if(activeConnectionPath == "/"):
            return None
        return activeConnectionPath

    def getCurrentConnectionUuid(self):
        activeConnectionPath = self.getCurrentConnection()
        if(activeConnectionPath == None):
            return None
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", activeConnectionPath)
        conn = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        uuidOf = conn.Get("org.freedesktop.NetworkManager.Connection.Active", "Uuid")
        return uuidOf


    def deactivateCurrentConnection(self):
        activeConnectionPath = self.getCurrentConnection()
        if(activeConnectionPath != None):
            proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
            nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
            nm.DeactivateConnection(activeConnectionPath)
            return True
        else:
            return False

    
    def activateConnectionByUuid(self, uuid):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
        connPath = self.networkingClient.getConnectionPathByUuid(uuid)
        nm.ActivateConnection(dbus.String(connPath), self.device["devicePath"], "/")


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
            apNow["rsn"] = APSecurityFlag.getAllFlagsFor(RsnFlags)
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
            all_aps.append(apNow)
        return all_aps