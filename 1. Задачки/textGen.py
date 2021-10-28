import pygame as pg
from random import randint, choice


pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 150)
def Gen():
    global myfont
    res = choice([True, False])
    a=randint(0,50)
    b=randint(0,9)
    if res==True:
        c=a+b
    if res == False:
        c=randint(0,59)
    text=str(a)+"+"+str(b)+"="+str(c)
    textSur = myfont.render(text, True, (255, 255, 255))
    return textSur, res
