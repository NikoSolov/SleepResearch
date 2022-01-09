import pygame as pg
import time
from init import *
from textGen import Gen
import serial

#----------------------------
#import imageio
#images = []
#vid=0
#---------------------------

pg.init()
pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 150)
game=True
clock=pg.time.Clock()
root=pg.display.set_mode((width,height))
fill=0
fillstep=1
new=True
file_not=False
dot_flag=True



if config["file"]!="None":
    try:
        fin=open("blocks/"+config["file"]+".txt", "r")
        #print(fin)
    except Exception as e:
        #print(e)
        file_not=True
        
while game:

    if new==True:
        root.fill((128,128,128))
        pg.draw.circle(root, (255,255,255), (width//2, height//2), (10))
        pg.display.update()

        if roundi==0 and int(config["tone_play"]): 
            sound.play(0)
            pg.time.delay(int(float(config["tone_delay"])*1000))
            sound.stop()
        a=time.time()

        dot_flag=True
        while time.time()-a<float(config["dot_time"]):
            pass
#        dot_flag=False
        roundi+=1
        if roundi>rounds: break
        a=time.time()
        new=False
        time_code.write(bytes("new"+str(roundi),'utf-8'))

        if config["file"]!="None" and file_not==False:
            d=fin.readline()
            #print(d)
            if d=="": break
            d=d.split()
            text = d[0] 
            res = bool(int(d[1]))
        else:
            #print("Gen")
            d=Gen()
            text = d[2] 
            res = bool(int(d[1]))
        if res==True: r+=1
        else: w+=1

    for event in pg.event.get():
        if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE): game=False
        if event.type==pg.MOUSEWHEEL:
            if event.y>0:
                good.fill-=event.y*int(config["sensivity"])
                bad.fill=0
            else:
                bad.fill-=event.y*int(config["sensivity"])
                good.fill=0
        if dot_flag==True: bad.fill=0; good.fill=0; dot_flag=False


    if abs(good.fill)>size or abs(bad.fill)>size:
        if abs(good.fill)>size:
            log.append([str(roundi),text,str(res),"True"])
            answer=True
        if abs(bad.fill)>size:
            log.append([str(roundi),text,str(res),"False"])
            answer=False


        if res == True and answer == True:
            TT+=1
        if res == False and answer == False:
            FF+=1
        if res == True and answer == False:
            TF+=1
        if res == False and answer == True:
            FT+=1
        
        good.fill=0
        bad.fill=0
        new=True


    if time.time()-a>float(config["time"]):
        log.append([str(roundi),text,str(res),"Missed"])
        bad.fill=good.fill=0
        missed+=1
        new=True

#-----------------------------v
    textSur = myfont.render(text, True, (255, 255, 255))
    root.fill((128,128,128))
    root.blit(textSur,((width-textSur.get_width())/2,(height-textSur.get_height())/2))
    good.draw(root)
    bad.draw(root)
    pg.display.update()
    clock.tick(60)
#    ---------------------------
#    pg.image.save(root, "vid/"+str(vid)+".png")
#    images.append(imageio.imread("vid/"+str(vid)+".png"))
#    vid+=1
#    ----------------------
#-----------------------------^
pg.quit()


#imageio.mimsave('vid/movie.gif', images)
fout=open("log.txt", "w")
fout.write("Раунд\tПример\tОценка_примера\tОтветил\n")
for i in log:
    fout.write(i[0]+"\t"+i[1]+"\t"+i[2]+"\t\t"+i[3]+"\n")
fout.write("Задачи\t\t\tОтветил\nTrue\tFalse\t\tT->T\tF->F\tT->F\tF->T\tMissed\n")
fout.write(str(r)+"\t"+str(w)+"\t\t"+str(TT)+"\t"+str(FF)+"\t"+str(TF)+"\t"+str(FT)+"\t"+str(missed)+"\n")
fout.close()
