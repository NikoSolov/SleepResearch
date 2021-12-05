import os

if not(os.path.exists("log_img")):
    os.mkdir("log_img")
if not(os.path.exists("log_txt")):
    os.mkdir("log_txt")

#========>config init<==========#
configstd={"fullscreen": 0, 
            "inverse": 0, 
            "round": 20, 
            "width": 1024, 
            "height": 768, 
            "possible": 200, 
            "freq": 0.25, 
            "radius_multiplier": 1.5}

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

width=int(config["width"])
height=int(config["height"])
posible=int(config["possible"])
coef=float(config["radius_multiplier"])




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