import os
import time
from enum import Enum
from random import uniform as rd

import pygame as pg
import xlsxwriter

import config as cfg
import siren
import trigger
import lightSensor
# ======== Load Configs ====================
cfg.loadConfig()
config = cfg.getConfig()
# <editor-fold desc="CONFIG">
# <editor-fold desc="General">
WINDOW_CONFIG = config["general"]["window"]
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = (WINDOW_CONFIG["width"], WINDOW_CONFIG["height"])
TIMESTAMPS_CONFIG = config["general"]["timeStamps"]
SIREN_TIME = config["general"]["siren"]["duration"]
ROUND = config["general"]["experiment"]["round"]
LIGHT_SIZE = config["general"]["timeStamps"]["lightSize"]
# </editor-fold>
# ------------------------------
# <editor-fold desc="Colors">
COLORS = config["PVT"]["color"]
C_PLUS = pg.Color(COLORS["plus"])
C_BG = pg.Color(COLORS["bg"])
C_CIRCLE = pg.Color(COLORS["circle"])
# </editor-fold>
# ------------------------------
# <editor-fold desc="Sizes">
SIZES = config["PVT"]["size"]
PLUS_SIZE = SIZES["plus"]["radius"]
PLUS_WIDTH = SIZES["plus"]["width"]
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
DIR_NAME = "PVT" + time.strftime("%d.%m.%y %H.%M.%S")
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
MainLog.merge_range("B1:F1", "First Reaction")
MainLog.write("B2", "Plus")
MainLog.write("C2", "EmptyTime")
MainLog.write("D2", "Empty")
MainLog.write("E2", "Circle")
MainLog.write("F2", "MSI")


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
reactions = {"Plus": None, "Empty": None, "Circle": None, "MSI": None}
# --------------
setTime = time.time()
trigger.send(1)
# </editor-fold>

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            print("Clicked")
            if status == Event.Plus and reactions["Plus"] is None:
                reactions["Empty"] = time.time() - setTime
                setTime = time.time()
                status = Event.MSI
            if status == Event.Empty and reactions["Empty"] is None:
                reactions["Empty"] = time.time() - setTime
                setTime = time.time()
                status = Event.MSI
            if status == Event.Circle and reactions["Circle"] is None:
                reactions["Circle"] = time.time() - setTime
                trigger.send(6)
                trigger.send(roundCounter + 1)
                setTime = time.time()
                status = Event.MSI
            if status == Event.MSI and reactions["MSI"] is None:
                reactions["MSI"] = time.time() - setTime
            print(*reactions.values(), sep="\n")

    root.fill(C_BG)

    lightSensor.draw(root)

    # ---------- Siren Plays ----------------
    if status == Event.Siren:
        # ------ playSiren ------------------
        siren.play()
        root.fill((0, 0, 0))
        if time.time() - setTime > SIREN_TIME:
            setTime = time.time()
            status = Event.Plus
            siren.stop()
            trigger.send(8)
            trigger.send(roundCounter + 1)

    if status == Event.Plus:
        lightSensor.pulse()
        # print("plus")
        MainLog.write(f"A{3 + roundCounter}", f"{roundCounter + 1}")
        MainLog.write(f"C{3 + roundCounter}", f"{currentEmptyTime}")
        pg.draw.rect(root, (255, 255, 255), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
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
            trigger.send(8)
            trigger.send(roundCounter + 1)
    if status == Event.Circle:
        pg.draw.circle(
            root,
            C_CIRCLE,
            (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2),
            20
        )
        if time.time() - setTime > ANSWER_TIME:
            setTime = time.time()
            status = Event.MSI
    if status == Event.MSI:
        # --------------- Fill SpreadSheet ------------
        MainLog.write(f"B{3 + roundCounter}", f"{reactions["Plus"]}")
        MainLog.write(f"D{3 + roundCounter}", f"{reactions["Empty"]}")
        MainLog.write(f"E{3 + roundCounter}", f"{reactions["Circle"]}")
        MainLog.write(f"F{3 + roundCounter}", f"{reactions["MSI"]}")

        if time.time() - setTime > MSI_TIME:
            setTime = time.time()
            status = Event.Plus
            reactions = {"Plus": None,
                         "Empty": None,
                         "Circle": None,
                         "MSI": None}
            roundCounter += 1
            trigger.send(4)
            trigger.send(roundCounter + 1)
    if roundCounter >= ROUND:
        trigger.send(8)
        trigger.send(roundCounter + 1)
        run = False
        clk.tick(60)
    pg.display.flip()

TABLE.close()
trigger.close()
