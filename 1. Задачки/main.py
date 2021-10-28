import pygame as pg
from textGen import Gen
import time

pg.init()
game=True
clock=pg.time.Clock()
width,height=1024,768
root=pg.display.set_mode((width,height))
c=20
r=w=p_r=p_w=s_r=s_w=0

new=True
while game:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            game=False
        if event.type==pg.MOUSEBUTTONDOWN and event.button<4:
            if res==True: p_r+=1
            else: p_w+=1
            new=True
    root.fill((128,128,128))


    if new==True:
        c-=1
        if c<0: break
        a=time.time()
        new=False
        
        textSur, res=Gen()
        if res==True: r+=1
        else: w+=1

    if time.time()-a>5:
        if res==True: s_r+=1
        else: s_w+=1
        new=True

    root.blit(textSur,((width-textSur.get_width())/2,(height-textSur.get_height())/2))
    clock.tick(60)
    pg.display.update()
pg.quit()

f=open("log.txt", "w")
f.write("Задачи\t\t\tНажатые\t\t\tПропущенные\nВерные\tНеверные\tВерные\tНеверные\tВерные\tНеверные\n")
f.write(str(r)+"\t"+str(w)+"\t\t"+str(p_r)+"\t"+str(p_w)+"\t\t"+str(s_r)+"\t"+str(s_w))
f.close()


