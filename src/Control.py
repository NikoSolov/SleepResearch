import time
from enum import Enum, auto
import pygame as pg
import config as cfg
import alarm
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
# </editor-fold>
# ------------------------------
# <editor-fold desc="Colors">
COLORS = config["Control"]["graphics"]["color"]
C_PLUS = pg.Color(COLORS["plus"])
C_BG = pg.Color(COLORS["bg"])
# </editor-fold>
# ------------------------------
# <editor-fold desc="Sizes">
SIZES = config["Control"]["graphics"]["size"]
PLUS_SIZE = SIZES["plus"]["radius"]
PLUS_WIDTH = SIZES["plus"]["width"]
# </editor-fold>
# ------------------------------
# <editor-fold desc="Durations">
DELAYS = config["Control"]["delay"]
PLUS_TIME = DELAYS["plus"]
# </editor-fold>
# ------------------------------
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


# --------- Vars ----------
class Event(Enum):
    Siren = auto()
    Plus = auto()

class TimeStamp(Enum):
    userInput = 6
    startControl = 7
    endProgram = 8
    killProgram = 9


status = Event.Siren
setTime = time.time()
run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            trigger.send(TimeStamp.userInput)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            trigger.send(TimeStamp.killProgram)

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
            trigger.send(TimeStamp.startControl)
            lightSensor.pulse()

    if status == Event.Plus:
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
            run = False

    clk.tick(60)
    pg.display.flip()

trigger.send(TimeStamp.endProgram)
trigger.close()
