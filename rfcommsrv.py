import bluetooth

hostMACAddress = '00:1A:7D:DA:71:13'
port = 3333
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)

while True:
    client, clientInfo = s.accept()
    try:
        while True:
            data = client.recv(size)
            if data:
                print(data)
                client.send(data)
    except:
        print("Closing socket")
        client.close()
s.close()
