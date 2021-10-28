import os

if not(os.path.exists("log_img")):
    os.mkdir("log_img")
if not(os.path.exists("log_txt")):
    os.mkdir("log_txt")
configstd={"fullscreen": 0, "inverse": 0, "round": 20, "width": 1024, "height": 768, "possible": 200, "freq": 0.25}

if not(os.path.exists("config.txt")):
    config=configstd
    f=open("config.txt", "w")
    for i in config:
        f.write(str(i)+" "+str(config[i])+"\n")
    f.close()
else:
    f=open("config.txt", "r")
    config={i.split(" ")[0]:float(i.split(" ")[1]) for i in f}
    flag=True
    for i in list(configstd.keys()):
        if not(i in list(config.keys())):
            a={i:configstd.get(i)}
            config.update(a)


    #print(config)

width=int(config["width"])
height=int(config["height"])
posible=int(config["possible"])
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
tim=0