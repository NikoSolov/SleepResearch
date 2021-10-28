import pygame as pg
from random import randint, choice
from init import *

pg.init()
if config["fullscreen"]: root=pg.display.set_mode((width,height), pg.FULLSCREEN)
else: root=pg.display.set_mode((width,height))

clock=pg.time.Clock()
game=True
photo=pg.Surface((width, height))

while game:

    if new==True:
        new=False
        ri+=1
        if ri>config["round"]: break
        photo.fill((128,128,128))
        pg.draw.circle(photo, (0,0,0), (hole.x, hole.y), hole.r)
        s=0
        s2=0

        ball.x, ball.y=ball.r, height-ball.r
        path.x, path.y=ball.x, ball.y

        sign=choice([True,False])
        c=1+randint(1,5)*sign    
        
        sign=1*(sign==False)-1*(sign==True)
        cstep=randint(1,5)*sign*0.01
        #cstep=sign*0.04
        print(c, cstep)

    det_x, det_y= ball.x, ball.y
    det2_x, det2_y = path.x, path.y

    for event in pg.event.get():
        if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE): game=False
        if event.type==pg.MOUSEWHEEL:
            if config["inverse"]: ball.y+=event.y*20
            else: ball.y-=event.y*20

    ball.y+=(-1)*c  
    ball.x+=5

    path.y+=(-1)*c  
    path.x+=5
    
    root.fill((128,128,128))
    pg.draw.circle(root, (0,0,0), (hole.x, hole.y), hole.r)
    pg.draw.circle(root, (128,0,0), (ball.x, ball.y), ball.r)
    pg.draw.line(photo, (0,255,0), (det_x, det_y), (ball.x, ball.y), 2)
    pg.draw.rect(photo, (0,0,255), (path.x, path.y, 3,3))
    pg.display.update()
    clock.tick(60)


    s+=((ball.x-det_x)**2 + (ball.y-det_y)**2)**(1/2)
    s2+=((path.x-det2_x)**2 + (path.y-det2_y)**2)**(1/2)
    c+=cstep

    l=((ball.x-hole.x)**2+(ball.y-hole.y)**2)**(1/2)
    flag=(l<=ball.r)


    if (ball.x+ball.r>width or ball.y+ball.r>height or ball.y-ball.r<0) or flag : 
        pg.draw.circle(photo, (255,0,0), (ball.x, ball.y), ball.r)
        pg.image.save(photo, "log_img/"+str(ri)+".png")      
        if flag: g+=1
        else: not_g+=1
        a.append([flag, round(s), round(s2)])
        new=True
        #print(round(s), round(s2))



pg.quit()
f=open("main_log.txt", "w")
f.write("Мыши:\tДобравшиеся\tПропавшие\n")
f.write("\t"+str(g)+"\t\t"+str(not_g)+"\n")
f.write("Раунд\tПопал\tДлина:\tСиний\tЗеленый\tРазница\n")
for i in range(len(a)):
    f.write(str(i+1)+"\t"+str(a[i][0])+"\t\t"+str(a[i][1])+"\t"+str(a[i][2])+"\t"+str(a[i][1]-a[i][2])+"\n")
f.close()