# -*- coding: utf-8 -*-
import time
from enum import Enum
from random import choice, randint

import pygame as pg
import xlsxwriter

import config as cfg
import lightSensor
import alarm
import trigger

# ============ GET ALL CONSTANTS =========
cfg.loadConfig()
config = cfg.getConfig()
# <editor-fold desc="CONFIG">
# <editor-fold desc="General">
WINDOW_CONFIG = config["general"]["window"]
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = (WINDOW_CONFIG["width"], WINDOW_CONFIG["height"])
ROUND = config["general"]["experiment"]["round"]
SUBJECT_NAME = config["general"]["experiment"]["name"]
SUBJECT_code = config["general"]["experiment"]["code"]
# </editor-fold>
# ----------------------------
# <editor-fold desc="Colors">
COLORS = config["Equation"]["graphics"]["colors"]
C_BG = COLORS["bg"]
C_PLUS = COLORS["plus"]
C_RIGHT = COLORS["right"]
C_WRONG = COLORS["wrong"]
FONT = config["Equation"]["graphics"]["font"]
# </editor-fold>
# ----------------------------
# <editor-fold desc="Sizes">
SIZES = config["Equation"]["graphics"]["sizes"]
S_PLUS_RADIUS = SIZES["plus"]["radius"]
S_PLUS_WIDTH = SIZES["plus"]["width"]
S_SQR_WIDTH = SIZES["squares"]["width"]
S_SQR_LENGTH = SIZES["squares"]["length"]
# </editor-fold>
# ----------------------------
# <editor-fold desc="Durations">
DURATIONS = config["Equation"]["duration"]
PLUS_TIME = DURATIONS["plus"]
ANSWER_TIME = DURATIONS["answer"]
FAST_ANSWER_TIME = DURATIONS["fastAnswer"]
# </editor-fold>
# ----------------------------
# <editor-fold desc="Control">
CONTROL = config["Equation"]["control"]
SENSE: float = CONTROL["sensitivity"]
print(SENSE)
INV: int = -1 if CONTROL["inverse"] else 1
# </editor-fold>
# ----------------------------
# <editor-fold desc="Other">
DIR_NAME = f"{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}_Tasks_{time.strftime("%H.%M.%S")}"
FILEPATH = config["Equation"]["file"]["path"]
file = open(FILEPATH, "r") if FILEPATH != "None" else None
# </editor-fold>
# </editor-fold>
# =========================================
trigger.update()

pg.font.init()
equationFont = pg.font.SysFont(FONT, SIZES["font"])

if WIN_FS:
    root = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
else:
    root = pg.display.set_mode(WIN_SIZE)
clk = pg.time.Clock()

# ====================================================
# <editor-fold desc="Create a Table">
TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}.xlsx")
MainLog = TABLE.add_worksheet("MainLog")
MainLog.merge_range("A1:B1", "Задачи")
MainLog.merge_range("C1:G1", "Ответил")
MainLog.write("A2", "True")
MainLog.write("B2", "False")
MainLog.write("C2", "T->T")
MainLog.write("D2", "F->F")
MainLog.write("E2", "T->F")
MainLog.write("F2", "F->T")
MainLog.write("G2", "Missed")

MainLog.write("A4", "Раунд")
MainLog.write("B4", "Пример")
MainLog.write("C4", "Оценка_примера")
MainLog.write("D4", "Ответил")
MainLog.write("E4", "Вывод")
MainLog.write("F4", "Время реакции")
# </editor-fold>
# ============== Vars ========================

rightLevel: float = 0
wrongLevel: float = 0


class Event(Enum):
    Siren = 0
    Plus = 1
    Answer = 2
    AnswerPlus = 3


def drawPlus():
    pg.draw.line(root, pg.Color(C_PLUS),
                 (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 - S_PLUS_RADIUS),
                 (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 + S_PLUS_RADIUS),
                 S_PLUS_WIDTH)
    pg.draw.line(root, pg.Color(C_PLUS),
                 (WIN_SIZE[0] // 2 - S_PLUS_RADIUS, WIN_SIZE[1] // 2),
                 (WIN_SIZE[0] // 2 + S_PLUS_RADIUS, WIN_SIZE[1] // 2),
                 S_PLUS_WIDTH)


status = Event.Siren
run = True
setTime = time.time()
roundCounter = 1
mainStats = {
    "Equation": {
        "True": 0,
        "False": 0
    },
    "Answer": {
        "TT": 0,
        "FF": 0,
        "TF": 0,
        "FT": 0,
        "Skip": 0
    }
}

equationSurf: pg.Surface

trigger.send(1)

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.MOUSEWHEEL and status == Event.Answer:
            if roundStats["ReactionTime"] == None:
                roundStats["ReactionTime"] = time.time() - setTime
                trigger.send(6)
            print(rightLevel, wrongLevel)
            if event.y * INV > 0:
                rightLevel += SENSE * event.y * INV
                wrongLevel = 0
            else:
                wrongLevel -= SENSE * event.y * INV
                rightLevel = 0

    root.fill(pg.Color(C_BG))
    lightSensor.draw(root)
    print(time.time() - setTime)
    # ---------- Siren Plays ----------------
    if status == Event.Siren:
        # ------ playSiren ------------------
        root.fill((0, 0, 0))
        alarm.play()
        if alarm.isDone():
            setTime = time.time()
            status = Event.Plus
            trigger.send(3)
            # -------- stopSiren ---------------
            # siren.stop()
            lightSensor.pulse()

    # ---------- Plus ----------------
    if status == Event.Plus:
        drawPlus()
        # --------- lightSensorOn -----------------
        if time.time() - setTime > DURATIONS["plus"]:
            setTime = time.time()
            status = Event.Answer
            # ------------- generate equation --------------
            if file is not None:
                lineFile = file.readline()
                # print(d)
                if lineFile == "":
                    run = False
                lineFile = lineFile.split()
                equationText = lineFile[0]
                equationScore = bool(int(lineFile[1]))
            else:
                equationScore = choice([True, False])
                # print(mainStats)
                # print(equationScore)
                a = randint(0, 50)
                b = randint(0, 9)
                if equationScore:
                    c = a + b
                else:
                    c = randint(0, 59)
                    while c == a + b:
                        c = randint(0, 59)
                equationText = f"{a}+{b}={c}"

            mainStats["Equation"][str(equationScore)] += 1
            # ----------- getSurfaceOfEquation -------------
            equationSurf = equationFont.render(equationText, True,
                                               pg.Color(COLORS["font"]))
            # ----------- create RoundStats ----------------
            roundStats = {
                "Equation": equationText,
                "Score": equationScore,
                "Answer": None,
                "Result": None,
                "ReactionTime": None
            }

    if status == Event.Answer:

        pg.draw.rect(root,
                     pg.Color(C_RIGHT),
                     ((WIN_SIZE[0] - S_SQR_LENGTH) // 2,
                      (WIN_SIZE[1] - 2 * S_SQR_LENGTH) // 4,
                      S_SQR_LENGTH, S_SQR_LENGTH),
                     S_SQR_WIDTH
                     )
        pg.draw.rect(root,
                     pg.Color(C_WRONG),
                     ((WIN_SIZE[0] - S_SQR_LENGTH) // 2,
                      (3 * WIN_SIZE[1] - 2 * S_SQR_LENGTH) // 4,
                      S_SQR_LENGTH, S_SQR_LENGTH),
                     S_SQR_WIDTH
                     )
        pg.draw.rect(root,
                     pg.Color(C_RIGHT),
                     ((WIN_SIZE[0] - S_SQR_LENGTH) // 2,
                      WIN_SIZE[1] // 4
                      + S_SQR_LENGTH // 2 - S_SQR_LENGTH * rightLevel,
                      S_SQR_LENGTH, S_SQR_LENGTH * rightLevel),
                     )
        pg.draw.rect(root,
                     pg.Color(C_WRONG),
                     ((WIN_SIZE[0] - S_SQR_LENGTH) // 2,
                      (3 * WIN_SIZE[1] - 2 * S_SQR_LENGTH) // 4,
                      S_SQR_LENGTH, S_SQR_LENGTH * wrongLevel),
                     )
        root.blit(equationSurf,
                  (WIN_SIZE[0] // 2 - equationSurf.get_width() // 2,
                   WIN_SIZE[1] // 2 - equationSurf.get_height() // 2))
        # --------- If One of Squares filled ---------------
        if rightLevel >= 1 or wrongLevel >= 1:
            if rightLevel >= 1:
                roundStats["Answer"] = True
            elif wrongLevel >= 1:
                roundStats["Answer"] = False
            else:
                roundStats["Answer"] = "Missed"

            if equationScore and rightLevel >= 1:
                mainStats["Answer"]["TT"] += 1
                roundStats["Result"] = True
            if equationScore and wrongLevel >= 1:
                mainStats["Answer"]["TF"] += 1
                roundStats["Result"] = False
            if not equationScore and rightLevel >= 1:
                mainStats["Answer"]["FT"] += 1
                roundStats["Result"] = False
            if not equationScore and wrongLevel >= 1:
                mainStats["Answer"]["FF"] += 1
                roundStats["Result"] = True

            status = Event.AnswerPlus
        # -----------------------------------------------------------
        if time.time() - setTime > DURATIONS["answer"]:  # wait for skip
            mainStats["Answer"]["Skip"] += 1
            status = Event.AnswerPlus

    if status == Event.AnswerPlus:
        print(mainStats)
        drawPlus()
        rightLevel = 0
        wrongLevel = 0

        if time.time() - setTime > DURATIONS["fastAnswer"]:
            # ---------- Fill SpreadSheet -----------------
            # ----------- MainStats --------------------
            MainLog.write("A3", f"{mainStats["Equation"]["True"]}")
            MainLog.write("B3", f"{mainStats["Equation"]["False"]}")
            MainLog.write("C3", f"{mainStats["Answer"]["TT"]}")
            MainLog.write("D3", f"{mainStats["Answer"]["FF"]}")
            MainLog.write("E3", f"{mainStats["Answer"]["TF"]}")
            MainLog.write("F3", f"{mainStats["Answer"]["FT"]}")
            MainLog.write("G3", f"{mainStats["Answer"]["Skip"]}")
            # ----------- RoundStats --------------------
            MainLog.write(f"A{4 + roundCounter}", f"{roundCounter}")
            MainLog.write(f"B{4 + roundCounter}", f"{roundStats["Equation"]}")
            MainLog.write(f"C{4 + roundCounter}", f"{roundStats["Score"]}")
            MainLog.write(f"D{4 + roundCounter}", f"{roundStats["Answer"]}")
            MainLog.write(f"E{4 + roundCounter}", f"{roundStats["Result"]}")
            MainLog.write(f"F{4 + roundCounter}",
                          f"{roundStats["ReactionTime"]}")
            # ======== Change Event ==================
            setTime = time.time()
            status = Event.Plus
            lightSensor.pulse()
            roundCounter += 1
            trigger.send(3)

    if roundCounter >= ROUND:
        run = False
    pg.display.flip()
    clk.tick(60)
trigger.send(8)
TABLE.close()
trigger.close()
