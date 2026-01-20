import time
import serial.tools.list_ports
import config as cfg
from enum import Enum

cfg.loadConfig()
config = cfg.getConfig()
print(config["general"]["timeStamps"])
portWork = True
portName = ""
ports = serial.tools.list_ports.comports()
timeCode = None
TRIGGER_ENABLE = config["general"]["timeStamps"]["trigger"]

class TimeStamp:
    alarm = 1
    startMouse = 2
    startTask = 3
    startPVT = 4
    circleAppear = 5
    userInput = 6
    startControl = 7
    endProgram = 8
    manualStamp = 9

def send(number: int):
    global portWork, TRIGGER_ENABLE
    if TRIGGER_ENABLE and portWork:
        timeCode.write(bytearray([number]))
        print(f"Send {number} as {bytearray([number])}")

def close():
    if portWork:
        timeCode.close()
        print("COM-Port closed")

def update():
    global timeCode, portName, portWork
    for port, desc, hwid in sorted(ports):
        print(port, desc)
        if "USB-SERIAL CH340" in desc:
            portName = port
            print(portName)
    if portName == "":
        portWork = False
        return

    try:
        print("Connecting...")
        while timeCode is None:
            timeCode = serial.Serial(port=portName, baudrate=9600, timeout=.1)
        print("Connected", portName)
    except Exception as e:
        portWork = False
        print(e)
