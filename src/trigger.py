import time
import serial.tools.list_ports
import config as cfg
import pygame as pg

cfg.loadConfig()
config = cfg.getConfig()
print(config["general"]["timeStamps"])
portWork = True
portName = ""
ports = serial.tools.list_ports.comports()
timeCode = None
TRIGGER_ENABLE = config["general"]["timeStamps"]["trigger"]

def triggerRoutine(program, event):
    match(program):
        case "Control":
            if event.type == pg.MOUSEBUTTONDOWN:
                send(6)
        case "PVT":
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                send(9)
                print("Manual Stamp")
        case _:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                send(9)
                print("Manual Stamp")

def send(number: int):
    global portWork, TRIGGER_ENABLE
    if TRIGGER_ENABLE and portWork:
        timeCode.write(bytearray([number]))

def close():
    if portWork:
        timeCode.close()

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
        while timeCode is None:
            timeCode = serial.Serial(port=portName, baudrate=9600, timeout=.1)
        print("Connected")
    except Exception as e:
        portWork = False
        print(e)
