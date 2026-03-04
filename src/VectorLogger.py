import config as cfg
import zipfile
import os

cfg.loadConfig()

# ------------------------------
# Vector Logger for Mouses
# Logging trail of the mouse as a vector image and archiving them in a zip file

class VectorLogger:
    # init archive 
    def __init__(self, DIR_NAME):
        self.DIR_NAME = DIR_NAME
        self.ImageArchive = zipfile.ZipFile(f"{self.DIR_NAME}/log_img.zip", "w")
    
    # add part of path after a notch
    def drawNotch(self, bPoints, notch = 0):
        # move to draw a bezier curve
        self.pathString += f"M {bPoints[0][0]} {bPoints[0][1]} Q {bPoints[1][0]} {bPoints[1][1]} {bPoints[2][0]} {bPoints[2][1]} "
        # then move to draw a vertical notch
        if notch != 0:
            self.pathString += f"M {bPoints[2][0]} {bPoints[2][1]} l {0} {notch} "

    # save generated trail bPoints
    def startTrail(self, bGenPoints, bCorridorPoints):
        self.gTrailPoints = bGenPoints
        self.CorridorPoints = bCorridorPoints
        self.pathString = ""

    # save (close) svg file, add to archive and delete
    def saveTrail(self, bPoints, graphName):
        self.drawNotch(bPoints)
        imageLogger = open(f"{self.DIR_NAME}/{graphName}.svg", "w")
        imageLogger.write(self.template((bPoints[2][0], bPoints[2][1])))
        imageLogger.close()

        self.ImageArchive.write(f"{self.DIR_NAME}/{graphName}.svg",
                          f"log_img/{graphName}.svg",
                          zipfile.ZIP_DEFLATED)
        os.remove(f"{self.DIR_NAME}/{graphName}.svg")

    
    # save last Trail and close archive
    def close(self):
        self.ImageArchive.close()
    
    # svg file Template
    def template(self, ballLastPos):
        config = cfg.getConfig()
        WIN_SIZE = [
            config["general"]["window"]["width"],
            config["general"]["window"]["height"]
        ]
        C_BG      = config["general"]["graphics"]["colors"]["bg"]
        C_GTRAIL  = config["Mouses"]["graphics"]["colors"]["gtrail"]
        C_STRAIL  = config["Mouses"]["graphics"]["colors"]["strail"]
        C_MOUSE   = config["Mouses"]["graphics"]["colors"]["mouse"]
        C_HOLE    = config["Mouses"]["graphics"]["colors"]["hole"]
        RADIUS    = config["Mouses"]["graphics"][ "sizes"]["radius"]
        WAIT_ZONE = config["Mouses"]["graphics"][ "sizes"]["waitZone"]

        return f"""<svg \
style="background:{C_BG}" \
width="{WIN_SIZE[0]}" height="{WIN_SIZE[1]}" \
xmlns="http://www.w3.org/2000/svg">
<rect \
id="BackGround" fill="{C_BG}" stroke="black" \
width="{WIN_SIZE[0]}" height="{WIN_SIZE[1]}" x="0" y="0" />
<circle \
id="Hole" fill="{C_HOLE}" \
cx="{WIN_SIZE[0] - RADIUS}" cy="{RADIUS}" r="{RADIUS}"/>
<circle \
id="disableArea" fill="none" \
cx="{RADIUS}" cy="{WIN_SIZE[1] - RADIUS}" r="{WAIT_ZONE}" \
stroke="red" stroke-width="3"/>

<path \
id="corridorArea" \
fill="#ffff00" \
fill-opacity="0.3" \
d="\
M {self.CorridorPoints[0][0][0]} {self.CorridorPoints[0][0][1]} \
Q {self.CorridorPoints[0][1][0]} {self.CorridorPoints[0][1][1]} \
{self.CorridorPoints[0][2][0]} {self.CorridorPoints[0][2][1]} \
L {WIN_SIZE[0]} {0} \
L {self.CorridorPoints[1][2][0]} {self.CorridorPoints[1][2][1]} \
Q {self.CorridorPoints[1][1][0]} {self.CorridorPoints[1][1][1]} \
{self.CorridorPoints[1][0][0]} \
{self.CorridorPoints[1][0][1]} \
"/>
<path \
id="generatedTrail" \
stroke = "{C_GTRAIL}" \
style="stroke-width:{5}; \
stroke-dasharray:none; \
stroke-linejoin:round; \
stroke-linecap:round" \
fill="none" \
d="M {self.gTrailPoints[0][0]} \
{self.gTrailPoints[0][1]} \
Q {self.gTrailPoints[1][0]} \
{self.gTrailPoints[1][1]} \
{self.gTrailPoints[2][0]} \
{self.gTrailPoints[2][1]}"/>
<circle \
id="Mouse" fill="{C_MOUSE}" \
cx="{ballLastPos[0]}" cy="{ballLastPos[1]}" r="{RADIUS}"/>
<path \
id="subjectTrail" fill="none" \
stroke="{C_STRAIL}"  stroke-width="{5}" \
style="stroke-width:3; \
stroke-dasharray:none; \
stroke-linejoin:round; \
stroke-linecap:round"
d="{self.pathString}"
/>
</svg>"""

       

#        <path \
# id="corridorArea" \
# fill="#ffff00" \
# fill-opacity="0.3" \
# d="\
# M {self.CorridorPoints[0][0][0]} {self.CorridorPoints[0][0][1]} \
# Q {self.CorridorPoints[0][1][0]} \
# {self.CorridorPoints[0][1][1]} \
# {self.CorridorPoints[0][2][0]} \
# {self.CorridorPoints[0][2][1]} \
# L {WIN_SIZE[0] - RADIUS} {RADIUS} \
# L {self.CorridorPoints[1][2][0]} {self.CorridorPoints[1][2][1]} \
# Q {self.CorridorPoints[1][1][0]} \
# {self.CorridorPoints[1][1][1]} \
# {self.CorridorPoints[1][0][0]} \
# {self.CorridorPoints[1][0][1]} \
# "/>

# <path \
# id="corridorArea" \
# fill="#ffff00" \
# fill-opacity="0.3" \
# d="\
# M {self.CorridorPoints[0][0][0]} {self.CorridorPoints[0][0][1]} \
# Q {self.CorridorPoints[0][1][0]} {self.CorridorPoints[0][1][1]} \
# {self.CorridorPoints[0][2][0]} {self.CorridorPoints[0][2][1]} \
# A {3 * RADIUS} {3 * RADIUS} 0 0 1 \
# {self.CorridorPoints[1][2][0]} {self.CorridorPoints[1][2][1]} \
# Q {self.CorridorPoints[1][1][0]} {self.CorridorPoints[1][1][1]} \
# {self.CorridorPoints[1][0][0]} \
# {self.CorridorPoints[1][0][1]} \
# "/>
