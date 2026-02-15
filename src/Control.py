from enum import Enum, auto
import pygame as pg
import config as cfg
import alarm
import trigger
import lightSensor
import numpy as np
from timer import Timer

# ======== Load Configs ====================
cfg.loadConfig()
config = cfg.getConfig()
# ------------------------------
WINDOW_CONFIG = config["general"]["window"]
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = np.array([WINDOW_CONFIG["width"], WINDOW_CONFIG["height"]])
TIMESTAMPS_CONFIG = config["general"]["timeStamps"]
# ------------------------------
COLORS = config["Control"]["graphics"]["color"]
C_PLUS = pg.Color(COLORS["plus"])
C_BG = pg.Color(COLORS["bg"])
# ------------------------------
SIZES = config["Control"]["graphics"]["size"]
PLUS_SIZE = SIZES["plus"]["radius"]
PLUS_WIDTH = SIZES["plus"]["width"]
# ------------------------------
DELAYS = config["Control"]["delay"]
PLUS_TIME = DELAYS["plus"]
# ------------------------------
# ======== Initialization ====================
trigger.update()
# -------------------
pg.init()
root = pg.display.set_mode(WIN_SIZE, flags = pg.FULLSCREEN if WIN_FS else pg.SHOWN)
clk = pg.time.Clock()

def drawGraphics(root, status):
    root.fill(C_BG)
    lightSensor.draw(root)
    match status:
        case Event.Siren:
            root.fill((0, 0, 0))
        case Event.Plus:
            pg.draw.line(
                root, C_PLUS,
                WIN_SIZE // 2 + np.array([0, -1]) * PLUS_SIZE,
                WIN_SIZE // 2 + np.array([0, 1]) * PLUS_SIZE,
                PLUS_WIDTH
            )
            pg.draw.line(
                root, C_PLUS,
                WIN_SIZE // 2 + np.array([-1, 0]) * PLUS_SIZE,
                WIN_SIZE // 2 + np.array([1, 0]) * PLUS_SIZE,
                PLUS_WIDTH
            )
    clk.tick(60)
    pg.display.flip()

# --------- Vars ----------
class Event(Enum):
    Siren = auto()
    Plus = auto()


status = Event.Siren
stageTimer = Timer()
run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            trigger.send(trigger.TimeStamp.userInput)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            trigger.send(trigger.TimeStamp.manualStamp)

    drawGraphics(root, status)

    # ---------- Siren Plays ----------------
    match status:
        case Event.Siren:
          # ------ playSiren ------------------
          alarm.play()
          if alarm.isDone():
              stageTimer.setTimer()
              status = Event.Plus
              trigger.send(trigger.TimeStamp.startControl)
              lightSensor.pulse()
        case Event.Plus:
            if stageTimer.wait(PLUS_TIME):
                run = False

trigger.send(trigger.TimeStamp.endProgram)
trigger.close()
