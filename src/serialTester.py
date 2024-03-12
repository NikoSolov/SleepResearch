import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
portName = ""

for port, desc, hwind in sorted(ports):
    print(port, desc)
    if "USB2.0-Serial" in desc:
        portName = port
        print(portName)
    if portName == "":
        portWork = False
        print("Don't found")
print("init..")

try:
    timeCode = serial.Serial(port = portName, baudrate=9600, timeout=.1)
    time.sleep(2)
except Exception as e:
    print(e)


while True:
    value = int.from_bytes(timeCode.read(), "big")
    if value == 0:
        print("-")
    else:
        print(value)