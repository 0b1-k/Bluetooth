import bluetooth
import sys

class BT(object):
    def __init__(self):
        self.btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def __exit__(self):
        self.Disconnect()
        
    def Connect(self, mac, port= 3333):
        self.btSocket.connect((mac, port))

    def Disconnect(self):
        try:
            self.btSocket.close()
        except Exception:
            pass
        
    def Discover(self):
        btDevices = bluetooth.discover_devices(lookup_names = True)
        if (len(btDevices) > 0):
                return btDevices
        else:
            raise Exception('no BT device!')

    def DumpDevices(self, btDeviceList):
        for mac, name in btDeviceList:
            print("BT device name: {0}, MAC: {1}".format(name, mac))
    
    def BindListen(self, mac, port=3333, backlog=1):
        self.btSocket.bind((mac, port))
        self.btSocket.listen(backlog)
        
    def Accept(self):
        client, clientInfo = self.btSocket.accept()
        return client, clientInfo
        
    def Send(self, data):
        self.btSocket.send(data)
        
    def Receive(self, size=1024):
        return self.btSocket.recv(size)
        
    
def StartBTClient():
    cli = BT()
    print('BT Discovery...')
    btDeviceList = cli.Discover()
    cli.DumpDevices(btDeviceList)
    mac = btDeviceList[0][0]
    name = btDeviceList[0][1]
    print('Connecting to first BT device found: {0}, MAC: {1}'.format(name, mac))
    cli.Connect(mac)
    print('Connected... Enter data or \'exit\' to terminate the connection.')
    while True:
        data = raw_input()
        if (data == 'exit'):
            break
        cli.Send(data)
    cli.Disconnect()

def GetFirstMAC():
    return '00:1A:7D:DA:71:13'

def StartBTServer():
    srv = BT()
    srv.BindListen(GetFirstMAC())    
    while True:
        client, clientInfo = srv.Accept()
        try:
            while True:
                data = srv.Receive()
                if (data is not None):
                    print(data)
                    client.Send(data)
        except:
            print("Closing socket")
        client.Disconnect()
    srv.Disconnect()

if __name__ == '__main__':
    cmd = sys.argv[1]
    if (cmd == 'server'):
        StartBTServer()
    elif (cmd == 'client'):
        StartBTClient()
    else:
        print("Bluetooth RFCOMM client/server demo")
        print("Copyright 2014 Nwazet, LLC.")
        print("Please specify 'client' or 'server'")
