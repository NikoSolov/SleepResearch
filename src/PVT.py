import os
import time
from enum import Enum, auto
from random import uniform as rd

import pygame as pg
import xlsxwriter
import numpy as np

import config as cfg
import lightSensor
import alarm
import trigger
from excelTools import writeDataToPage

# ======== Load Configs ====================
cfg.loadConfig()
config = cfg.getConfig()
# <editor-fold desc="CONFIG">
# <editor-fold desc="General">
WINDOW_CONFIG = config["general"]["window"]
print(WINDOW_CONFIG)
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = np.array([WINDOW_CONFIG["width"], WINDOW_CONFIG["height"]])
TIMESTAMPS_CONFIG = config["general"]["timeStamps"]
ROUND = config["general"]["experiment"]["round"]
SUBJECT_NAME = config["general"]["experiment"]["name"]
SUBJECT_code = config["general"]["experiment"]["code"]
# </editor-fold>
# ------------------------------
# <editor-fold desc="Colors">
COLORS = config["PVT"]["graphics"]["color"]
C_PLUS = pg.Color(COLORS["plus"])
C_BG = pg.Color(COLORS["bg"])
C_CIRCLE = pg.Color(COLORS["circle"])
# </editor-fold>
# ------------------------------
# <editor-fold desc="Sizes">
SIZES = config["PVT"]["graphics"]["size"]
PLUS_SIZE = SIZES["plus"]["radius"]
PLUS_WIDTH = SIZES["plus"]["width"]
RADIUS = SIZES["circleRadius"]
# </editor-fold>
# ------------------------------
# <editor-fold desc="Durations">
DELAYS = config["PVT"]["delay"]
MSI_TIME = DELAYS["msi"]
PLUS_TIME = DELAYS["plus"]
ANSWER_TIME = DELAYS["answer"]


def emptyTime(): return rd(DELAYS["emptyMin"], DELAYS["emptyMax"])


# </editor-fold>
# ------------------------------
# <editor-fold desc="Logger">
DIR_NAME = f'{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}_PVT_{time.strftime("%H.%M.%S")}'
# </editor-fold>
# </editor-fold>
# ======== Initialization ====================
# -------------------
pg.init()
root = pg.display.set_mode(WIN_SIZE, flags = pg.FULLSCREEN if WIN_FS else pg.SHOWN)
clk = pg.time.Clock()

# --------- Setting up SpreadSheet -------
# <editor-fold desc="Creating Folder">
if not (os.path.exists("result")):
    os.mkdir("result")
# </editor-fold>

# <editor-fold desc="CREATE TABLE">
TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}.xlsx")
MainLog = TABLE.add_worksheet("MainLog")
writeDataToPage(MainLog, {
    "A1:A2": "Round",
    "B1:E1": "First Reaction",
    "B2":    "EmptyTime",
    "C2":    "FalseAnswer",
    "D2":    "RightAnswer",
    "E2":    "at MSI?",
})

TriggerLog = TABLE.add_worksheet("TimeStamps")
trigger.update(TriggerLog)

# </editor-fold>
# --------- Vars ----------
class Event(Enum):
    Siren = auto()
    Plus = auto()
    Empty = auto()
    Circle = auto()
    MSI = auto()

# <editor-fold desc="Creating Classes and Variables">
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
setTime = time.time()

# </editor-fold>

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
            if ((status == Event.Plus or status == Event.Empty)
                    and reactions["wrongAnswer"] is None):
                reactions["wrongAnswer"] = time.time() - setTime
                setTime = time.time()
                status = Event.MSI

            elif ((status == Event.Circle or status == Event.MSI)
                  and reactions["rightAnswer"] is None):
                reactions["rightAnswer"] = time.time() - setTime
                setTime = time.time()
                if status == Event.MSI:
                    reactions["MSI"] = True
                    reactions["rightAnswer"] += ANSWER_TIME
                status = Event.MSI
            print(reactions)

    drawGraphics(root, status)
    # ---------- Siren Plays ----------------
    if status == Event.Siren:
        # ------ playSiren ------------------
        alarm.play()
        if alarm.isDone():
            setTime = time.time()
            status = Event.Plus
            trigger.send(trigger.TimeStamp.startPVT)
            lightSensor.pulse()

    if status == Event.Plus:

        # print("plus")
        writeDataToPage(MainLog, {
            f"A{3 + roundCounter}": f"{roundCounter + 1}",
            f"B{3 + roundCounter}": f"{currentEmptyTime}"
        })
        # print(time.time() - setTime)
        if time.time() - setTime > PLUS_TIME:
            status = Event.Empty
            currentEmptyTime = emptyTime()
    if status == Event.Empty:
        # print(currentEmptyTime)
        if time.time() - setTime > currentEmptyTime:
            setTime = time.time()
            status = Event.Circle
            trigger.send(trigger.TimeStamp.circleAppear)
            # trigger.send(roundCounter + 1)
    if status == Event.Circle:
        if time.time() - setTime > ANSWER_TIME:
            setTime = time.time()
            status = Event.MSI
    if status == Event.MSI:
        if time.time() - setTime > MSI_TIME:
            # --------------- Fill SpreadSheet ------------
            writeDataToPage(MainLog, {
                f'C{3 + roundCounter}': f'{reactions["wrongAnswer"]}',
                f'D{3 + roundCounter}': f'{reactions["rightAnswer"]}',
                f'E{3 + roundCounter}': f'{reactions["MSI"]}'
            })

            setTime = time.time()
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

TABLE.close()
trigger.close()
