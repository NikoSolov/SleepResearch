import pygame as pg
import lightSensor
import config as cfg

cfg.loadConfig()
config = cfg.getConfig()

class Graphics():
  def __init__(self, program):
    pg.init()
    if program == "Equation":
      pg.font.init()
    # ------------------------------
    self.WIN_SIZE = pg.Vector2([
       config["general"]["window"]["width"], 
       config["general"]["window"]["height"]
    ])
    # ------------------------------
    self.root = pg.display.set_mode(
      self.WIN_SIZE, 
      flags = pg.FULLSCREEN if config["general"]["window"]["fullScreen"] 
      else pg.SHOWN
    )
    self.clk = pg.time.Clock()
    self.program = program
    self.generalGraphicDict = config["general"]["graphics"]
    self.programGraphicDict = config[self.program]["graphics"]

    self.generalColorDict = self.generalGraphicDict["colors"]
    self.generalSizeDict  = self.generalGraphicDict["sizes"]

    self.programColorDict = self.programGraphicDict["colors"]
    self.programSizeDict  = self.programGraphicDict["sizes"]

  def drawInit(self):
    self.root.fill(self.generalColorDict["bg"])
    lightSensor.draw(self.root)     
  def drawPlus(self):
      C_PLUS = pg.Color(self.generalColorDict["plus"])
      S_PLUS_RADIUS = self.generalSizeDict["plus"]["radius"]
      S_PLUS_WIDTH  = self.generalSizeDict["plus"]["width"]
      pg.draw.line(self.root, C_PLUS,
                  self.WIN_SIZE // 2 + pg.Vector2([0, -1]) *  S_PLUS_RADIUS,
                  self.WIN_SIZE // 2 + pg.Vector2([0,  1]) *  S_PLUS_RADIUS,
                  S_PLUS_WIDTH)
      pg.draw.line(self.root, C_PLUS,
                  self.WIN_SIZE // 2 + pg.Vector2([-1, 0]) *  S_PLUS_RADIUS,
                  self.WIN_SIZE // 2 + pg.Vector2([ 1, 0]) *  S_PLUS_RADIUS,
                  S_PLUS_WIDTH)

  def drawControl(self, status, Event):
    self.drawInit()
    match status:
        case Event.Siren:
          self.root.fill((0, 0, 0))
        case Event.Plus:
          self.drawPlus()
    self.update()

  def drawPVT(self, status, Event):
    self.drawInit()
    match status:
        case Event.Siren:
          self.root.fill((0, 0, 0))
        case Event.Plus:
          self.drawPlus()
        case Event.Circle:
            pg.draw.circle(
                self.root,
                pg.Color(self.programColorDict["circle"]),
                self.WIN_SIZE // 2,
                self.programSizeDict["circleRadius"]
            )
    self.update()

  def drawTasks(self, status, Event, equationText, rightLevel, wrongLevel):
    # ----------------------------
    C_RIGHT = self.programColorDict['right']
    C_WRONG = self.programColorDict['wrong']
    C_FONT = self.programColorDict['font']
    FONT = self.programGraphicDict['font']
    # ----------------------------
    S_SQR_WIDTH = self.programSizeDict['squares']['width']
    S_SQR_LENGTH = self.programSizeDict['squares']['length']
    # ----------------------------    
    equationFont = pg.font.SysFont(FONT, self.programSizeDict['font'])

    self.drawInit()

    def drawSquare(
          color = C_RIGHT, 
          pos = [
              (self.WIN_SIZE[0] - S_SQR_LENGTH) // 2,
              (self.WIN_SIZE[1] - 2 * S_SQR_LENGTH) // 4
          ], 
          sqrHeight = 1, 
          sqrWidth = S_SQR_WIDTH
      ):
      pg.draw.rect(self.root, pg.Color(color),
          (
              *pos,
              S_SQR_LENGTH, 
              S_SQR_LENGTH * sqrHeight
          ), 
          sqrWidth
      )

    match status:
        case Event.Siren:
            self.root.fill((0, 0, 0))
        case Event.Plus | Event.AnswerPlus:
            self.drawPlus()
        case Event.Answer:
            drawSquare(
                color = C_RIGHT, 
                pos = (
                    self.WIN_SIZE // 2 - pg.Vector2([0, self.WIN_SIZE[1]//4]) 
                    - pg.Vector2([1,1]) * S_SQR_LENGTH // 2
                )
            )
            drawSquare(
                color = C_WRONG, 
                pos = (
                    self.WIN_SIZE // 2 + pg.Vector2([0, self.WIN_SIZE[1]//4]) 
                    - pg.Vector2([1,1]) * S_SQR_LENGTH // 2
                )
            )
            drawSquare(
                color = C_RIGHT, 
                pos = (
                    self.WIN_SIZE // 2 - pg.Vector2([0, self.WIN_SIZE[1]//4])
                    - pg.Vector2([1, 2*rightLevel-1]) * S_SQR_LENGTH // 2
                ),
                sqrWidth = 0,
                sqrHeight = rightLevel
            )
            drawSquare(
                color = C_WRONG, 
                pos = (
                    self.WIN_SIZE // 2 
                    + pg.Vector2([0, self.WIN_SIZE[1]//4]) 
                    - pg.Vector2([1,1]) * S_SQR_LENGTH // 2
                ),
                sqrWidth = 0,
                sqrHeight = wrongLevel
            )
            equationSurf = equationFont.render(
                equationText, True, pg.Color(C_FONT)
            )
            self.root.blit(equationSurf,
                self.WIN_SIZE // 2 - pg.Vector2(equationSurf.get_size()) // 2
            )
    self.update()    

  def drawMouses(self, status, Event, BallPos):
    self.drawInit()
    C_MOUSE = self.programColorDict["mouse"]
    C_HOLE  = self.programColorDict["hole"]
    RADIUS = self.programSizeDict["radius"]

    # -------- draw a hole ----------
    pg.draw.circle(
        self.root,
        pg.Color(C_HOLE),
        (self.WIN_SIZE[0] - RADIUS, RADIUS),
        RADIUS
    )

    match status:
        case Event.siren:
          self.root.fill((0, 0, 0))
        case Event.answer:
            # ------- draw a mouse ---------
            pg.draw.circle(self.root, pg.Color(C_MOUSE), BallPos, RADIUS)
        case Event.plus:
            self.drawPlus()

    self.update()

  def update(self):
    self.clk.tick(60)
    pg.display.flip()
  def close(self):
    pg.quit()

