import os
import time
from enum import Enum
from random import uniform as rd

import pygame as pg
import xlsxwriter

import config as cfg
import lightSensor
import alarm
import trigger

# ======== Load Configs ====================
cfg.loadConfig()
config = cfg.getConfig()
# <editor-fold desc="CONFIG">
# <editor-fold desc="General">
WINDOW_CONFIG = config["general"]["window"]
print(WINDOW_CONFIG)
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = (WINDOW_CONFIG["width"], WINDOW_CONFIG["height"])
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
DIR_NAME = f"{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}_PVT_{time.strftime("%H.%M.%S")}"
# </editor-fold>
# </editor-fold>
# ======== Initialization ====================
trigger.update()
# -------------------
pg.init()
if WIN_FS:
    root = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
else:
    root = pg.display.set_mode(WIN_SIZE)
clk = pg.time.Clock()

# --------- Setting up SpreadSheet -------
# <editor-fold desc="Creating Folder">
if not (os.path.exists("result")):
    os.mkdir("result")
# </editor-fold>

# <editor-fold desc="CREATE TABLE">
TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}.xlsx")
MainLog = TABLE.add_worksheet("MainLog")
MainLog.merge_range("A1:A2", "Round")
MainLog.merge_range("B1:E1", "First Reaction")
MainLog.write("B2", "EmptyTime")
MainLog.write("C2", "FalseAnswer")
MainLog.write("D2", "RightAnswer")
MainLog.write("E2", "at MSI?")


# </editor-fold>
# --------- Vars ----------
class Event(Enum):
    Siren = 0
    Plus = 1
    Empty = 2
    Circle = 3
    MSI = 4


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

trigger.send(1)

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            print("Clicked")
            trigger.send(6)
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

    root.fill(C_BG)
    lightSensor.draw(root)

    # ---------- Siren Plays ----------------
    if status == Event.Siren:
        # ------ playSiren ------------------
        alarm.play()
        root.fill((0, 0, 0))
        if alarm.isDone():
            setTime = time.time()
            status = Event.Plus
            trigger.send(4)
            lightSensor.pulse()

    if status == Event.Plus:

        # print("plus")
        MainLog.write(f"A{3 + roundCounter}", f"{roundCounter + 1}")
        MainLog.write(f"B{3 + roundCounter}", f"{currentEmptyTime}")
        pg.draw.line(root, C_PLUS,
                     (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 - PLUS_SIZE),
                     (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 + PLUS_SIZE),
                     PLUS_WIDTH)
        pg.draw.line(root, C_PLUS,
                     (WIN_SIZE[0] // 2 - PLUS_SIZE, WIN_SIZE[1] // 2),
                     (WIN_SIZE[0] // 2 + PLUS_SIZE, WIN_SIZE[1] // 2),
                     PLUS_WIDTH)
        # print(time.time() - setTime)
        if time.time() - setTime > PLUS_TIME:
            status = Event.Empty
            currentEmptyTime = emptyTime()
    if status == Event.Empty:
        # print(currentEmptyTime)
        if time.time() - setTime > currentEmptyTime:
            setTime = time.time()
            status = Event.Circle
            trigger.send(5)
            # trigger.send(roundCounter + 1)
    if status == Event.Circle:
        pg.draw.circle(
            root,
            C_CIRCLE,
            (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2),
            RADIUS
        )
        if time.time() - setTime > ANSWER_TIME:
            setTime = time.time()
            status = Event.MSI
    if status == Event.MSI:
        if time.time() - setTime > MSI_TIME:
            # --------------- Fill SpreadSheet ------------
            MainLog.write(f"C{3 + roundCounter}",
                          f"{reactions["wrongAnswer"]}")
            MainLog.write(f"D{3 + roundCounter}",
                          f"{reactions["rightAnswer"]}")
            MainLog.write(f"E{3 + roundCounter}", f"{reactions["MSI"]}")

            setTime = time.time()
            status = Event.Plus
            reactions = {
                "wrongAnswer": None,
                "rightAnswer": None,
                "MSI": False
            }
            roundCounter += 1
            trigger.send(4)
            lightSensor.pulse()

    if roundCounter >= ROUND:
        run = False

    # clk.tick(60)
    pg.display.flip()
trigger.send(8)

TABLE.close()
trigger.close()
