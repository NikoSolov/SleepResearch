# -*- coding: utf-8 -*-
import time
from enum import Enum
from random import choice, randint

import pygame as pg

import config as cfg
import lightSensor
import alarm
import trigger
from excelTools import ExcelTable
from timer import Timer
from graphics import Graphics

# ============ GET ALL CONSTANTS =========
cfg.loadConfig()
config = cfg.getConfig()
# ----------------------------
ROUND = config['general']['experiment']['round']
SUBJECT_NAME = config['general']['experiment']['name']
SUBJECT_code = config['general']['experiment']['code']
# ----------------------------
DURATIONS = config['Equation']['duration']
PLUS_TIME = DURATIONS['plus']
ANSWER_TIME = DURATIONS['answer']
FAST_ANSWER_TIME = DURATIONS['fastAnswer']
# ----------------------------
CONTROL = config['Equation']['control']
SENSE: float = CONTROL['sensitivity']
print(SENSE)
INV: int = -1 if CONTROL['inverse'] else 1
# ----------------------------
DIR_NAME = f"{SUBJECT_NAME}{SUBJECT_code}_{time.strftime('%d.%m.%y')}_Tasks_{time.strftime('%H.%M.%S')}"
FILEPATH = config['Equation']['file']['path']
file = open(FILEPATH, 'r') if FILEPATH != "None" else None
# =========================================
TasksGraphics = Graphics("Equation")

# ====================================================
TasksTable = ExcelTable("result", f"{DIR_NAME}.xlsx")
TasksTable.createPage("MainLog")
TasksTable.writeDataToPage("MainLog", {
    "A1:B1": "Задачи",
    "C1:G1": "Ответил",
    "A2": "True",
    "B2": "False",
    "C2": "T->T",
    "D2": "F->F",
    "E2": "T->F",
    "F2": "F->T",
    "G2": "Missed",
    "A4": "Раунд",
    "B4": "Пример",
    "C4": "Оценка_примера",
    "D4": "Ответил",
    "E4": "Вывод",
    "F4": "Время реакции"
})

TasksTable.createPage("TimeStamps")
trigger.update(TasksTable, "TimeStamps")

# ============== Vars ========================

rightLevel: float = 0
wrongLevel: float = 0
equationText: str = ""

class Event(Enum):
    Siren = 0
    Plus = 1
    Answer = 2
    AnswerPlus = 3

status = Event.Siren
run = True
stageTimer = Timer()

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


while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            trigger.send(trigger.TimeStamp.manualStamp)
        if event.type == pg.MOUSEWHEEL and status == Event.Answer:
            notch = event.y * INV
            rightLevel, wrongLevel = (
                (rightLevel + SENSE * notch, 0)  
                if (notch > 0) else 
                (0, wrongLevel - SENSE * notch)
            )
            print(rightLevel, wrongLevel)

    TasksGraphics.drawTasks(status, Event, equationText, rightLevel, wrongLevel)

    # ---------- Siren Plays ----------------
    if status == Event.Siren:
        # ------ playSiren ------------------
        alarm.play()
        if alarm.isDone():
            stageTimer.setTimer()
            status = Event.Plus
            # -------- stopSiren ---------------
            lightSensor.pulse()

    # ---------- Plus ----------------
    if status == Event.Plus:
        # --------- lightSensorOn -----------------
        if stageTimer.wait(DURATIONS['plus']):
            stageTimer.setTimer()
            status = Event.Answer
            trigger.send(trigger.TimeStamp.startTask)
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

            mainStats['Equation'][str(equationScore)] += 1
            roundStats = {
                "Equation": equationText,
                "Score": equationScore,
                "Answer": None,
                "Result": None,
                "ReactionTime": None
            }

    if status == Event.Answer:
        if rightLevel >= 1 or wrongLevel >= 1:
            if roundStats['ReactionTime'] == None:
                roundStats['ReactionTime'] = stageTimer.getDelta()
                print('GOTEM')
                trigger.send(trigger.TimeStamp.userInput)

            levels = {
                'right': rightLevel >= 1,
                'wrong': wrongLevel >= 1
            }
            roundStats['Answer'] = (
                True     if levels['right'] else
                False    if levels['wrong'] else
                "Missed"
            )
            confusionMatrix = {
                'TT':     equationScore and levels['right'],
                'FF': not equationScore and levels['wrong'],
                'TF':     equationScore and levels['wrong'],
                'FT': not equationScore and levels['right']
            }

            roundStats['Result'] = (
                True  if confusionMatrix['TT'] or confusionMatrix['FF'] else
                False if confusionMatrix['TF'] or confusionMatrix['FT']  else
                None
            )
            
            mainStats['Answer'][
                next((key for key, value in confusionMatrix.items() if value))
            ] += 1
            # print(next((key for key, value in confusionMatrix.items() if value)), mainStats['Answer'])
            status = Event.AnswerPlus
        # -----------------------------------------------------------
        if stageTimer.wait(DURATIONS['answer']):  # wait for skip
            mainStats['Answer']['Skip'] += 1
            status = Event.AnswerPlus

    if status == Event.AnswerPlus:
        # print(mainStats)
        rightLevel = 0
        wrongLevel = 0

        if stageTimer.wait(DURATIONS['fastAnswer']):
            # ---------- Fill SpreadSheet -----------------
            # ----------- MainStats --------------------
            TasksTable.writeDataToPage("MainLog", {
                "A3": f"{mainStats['Equation']['True']}",
                "B3": f"{mainStats['Equation']['False']}",
                "C3": f"{mainStats['Answer']['TT']}",
                "D3": f"{mainStats['Answer']['FF']}",
                "E3": f"{mainStats['Answer']['TF']}",
                "F3": f"{mainStats['Answer']['FT']}",
                "G3": f"{mainStats['Answer']['Skip']}",
                # ----------- RoundStats --------------------
                f"A{4 + roundCounter}": f"{roundCounter}",
                f"B{4 + roundCounter}": f"{roundStats['Equation']}",
                f"C{4 + roundCounter}": f"{roundStats['Score']}",
                f"D{4 + roundCounter}": f"{roundStats['Answer']}",
                f"E{4 + roundCounter}": f"{roundStats['Result']}",
                f"F{4 + roundCounter}": f"{roundStats['ReactionTime']}"
            })

            # ======== Change Event ==================
            stageTimer.setTimer()
            status = Event.Plus
            lightSensor.pulse()
            roundCounter += 1
            # trigger.send(TimeStamp.startTask)

    if roundCounter > ROUND:
        run = False

trigger.send(trigger.TimeStamp.endProgram)
TasksGraphics.close()
TasksTable.close()
trigger.close()
