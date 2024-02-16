import os
from enum import Enum

import numpy
import pygame as pg
import serial.tools.list_ports
import xlsxwriter

import config as cfg
from random import uniform as rd
import time

# ---- Load configs ----------
pg.mixer.init(44100, -16, 2, 512)
pg.init()

cfg.loadConfig()
config = cfg.getConfig()

WINDOW_CONFIG = config["general"]["window"]
TIMESTAMPS_CONFIG = config["general"]["timeStamps"]
PVT_CONFIG = config["PVT"]
COLORS = PVT_CONFIG["color"]
DELAYS = PVT_CONFIG["delay"]
print(PVT_CONFIG)
# ---- Load Constants --------
WIN_FS = WINDOW_CONFIG["fullScreen"]
WIN_SIZE = (WINDOW_CONFIG["width"], WINDOW_CONFIG["height"])
ROUND = config["general"]["experiment"]["round"]
PLUS_TIME = DELAYS["plus"]
ANSWER_TIME = DELAYS["answer"]
emptyTime = lambda: rd(DELAYS["emptyMin"], DELAYS["emptyMax"])
MSI_TIME = PVT_CONFIG["delay"]["msi"]
C_PLUS = pg.Color(COLORS["plus"])
C_BG = pg.Color(COLORS["bg"])
C_CIRCLE = pg.Color(COLORS["circle"])
PLUS_SIZE = PVT_CONFIG["size"]["plus"]["radius"]
PLUS_WIDTH = PVT_CONFIG["size"]["plus"]["width"]
LIGHT_SIZE = config["general"]["timeStamps"]["lightSize"]
# ---- Load Constants --------
if WIN_FS:
    root = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
else:
    root = pg.display.set_mode(WIN_SIZE)
clk = pg.time.Clock()

class Event(Enum):
    Cross = 1
    Empty = 2
    Circle = 3
    MSI = 4


# ------------------- Set Trigger -------------------
port_work = True
portname = ""
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    if "USB-SERIAL CH340" in desc:
        portname = port
if portname == "":  port_work = False

try:
    time_code = serial.Serial(port=portname, baudrate=9600, timeout=.1)
    time.sleep(2)
except Exception as e:
    port_work = False
#    print(e)
# ---------------- set Siren -------------------------
# create the siren's sample
TONE = config["general"]["tone"]
arr = numpy.array(
    [int(TONE["volume"]) * numpy.sin(2.0 * numpy.pi * int(TONE["freq"]) * x / 44100) for x in
     range(0, 44100)]).astype(numpy.int16)
arr2 = numpy.c_[arr, arr]
sound = pg.sndarray.make_sound(arr2)
start_prog = True
# play tone
if int(TONE["enable"]) and start_prog == True:  # and port_work==True:
    print("play")
    if port_work: time_code.write(bytearray([1]))
    sound.play(-1)
    pg.time.wait(int(float(TONE["delay"]) * 1000))
    sound.stop()

# --------- Setting up SpreadSheet -------
if not (os.path.exists("result")):
    os.mkdir("result")

DIR_NAME = "PVT" + time.strftime("%d.%m.%y %H.%M.%S")
TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}.xlsx")
MainLog = TABLE.add_worksheet("MainLog")
MainLog.merge_range("A1:A2", "Round")
MainLog.merge_range("B1:F1", "First Reaction")
MainLog.write("B2", "Plus")
MainLog.write("C2", "EmptyTime")
MainLog.write("D2", "Empty")
MainLog.write("E2", "Circle")
MainLog.write("F2", "MSI")
# --------- Vars ----------
run = True
status = Event.Cross
setTime = time.time()
# setRoundTime=time.time()
currentEmptyTime = emptyTime()
roundCounter = 0
reactions = {"Plus": None, "Empty": None, "Circle": None, "MSI": None}


if port_work: time_code.write(bytearray([40+(roundCounter+1)]))
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            print("Clicked")
            if status == Event.Cross and reactions["Plus"] is None:
                reactions["Plus"] = time.time() - setTime
            if status == Event.Empty and reactions["Empty"] is None:
                reactions["Empty"] = time.time() - setTime
                setTime = time.time()
                status = Event.MSI
            if status == Event.Circle and reactions["Circle"] is None:
                reactions["Circle"] = time.time() - setTime
                if port_work: time_code.write(bytearray([60 + (roundCounter + 1)]))
                setTime = time.time()
                status = Event.MSI
            if status == Event.MSI and reactions["MSI"] is None:
                reactions["MSI"] = time.time() - setTime
            print(*reactions.values(), sep="\n")



    root.fill(C_BG)
    pg.draw.rect(root, (0, 0, 0), (0, 0, LIGHT_SIZE, LIGHT_SIZE))

    if status == Event.Cross:
        #print("plus")
        MainLog.write(f"A{3 + roundCounter}", f"{roundCounter+1}")
        MainLog.write(f"C{3 + roundCounter}", f"{currentEmptyTime}")
        pg.draw.rect(root, (255, 255, 255), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
        pg.draw.line(root,C_PLUS, (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 - PLUS_SIZE), (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 + PLUS_SIZE), PLUS_WIDTH)
        pg.draw.line(root, C_PLUS, (WIN_SIZE[0] // 2 - PLUS_SIZE, WIN_SIZE[1] // 2), (WIN_SIZE[0] // 2 + PLUS_SIZE, WIN_SIZE[1] // 2), PLUS_WIDTH)
        #print(time.time() - setTime)
        if (time.time() - setTime > PLUS_TIME):
            setTime = time.time()
            status = Event.Empty
            currentEmptyTime = emptyTime()
    if status == Event.Empty:
        #print(currentEmptyTime)
        if (time.time() - setTime > currentEmptyTime):
            setTime = time.time()
            status = Event.Circle
            if port_work: time_code.write(bytearray([80 + (roundCounter + 1)]))
    if status == Event.Circle:
        pg.draw.circle(
            root,
            C_CIRCLE,
            (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2),
            20
        )
        if (time.time() - setTime > ANSWER_TIME):
            setTime = time.time()
            status = Event.MSI
    if status == Event.MSI:
        # --------------- Fill SpreadSheet ------------
        MainLog.write(f"B{3 + roundCounter}", f"{reactions["Plus"]}")
        MainLog.write(f"D{3 + roundCounter}", f"{reactions["Empty"]}")
        MainLog.write(f"E{3 + roundCounter}", f"{reactions["Circle"]}")
        MainLog.write(f"F{3 + roundCounter}", f"{reactions["MSI"]}")

        if (time.time() - setTime > MSI_TIME):
            setTime = time.time()
            status = Event.Cross
            reactions = {"Plus": None, "Empty": None, "Circle": None, "MSI": None}
            roundCounter += 1
            if port_work: time_code.write(bytearray([40 + (roundCounter + 1)]))
    if roundCounter >= ROUND:
        if port_work: time_code.write(bytearray([80 + (roundCounter + 1)]))
        run = False
#    clk.tick(60)
    pg.display.flip()

TABLE.close()