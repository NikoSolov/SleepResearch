import time
from enum import Enum, auto
from random import uniform as rd

import pygame as pg
import numpy as np

import config as cfg
import lightSensor
import alarm
import trigger
from excelTools import ExcelTable
from timer import Timer

# ======== Load Configs ====================
cfg.loadConfig()
config = cfg.getConfig()
# ------------------------------
WINDOW_CONFIG = config["general"]["window"]
print(WINDOW_CONFIG)
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = np.array([WINDOW_CONFIG["width"], WINDOW_CONFIG["height"]])
TIMESTAMPS_CONFIG = config["general"]["timeStamps"]
ROUND = config["general"]["experiment"]["round"]
SUBJECT_NAME = config["general"]["experiment"]["name"]
SUBJECT_code = config["general"]["experiment"]["code"]
# ------------------------------
COLORS = config["PVT"]["graphics"]["color"]
C_PLUS = pg.Color(COLORS["plus"])
C_BG = pg.Color(COLORS["bg"])
C_CIRCLE = pg.Color(COLORS["circle"])
# ------------------------------
SIZES = config["PVT"]["graphics"]["size"]
PLUS_SIZE = SIZES["plus"]["radius"]
PLUS_WIDTH = SIZES["plus"]["width"]
RADIUS = SIZES["circleRadius"]
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
pg.init()
root = pg.display.set_mode(WIN_SIZE, flags = pg.FULLSCREEN if WIN_FS else pg.SHOWN)
clk = pg.time.Clock()

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

def drawGraphics(root, status):
    root.fill(C_BG)
    lightSensor.draw(root)

    match status:
        case Event.Siren:
            root.fill((0, 0, 0))
        case Event.Plus:
            pg.draw.line(root, pg.Color(C_PLUS),
                        WIN_SIZE // 2 + np.array([0, -1]) *  PLUS_SIZE,
                        WIN_SIZE // 2 + np.array([0,  1]) *  PLUS_SIZE,
                        PLUS_WIDTH)
            pg.draw.line(root, pg.Color(C_PLUS),
                        WIN_SIZE // 2 + np.array([-1, 0]) *  PLUS_SIZE,
                        WIN_SIZE // 2 + np.array([ 1, 0]) *  PLUS_SIZE,
                        PLUS_WIDTH)
        case Event.Circle:
            pg.draw.circle(
                root,
                C_CIRCLE,
                WIN_SIZE // 2,
                RADIUS
            )
    clk.tick(60)
    pg.display.flip()

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

    drawGraphics(root, status)
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

PVTTable.close()
trigger.close()
