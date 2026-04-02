from enum import Enum, auto
import pygame as pg
import config as cfg
from alarm import Alarm
from trigger import Trigger, TimeStamp
from lightSensor import LightSensor
from timer import Timer
from excelTools import ExcelTable
import time
from graphics import Graphics

def run():
    # ======== Load Configs ====================
    cfg.loadConfig()
    config = cfg.getConfig()
    # ------------------------------
    DELAYS = config["Control"]["delay"]
    PLUS_TIME = DELAYS["plus"]
    # ------------------------------
    # ======== Initialization ====================
    SUBJECT_NAME = config["general"]["experiment"]["name"]
    SUBJECT_code = config["general"]["experiment"]["code"]
    DIR_NAME = f'{SUBJECT_NAME}{SUBJECT_code}_{time.strftime("%d.%m.%y")}_Control_{time.strftime("%H.%M.%S")}'

    ControlTable = ExcelTable("result", f"{DIR_NAME}.xlsx")
    ControlTable.createPage("TimeStamps")
    trigger = Trigger()
    trigger.update(ControlTable, "TimeStamps")
    # -------------------
    lightSensor = LightSensor()
    ControlGraphics = Graphics("Control", lightSensor)
    # --------- Vars ----------
    class Event(Enum):
        Siren = auto()
        Plus = auto()

    status = Event.Siren
    stageTimer = Timer()
    run = True

    alarm = Alarm()

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                trigger.send(TimeStamp.userInput)
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                trigger.send(TimeStamp.manualStamp)

        ControlGraphics.drawControl(status, Event)

        # ---------- Siren Plays ----------------
        match status:
            case Event.Siren:
                # ------ playSiren ------------------
                alarm.play()
                if alarm.isDone():
                    stageTimer.setTimer()
                    status = Event.Plus
                    trigger.send(TimeStamp.startControl)
                    lightSensor.pulse()
            case Event.Plus:
                if stageTimer.wait(PLUS_TIME):
                    run = False

    trigger.send(TimeStamp.endProgram)
    ControlGraphics.close()
    ControlTable.close()
    trigger.close()

if __name__ == "__main__":
    run()