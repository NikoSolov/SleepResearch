import time
from enum import Enum
from os import mkdir, path
from random import choice as ch
from random import uniform as rd

import numpy as np
import pygame as pg
import xlsxwriter

import config as cfg
import lightSensor
import alarm
import trigger

# ====== Setting up Config =========
cfg.loadConfig()
config = cfg.getConfig()
# <editor-fold desc="CONFIG">
# ========= CONFIG ==========
# <editor-fold desc="General">
WIN_SIZE = np.array([config["general"]["window"]["width"],
                     config["general"]["window"]["height"]])
FULLSCREEN = config["general"]["window"]["fullScreen"]
ROUND = config["general"]["experiment"]["round"]
SUBJECT_NAME = config["general"]["experiment"]["name"]
SUBJECT_code = config["general"]["experiment"]["code"]
# </editor-fold>
# ---------------------------
# <editor-fold desc="Sizes">
SIZES = config["Mouses"]["graphics"]["sizes"]
RADIUS = SIZES["radius"]
WAIT_ZONE = SIZES["waitZone"]
DISTANCE_MULTIPLIER = SIZES["distMul"]
STEP = SIZES["speed"]
MAX_DISPERSION = SIZES["maxDispersion"]
# </editor-fold>
# ---------------------------
# <editor-fold desc="Colors">
COLORS = config["Mouses"]["graphics"]["colors"]
C_BG = COLORS["bg"]
C_GTRAIL = COLORS["gtrail"]
C_STRAIL = COLORS["strail"]
C_MOUSE = COLORS["mouse"]
C_HOLE = COLORS["hole"]
# </editor-fold>
# ---------------------------
# <editor-fold desc="Control">
CONTROL = config["Mouses"]["control"]
SENSITIVITY = CONTROL["sensitivity"]
INVERSE = -1 if CONTROL["sensitivity"] else 1
# </editor-fold>
# ---------------------------
# <editor-fold desc="Logger">
DIR_NAME = (f"{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}"
            f"_Mouses_{time.strftime("%H.%M.%S")}")
LOG_FREQ = config["Mouses"]["logger"]["freq"]
# </editor-fold>
# </editor-fold>
# ====== Initialization ==================
trigger.update()
# ------------------------------
pg.init()
if FULLSCREEN:
    root = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
else:
    root = pg.display.set_mode(WIN_SIZE)
clk = pg.time.Clock()
# -------- Setting Log Files -------------
# <editor-fold desc="Creating Folders">
if not (path.exists("result")):
    mkdir("result")
if not (path.exists(f"result/{DIR_NAME}")):
    mkdir(f"result/{DIR_NAME}")
if not (path.exists(f"result/{DIR_NAME}/log_img")):
    mkdir(f"result/{DIR_NAME}/log_img")
# </editor-fold>

# <editor-fold desc="Creating TABLE">
# --- Setup Excel SpreadSheet -------------
TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}/{DIR_NAME}.xlsx")
# ---- Fill Up Defaults ----------------------
MainLog = TABLE.add_worksheet("MainLog")
MainLog.write("A1", "Arrived")
MainLog.write("B1", "Missed")
MainLog.write("C1", "Skipped")
MainLog.merge_range("D1:E1", "Screen Resolution")
MainLog.write("D2", f"{WIN_SIZE[0]}")
MainLog.write("E2", f"{WIN_SIZE[1]}")
MainLog.merge_range("A3:A4", "Round #")
MainLog.merge_range("B3:B4", "Result")
MainLog.merge_range("C3:C4", "Notches")
MainLog.merge_range("D3:D4", "Reaction Time")
MainLog.merge_range("E3:F3", "Last coord")
MainLog.write("E4", "x")
MainLog.write("F4", "y")


# </editor-fold>

# --------- Vars --------------
# <editor-fold desc="Creating Classes and Variables">
def imageSample(subjectPath): return f"""
<svg
   style="background:{C_BG}"
   width="{WIN_SIZE[0]}" height="{WIN_SIZE[1]}"
   xmlns="http://www.w3.org/2000/svg">
  <rect
     id="BackGround" style="fill:{C_BG}"
     width="{WIN_SIZE[0]}" height="{WIN_SIZE[1]}" x="0" y="0" />
  <circle
     id="Hole" fill="{C_HOLE}"
     cx="{WIN_SIZE[0] - RADIUS}" cy="{RADIUS}" r="{RADIUS}"/>
  <circle
     id="Hole" fill="none"
     cx="{RADIUS}" cy="{WIN_SIZE[1] - RADIUS}" r="{WAIT_ZONE}"
     stroke="red" stroke-width="3"/>
  <path
     id="generatedTrail"
     stroke = "{C_GTRAIL}"
     style="        
        stroke-width:{5};
        stroke-dasharray:none;
        stroke-linejoin:round;
        stroke-linecap:round"

     fill="none"
     d="M {Ball.P0[0]} {Ball.P0[1]} 
        Q {Ball.P1[0]} {Ball.P1[1]} 
          {Ball.P2[0]} {Ball.P2[1]}"
      />
  <circle
     id="Mouse" fill="{C_MOUSE}"
     cx="{Ball.getPos()[0]}" cy="{Ball.getPos()[1]}" r="{RADIUS}"/>
  <path
     id="subjectTrail" fill="none"
     stroke="{C_STRAIL}"  stroke-width="{5}"
     d="{subjectPath}"
     style="stroke-width:3;
            stroke-dasharray:none;
            stroke-linejoin:round;
            stroke-linecap:round"/>
</svg>
"""


class Ball:
    t = 0
    d = 0
    a = 100
    yOffset = 0
    lastT = 0
    P0 = np.array([RADIUS, WIN_SIZE[1] - RADIUS])
    P1 = np.array([])
    P2 = np.array([WIN_SIZE[0] - 3 * RADIUS, RADIUS])
    S = 0

    @staticmethod
    def init(step: float):
        Ball.t = 0
        Ball.yOffset = 0
        Ball.lastT = 0
        Ball.d = rd(0.07, MAX_DISPERSION)  # 0.07 - experimental
        Ball.lastPos = [RADIUS, WIN_SIZE[1] - RADIUS]
        # print(Ball.d)
        Ball.P2 = np.array(ch([
            [WIN_SIZE[0] - 3 * RADIUS,
             RADIUS * (1 - Ball.d) - Ball.a * Ball.d],
            [WIN_SIZE[0] - RADIUS,
             3 * RADIUS * (1 - Ball.d) + (WIN_SIZE[1] - RADIUS) * Ball.d]
        ]))

        Ball.P1 = np.array(ch([
            [(Ball.P2[0] + Ball.P0[0]) // 2, Ball.P2[1]],
            [(Ball.P2[0] + Ball.P0[0]) // 2, Ball.P0[1]],
            [Ball.P0[0], (Ball.P2[1] + Ball.P0[1]) // 2],
            # [Ball.P2[0], (Ball.P2[1] + Ball.P0[1]) // 2],
        ]))

        Ball.S = step

    @staticmethod
    def getPos():
        return Ball.func(Ball.t) + np.array([0, Ball.yOffset])

    @staticmethod
    def func(t: float):
        return (Ball.P0 * (1 - t) ** 2
                + 2 * Ball.P1 * (1 - t) * t
                + Ball.P2 * t ** 2)

    @staticmethod
    def funcDer(t: float):
        return (-2 * Ball.P0 * (1 - t)
                + 2 * Ball.P1 * (1 - 2 * t)
                + 2 * Ball.P2 * t)

    @staticmethod
    def getPartial():
        bPoints = ([Ball.func(Ball.lastT),
                    (Ball.t - Ball.lastT) / 2
                    * Ball.funcDer(Ball.lastT) + Ball.func(Ball.lastT),
                    Ball.func(Ball.t)]
                   + np.array([0, Ball.yOffset]))

        return f"""M {bPoints[0][0]} {bPoints[0][1]} 
        Q {bPoints[1][0]} {bPoints[1][1]} 
          {bPoints[2][0]} {bPoints[2][1]} 
        """

    @staticmethod
    def step():
        Ball.t += Ball.S / np.linalg.norm(
            2 * (Ball.P0 - 2 * Ball.P1 + Ball.P2) * Ball.t +
            (2 * (Ball.P1 - Ball.P0)))

    @staticmethod
    def getDots():
        return [Ball.P0, Ball.P1, Ball.P2]

    @staticmethod
    def touchWall():
        return any(Ball.getPos() <= np.array([RADIUS, RADIUS])) or any(
            Ball.getPos() >= WIN_SIZE - RADIUS)

    @staticmethod
    def touchHole():
        return np.linalg.norm(Ball.getPos() - np.array(
            [WIN_SIZE[0] - RADIUS, RADIUS])) < 1.5 * RADIUS


class Event(Enum):
    siren = 0
    init = 1
    answer = 2


run = True

roundCounter = 0
loggerStep = 0
loggerTime = time.time()
pathString = ""
status = Event.siren
imageLogger = None
mainStats = {
    "arrived": 0,
    "missed": 0,
    "skip": 0,
}
roundStats = {
    "notches": 0,
    "answer": "Skip",
    "reactionTime": 0,
    "ableToMove": False
}
# </editor-fold>
# ================================
roundTimer = 0

trigger.send(1)

while run:
    for event in pg.event.get():
        # -------- Hard Quitting ------------
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        # -------- Mouse process ------------
        if event.type == pg.MOUSEWHEEL and status == Event.answer:
            if roundStats["reactionTime"] == 0:
                roundStats["reactionTime"] = time.time() - roundTimer
                trigger.send(6)
            # wait until mouse passes WaitZone
            if np.linalg.norm(
                    Ball.getPos() - np.array([RADIUS, WIN_SIZE[1] - RADIUS])
            ) > WAIT_ZONE:
                roundStats["ableToMove"] = True

            if roundStats["ableToMove"]:
                pathString += Ball.getPartial()
                pathString += (
                    f"""M {Ball.getPos()[0]} {Ball.getPos()[1]} 
            l {0} {-SENSITIVITY * event.y}""")
                Ball.lastT = Ball.t
                Ball.yOffset -= SENSITIVITY * event.y
                roundStats["notches"] += 1

    if not run:
        # ------- draw last position -------
        pathString += Ball.getPartial()
        imageLogger.write(imageSample(pathString))
        imageLogger.close()
        # ------- quit program -------
        continue

    # -------- color background ----------
    root.fill(pg.Color(C_BG))
    # -------- draw a hole ----------
    pg.draw.circle(root,
                   pg.Color(C_HOLE),
                   (WIN_SIZE[0] - RADIUS, RADIUS),
                   RADIUS
                   )
    # -------- draw light square ----------
    lightSensor.draw(root)

    # ---------- Siren Plays ----------------
    if status == Event.siren:
        # ------ playSiren ------------------
        alarm.play()
        root.fill((0, 0, 0))
        if alarm.isDone():
            setTime = time.time()
            status = Event.init

    if status == Event.init:
        roundCounter += 1
        lightSensor.pulse()
        # <editor-fold desc="Create Trajectory Table">
        TRAJECTORY_LOG = TABLE.add_worksheet(f"Trajectories_{roundCounter}")
        # ------- Default Headers-------------
        TRAJECTORY_LOG.merge_range("A1:C1", "Trajectory")
        TRAJECTORY_LOG.write("B2", "Generated")
        TRAJECTORY_LOG.write("C2", "Subject")
        TRAJECTORY_LOG.write("A3", "x")
        TRAJECTORY_LOG.write("C3", "y")
        TRAJECTORY_LOG.write("B3", "y")
        TRAJECTORY_LOG.merge_range("F1:G1", "Screen Resolution")
        TRAJECTORY_LOG.write("E1", "Frequency")
        # --------- Fill with vars --------------
        TRAJECTORY_LOG.write("E2", f"{LOG_FREQ}")
        TRAJECTORY_LOG.write("F2", f"{WIN_SIZE[0]}")
        TRAJECTORY_LOG.write("G2", f"{WIN_SIZE[1]}")
        # ==========================================
        # </editor-fold>

        # <editor-fold desc="Setting up">
        # -------- Answer --------
        status = Event.answer
        roundStats = {
            "notches": 0,
            "answer": "Skip",
            "reactionTime": 0,
            "ableToMove": False
        }
        Ball.init(STEP)
        # -------- Logger --------
        loggerStep = 0
        # -------- Image ---------
        imageLogger = open(f"result/{DIR_NAME}/log_img/{roundCounter}.svg",
                           "w")
        pathString = ""
        # -------- Timers --------
        roundTimer = time.time()
        loggerTime = roundTimer
        # ------ Timestamp ------
        trigger.send(2)
        # trigger.send(roundCounter)
        # </editor-fold>

    if status == Event.answer:
        # ------- draw a mouse ---------
        pg.draw.circle(root, pg.Color(C_MOUSE), Ball.getPos(), RADIUS)
        # ------- make a step ---------
        Ball.step()
        # ------- log positions ---------
        if (time.time() - loggerTime) > LOG_FREQ:
            TRAJECTORY_LOG.write(f"A{loggerStep + 4}", int(Ball.getPos()[0]))
            TRAJECTORY_LOG.write(f"B{loggerStep + 4}",
                                 int(Ball.func(Ball.t)[1]))
            TRAJECTORY_LOG.write(f"C{loggerStep + 4}", int(Ball.getPos()[1]))
            loggerStep += 1
            loggerTime = time.time()

        if Ball.touchWall() or Ball.touchHole():
            status = Event.init
            # --------------- Write File And Close ----------
            pathString += Ball.getPartial()
            imageLogger.write(imageSample(pathString))
            imageLogger.close()
            # -------------
            if Ball.touchHole():
                print("got it")
                roundStats["answer"] = "Arrived"
                mainStats["arrived"] += 1
            elif roundStats["notches"] > 0:
                roundStats["answer"] = "Missed"
                mainStats["missed"] += 1
            else:
                roundStats["answer"] = "Skipped"
                mainStats["skip"] += 1

            # ======== Fill Round Log =========
            print(roundStats)
            MainLog.write(f"A{roundCounter + 4}", roundCounter)
            MainLog.write(f"B{roundCounter + 4}", roundStats["answer"])
            MainLog.write(f"C{roundCounter + 4}", roundStats["notches"])
            MainLog.write(f"D{roundCounter + 4}", roundStats["reactionTime"])
            MainLog.write(f"E{roundCounter + 4}", Ball.getPos()[0])
            MainLog.write(f"F{roundCounter + 4}", Ball.getPos()[1])

    if roundCounter >= ROUND:
        run = False

    pg.display.flip()
    clk.tick(60)

# ------- Filling the Main Log --------------
trigger.send(8)
trigger.close()
MainLog.write("A2", f'{mainStats["arrived"]}')
MainLog.write("B2", f'{mainStats["missed"]}')
MainLog.write("C2", f'{mainStats["skip"]}')

TABLE.close()
