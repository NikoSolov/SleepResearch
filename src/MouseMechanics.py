import numpy as np
from random import choice as ch
from random import uniform as rd
import config as cfg

class MouseMechanics():

    def __init__(self):
        # Constants
        cfg.loadConfig()
        config = cfg.getConfig()
        SIZES = config["Mouses"]["graphics"]["sizes"]

        self.RADIUS_MOUSE = SIZES["radius"]
        self.RADIUS_HOLE = SIZES["radius"]

        self.WAIT_ZONE = SIZES["waitZone"]
        self.DISTANCE_MULTIPLIER = SIZES["distMul"]
        self.STEP = SIZES["speed"]
        self.MAX_DISPERSION = SIZES["maxDispersion"]

        self.WIN_SIZE = np.array([config["general"]["window"]["width"],
                            config["general"]["window"]["height"]])

        self.START_POS = np.array([self.RADIUS_MOUSE, self.WIN_SIZE[1]-self.RADIUS_MOUSE])
        self.HOLE_POS = np.array([self.WIN_SIZE-self.RADIUS_HOLE])
        self.P0 = self.START_POS
        self.BOTTOM_POS = lambda disp: np.array([
            self.WIN_SIZE[0] - self.RADIUS_MOUSE,
            (1 - disp) * (self.RADIUS_HOLE + 2 * np.sqrt(self.RADIUS_HOLE * self.RADIUS_MOUSE)) + disp * (np.min(self.WIN_SIZE) - self.RADIUS_MOUSE)
        ])
        self.TOP_POS = lambda disp: np.array([
            (1 - disp) * (self.WIN_SIZE[0] - self.RADIUS_HOLE - 2 * np.sqrt(self.RADIUS_HOLE * self.RADIUS_MOUSE)) + disp * (self.WIN_SIZE[0] - np.min(self.WIN_SIZE) + self.RADIUS_MOUSE),
            self.RADIUS_MOUSE
        ])
        self.TOP_POS2 = lambda disp: np.array([
            self.WIN_SIZE[0] - self.RADIUS_HOLE - 2 * np.sqrt(self.RADIUS_HOLE * self.RADIUS_MOUSE),
            (1 - disp) * self.RADIUS_MOUSE + disp * (3*self.RADIUS_MOUSE-np.min(self.WIN_SIZE))
        ])

        self.CRIT_POS = [self.BOTTOM_POS, self.TOP_POS]

        # Variables
        self.disp = rd(0.001, self.MAX_DISPERSION)  # 0.001 - min by imperical way
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
        self.disp = rd(0.001, self.MAX_DISPERSION)  # 0.001 - min by imperical way
        self.BallPos = self.START_POS

        choice = ch([0, 1, 2, 3])
        self.P2 = [
            self.BOTTOM_POS(self.disp),
            self.TOP_POS(self.disp)
        ][choice // 2]

        if choice == 2:
            self.P2 = self.TOP_POS2(self.disp)

        self.P1 = [
            np.array([(self.P2[0] + self.P0[0])/2, self.P0[1]]),
            # np.array([(self.P2[0] + self.P0[0])/2, self.P2[1]]), # to keep symmetry
            np.array([self.P0[0], (self.P2[1] + self.P0[1])/2]),
            # np.array([self.P2[0], (self.P2[1] + self.P0[1])/2]) # will fly back
        ][choice % 2]

        # self.answer = [
        #     [
        #        self.CRIT_POS[0](0)[1] - self.RADIUS_MOUSE
        #      - (self.P2[1] - self.RADIUS_MOUSE) 
        #      * ((
        #          (self.CRIT_POS[0](0)[0] - self.RADIUS_HOLE)
        #         /(self.P2[0] - self.RADIUS_HOLE)
        #     )** 2),
        #        self.CRIT_POS[1](0)[1] - self.RADIUS_MOUSE
        #      - (self.P2[1] - self.RADIUS_MOUSE) 
        #      * ((
        #          (self.CRIT_POS[0](0)[0] - self.RADIUS_HOLE)
        #         /(self.P2[0] - self.RADIUS_HOLE)
        #     )** 2)
        #     ],
        #     [
        #        self.CRIT_POS[0](0)[1] - self.RADIUS_MOUSE
        #      - (self.P2[1] - self.RADIUS_MOUSE) 
        #      * np.sqrt(
        #          (self.CRIT_POS[0](0)[0]         - self.RADIUS_HOLE)
        #        / (self.P2[0] - self.RADIUS_HOLE)
        #     ),
        #        self.CRIT_POS[1](0)[1] - self.RADIUS_MOUSE
        #      - (self.P2[1] - self.RADIUS_MOUSE) 
        #      * np.sqrt(
        #          (self.CRIT_POS[0](0)[0]         - self.RADIUS_HOLE)
        #        / (self.P2[0] - self.RADIUS_HOLE)
        #     )
        #     ]
        # ]
        # # ][choice]
        # ic(self.answer)

    def getPos(self):
        return self.function(self.t) + np.array([0, self.yOffset])

    def step(self):
        self.t += self.STEP / np.linalg.norm(
            2 * (self.P0 - 2 * self.P1 + self.P2) * self.t +
            2 * (self.P1 - self.P0)
        )

    def touchWall(self) -> bool:
        return (
            any(self.getPos() <= self.RADIUS_MOUSE) or
            any(self.getPos() >= self.WIN_SIZE - self.RADIUS_MOUSE)
        )

    def touchHole(self) -> bool:
        return np.linalg.norm(
            self.getPos() - np.array([self.WIN_SIZE[0] - self.RADIUS_HOLE, self.RADIUS_HOLE])
        ) < (self.DISTANCE_MULTIPLIER/2) * (self.RADIUS_MOUSE + self.RADIUS_HOLE) # ???
        # ) < self.DISTANCE_MULTIPLIER * self.RADIUS_MOUSE # ???

    def drag(self, delta):
        self.lastT = self.t
        self.yOffset += delta
        # ic(self.yOffset)

    def isOutWaitZone(self) -> bool:
        return np.linalg.norm(
            self.getPos() - np.array([self.RADIUS_MOUSE, self.WIN_SIZE[1] - self.RADIUS_MOUSE])
        ) > self.WAIT_ZONE

    def bezier(self, t:float, P0, P1, P2):
        return (
            P0 * (1 - t) * (1 - t)
          + P1 * 2 * (1 - t) * t
          + P2 * t * t 
        )

    def function(self, t: float):
        return self.bezier(
            t, 
            self.P0,
            self.P1,
            self.P2
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
    
    def getCorridor(self):
        P2 = [
            self.BOTTOM_POS(0),
            self.TOP_POS(0)
        ]

        P1 = [
            np.array([(P2[0][0] + self.P0[0])/2, self.P0[1]]),
            np.array([self.P0[0], (P2[1][1] + self.P0[1])/2]),
        ]

        endP2 = [
            np.array([
                self.WIN_SIZE[0],
                (P2[0][1]-self.START_POS[1])
                /((P2[0][0]-self.START_POS[0])**2)
                *((self.WIN_SIZE[0]-self.START_POS[0])**2)
                 + self.START_POS[1]
            ]),
            np.array([
                (P2[1][0]-self.START_POS[0])
                /((2*P2[1][1]-self.WIN_SIZE[1])**2) 
                *((self.START_POS[1])**2)
                + self.START_POS[0],
                0
            ])
        ]
        return (
            [self.P0, P1[0], endP2[0]],
            [self.P0, P1[1], endP2[1]]
        )
    
    def inCorridor(self) -> bool:
        cur = self.getPos()

        P2_bot = self.BOTTOM_POS(0)
        P2_top = self.TOP_POS(0)

        P1_bot = np.array([(P2_bot[0] + self.P0[0]) / 2, self.P0[1]], dtype=int)
        P1_top = np.array([self.P0[0], (P2_top[1] + self.P0[1]) / 2], dtype=int)

        coef_bot = self.P0 - 2.0 * P1_bot + P2_bot
        coef_top = self.P0 - 2.0 * P1_top + P2_top

        t12 = ((self.P0 - P1_bot - np.sqrt(cur * coef_bot + P1_bot**2 - P2_bot * self.P0)) / coef_bot)[1]
        t21 = ((self.P0 - P1_top + np.sqrt(cur * coef_top + P1_top**2 - P2_top * self.P0)) / coef_top)[0]

        botPosX1 = self.bezier(t12, self.P0, P1_bot, P2_bot).astype(int)
        botPosX2 = self.bezier(t21, self.P0, P1_top, P2_top).astype(int)

        return (botPosX1[0] - cur[0]) > 0 and (cur[1] - botPosX2[1]) > 0