# import libraries
import os
import numpy
import pygame as pg
import serial
import time
import serial.tools.list_ports

dir_name="Mouse "+time.strftime("%d.%m.%y %H.%M.%S")

# get settings from configuration file
configstd={"fullscreen": 0, 
            "inverse": 0, 
            "round": 20, 
            "width": 1024, 
            "height": 768, 
            "possible": 200, 
            "freq": 0.25, 
            "radius_multiplier": 1.5,
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
if int(config["tone_play"])==1:
    if port_work: time_code.write(bytearray([1]))      
    sound.play(-1)
    pg.time.wait(int(float(config["tone_delay"])*1000))
    sound.stop()

# set to start program
main=True
#-----------------------------------------------------
#-----------------------------------------------------
from random import randint, choice

posible=int(config["possible"])
coef=float(config["radius_multiplier"])

photo=pg.Surface((width, height))
if not(os.path.exists("res")):
    os.mkdir("res")
if not(os.path.exists("res/"+dir_name)):
    os.mkdir("res/"+dir_name)
if not(os.path.exists("res/"+dir_name+"/log_img")):
    os.mkdir("res/"+dir_name+"/log_img")
if not(os.path.exists("res/"+dir_name+"/log_txt")):
    os.mkdir("res/"+dir_name+"/log_txt")

class ball():
    x=0
    r=40
    y=height-r*2

class hole():
    r=40
    x=width-r
    y=r

class path():
    x=0
    y=0

new=True
a=[]
g=0
not_g=0
a_g=0
s=0
s2=0
ri=0
tim=0


