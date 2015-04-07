Plug your Bluetooth USB dongle into your machine and check that it is recognized.

From the Linux command line, run 'lsusb'.

root@dev:/home# lsusb
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. 
Bus 001 Device 004: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)

You should see a line containing 'Bluetooth Dongle' among the listed devices.
If not, reboot your machine, log in and run 'dmesg | grep usb' looking for USB-related issues.

Install the Bluetooth stack, utilities and library:
sudo apt-get install libbluetooth-dev bluez-utils

The Bluetooth daemon will automatically start upon installation.

Check that a Bluetooth device has been registered using 'hciconfig'.
The output should look like this:

root@dev:/home# hciconfig
hci0:	Type: BR/EDR  Bus: USB
	BD Address: 00:1A:7D:DA:71:13  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING PSCAN 
	RX bytes:1449 acl:0 sco:0 events:69 errors:0
	TX bytes:1328 acl:0 sco:0 commands:69 errors:0


Ensure that the Bluetooth device is discoverable and identifiable from another Bluetooth-enabled system with 'hciconfig hci0 piscan'
You may want to make the device permanently discoverable by adding 'hciconfig hci0 piscan' to the '/etc/rc.local' file right before the 'exit 0' statement at the end of the script. 

Validate with 'hciconfig' again. The interface for the interface 'hci0' should now reflect the following:

root@dev:/home# hciconfig
hci0:	Type: BR/EDR  Bus: USB
	BD Address: 00:1A:7D:DA:71:13  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING PSCAN ISCAN 
	RX bytes:1462 acl:0 sco:0 events:71 errors:0
	TX bytes:1335 acl:0 sco:0 commands:71 errors:0


Don't enable the 'auth' option at this stage. Remove it with 'hciconfig hci0 noauth' if it is enabled.
Leaving the 'auth' option will cause errors such as 'Bluetooth Error: (52, 'Invalid exchange')' later as the demo code doesn't deal with authentication.

To ensure that all is well, ping the Bluetooth MAC address of the Raspberry Pi using 'sudo l2ping 00:1A:7D:DA:71:13' from another Bluetooth-capable system.
Of course, replace the MAC address passed to the 'l2ping' command with the one returned by 'hciconfig hci0' on the line starting with 'BD Address'.

Install the Python 2.7 development environment, as needed:
sudo apt-get install python-dev

Switch to the /home directory of the machine (or any other that you like).
Install PyBluez, the Bluetooth Python module.
  
cd /home
wget http://pybluez.googlecode.com/files/PyBluez-0.18.tar.gz
gunzip PyBluez-0.18.tar.gz
tar -xf PyBluez-0.18.tar
rm PyBluez-0.18.tar
cd PyBluez-*
python setup.py install

Repeat this procedure on the client & servers machines where Bluetooth python code will be running.

Once the PyBluez module is compiled and installed where needed, test the sample client / server code that make use of it.
Note that the client and the server can run on any Bluetooth-capable system.
In addition, the role of the machines can be switched at any time.

* make bt.py executable.

chmod +x bt.py

* Run the server

root@dev:/home# ./bt.py server

The server will initializes itself with a message showing the MAC address of the first Bluetooth dongle it found:

Listening for connections on: 00:1A:7D:DA:71:13

* Run the client on another bluetooth-capable machine.

chmod +x bt.py

$ ./bt.py client
BT Discovery...
BT device name: dev-0, MAC: 00:1A:7D:DA:71:13
Connecting to first BT device found: dev-0, MAC: 00:1A:7D:DA:71:13
Connected... Enter data or 'exit' to terminate the connection.

The client starts by searching for a Bluetooth device and attempts to connect to the first one it finds.


BT Discovery...
BT device name: dev-0, MAC: 00:1A:7D:DA:71:13
Connecting to first BT device found: dev-0, MAC: 00:1A:7D:DA:71:13
Connected... Enter data or 'exit' to terminate the connection.
Hi there!
How is it going?
Well... bye!
exit

References:

An Introduction to Bluetooth Programming
http://people.csail.mit.edu/albert/bluez-intro/

Bluetooth Programming with Python 3
http://blog.kevindoran.co/bluetooth-programming-with-python-3/

pybluez
https://code.google.com/p/pybluez/

hcitool, auth, rfcomm, obexftp usage notes:
http://www.pizzhacks.com/bugdrome/2010/12/bluetooth-applications-in-gnulinux-notes/
http://www.computersolutions.cn/blog/2012/03/bluetooth-notes-for-debian-linux/

