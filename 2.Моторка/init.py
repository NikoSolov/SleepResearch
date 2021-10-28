import os

if not(os.path.exists("log_img")):
    os.mkdir("log_img")
if not(os.path.exists("log_txt")):
    os.mkdir("log_txt")

if not(os.path.exists("config.txt")):
    config={"fullscreen": 1, "inverse": 1, "round": 20, "width": 1024, "ratio": "4/3"}
    f=open("config.txt", "w")
    for i in config:
        f.write(str(i)+" "+str(config[i])+"\n")
    f.close()
else:
    f=open("config.txt", "r")
    config={i.split(" ")[0]:int(i.split(" ")[1]) for i in f}
    print(config)

width=config["width"]
height=config["height"]
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
s=0
s2=0
ri=0