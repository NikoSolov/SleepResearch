import time
from enum import Enum, auto
from random import uniform as rd
import config as cfg
from lightSensor import LightSensor
from alarm import Alarm
from trigger import Trigger, TimeStamp
from excelTools import ExcelTable
from timer import Timer
from graphics import Graphics, GraphicsEvents

def run():
    # ======== Load Configs ====================
    cfg.loadConfig()
    config = cfg.getConfig()
    # ------------------------------
    ROUND = config["PVT"]["experiment"]["round"]
    SUBJECT_NAME = config["general"]["experiment"]["name"]
    SUBJECT_code = config["general"]["experiment"]["code"]
    # ------------------------------
    DELAYS = config["PVT"]["delay"]
    MSI_TIME = DELAYS["msi"]
    PLUS_TIME = DELAYS["plus"]
    ANSWER_TIME = DELAYS["answer"]
    emptyTime = lambda: rd(DELAYS["emptyMin"], DELAYS["emptyMax"])
    # ------------------------------
    DIR_NAME = f'{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}_PVT_{time.strftime("%H.%M.%S")}'
    # ======== Initialization ====================
    # -------------------
    lightSensor = LightSensor()
    PVTGraphics = Graphics("PVT", lightSensor)

    # --------- Setting up SpreadSheet -------
    PVTTable = ExcelTable("result", f"{DIR_NAME}.xlsx")
    PVTTable.createPage("MainLog")
    PVTTable.createPage("TimeStamps")

    PVTTable.writeDataToPage("MainLog", {
        "A1:A2": "Round",
        "B1:E1": "First Reaction",
        "B2":    "EmptyTime",
        "C2":    "FalseAnswer",
        "D2":    "RightAnswer",
        "E2":    "at MSI?",
    })

    trigger = Trigger()
    trigger.update(PVTTable, "TimeStamps")
    alarm = Alarm(trigger)

    # --------- Vars ----------
    class Event(Enum):
        Siren  = auto()
        StartTrail = auto()
        Plus   = auto()
        Empty  = auto()
        Circle = auto()
        MSI    = auto()

    run = True
    status = Event.Siren
    currentEmptyTime = emptyTime()
    roundCounter = 0
    reactions = {
        "wrongAnswer": None,
        "rightAnswer": None,
        "MSI": False
    }
    # --------------

    stageTimer = Timer()

    while run:
        events = PVTGraphics.get_events()
        if GraphicsEvents.windowClose in events:
            run = False
        if GraphicsEvents.spacePressed in events:
            trigger.send(TimeStamp.manualStamp)
        if GraphicsEvents.mousePressed in events:
            print("Clicked")
            trigger.send(TimeStamp.userInput)
            if (
                (status == Event.Plus or status == Event.Empty)
                    and reactions["wrongAnswer"] is None
            ):
                reactions["wrongAnswer"] = stageTimer.getDelta()
                stageTimer.setTimer()
                status = Event.MSI

            elif (
                (status == Event.Circle or status == Event.MSI)
                and reactions["rightAnswer"] is None
            ):

                reactions["rightAnswer"] = stageTimer.getDelta()
                stageTimer.setTimer()

                if status == Event.MSI:
                    reactions["MSI"] = True
                    reactions["rightAnswer"] += ANSWER_TIME
                status = Event.MSI
            print(reactions)

        PVTGraphics.drawPVT(status, Event)
        # ---------- Siren Plays ----------------
        match status:
            case Event.Siren:
                # ------ playSiren ------------------
                alarm.play()
                if alarm.isDone():
                    status = Event.StartTrail

            case Event.StartTrail:
                trigger.send(TimeStamp.startPVT)
                lightSensor.pulse()
                stageTimer.setTimer()
                status = Event.Plus

            case Event.Plus:
                PVTTable.writeDataToPage("MainLog", {
                    f"A{3 + roundCounter}": roundCounter + 1,
                    f"B{3 + roundCounter}": currentEmptyTime
                })
                if stageTimer.wait(PLUS_TIME):
                    currentEmptyTime = emptyTime()
                    status = Event.Empty

            case Event.Empty:
                if stageTimer.wait(currentEmptyTime):
                    stageTimer.setTimer()
                    status = Event.Circle
                    trigger.send(TimeStamp.circleAppear)

            case Event.Circle:
                if stageTimer.wait(ANSWER_TIME):
                    stageTimer.setTimer()
                    status = Event.MSI

            case Event.MSI:
                if stageTimer.wait(MSI_TIME):
                    stageTimer.setTimer()
                    # --------------- Fill SpreadSheet ------------
                    PVTTable.writeDataToPage("MainLog", {
                        f'C{3 + roundCounter}': reactions["wrongAnswer"],
                        f'D{3 + roundCounter}': reactions["rightAnswer"],
                        f'E{3 + roundCounter}': reactions["MSI"        ]
                    })
                    status = Event.StartTrail
                    reactions = {
                        "wrongAnswer": None,
                        "rightAnswer": None,
                        "MSI": False
                    }
                    roundCounter += 1
                    if roundCounter >= ROUND:
                        run = False

    trigger.send(TimeStamp.endProgram)
    PVTGraphics.close()
    PVTTable.close()
    trigger.close()

if __name__ == "__main__":
    run()