import time

import pygame as pg

import config as cfg

cfg.loadConfig()
config = cfg.getConfig()

LIGHT_DURATION = 0.1
LIGHT_ENABLE = config["general"]["timeStamps"]["light"]
LIGHT_SIZE = config["general"]["timeStamps"]["lightSize"]
lightTime = 0


def pulse():
    global lightTime
    lightTime = time.time()


def draw(root):
    global lightTime, LIGHT_DURATION
    if LIGHT_ENABLE:
        pg.draw.rect(root, (0, 0, 0), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
        if time.time() - lightTime <= LIGHT_DURATION:
            pg.draw.rect(root, (255, 255, 255), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
            lightOn = False
