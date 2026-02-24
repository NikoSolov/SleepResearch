from datetime import datetime
import serial.tools.list_ports
import config as cfg
from excelTools import ExcelTable

cfg.loadConfig()
config = cfg.getConfig()
print(config["general"]["timeStamps"])
portWork = True
portName = ""
ports = serial.tools.list_ports.comports()
timeCode = None
TRIGGER_ENABLE = config["general"]["timeStamps"]["trigger"]
logTable = None
logTablePageName = ""
loggerCount = 0
firstStamp = None
deltaTime = None

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
    global portWork, TRIGGER_ENABLE, loggerCount, logTable, logTablePageName, firstStamp, deltaTime
    if TRIGGER_ENABLE and portWork:
        timeCode.write(bytearray([number]))
        print(f"Send {number} as {bytearray([number])}")

    if logTable is not None:
        if deltaTime is not None:
            deltaTime = datetime.now() - firstStamp
            minutes = deltaTime.seconds // 60
            seconds = deltaTime.seconds % 60
            milliseconds = deltaTime.microseconds // 1000            

        logTable.writeDataToPage(logTablePageName, {
            f"A{loggerCount + 2}": datetime.now().strftime('%T.%f')[:-3],
            f"B{loggerCount + 2}": number,
            f"C{loggerCount + 2}": 
            "00:00.000" if deltaTime is None else  
            f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        })

        if firstStamp is None:
            firstStamp = datetime.now()
            deltaTime = datetime.now() - firstStamp

        loggerCount += 1


def close():
    if portWork:
        timeCode.close()
        print("COM-Port closed")

def update(Table: ExcelTable = None, Page: str = ""):
    global timeCode, portName, portWork, logTable, logTablePageName, loggerCount
    logTable = Table
    logTablePageName = Page
    loggerCount = 0
    if logTable is not None:
        logTable.writeDataToPage(logTablePageName, {
            "A1": "Time",
            "B1": "Stamp",
            "C1": "Delta"
        })
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
