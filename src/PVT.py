import time
from enum import Enum, auto
from random import uniform as rd

import pygame as pg

import config as cfg
import lightSensor
import alarm
import trigger
from excelTools import ExcelTable
from timer import Timer
from graphics import Graphics

# ======== Load Configs ====================
cfg.loadConfig()
config = cfg.getConfig()
# ------------------------------
TIMESTAMPS_CONFIG = config["general"]["timeStamps"]
ROUND = config["general"]["experiment"]["round"]
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
PVTGraphics = Graphics("PVT")

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

trigger.update(PVTTable, "TimeStamps")

# --------- Vars ----------
class Event(Enum):
    Siren = auto()
    Plus = auto()
    Empty = auto()
    Circle = auto()
    MSI = auto()

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
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            trigger.send(trigger.TimeStamp.manualStamp)
        if event.type == pg.MOUSEBUTTONDOWN:
            print("Clicked")
            trigger.send(trigger.TimeStamp.userInput)
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
              stageTimer.setTimer()
              status = Event.Plus
              trigger.send(trigger.TimeStamp.startPVT)
              lightSensor.pulse()

        case Event.Plus:
            PVTTable.writeDataToPage("MainLog", {
                f"A{3 + roundCounter}": f"{roundCounter + 1}",
                f"B{3 + roundCounter}": f"{currentEmptyTime}"
            })
            if stageTimer.wait(PLUS_TIME):
                currentEmptyTime = emptyTime()
                status = Event.Empty

        case Event.Empty:
            if stageTimer.wait(currentEmptyTime):
                stageTimer.setTimer()
                status = Event.Circle
                trigger.send(trigger.TimeStamp.circleAppear)

        case Event.Circle:
            if stageTimer.wait(ANSWER_TIME):
                stageTimer.setTimer()
                status = Event.MSI

        case Event.MSI:
            if stageTimer.wait(MSI_TIME):
                stageTimer.setTimer()
                # --------------- Fill SpreadSheet ------------
                PVTTable.writeDataToPage("MainLog", {
                    f'C{3 + roundCounter}': f'{reactions["wrongAnswer"]}',
                    f'D{3 + roundCounter}': f'{reactions["rightAnswer"]}',
                    f'E{3 + roundCounter}': f'{reactions["MSI"]}'
                })
                status = Event.Plus
                reactions = {
                    "wrongAnswer": None,
                    "rightAnswer": None,
                    "MSI": False
                }
                roundCounter += 1
                trigger.send(trigger.TimeStamp.startPVT)
                lightSensor.pulse()

    if roundCounter >= ROUND:
        run = False

trigger.send(trigger.TimeStamp.endProgram)
PVTGraphics.close()
PVTTable.close()
trigger.close()
