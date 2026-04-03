import numpy
import pygame as pg
import config as cfg
from trigger import Trigger, TimeStamp
from timer import Timer

class Alarm():
    def __init__(self, trigger: Trigger):
        cfg.loadConfig()
        config = cfg.getConfig()
        self.trigger = trigger
        pg.mixer.init()
        self.TONE = config["general"]["alarm"]
        self.WAVE_DATA = numpy.array([int(self.TONE["volume"]) * numpy.sin(
            2.0 * numpy.pi * int(self.TONE["freq"]) * x / 44100) for x in
                                range(0, 44100)]).astype(numpy.int16)
        self.sound = pg.sndarray.make_sound(numpy.c_[self.WAVE_DATA, self.WAVE_DATA])
        self.playFlag = False
        self.sirenTimer = Timer()

    def play(self):
        if int(self.TONE["enable"]) and not self.playFlag:
            self.trigger.send(TimeStamp.alarm)
            self.sound.play(-1)
            self.playFlag = True
            self.sirenTimer.setTimer()

    def isDone(self):
        if not int(self.TONE["enable"]) or (self.playFlag and self.sirenTimer.wait(self.TONE["duration"])):
            self.sound.stop()
            self.playFlag = False
            return True
        return False
