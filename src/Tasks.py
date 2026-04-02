import time
from enum import Enum, auto
from random import choice, randint, sample, shuffle
import pygame as pg
import config as cfg
from lightSensor import LightSensor
from alarm import Alarm
from trigger import Trigger, TimeStamp
from excelTools import ExcelTable
from timer import Timer
from graphics import Graphics
from icecream import ic

def run():
    # ============ GET ALL CONSTANTS =========
    cfg.loadConfig()
    config = cfg.getConfig()
    # ----------------------------
    ROUND = config['Equation']['experiment']['round']
    SUBJECT_NAME = config['general']['experiment']['name']
    SUBJECT_code = config['general']['experiment']['code']
    # ----------------------------
    DURATIONS = config['Equation']['duration']
    PLUS_TIME        = DURATIONS['plus']
    ANSWER_TIME      = DURATIONS['answer']
    FAST_ANSWER_TIME = DURATIONS['fastAnswer']
    TERM_TIME        = DURATIONS['term'] # in seconds
    PAUSE_TIME       = DURATIONS['pause'] # in seconds
    # ----------------------------
    CONTROL = config['Equation']['control']
    SENSE: float = CONTROL['sensitivity']
    # print(SENSE)
    INV: int = -1 if config["general"]["control"]["inverse"] else 1
    # ----------------------------
    DIR_NAME = f"{SUBJECT_NAME}{SUBJECT_code}_{time.strftime('%d.%m.%y')}_Tasks_{time.strftime('%H.%M.%S')}"
    FILEPATH = config['Equation']['experiment']['filePath']
    file = open(FILEPATH, 'r') if FILEPATH != "None" else None
    # ---------------------------
    TERM_COUNT = config['Equation']['experiment']['generatedTermCount']
    FILE_MODE  = config['Equation']['experiment']['fileMode']
    # =========================================
    lightSensor = LightSensor()
    TasksGraphics = Graphics("Equation", lightSensor)

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
    trigger = Trigger()
    trigger.update(TasksTable, "TimeStamps")

    # ============== Vars ========================

    rightLevel: float = 0
    wrongLevel: float = 0
    equationText: str = ""
    shownEquationText: str = ""

    class Event(Enum):
        Siren      = auto()
        Plus       = auto()
        Answer     = auto()
        AnswerPlus = auto()
        Term       = auto()
        Pause      = auto()
    
    alarm = Alarm()

    status = Event.Siren
    run = True
    stageTimer = Timer()
    termIndex = 0
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

    def gen(length, repeats):
        while True:
            a = [True]*(length//2) + [False]*(length//2)
            shuffle(a)
            if not any(all(a[i]==a[i+j] for j in range(repeats+1)) for i in range(length-repeats)):
                return a

    def equationGenerator(equationScore: bool, termCount: int = 2):
        ic(equationScore)
        while True:
            firstTerm = [choice([randint(1, 9), randint(10, 50)])]
            term = firstTerm + sample(range(1, 9), termCount - 1)
            ic(term)
            if equationScore:
                term.append(sum(term))
            else:
                wrongChoiceForTwo = choice([True, False])
                wrongChoice = choice([
                    "plusMinusDelta", 
                    "plusMinusDelta2", 
                    "minusRandom", 
                    # "oldStyle"
                ])
                ic(wrongChoice)
                if termCount == 2 and wrongChoiceForTwo:
                    ic("minusNotPlus")
                    term.append(term[0] - term[1])
                else:
                    match wrongChoice:
                        case "plusMinusDelta":
                            term.append(sum(term) + choice([-1, 1]) * randint(1, 3))
                        case "plusMinusDelta2":
                            term.append(sum(term) + choice([-1, 1]) * 10)
                        case "minusRandom":
                            term.append(sum(term) - choice(term))
                        # case "oldStyle":
                        #     c = randint(0, 50 + termCount*9)
                        #     while c == sum(term):
                        #         c = randint(0, 50 + termCount*9)
                        #     term.append(c)
            if len(term) == termCount + 1 and term[-1] > 0:
                break

        equationText = f"{term[0]}"
        for i in term[1:-1]:
            equationText += f"+{i}"
        equationText += f"={term[-1]}"

        return equationText

    genChoices = gen(ROUND, 3)

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                trigger.send(TimeStamp.manualStamp)
            if event.type == pg.MOUSEWHEEL and status == Event.Answer:
                notch = event.y * INV
                rightLevel, wrongLevel = (
                    (rightLevel + SENSE * notch, 0)  
                    if (notch > 0) else 
                    (0, wrongLevel - SENSE * notch)
                )
                # print(rightLevel, wrongLevel)

        TasksGraphics.drawTasks(status, Event, shownEquationText, rightLevel, wrongLevel)

        match status:
            # ---------- Siren Plays ----------------
            case Event.Siren:
                # ------ playSiren ------------------
                alarm.play()
                if alarm.isDone():
                    stageTimer.setTimer()
                    status = Event.Plus
                    # -------- stopSiren ---------------
                    lightSensor.pulse()

            # ---------- Plus ----------------
            case Event.Plus:
                # --------- lightSensorOn -----------------
                if stageTimer.wait(PLUS_TIME):
                    trigger.send(TimeStamp.startTask)
                    # ------------- generate equation --------------
                    if file is not None and FILE_MODE:
                        lineFile = file.readline()
                        if lineFile == "":
                            run = False
                        lineFile = lineFile.split()
                        equationText = lineFile[0]
                        equationScore = bool(int(lineFile[1]))
                    else:
                        equationScore = genChoices[roundCounter - 1]
                        equationText = equationGenerator(equationScore, TERM_COUNT)

                    textParts = equationText.split("+")

                    if len(textParts) > 2:
                        status = Event.Term
                        shownEquationText = f"{textParts[0]}+{textParts[1]}"
                        termIndex = 0
                    else:
                        status = Event.Answer
                        shownEquationText = equationText

                    mainStats['Equation'][str(equationScore)] += 1
                    roundStats = {
                        "Equation": equationText,
                        "Score": equationScore,
                        "Answer": None,
                        "Result": None,
                        "ReactionTime": None
                    }
                    stageTimer.setTimer()

            case Event.Term:
                if stageTimer.wait(TERM_TIME):
                    termIndex += 1
                    ic(termIndex, len(textParts))
                    if termIndex < len(textParts) - 1:
                        shownEquationText = f"+{textParts[termIndex + 1]}"
                    status = Event.Pause
                    stageTimer.setTimer()

            case Event.Pause:
                if stageTimer.wait(PAUSE_TIME):
                    if termIndex < len(textParts) - 2:
                        status = Event.Term
                    else:
                        status = Event.Answer
                    stageTimer.setTimer()

            case Event.Answer:
                if rightLevel >= 1 or wrongLevel >= 1:
                    if roundStats['ReactionTime'] == None:
                        roundStats['ReactionTime'] = stageTimer.getDelta()
                        trigger.send(TimeStamp.userInput)

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
                if stageTimer.wait(ANSWER_TIME):  # wait for skip
                    mainStats['Answer']['Skip'] += 1
                    status = Event.AnswerPlus
            case Event.AnswerPlus:
                # print(mainStats)
                rightLevel = 0
                wrongLevel = 0

                if stageTimer.wait(FAST_ANSWER_TIME):
                    # ---------- Fill SpreadSheet -----------------
                    # ----------- MainStats --------------------
                    TasksTable.writeDataToPage("MainLog", {
                        "A3": mainStats['Equation']['True' ],
                        "B3": mainStats['Equation']['False'],
                        "C3": mainStats['Answer']['TT'  ],
                        "D3": mainStats['Answer']['FF'  ],
                        "E3": mainStats['Answer']['TF'  ],
                        "F3": mainStats['Answer']['FT'  ],
                        "G3": mainStats['Answer']['Skip'],
                        # ----------- RoundStats --------------------
                        f"A{4 + roundCounter}": roundCounter,
                        f"B{4 + roundCounter}": roundStats['Equation'    ],
                        f"C{4 + roundCounter}": roundStats['Score'       ],
                        f"D{4 + roundCounter}": roundStats['Answer'      ],
                        f"E{4 + roundCounter}": roundStats['Result'      ],
                        f"F{4 + roundCounter}": roundStats['ReactionTime']
                    })

                    # ======== Change Event ==================
                    stageTimer.setTimer()
                    status = Event.Plus
                    lightSensor.pulse()
                    roundCounter += 1
                    # trigger.send(TimeStamp.startTask)

        if roundCounter > ROUND:
            run = False

    trigger.send(TimeStamp.endProgram)
    TasksGraphics.close()
    TasksTable.close()
    trigger.close()

if __name__ == "__main__":  
    run()