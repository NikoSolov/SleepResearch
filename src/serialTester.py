import config as cfg
import serial.tools.list_ports
import time

cfg.loadConfig()
config = cfg.getConfig()
print(config["general"]["timeStamps"])
portWork = True
portName = ""
ports = serial.tools.list_ports.comports()
timeCode = None
TRIGGER_ENABLE = config["general"]["timeStamps"]["trigger"]


def update():
    global timeCode, portName, portWork
    for port, desc, hwid in sorted(ports):
        if "USB-SERIAL CH340" in desc:
            portName = port
            print(portName)
    if portName == "":
        portWork = False
        return

    try:
        print("Connecting...")
        timeCode = None
        while timeCode is None:
            timeCode = serial.Serial(port=portName, baudrate=9600, timeout=.1)
        print("Connected")
    except Exception as e:
        portWork = False
        print(e)

update()



#
# for port, desc, hwind in sorted(ports):
#     print(port, desc)
#     if "USB2.0-Serial" in desc:
#         portName = port
#         print(portName)
#     if portName == "":
#         portWork = False
#         print("Don't found")
# print("init..")
#
# try:
#     timeCode = serial.Serial(port = portName, baudrate=9600, timeout=.1)
#     time.sleep(2)
# except Exception as e:
#     print(e)
#
#
# while True:
#     value = int.from_bytes(timeCode.read(), "big")
#     if value == 0:
#         print("-")
#     else:
#         print(value)