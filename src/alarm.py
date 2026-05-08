import config as cfg
from trigger import Trigger, TimeStamp
from timer import Timer
from graphics import Sound

class Alarm():
    def __init__(self, trigger: Trigger):
        cfg.loadConfig()
        config = cfg.getConfig()
        self.trigger = trigger
        self.TONE = config["general"]["alarm"]
        self.sound = Sound(
            self.TONE["volume"],
            self.TONE["freq"]
        )

        self.playFlag = False
        self.sirenTimer = Timer()

    def play(self):
        if int(self.TONE["enable"]) and not self.playFlag:
            self.trigger.send(TimeStamp.alarm)
            self.sound.play()
            self.playFlag = True
            self.sirenTimer.setTimer()

    def isDone(self):
        if not int(self.TONE["enable"]) or (self.playFlag and self.sirenTimer.wait(self.TONE["duration"])):
            self.sound.stop()
            self.playFlag = False
            return True
        return False
