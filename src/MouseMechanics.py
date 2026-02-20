import numpy as np
from random import choice as ch
from random import uniform as rd
import config as cfg

cfg.loadConfig()

config = cfg.getConfig()
SIZES = config["Mouses"]["graphics"]["sizes"]

RADIUS_MOUSE = SIZES["radius"]
RADIUS_HOLE = SIZES["radius"]

WAIT_ZONE = SIZES["waitZone"]
DISTANCE_MULTIPLIER = SIZES["distMul"]
STEP = SIZES["speed"]
MAX_DISPERSION = SIZES["maxDispersion"]


WIN_SIZE = np.array([config["general"]["window"]["width"],
                     config["general"]["window"]["height"]])

class MouseMechanics():

    def __init__(self):
        # Constants
        self.START_POS = np.array([RADIUS_MOUSE, WIN_SIZE[1]-RADIUS_MOUSE])
        self.HOLE_POS = np.array([WIN_SIZE-RADIUS_HOLE])
        self.P0 = self.START_POS
        self.BOTTOM_POS = lambda disp: np.array([
            WIN_SIZE[0] - RADIUS_MOUSE,
            (1 - disp) * (RADIUS_HOLE + 2 * np.sqrt(RADIUS_HOLE * RADIUS_MOUSE)) + disp * (np.min(WIN_SIZE) - RADIUS_MOUSE)
        ])
        self.TOP_POS = lambda disp: np.array([
            (1 - disp) * (WIN_SIZE[0] - RADIUS_HOLE - 2 * np.sqrt(RADIUS_HOLE * RADIUS_MOUSE)) + disp * (WIN_SIZE[0] - np.min(WIN_SIZE) + RADIUS_MOUSE),
            RADIUS_MOUSE
        ])

        self.CRIT_POS = [self.BOTTOM_POS, self.TOP_POS]

        self.STEP = STEP
        # Variables
        self.disp = rd(0.001, MAX_DISPERSION)  # 0.001 - min by imperical way
        self.P2 = ch([
            self.BOTTOM_POS(self.disp),
            self.TOP_POS(self.disp)
        ])
        self.P1 = ch([
            np.array([(self.P2[0] + self.START_POS[0])/2, self.START_POS[1]]),
            np.array([self.START_POS[0], (self.P2[1] + self.START_POS[1])/2])
        ])
        self.t = 0
        self.lastT = 0
        self.BallPos = self.START_POS
        self.yOffset = 0

    def startTrail(self):
        self.t = 0
        self.yOffset = 0
        self.lastT = 0
        self.disp = rd(0.001, MAX_DISPERSION)  # 0.001 - min by imperical way
        self.BallPos = self.START_POS

        choice = ch([0, 1, 2, 3])
        self.P2 = [
            self.BOTTOM_POS(self.disp),
            self.TOP_POS(self.disp)
        ][choice // 2]

        self.P1 = [
            np.array([(self.P2[0] + self.P0[0])/2, self.P0[1]]),
            # np.array([(self.P2[0] + self.P0[0])/2, self.P2[1]]), # to keep symmetry
            np.array([self.P0[0], (self.P2[1] + self.P0[1])/2]),
            # np.array([self.P2[0], (self.P2[1] + self.P0[1])/2]) # will fly back
        ][choice % 2]

        # self.answer = [
        #     [
        #         self.CRIT_POS[choice // 2](0)[1] 
        #      - (self.CRIT_POS[choice // 2](self.disp)[1] - RADIUS_MOUSE) 
        #      * (
        #          (self.CRIT_POS[choice // 2](0)[0]         - RADIUS_HOLE) 
        #        / (self.CRIT_POS[choice // 2](self.disp)[0] - RADIUS_HOLE)
        #        ) ** 2
        #      - RADIUS_MOUSE,
        #     ],
        #     0,
        #     0,
        #     0
        # ][choice]
        # print(self.answer)

    def getPos(self):
        return self.function(self.t) + np.array([0, self.yOffset])

    def step(self):
        self.t += self.STEP / np.linalg.norm(
            2 * (self.P0 - 2 * self.P1 + self.P2) * self.t +
            2 * (self.P1 - self.P0)
        )

    def touchWall(self) -> bool:
        return (
            any(self.getPos() <= RADIUS_MOUSE) or
            any(self.getPos() >= WIN_SIZE - RADIUS_MOUSE)
        )

    def touchHole(self) -> bool:
        return np.linalg.norm(
            self.getPos() - np.array([WIN_SIZE[0] - RADIUS_HOLE, RADIUS_HOLE])
        ) < (DISTANCE_MULTIPLIER/2) * (RADIUS_MOUSE + RADIUS_HOLE) # ???
        # ) < DISTANCE_MULTIPLIER * RADIUS_MOUSE # ???

    def drag(self, delta):
        self.lastT = self.t
        self.yOffset += delta
        print(self.yOffset)

    def isOutWaitZone(self) -> bool:
        return np.linalg.norm(
            self.getPos() - np.array([RADIUS_MOUSE, WIN_SIZE[1] - RADIUS_MOUSE])
        ) > WAIT_ZONE

    def function(self, t: float):
        return (
            self.P0 * (1 - t) * (1 - t)
          + self.P1 * 2 * (1 - t) * t
          + self.P2 * t * t 
        )

    def derivative(self, t):
        return (
          - self.P0 * 2 * (1 - t)
          + self.P1 * 2 * (1 - 2 * t)
          + self.P2 * 2 * t 
        )

    def getPartial(self):
        return (np.array([
            self.function(self.lastT), # last Pos
            (self.t - self.lastT) / 2 * self.derivative(self.lastT) + self.function(self.lastT),
            self.function(self.t) # current Pos
        ]) + np.array([0, self.yOffset])).astype(np.int16)
        
    def getDots(self):
        return np.array([self.P0, self.P1, self.P2]).astype(np.int16)