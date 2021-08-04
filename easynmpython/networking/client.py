import dbus 
from .devicetype import DeviceType

class NetworkingClient:
    def __init__(self, bus):
        self.bus = bus  


    def getConnections(self):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
        conns = []
        for conn in settings.ListConnections():
            con_proxy = self.bus.get_object("org.freedesktop.NetworkManager", conn)
            settings_connection = dbus.Interface(
                    con_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
            )
            sett = settings_connection.GetSettings()
            uuid = sett["connection"]["uuid"]
            conns.append({"uuid": uuid, "path": conn, "settings": sett})
        return conns

    def disableWireless(self):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        prop_iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        prop_iface.Set("org.freedesktop.NetworkManager", "WirelessEnabled", dbus.Boolean(False))

    
    def enableWireless(self):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        prop_iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        prop_iface.Set("org.freedesktop.NetworkManager", "WirelessEnabled", dbus.Boolean(True))



    def getConnectionByUuid(self, uuidToSearch):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
        conns = []
        conn = settings.GetConnectionByUuid(uuidToSearch)
        con_proxy = self.bus.get_object("org.freedesktop.NetworkManager", conn)
        settings_connection = dbus.Interface(
                con_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
        )
        sett = settings_connection.GetSettings()
        uuid = sett["connection"]["uuid"]
        return {"uuid": uuid, "path": conn, "settings": sett}
    
    def getConnectionPathByUuid(self, uuid):
        conns = self.getConnections()
        for conn in conns:
            if(conn["uuid"] == uuid):
                return conn["path"]
        return None

    def deactivateConnectionByUuid(self, uuid):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
        connPath = self.getConnectionPathByUuid(uuid)
        nm.DeactivateConnection(connPath)
    
    def getActiveConnections(self):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        AC = proxy.Get("org.freedesktop.NetworkManager", "ActiveConnections", dbus_interface=dbus.PROPERTIES_IFACE)
        conns = []
        for activeConn in AC:
            pather = self.bus.get_object("org.freedesktop.NetworkManager", activeConn)
            uuid = pather.Get("org.freedesktop.NetworkManager.Connection.Active", "Uuid", dbus_interface=dbus.PROPERTIES_IFACE)
            conns.append({"uuid": uuid, "path": activeConn})
        return conns

    def getActiveConnectionsWithDescription(self):
        acs = self.getActiveConnections()
        for ac in acs:
            desc = self.getConnectionByUuid(ac["uuid"])
            ac["description"] = desc
        return acs

    
    def isConnectionActivated(self, uuid):
        activated = self.getActiveConnections()
        for active in activated:
            if(uuid == str(active["uuid"])):
                return True, active["path"]
        return False, None

    def getDevices(self):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
        ret = []
        for device in manager.GetDevices():
            ret.append(device)
        return ret

    def getDevicesWithDescription(self):
        devices = self.getDevices()
        ret = []
        for device in devices:
            dev_proxy = self.bus.get_object("org.freedesktop.NetworkManager", device)
            prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
            iface = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
            dtype = prop_iface.Get("org.freedesktop.NetworkManager.Device", "DeviceType")
            state = prop_iface.Get("org.freedesktop.NetworkManager.Device", "State")
            ret.append({
                "name": str(iface), 
                "type": DeviceType(dtype),
                "state": int(state),
                "devicePath": str(device)
            })
        return ret

    
    def getDevicesViaType(self, deviceType):
        devices = self.getDevicesWithDescription()
        ret = []
        for device in devices:
            if(device["type"] == deviceType):
                ret.append(device)
        return ret



 

