from timer import Timer
import config as cfg

class LightSensor:
    def __init__(self):
        cfg.loadConfig()
        config = cfg.getConfig()
        self.LIGHT_DURATION = 0.1
        self.LIGHT_ENABLE = config["general"]["timeStamps"]["light"]
        self.lightTimer = Timer()

    def pulse(self):
        self.lightTimer.setTimer()

    def lightUp(self):
        return True if (self.LIGHT_ENABLE and not self.lightTimer.wait(self.LIGHT_DURATION)) else False