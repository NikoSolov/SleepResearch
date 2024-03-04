import time
import numpy
import pygame as pg
import config as cfg

cfg.loadConfig()
config = cfg.getConfig()

pg.mixer.init()
TONE = config["general"]["siren"]
WAVE_DATA = numpy.array([int(TONE["volume"]) * numpy.sin(
    2.0 * numpy.pi * int(TONE["freq"]) * x / 44100) for x in
                         range(0, 44100)]).astype(numpy.int16)
sound = pg.sndarray.make_sound(numpy.c_[WAVE_DATA, WAVE_DATA])
playFlag = False
sirenTime = 0

SIREN_TIME = TONE["duration"]


def play():
    global sound, playFlag, sirenTime
    if int(TONE["enable"]) and not playFlag:
        sound.play(-1)
        playFlag = True
        sirenTime = time.time()


def isDone():
    if playFlag and time.time() - sirenTime > SIREN_TIME:
        stop()
        return True
    return False


def stop():
    global playFlag
    if playFlag:
        sound.stop()
        playFlag = False
