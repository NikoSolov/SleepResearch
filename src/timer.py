from time import time

class Timer():
  def __init__(self):
    self.savedTime = time()
  def setTimer(self, curTime=None):
    self.savedTime = time() if curTime is None else curTime
  def getTimer(self):
    return self.savedTime
  def wait(self, duration):
    return (time() - self.savedTime) > duration
  def getDelta(self):
    return (time() - self.savedTime)

