import pygame as pg
import os
import numpy


pg.mixer.init(44100,-16,2,512)

if not(os.path.exists("blocks")):
    os.mkdir("blocks")

#=========> config init <==============#
configstd={"fullscreen": 0, 
            "inverse": 0, 
            "round": 20, 
            "width": 1024, 
            "height": 768, 
            "sensivity": 20, 
            "time":5, 
            "dot_time":0.5,
            "file": "None",
            "tone_play": 1,
            "tone_rate": 440,
            "tone_volume": 4096,
            "tone_delay": 1.5,
            "COM-Port": "COM21",
            "COM-Rate": 115200
            }

config={}
if not(os.path.exists("config.txt")):
    config=configstd
    f=open("config.txt", "w")
    for i in config:
        f.write(str(i)+" "+str(config[i])+"\n")
    f.close()
else:
    f=open("config.txt", "r")
    for i in f:
        try:
            if '\n' in i:
                config.update({i.split(" ")[0]:i.split(" ")[1][:-1]}) 
            else:
                config.update({i.split(" ")[0]:i.split(" ")[1]}) 
        except Exception as e:
            pass
    
    for i in configstd.keys():
        if not(i in config.keys()):
            config.update({i:configstd.get(i)}) 
#    print(config)    
#====================================================#

            
rounds=int(config["round"])
roundi=0
r=w=TT=FF=TF=FT=missed=0
sqr=200
red=0
green=0
width,height=int(config["width"]), int(config["height"])
log=[]
answer=True
class sqr():
    intances=[]
    def __init__(self, x, y, size, color, fill=0):
        self.x=x
        self.y=y
        self.size=size
        self.color=color
        self.fill=fill
        sqr.intances.append(self)
    def draw(self, root):
        pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.size), width=2)
        if self.fill<0:
        #    print(self.x, self.size-self.fill, self.size, self.fill)
            pg.draw.rect(root, self.color, (self.x, self.y+self.size+self.fill, self.size, abs(self.fill)))
        elif self.fill>0:
            pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.fill))

size=100
good=sqr((width-size)/2, height/4-size/2, size, (0,255,0))
bad=sqr((width-size)/2, height*(3/4)-size/2, size, (255,0,0))

arr = numpy.array([int(config["tone_volume"]) * numpy.sin(2.0 * numpy.pi * int(config["tone_rate"]) * x /44100) for x in range(0, 44100)]).astype(numpy.int16)
arr2 = numpy.c_[arr,arr]
sound = pg.sndarray.make_sound(arr2)

time_code=serial.Serial(port=config["COM-Port"], baudrate=int(config["COM-Rate"]), timeout=.1)


'''
    def draw(self, root):
        pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.size), width=2)
        if self.fill<0:
            pg.draw.rect(root, self.color, (self.x, self.size-self.fill, self.size, self.fill))
        elif self.fill>0:
            pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.fill))
'''
'''
    def draw(root):
        for i in sqr.intances:  
            pg.draw.rect(root, i.color, (i.x, i.y, i.size, i.size), width=2)

            if i.fill<0:
                pg.draw.rect(root, i.color, (i.x, i.y+i.size-i.fill, i.size, i.fill))
            elif i.fill>0:
                pg.draw.rect(root, i.color, (i.x, i.y, i.size, i.fill))
'''