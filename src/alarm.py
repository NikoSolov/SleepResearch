import time
import numpy
import pygame as pg
import config as cfg
import trigger


class Alarm():
    def __init__(self):
        cfg.loadConfig()
        config = cfg.getConfig()
        pg.mixer.init()
        self.TONE = config["general"]["alarm"]
        self.WAVE_DATA = numpy.array([int(self.TONE["volume"]) * numpy.sin(
            2.0 * numpy.pi * int(self.TONE["freq"]) * x / 44100) for x in
                                range(0, 44100)]).astype(numpy.int16)
        self.sound = pg.sndarray.make_sound(numpy.c_[self.WAVE_DATA, self.WAVE_DATA])
        self.playFlag = False
        self.sirenTime = 0

    def play(self):
        if int(self.TONE["enable"]) and not self.playFlag:
            trigger.send(trigger.TimeStamp.alarm)
            self.sound.play(-1)
            self.playFlag = True
            self.sirenTime = time.time()

    def isDone(self):
        if not int(self.TONE["enable"]) or (self.playFlag and time.time() - self.sirenTime > self.TONE["duration"]):
            self.sound.stop()
            self.playFlag = False
            return True
        return False
