import time
from enum import Enum, auto
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
from MouseMechanics import MouseMechanics
# ====== Setting up Config =========
def run(): 
    cfg.loadConfig()
    config = cfg.getConfig()
    # ========= CONFIG ==========
    WIN_SIZE = [
        config["general"]["window"]["width"],
        config["general"]["window"]["height"]
    ]
    TRIAL_GROUPS = config["Mouses"]["experiment"]["countOfGroup"]
    TRIALS       = config["Mouses"]["experiment"]["countInGroup"]
    SUBJECT_NAME = config["general"]["experiment"]["name"]
    SUBJECT_code = config["general"]["experiment"]["code"]
    # ---------------------------
    CONTROL = config["Mouses"]["control"]
    SENSITIVITY = CONTROL["sensitivity"]
    INVERSE = -1 if CONTROL["inverse"] else 1
    # ---------------------------
    PLUS_TIME = config["Mouses"]["duration"]["plus"]
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
        "F2": f"{WIN_SIZE[0]}",
        "G2": f"{WIN_SIZE[1]}",
        "A3:A4": "Round #",
        "B3:B4": "Group #",
        "C3:C4": "Trial #",
        "D3:D4": "Result",
        "E3:E4": "Notches",
        "F3:F4": "Reaction Time",
        "G3:H3": "Last coord",
        "G4": "x",
        "H4": "y"
    })

    trigger.update(MousesTable, "TimeStamps")
    vecLogger = VectorLogger(f"result/{DIR_NAME}")

    class Event(Enum):
        siren = auto()
        init = auto()
        answer = auto()
        plus = auto()

    run = True

    # roundCounter = 0
    trialCounter = 0
    groupCounter = 0
    loggerStep = 0
    loggerTimer = Timer()
    roundTimer = Timer()
    plusTimer = Timer()
    
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

    status = Event.siren

    Ball = MouseMechanics()

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
                if roundStats["ableToMove"] and roundStats["reactionTime"] == 0:
                    roundStats["reactionTime"] = roundTimer.getDelta()
                    trigger.send(trigger.TimeStamp.userInput)
                # wait until mouse passes WaitZone
                if Ball.isOutWaitZone():
                    roundStats["ableToMove"] = True

                if roundStats["ableToMove"]:
                    vecLogger.drawNotch(
                        Ball.getPartial(), 
                        -INVERSE * SENSITIVITY * event.y
                    )
                    Ball.drag(-INVERSE * SENSITIVITY * event.y)
                    roundStats["notches"] += 1
        
        if not run:
            # ------- draw last position -------
            vecLogger.saveTrail(Ball.getPartial(), f"{groupCounter + 1}_{trialCounter + 1}")
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

                MousesTable.createPage(f"Trajectories_{groupCounter + 1}_{trialCounter + 1}")
                # ------- Default Headers-------------
                MousesTable.writeDataToPage(f"Trajectories_{groupCounter + 1}_{trialCounter + 1}", {
                    "A1:C1": "Trajectory",
                    "B2": "Generated",
                    "C2": "Subject",
                    "D1:D3": "In Corridor?",
                    "A3": "x",
                    "B3": "y",
                    "C3": "y",
                    "F1:G1": "Screen Resolution",
                    "E1": "Frequency",
                # --------- Fill with vars --------------
                    "E2": f"{LOG_FREQ}",
                    "F2": f"{WIN_SIZE[0]}",
                    "G2": f"{WIN_SIZE[1]}"
                })
                # ==========================================
                # -------- Answer --------
                roundStats = {
                    "notches": 0,
                    "answer": "Skip",
                    "reactionTime": 0,
                    "ableToMove": False
                }
                Ball.startTrail()
                # -------- Logger --------
                loggerStep = 0
                # -------- Image ---------
                vecLogger.startTrail(Ball.getDots(), Ball.getCorridor())
                # -------- Timers --------
                roundTimer.setTimer()
                loggerTimer.setTimer(roundTimer.getTimer())
                # ------ Timestamp ------
                trigger.send(trigger.TimeStamp.startMouse)

                status = Event.answer
        
            case Event.answer:
                # ------- make a step ---------
                Ball.step()
                # ------- log positions ---------
                if loggerTimer.wait(LOG_FREQ):
                    MousesTable.writeDataToPage(f"Trajectories_{groupCounter + 1}_{trialCounter + 1}", {
                        f"A{loggerStep + 4}": int(Ball.getPos()[0]),
                        f"B{loggerStep + 4}": int(Ball.function(Ball.t)[1]),
                        f"C{loggerStep + 4}": int(Ball.getPos()[1]),
                        f"D{loggerStep + 4}": int(Ball.inCorridor())
                    })
                    loggerStep += 1
                    loggerTimer.setTimer()
                    Ball.inCorridor()

                if Ball.touchWall() or Ball.touchHole():
                    # --------------- Write File And Close ----------
                    vecLogger.saveTrail(
                        Ball.getPartial(),
                        f"{groupCounter + 1}_{trialCounter + 1}"
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
                    tableRow = (groupCounter * TRIALS + trialCounter) + 5
                    MousesTable.writeDataToPage("MainLog", {
                        f"A{tableRow}": (groupCounter * TRIALS + trialCounter) + 1,
                        f"B{tableRow}": groupCounter + 1,
                        f"C{tableRow}": trialCounter + 1,
                        f"D{tableRow}": roundStats["answer"],
                        f"E{tableRow}": roundStats["notches"],
                        f"F{tableRow}": roundStats["reactionTime"],
                        f"G{tableRow}": Ball.getPos()[0],
                        f"H{tableRow}": Ball.getPos()[1]
                    })

                    trialCounter += 1
                    status = Event.init

                    if trialCounter >= TRIALS:
                        trialCounter = 0
                        groupCounter += 1                        
                        plusTimer.setTimer()
                        status = Event.plus

                    if groupCounter >= TRIAL_GROUPS:
                        run = False

            case Event.plus:
                if plusTimer.wait(PLUS_TIME):
                    status = Event.init

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

if __name__ == "__main__":
    run()