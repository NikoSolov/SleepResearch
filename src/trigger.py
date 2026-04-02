from datetime import datetime
import serial.tools.list_ports
import config as cfg
from excelTools import ExcelTable
from icecream import ic

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

class Trigger():
    def __init__(self):
        cfg.loadConfig()
        config = cfg.getConfig()
        print(config["general"]["timeStamps"])
        self.portWork = False
        self.portName = ""
        self.timeCode = None
        self.TRIGGER_ENABLE = config["general"]["timeStamps"]["trigger"]
        self.logTable = None
        self.logTablePageName = ""
        self.loggerCount = 0
        self.firstStamp = None
        self.deltaTime = None

    def test(self):
        if self.portWork and self.timeCode.is_open:
            ic("triggerTest")
            try:
                self.timeCode.write(bytearray('Trigger Test!', "ascii"))
                ic(f"Send Trigger Test!")
            except serial.serialutil.SerialException as e:
                ic(e)
                self.close()
                return

    def send(self, number: int):
        if self.TRIGGER_ENABLE and self.portWork and self.timeCode.is_open:
            ic("triggerSend")
            try:
                self.timeCode.write(bytearray([number]))
                ic(f"Send {number} as {bytearray([number])}")
            except serial.serialutil.SerialException as e:
                ic(e)
                self.close()
                return

        if self.logTable is not None:
            if self.deltaTime is not None:
                self.deltaTime = datetime.now() - self.firstStamp
                minutes = self.deltaTime.seconds // 60
                seconds = self.deltaTime.seconds % 60
                milliseconds = self.deltaTime.microseconds // 1000            

            self.logTable.writeDataToPage(self.logTablePageName, {
                f"A{self.loggerCount + 2}": number,
                f"B{self.loggerCount + 2}": datetime.now().strftime('%T.%f')[:-3],
                f"C{self.loggerCount + 2}": 
                "00:00.000" if self.deltaTime is None else  
                f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
            })

            if self.firstStamp is None:
                self.firstStamp = datetime.now()
                self.deltaTime = datetime.now() - self.firstStamp

            self.loggerCount += 1


    def close(self):
        if self.timeCode is not None and self.timeCode.is_open:        
            self.timeCode.close()
            self.portWork = False
            self.portName = ""
            ic("COM-Port closed")

    def update(self, Table: ExcelTable = None, Page: str = ""):
        self.logTable = Table
        self.logTablePageName = Page
        self.loggerCount = 0
        if self.logTable is not None:
            self.logTable.writeDataToPage(self.logTablePageName, {
                "A1": "Stamp",
                "B1": "Time",
                "C1": "Delta"
            })

        self.close()
        for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
            ic(port, desc)
            if "USB-SERIAL CH340" in desc:
                self.portName = port
        if self.portName == "": return

        try:
            ic("Connecting to", self.portName)
            while self.timeCode is None:
                self.timeCode = serial.Serial(port=self.portName, baudrate=9600, timeout=.1)
            if not self.timeCode.is_open: self.timeCode.open()
            ic("Connected", self.portName, self.timeCode.is_open)
            self.portWork = True
        except Exception as e:
            ic(e)
