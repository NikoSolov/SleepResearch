# import libraries

import pygame as pg
import os
import numpy
import serial
import serial.tools.list_ports

import time 

file_name="Tasks "+time.strftime("%d.%m.%y %H.%M.%S")

# get settings from configuration file
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
        
#====================================================#
# initialize libraries
pg.mixer.init(44100,-16,2,512)
pg.init()

# initialize window
width,height=int(config["width"]), int(config["height"])
if int(config["fullscreen"]): root=pg.display.set_mode((width,height), pg.FULLSCREEN)
else: root=pg.display.set_mode((width,height))
clock=pg.time.Clock()

#initialize COM-Port 
port_work=True
portname=""
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    if "USB-SERIAL CH340" in desc:
        portname=port
if portname=="":  port_work=False

try:
    time_code=serial.Serial(port=portname, baudrate=9600, timeout=.1)
    time.sleep(2)
except Exception as e:
    port_work=False
#    print(e)

# create the siren's sample
arr = numpy.array([int(config["tone_volume"]) * numpy.sin(2.0 * numpy.pi * int(config["tone_rate"]) * x /44100) for x in range(0, 44100)]).astype(numpy.int16)
arr2 = numpy.c_[arr,arr]
sound = pg.sndarray.make_sound(arr2)

#play tone
if int(config["tone_play"])==1:# and port_work==True:
    print("play")
    if port_work: time_code.write(bytearray([1]))      
    sound.play(-1)
    pg.time.wait(int(float(config["tone_delay"])*1000))
    sound.stop()


# set to start program
main=True
#-----------------------------------------------------------------
#-----------------------------------------------------------------
from textGen import Gen
roundi=0

pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 150)

if not(os.path.exists("res")):
    os.mkdir("res")

if not(os.path.exists("blocks")):
    os.mkdir("blocks")

r=w=TT=FF=TF=FT=missed=0
sqr=200
red=0
green=0

log=[]
answer=True

fill=0
fillstep=1
new=True
file_not=False
dot_flag=True

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

if config["file"]!="None":
    try:
        fin=open("blocks/"+config["file"]+".txt", "r")
        #print(fin)
    except Exception as e:
        #print(e)
        file_not=True




size=100
good=sqr((width-size)/2, height/4-size/2, size, (0,255,0))
bad=sqr((width-size)/2, height*(3/4)-size/2, size, (255,0,0))
