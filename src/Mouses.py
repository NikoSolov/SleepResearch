import time
from enum import Enum
from random import choice as ch
from random import uniform as rd

import numpy as np
import pygame as pg

import config as cfg
import lightSensor
import alarm
import trigger
from excelTools import ExcelTable
from timer import Timer
from graphics import Graphics
from VectorLogger import VectorLogger

# ====== Setting up Config =========
cfg.loadConfig()
config = cfg.getConfig()
# ========= CONFIG ==========
WIN_SIZE = np.array([config["general"]["window"]["width"],
                     config["general"]["window"]["height"]])
FULLSCREEN = config["general"]["window"]["fullScreen"]
ROUND = config["general"]["experiment"]["round"]
SUBJECT_NAME = config["general"]["experiment"]["name"]
SUBJECT_code = config["general"]["experiment"]["code"]
# ---------------------------
SIZES = config["Mouses"]["graphics"]["sizes"]
RADIUS = SIZES["radius"]
WAIT_ZONE = SIZES["waitZone"]
DISTANCE_MULTIPLIER = SIZES["distMul"]
STEP = SIZES["speed"]
MAX_DISPERSION = SIZES["maxDispersion"]
# ---------------------------
COLORS = config["Mouses"]["graphics"]["colors"]
C_BG = COLORS["bg"]
C_GTRAIL = COLORS["gtrail"]
C_STRAIL = COLORS["strail"]
C_MOUSE = COLORS["mouse"]
C_HOLE = COLORS["hole"]
# ---------------------------
CONTROL = config["Mouses"]["control"]
SENSITIVITY = CONTROL["sensitivity"]
INVERSE = -1 if CONTROL["inverse"] else 1
# ---------------------------
DIR_NAME = (f'{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}'
            f'_Mouses_{time.strftime("%H.%M.%S")}')
LOG_FREQ = config["Mouses"]["logger"]["freq"]
# ====== Initialization ==================
# ------------------------------
MousesGraphics = Graphics("Mouses")

# -------- Setting Log Files -------------
MousesTable = ExcelTable(f"result/{DIR_NAME}", f"{DIR_NAME}.xlsx")
MousesTable.createPage("MainLog")
MousesTable.createPage("TimeStamps")
# ---- Fill Up Defaults ----------------------
MousesTable.writeDataToPage("MainLog", {
    "A1": "Arrived",
    "B1": "Missed",
    "C1": "Skipped",
    "D1:E1": "Screen Resolution",
    "D2": f"{WIN_SIZE[0]}",
    "E2": f"{WIN_SIZE[1]}",
    "A3:A4": "Round #",
    "B3:B4": "Result",
    "C3:C4": "Notches",
    "D3:D4": "Reaction Time",
    "E3:F3": "Last coord",
    "E4": "x",
    "F4": "y"
})

trigger.update(MousesTable, "TimeStamps")
vecLogger = VectorLogger(f"result/{DIR_NAME}")

class Ball:
    t = 0
    d = 0
    a = 100
    yOffset = 0
    lastT = 0
    P0 = np.array([RADIUS, WIN_SIZE[1] - RADIUS])
    P2 = np.array([WIN_SIZE[0] - 3 * RADIUS, RADIUS])
    P1 = np.array([(P2[0] + P0[0]) // 2, P2[1]])
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
        return (
            Ball.P0 * (1 - t) * (1 - t)
          + Ball.P1 * 2 * (1 - t) * t
          + Ball.P2 * t * t
        )

    @staticmethod
    def funcDer(t: float):
        return (
          - Ball.P0 * 2 * (1 - t)
          + Ball.P1 * 2 * (1 - 2 * t)
          + Ball.P2 * 2 * t
        )

    @staticmethod
    def getPartial():
        bPoints = ([Ball.func(Ball.lastT),
                    (Ball.t - Ball.lastT) / 2
                    * Ball.funcDer(Ball.lastT) + Ball.func(Ball.lastT),
                    Ball.func(Ball.t)]
                   + np.array([0, Ball.yOffset]))
        return bPoints

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
loggerTimer = Timer()
roundTimer = Timer()
status = Event.siren
mainStats = {
    "arrived": 0,
    "missed":  0,
    "skip":    0,
}
roundStats = {
    "notches":      0,
    "answer":       "Skip",
    "reactionTime": 0,
    "ableToMove":   False
}

while run:
    for event in pg.event.get():
        # -------- Hard Quitting ------------
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        # -------- Manual TimeStamp ---------
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            trigger.send(trigger.TimeStamp.manualStamp)
        # -------- Mouse process ------------
        if event.type == pg.MOUSEWHEEL and status == Event.answer:
            if roundStats["ableToMove"] and roundStats[
                "reactionTime"] == 0:
                roundStats["reactionTime"] = roundTimer.getDelta()
                trigger.send(trigger.TimeStamp.userInput)
            # wait until mouse passes WaitZone
            if np.linalg.norm(
                    Ball.getPos() - np.array(
                        [RADIUS, WIN_SIZE[1] - RADIUS])
            ) > WAIT_ZONE:
                roundStats["ableToMove"] = True

            if roundStats["ableToMove"]:
                vecLogger.drawNotch(
                    Ball.getPartial(), 
                    Ball.getPos(), 
                    -INVERSE * SENSITIVITY * event.y
                )

                Ball.lastT = Ball.t
                Ball.yOffset -= SENSITIVITY * event.y * INVERSE
                roundStats["notches"] += 1
    

    if not run:
        # ------- draw last position -------
        vecLogger.saveTrail(Ball.getPartial(), Ball.getPos(), roundCounter)
        continue

    MousesGraphics.drawMouses(status, Event, Ball.getPos())

    # ---------- Siren Plays ----------------
    match status:
        case Event.siren:
            # ------ playSiren ------------------
            alarm.play()
            if alarm.isDone():
                status = Event.init
        case Event.init:
            lightSensor.pulse()
            roundCounter += 1
            MousesTable.createPage(f"Trajectories_{roundCounter}")
            # ------- Default Headers-------------
            MousesTable.writeDataToPage(f"Trajectories_{roundCounter}", {
                "A1:C1": "Trajectory",
                "B2": "Generated",
                "C2": "Subject",
                "A3": "x",
                "C3": "y",
                "B3": "y",
                "F1:G1": "Screen Resolution",
                "E1": "Frequency",
            # --------- Fill with vars --------------
                "E2": f"{LOG_FREQ}",
                "F2": f"{MousesGraphics.WIN_SIZE[0]}",
                "G2": f"{MousesGraphics.WIN_SIZE[1]}"
            })
            # ==========================================
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
            vecLogger.startTrail(Ball.getDots())
            # -------- Timers --------
            roundTimer.setTimer()
            loggerTimer.setTimer(roundTimer.getTimer())
            # ------ Timestamp ------
            trigger.send(trigger.TimeStamp.startMouse)
    
        case Event.answer:
            # ------- make a step ---------
            Ball.step()
            # ------- log positions ---------
            if loggerTimer.wait(LOG_FREQ):
                MousesTable.writeDataToPage(f"Trajectories_{roundCounter}", {
                    f"A{loggerStep + 4}": int(Ball.getPos()[0]),
                    f"B{loggerStep + 4}": int(Ball.func(Ball.t)[1]),
                    f"C{loggerStep + 4}": int(Ball.getPos()[1])
                })

                loggerStep += 1
                loggerTimer.setTimer()

            if Ball.touchWall() or Ball.touchHole():
                status = Event.init
                
                # --------------- Write File And Close ----------
                vecLogger.saveTrail(
                    Ball.getPartial(),
                    Ball.getPos(),
                    roundCounter
                )
                # -------------
        
                if Ball.touchHole(): print("got it")
                roundStats["answer"] = (
                    "Arrived" if Ball.touchHole()          else 
                    "Missed"  if roundStats["notches"] > 0 else 
                    "Skipped"
                )
                mainStats[
                    "arrived" if Ball.touchHole()          else 
                    "missed"  if roundStats["notches"] > 0 else 
                    "skip"
                ] += 1

                # ======== Fill Round Log =========
                print(roundStats)
                MousesTable.writeDataToPage("MainLog", {
                    f"A{roundCounter + 4}": roundCounter,
                    f"B{roundCounter + 4}": roundStats["answer"],
                    f"C{roundCounter + 4}": roundStats["notches"],
                    f"D{roundCounter + 4}": roundStats["reactionTime"],
                    f"E{roundCounter + 4}": Ball.getPos()[0],
                    f"F{roundCounter + 4}": Ball.getPos()[1]
                })
                if roundCounter >= ROUND:
                    run = False


# ------- Filling the Main Log --------------
trigger.send(trigger.TimeStamp.endProgram)
trigger.close()
MousesGraphics.close()
vecLogger.close()
MousesTable.writeDataToPage("MainLog", {
    "A2": f'{mainStats["arrived"]}',
    "B2": f'{mainStats["missed"]}',
    "C2": f'{mainStats["skip"]}'
})
MousesTable.close()
