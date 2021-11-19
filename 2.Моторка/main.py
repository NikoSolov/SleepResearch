import pygame as pg
from random import randint, choice
from init import *
from time import time
#----------------------------
#import imageio
#images = []
#---------------------------

pg.init()
if config["fullscreen"]: root=pg.display.set_mode((width,height), pg.FULLSCREEN)
else: root=pg.display.set_mode((width,height))

clock=pg.time.Clock()
game=True
photo=pg.Surface((width, height))
#vid=0
while game:
    
    if new==True:
        ri+=1
        if ri>config["round"]: break
        f=open("log_txt/"+str(ri)+".txt", "w")
        f.write("Траектории | Разрешение: "+str(width)+"x"+str(height)+" | Частота в секундах: "+str(config["freq"])+"\n")
        f.write("Зеленая\t\tСиняя\n")
        f.write("x\ty\tx\ty\n")
        tim=time()
        new=False
        photo.fill((128,128,128))
        pg.draw.circle(photo, (0,0,0), (hole.x, hole.y), hole.r)
        pg.draw.rect(photo, (255,0,0), (0,height-posible,posible, posible), width=2)
        s=0
        s2=0
#-norm------------------------------------------------v
        ball.x, ball.y=ball.r, height-ball.r
        path.x, path.y=ball.x+ball.r/2, ball.y-ball.r/2
#-------------------------------------------------^

        sign=choice([[True,1],[False,-1]])
        c=sign[1]*0.001*randint(4,8)

#-----------------------------------------------------v
    det_x, det_y= ball.x+ball.r/2, ball.y-ball.r/2
    det2_x, det2_y = path.x, path.y
#-----------------------------------------------------^

    for event in pg.event.get():
        if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE): game=False
        if event.type==pg.MOUSEWHEEL and (ball.x>posible or ball.y<height-posible):
            if config["inverse"]: ball.y+=event.y*20
            else: ball.y-=event.y*20
#-----------------------------------------------------------------------------------------------------------------v
#    print((time()-tim))
    
    if (time()-tim)>config["freq"]:
        tim=time()
#        print("check")
        f.write(str(int(ball.x+ball.r/2))+"\t"+str(int(ball.y-ball.r/2))+"\t"+str(int(path.x))+"\t"+str(int(path.y))+"\n")

    ball.y+=c*((not(sign[0]))*width-ball.x)
    ball.x+=5
    path.y+=c*((not(sign[0]))*width-ball.x)
    path.x+=5
    

    root.fill((128,128,128))
    pg.draw.circle(root, (0,0,0), (hole.x, hole.y), hole.r)
    pg.draw.circle(root, (128,0,0), (ball.x, ball.y), ball.r)
#------------------------------------------------------------------------------------------------------------------v
    pg.draw.line(photo, (0,255,0), (det_x, det_y), (ball.x+ball.r/2, ball.y-ball.r/2), 2)
    pg.draw.rect(photo, (0,0,255), (path.x, path.y, 3,3))
#-------------------------------------------------------------------------------------------------------------------^

    pg.display.update()
#    ---------------------------
#    pg.image.save(root, "vid/"+str(vid)+".png")
#    images.append(imageio.imread("vid/"+str(vid)+".png"))
#    vid+=1
#    ----------------------
    clock.tick(60)


    s+=(((ball.x+ball.r/2)-det_x)**2 + ((ball.y-ball.r/2)-det_y)**2)**(1/2)
    s2+=((path.x-det2_x)**2 + (path.y-det2_y)**2)**(1/2)


    l=((ball.x-hole.x)**2+(ball.y-hole.y)**2)**(1/2)
    flag=(l<=1.5*ball.r)
    if (ball.x+ball.r>width or ball.y+ball.r>height or ball.y-ball.r<0) or flag : 
        #pg.draw.circle(photo, (255,0,0), (ball.x, ball.y), ball.r)
        f.write(str(int(ball.x))+"\t"+str(int(ball.y))+"\t"+str(int(path.x))+"\t"+str(int(path.y))+"\n")
        f.close()
        pg.image.save(photo, "log_img/"+str(ri)+".png")      
        if flag: g+=1
        else: not_g+=1
        a.append([flag, round(s), round(s2)])
        new=True


pg.quit()
#imageio.mimsave('vid/movie.gif', images)
f=open("main_log.txt", "w")
f.write("Мыши:\tДобравшиеся\tПропавшие\n")
f.write("\t"+str(g)+"\t\t"+str(not_g)+"\n")
f.write("Раунд\tПопал\tДлина:\tСиний\tЗеленый\tРазница\n")
for i in range(len(a)):
    f.write(str(i+1)+"\t"+str(a[i][0])+"\t\t"+str(a[i][1])+"\t"+str(a[i][2])+"\t"+str(a[i][1]-a[i][2])+"\n")
f.close()
